import requests
import json
from datetime import datetime

# ID a jména
FOTKY = {
    "25583": "Oliver",
    "25017": "Matouš"
}
LOG_FILE = "log_hlasu.txt"

def hlidej():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest"
    }
    cas = datetime.now().strftime("%d.%m. %H:%M")
    zapis_text = ""

    # Tohle je ten skrytý odkaz, kam si web chodí pro počty hlasů
    api_url = "https://diteajacasopis.cz/wp-admin/admin-ajax.php"

    for photo_id, jmeno in FOTKY.items():
        print(f"Dotazuji se na {jmeno}...")
        
        # Tohle jsou data, která musíme webu poslat, aby nám odpověděl
        payload = {
            "action": "jet_engine_get_posts_count",
            "store": "oblibene",
            "post_id": photo_id
        }
        
        try:
            r = requests.post(api_url, headers=headers, data=payload, timeout=20)
            
            if r.status_code == 200:
                # Web vrací odpověď ve formátu {"success": true, "data": {"count": "390"}}
                data = r.json()
                if data.get("success") and "data" in data:
                    pocet = data["data"].get("count", "0")
                    zapis_text += f"{cas} | {jmeno}: {pocet} hlasů\n"
                    print(f"--- {jmeno}: {pocet} hlasů")
                else:
                    zapis_text += f"{cas} | {jmeno}: Nenalezeno v databázi\n"
            else:
                zapis_text += f"{cas} | {jmeno}: API chyba ({r.status_code})\n"
                    
        except Exception as e:
            zapis_text += f"{cas} | {jmeno}: Chyba připojení: {e}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(zapis_text)
    print("Hotovo.")

if __name__ == "__main__":
    hlidej()
