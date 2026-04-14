import requests
import re
from datetime import datetime
import time

# NASTAVENÍ: ID, Jméno a STRÁNKA, na které se aktuálně nacházíte
HLIDANE_FOTKY = [
    {"id": "25583", "jmeno": "Oliver", "page": "1"}, # Oliver je (asi) na začátku?
    {"id": "25017", "jmeno": "Matouš", "page": "6"}  # Matouš je na straně 6
]

LOG_FILE = "log_hlasu.txt"

def hlidej():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }
    cas = datetime.now().strftime("%d.%m. %H:%M")
    zapis_text = ""

    for fotka in HLIDANE_FOTKY:
        # Robot jde přímo na stránku, kde máš Matouše/Olivera
        url = f"https://diteajacasopis.cz/top-100/?jsf=jet-engine:top100&pagenum={fotka['page']}"
        print(f"Kontroluji {fotka['jmeno']} na straně {fotka['page']}...")
        
        try:
            r = requests.get(url, headers=headers, timeout=30)
            html = r.text
            
            # Hledáme číslo hlasů u konkrétního ID
            vzor = rf'data-post="{fotka["id"]}".*?>(\d+)<'
            nalez = re.search(vzor, html, re.DOTALL)
            
            if nalez:
                pocet = nalez.group(1)
                zapis_text += f"{cas} | {fotka['jmeno']}: {pocet} hlasů\n"
                print(f"--- Najito: {pocet}")
            else:
                zapis_text += f"{cas} | {fotka['jmeno']}: Na straně {fotka['page']} ho nevidím\n"
                print(f"--- Nenalezeno.")
            
            time.sleep(1) # Pauza mezi načítáním stránek

        except Exception as e:
            zapis_text += f"{cas} | {fotka['jmeno']}: Chyba: {str(e)}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(zapis_text)
    print("Hotovo.")

if __name__ == "__main__":
    hlidej()
