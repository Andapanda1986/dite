import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

# Seznam k hlídání - ID a Jméno
FOTKY = {
    "25583": "Oliver",
    "25017": "Matouš"
}
LOG_FILE = "log_hlasu.txt"

def hlidej():
    # Simulujeme prohlížeč, aby nás web neblokoval
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    cas = datetime.now().strftime("%d.%m. %H:%M")
    zapis_text = ""
    
    for photo_id, jmeno in FOTKY.items():
        url = f"https://diteajacasopis.cz/profil/{photo_id}/"
        print(f"Kontroluji {jmeno}...")
        
        try:
            r = requests.get(url, headers=headers, timeout=20)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "html.parser")
                
                # Hledáme přímo tu značku, kterou jsi mi poslala v kódu
                span_hlasy = soup.find("span", class_="jet-engine-data-post-count", attrs={"data-post": photo_id})
                
                if span_hlasy:
                    pocet = span_hlasy.get_text(strip=True)
                    zapis_text += f"{cas} | {jmeno}: {pocet} hlasů\n"
                    print(f"--- Najito: {pocet} hlasů")
                else:
                    # Záložní plán, pokud by to nenašel přesně, prohledá text
                    cely_text = soup.get_text(" ", strip=True)
                    najit_cislo = re.search(r"(\d+)\s*hlas", cely_text)
                    if najit_cislo:
                        zapis_text += f"{cas} | {jmeno}: {najit_cislo.group(1)} hlasů\n"
                    else:
                        zapis_text += f"{cas} | {jmeno}: Číslo nenalezeno\n"
            else:
                zapis_text += f"{cas} | {jmeno}: Stránka nedostupná ({r.status_code})\n"
                
        except Exception as e:
            zapis_text += f"{cas} | {jmeno}: Chyba: {e}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(zapis_text)
    print("Hotovo.")

if __name__ == "__main__":
    hlidej()
