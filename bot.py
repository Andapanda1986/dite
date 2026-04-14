import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

# === NASTAVENÍ ===
FOTKY = {
    "25583": "Oliver",
    "25017": "já"
}
URL = "https://diteajacasopis.cz/top-100/"
LOG_FILE = "log_hlasu.txt"

def hlidej():
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(URL, headers=headers, timeout=20)
        soup = BeautifulSoup(r.text, "html.parser")
        cas = datetime.now().strftime("%d.%m. %H:%M")
        zapis_text = ""

        for photo_id, jmeno in FOTKY.items():
            # Hledáme div, který obsahuje dané ID
            block = soup.find(attrs={"data-id": photo_id}) or soup.find(id=re.compile(photo_id))
            
            if block:
                cely_text = block.get_text(" ", strip=True)
                najit_cislo = re.search(r"(\d+)\s*hlas", cely_text)
                
                if najit_cislo:
                    pocet = najit_cislo.group(1)
                    zapis_text += f"{cas} | {jmeno}: {pocet} hlasů\n"
                else:
                    zapis_text += f"{cas} | {jmeno}: Číslo nenalezeno\n"
            else:
                zapis_text += f"{cas} | {jmeno}: ID {photo_id} na stránce nevidím\n"

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(zapis_text)
        print("Hotovo.")

    except Exception as e:
        print(f"Chyba: {e}")

if __name__ == "__main__":
    hlidej()
