import requests
import re
import json
from datetime import datetime

FOTKY = {
    "25583": "Oliver",
    "25017": "Matouš"
}
URL = "https://diteajacasopis.cz/top-100/"
LOG_FILE = "log_hlasu.txt"

def hlidej():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }
    cas = datetime.now().strftime("%d.%m. %H:%M")
    zapis_text = ""
    
    try:
        r = requests.get(URL, headers=headers, timeout=30)
        html = r.text
        
        for photo_id, jmeno in FOTKY.items():
            # Hledáme číslo v celém kódu stránky, které je blízko "data-post": "ID"
            # Zkusíme několik verzí, jak to tam ten systém může mít schované
            vzor = rf'data-post="{photo_id}".*?>(\d+)<'
            nalez = re.search(vzor, html, re.DOTALL)
            
            if not nalez:
                # Druhý pokus: hledání v JSON datech, která JetEngine občas vypisuje do skriptu
                vzor_json = rf'"{photo_id}":.*?"count":"?(\d+)"?'
                nalez = re.search(vzor_json, html)

            if nalez:
                pocet = nalez.group(1)
                zapis_text += f"{cas} | {jmeno}: {pocet} hlasů\n"
                print(f"--- {jmeno}: {pocet} hlasů")
            else:
                zapis_text += f"{cas} | {jmeno}: Nenalezeno na 1. straně (zkuste pagenum)\n"
                print(f"--- {jmeno} nenalezen.")

    except Exception as e:
        zapis_text += f"{cas} | Chyba: {str(e)}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(zapis_text)
    print("Hotovo.")

if __name__ == "__main__":
    hlidej()
