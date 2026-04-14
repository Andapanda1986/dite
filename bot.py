import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

# ID a jména z tvého kódu
FOTKY = {
    "25583": "Oliver",
    "25017": "Matouš"
}
BASE_URL = "https://diteajacasopis.cz/top-100/?jsf=jet-engine:top100&pagenum="
LOG_FILE = "log_hlasu.txt"

def hlidej():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    cas = datetime.now().strftime("%d.%m. %H:%M")
    nalezeno_celkem = {}
    
    # Prohledáme stránky 1 až 10
    for page in range(1, 11):
        url = f"{BASE_URL}{page}"
        print(f"Hledám na stránce {page}...")
        
        try:
            r = requests.get(url, headers=headers, timeout=20)
            soup = BeautifulSoup(r.text, "html.parser")
            
            for photo_id, jmeno in FOTKY.items():
                if photo_id in nalezeno_celkem:
                    continue
                
                # Hledáme přesně tu značku, co jsi mi poslala
                vysledek = soup.find("span", {"data-post": photo_id, "class": "jet-engine-data-post-count"})
                
                if vysledek:
                    pocet = vysledek.get_text(strip=True)
                    nalezeno_celkem[photo_id] = (jmeno, pocet)
                    print(f"--- {jmeno} najit na stranke {page}: {pocet} hlasů")

            if len(nalezeno_celkem) == len(FOTKY):
                break
            
            time.sleep(0.5) # Rychlá pauza mezi stránkami
            
        except Exception as e:
            print(f"Chyba na strance {page}: {e}")

    # Zápis do logu
    zapis_text = ""
    for photo_id, jmeno in FOTKY.items():
        if photo_id in nalezeno_celkem:
            jm, pc = nalezeno_celkem[photo_id]
            zapis_text += f"{cas} | {jm}: {pc} hlasů\n"
        else:
            zapis_text += f"{cas} | {jmeno}: Nenalezeno na prvních 10 stranách\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(zapis_text)
    print("Hotovo.")

if __name__ == "__main__":
    hlidej()
