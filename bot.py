import requests
import re
from datetime import datetime
import time

# Seznam ID a jmen, která chceme sledovat
FOTKY = {
    "25583": "Oliver",
    "25017": "Matouš"
}

LOG_FILE = "log_hlasu.txt"

def hlidej():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }
    cas = datetime.now().strftime("%d.%m. %H:%M")
    vysledky = {}
    
    # Projdeme prvních 10 stránek, abychom je našli kdekoli
    for page in range(1, 11):
        # Na první stránku jdeme přímo, na ostatní přes pagenum
        url = "https://diteajacasopis.cz/top-100/"
        if page > 1:
            url += f"?jsf=jet-engine:top100&pagenum={page}"
            
        print(f"Hledám na straně {page}...")
        
        try:
            r = requests.get(url, headers=headers, timeout=30)
            html = r.text
            
            for photo_id, jmeno in FOTKY.items():
                if photo_id in vysledky:
                    continue # Pokud už jsme ho našli na dřívější straně, neřešíme
                
                # Hledáme ID a počet hlasů
                vzor = rf'data-post="{photo_id}".*?>(\d+)<'
                nalez = re.search(vzor, html, re.DOTALL)
                
                if nalez:
                    vysledky[photo_id] = nalez.group(1)
                    print(f"--- {jmeno} nalezen na str. {page}: {nalez.group(1)} hlasů")

            # Pokud už máme oba, nemusíme prohledávat další stránky
            if len(vysledky) == len(FOTKY):
                break
                
            time.sleep(0.5) # Krátká pauza pro stabilitu

        except Exception as e:
            print(f"Chyba na straně {page}: {e}")

    # Příprava textu pro zápis
    zapis_text = ""
    for photo_id, jmeno in FOTKY.items():
        pocet = vysledky.get(photo_id, "Nenalezeno")
        zapis_text += f"{cas} | {jmeno}: {pocet} hlasů\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(zapis_text)
    print("Hotovo. Výsledky zapsány.")

if __name__ == "__main__":
    hlidej()
