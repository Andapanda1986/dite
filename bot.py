import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time

FOTKY = {
    "25583": "Oliver",
    "25017": "já"
}
# Základní URL bez čísla stránky
BASE_URL = "https://diteajacasopis.cz/top-100/?jsf=jet-engine:top100&pagenum="
LOG_FILE = "log_hlasu.txt"

def hlidej():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    cas = datetime.now().strftime("%d.%m. %H:%M")
    nalezeno_celkem = {}
    
    # Prohledáme prvních 10 stránek
    for page in range(1, 11):
        url = f"{BASE_URL}{page}"
        print(f"Hledám na stránce {page}...")
        
        try:
            r = requests.get(url, headers=headers, timeout=20)
            soup = BeautifulSoup(r.text, "html.parser")
            
            for photo_id, jmeno in FOTKY.items():
                if photo_id in nalezeno_celkem:
                    continue  # Pokud už jsme fotku našli na minulé stránce, přeskočíme
                
                # Hledáme text s ID
                for element in soup.find_all(text=re.compile(photo_id)):
                    rodic = element.parent
                    # Vyšplháme kousek nahoru v HTML, abychom našli počet hlasů
                    for _ in range(5):
                        if not rodic: break
                        obsah = rodic.get_text(" ", strip=True)
                        najit_cislo = re.search(r"(\d+)\s*hlas", obsah)
                        if najit_cislo:
                            nalezeno_celkem[photo_id] = (jmeno, najit_cislo.group(1))
                            print(f"--- Najito! {jmeno}: {najit_cislo.group(1)} hlasů")
                            break
                        rodic = rodic.parent
            
            # Pokud už máme všechny, můžeme přestat listovat
            if len(nalezeno_celkem) == len(FOTKY):
                break
                
            time.sleep(1) # Malá pauza, ať nejsme za agresivní boty
            
        except Exception as e:
            print(f"Chyba na stránce {page}: {e}")

    # Zápis výsledků
    zapis_text = ""
    for photo_id, jmeno in FOTKY.items():
        if photo_id in nalezeno_celkem:
            jmeno, pocet = nalezeno_celkem[photo_id]
            zapis_text += f"{cas} | {jmeno}: {pocet} hlasů\n"
        else:
            zapis_text += f"{cas} | {jmeno}: ID {photo_id} nenalezeno na prvních 10 stranách\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(zapis_text)
    print("Hotovo.")

if __name__ == "__main__":
    hlidej()
