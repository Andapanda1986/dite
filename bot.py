import requests
import re
from datetime import datetime

FOTKY = {
    "25583": "Oliver",
    "25017": "Matouš"
}
LOG_FILE = "log_hlasu.txt"

def hlidej():
    session = requests.Session() # Session si pamatuje cookies jako prohlížeč
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    cas = datetime.now().strftime("%d.%m. %H:%M")
    zapis_text = ""
    
    try:
        # 1. KROK: Načteme hlavní stránku, abychom získali "heslo" (nonce)
        print("Načítám hlavní stránku pro získání klíče...")
        r_init = session.get("https://diteajacasopis.cz/top-100/", headers=headers, timeout=20)
        
        # Hledáme v kódu řetězec "nonce":"xyz123"
        nonce_match = re.search(r'"nonce":"([a-zA-Z0-9]+)"', r_init.text)
        
        if not nonce_match:
            # Zkusíme druhý formát, někdy je to jako jetEnginePublicConfig
            nonce_match = re.search(r'nonce":"([a-zA-Z0-9]+)"', r_init.text)

        if nonce_match:
            nonce = nonce_match.group(1)
            print(f"Klíč nalezen: {nonce}")
            
            # 2. KROK: Dotaz na každou fotku zvlášť s použitím klíče
            api_url = "https://diteajacasopis.cz/wp-admin/admin-ajax.php"
            
            for photo_id, jmeno in FOTKY.items():
                payload = {
                    "action": "jet_engine_get_posts_count",
                    "store": "oblibene",
                    "post_id": photo_id,
                    "nonce": nonce # Tady to heslo použijeme!
                }
                
                r_api = session.post(api_url, data=payload, headers=headers, timeout=20)
                
                if r_api.status_code == 200:
                    data = r_api.json()
                    if data.get("success"):
                        pocet = data["data"].get("count", "0")
                        zapis_text += f"{cas} | {jmeno}: {pocet} hlasů\n"
                        print(f"--- {jmeno}: {pocet} hlasů")
                    else:
                        zapis_text += f"{cas} | {jmeno}: Server klíč odmítl\n"
                else:
                    zapis_text += f"{cas} | {jmeno}: API chyba ({r_api.status_code})\n"
        else:
            zapis_text += f"{cas} | Nepodařilo se získat bezpečnostní klíč z webu\n"
            print("Klíč nenalezen.")

    except Exception as e:
        zapis_text += f"{cas} | Kritická chyba: {str(e)}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(zapis_text)
    print("Hotovo.")

if __name__ == "__main__":
    hlidej()
