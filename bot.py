import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

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
        # Použijeme přímé hledání, které nám minule aspoň odpovědělo
        url = f"https://diteajacasopis.cz/top-100/?_s={photo_id}"
        
        try:
            r = requests.get(url, headers=headers, timeout=20)
            soup = BeautifulSoup(r.text, "html.parser")
            
            # Najdeme ten velký blok, co jsi mi poslala (obsahuje ID fotky)
            blok = soup.find(attrs={"data-post-id": photo_id})
            
            if blok:
                # V tomto bloku najdeme tu specifickou třídu pro hlasy
                span_hlasy = blok.find("span", class_="jet-engine-data-post-count")
                if span_hlasy:
                    pocet = span_hlasy.get_text(strip=True)
                else:
                    # Pokud tam není span, zkusíme najít jakékoliv číslo u slova hlas v tom bloku
                    text_bloku = blok.get_text(" ", strip=True)
                    najit = re.search(r"(\d+)\s*hlas", text_bloku)
                    pocet = najit.group(1) if najit else "???"
                
                zapis_text += f"{cas} | {jmeno}: {pocet} hlasů\n"
                print(f"--- {jmeno}: {pocet}")
            else:
                # Pokud nenajde blok, zkusí aspoň prohledat celou stránku na tvé ID
                cely_web = soup.get_text(" ", strip=True)
                # Hledáme číslo, které je blízko tvého jména nebo ID
                vzor = rf"{photo_id}.*?(\d+)\s*hlas"
                najito = re.search(vzor, cely_web, re.IGNORECASE)
                if najito:
                    zapis_text += f"{cas} | {jmeno}: {najito.group(1)} hlasů (odhad)\n"
                else:
                    zapis_text += f"{cas} | {jmeno}: Nenalezeno na webu\n"
                    
        except Exception as e:
            zapis_text += f"{cas} | {jmeno}: Chyba: {e}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(zapis_text)
    print("Hotovo.")

if __name__ == "__main__":
    hlidej()
