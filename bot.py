import requests
import re
from datetime import datetime

# ID a jména
FOTKY = {
    "25583": "Oliver",
    "25017": "Matouš"
}
LOG_FILE = "log_hlasu.txt"

def hlidej():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    cas = datetime.now().strftime("%d.%m. %H:%M")
    zapis_text = ""

    for photo_id, jmeno in FOTKY.items():
        # Zkusíme přímo vyhledávací stránku, která vrací nejméně zbytečností
        url = f"https://diteajacasopis.cz/top-100/?_s={photo_id}"
        
        try:
            r = requests.get(url, headers=headers, timeout=20)
            html_kod = r.text
            
            # Hledáme číslo, které je v těsné blízkosti tvého ID v tom skrytém JetEngine kódu
            # Hledáme vzor: data-post="25017">ČÍSLO</span>
            vzor = rf'data-post="{photo_id}"[^>]*>(\d+)<\/span>'
            najito = re.search(vzor, html_kod)
            
            if najito:
                pocet = najito.group(1)
                zapis_text += f"{cas} | {jmeno}: {pocet} hlasů\n"
                print(f"--- {jmeno}: Najito {pocet}")
            else:
                # Druhý pokus: Hledáme jakékoliv číslo u slova "post-count" a tvého ID
                vzor_zalozni = rf'post="{photo_id}".*?(\d+)'
                najito_zalozni = re.search(vzor_zalozni, html_kod, re.DOTALL)
                if najito_zalozni:
                    pocet = najito_zalozni.group(1)
                    zapis_text += f"{cas} | {jmeno}: {pocet} hlasů (záloha)\n"
                else:
                    zapis_text += f"{cas} | {jmeno}: Číslo nenalezeno (web ho skrývá)\n"
                    
        except Exception as e:
            zapis_text += f"{cas} | {jmeno}: Chyba: {e}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(zapis_text)
    print("Hotovo.")

if __name__ == "__main__":
    hlidej()
