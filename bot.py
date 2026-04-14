import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

# Nastavení jmen a ID
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
        # Zkusíme hledat přímo přes vyhledávací parametr webu
        search_url = f"https://diteajacasopis.cz/top-100/?_s={photo_id}"
        print(f"Hledám {jmeno} (ID {photo_id})...")
        
        try:
            r = requests.get(search_url, headers=headers, timeout=20)
            soup = BeautifulSoup(r.text, "html.parser")
            
            # Hledáme tu tvoji známou značku s hlasy
            vysledek = soup.find("span", {"data-post": photo_id, "class": "jet-engine-data-post-count"})
            
            if vysledek:
                pocet = vysledek.get_text(strip=True)
                zapis_text += f"{cas} | {jmeno}: {pocet} hlasů\n"
                print(f"--- Najito: {pocet}")
            else:
                # Záložní pokus - najít jakékoliv číslo u slova hlas na této stránce
                text_stranky = soup.get_text(" ", strip=True)
                najit_cislo = re.search(r"(\d+)\s*hlas", text_stranky)
                if najit_cislo:
                    zapis_text += f"{cas} | {jmeno}: {najit_cislo.group(1)} hlasů\n"
                else:
                    zapis_text += f"{cas} | {jmeno}: Nenalezeno (ani přes hledání)\n"
        
        except Exception as e:
            zapis_text += f"{cas} | {jmeno}: Chyba: {e}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(zapis_text)
    print("Hotovo.")

if __name__ == "__main__":
    hlidej()
