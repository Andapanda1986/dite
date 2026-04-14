Python
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

# === TADY ZMĚŇ JEN TYTO ÚDAJE (čísla z HTML a jména) ===
FOTKY = {
    "25583": "Oliver",    # První číslo fotky a jméno
    "25017": "já"    # Druhé číslo fotky a jméno
}
# ======================================================

URL = "https://diteajacasopis.cz/top-100/"
LOG_FILE = "log_hlasu.txt"

def hlidej():
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(URL, headers=headers, timeout=20)
        soup = BeautifulSoup(r.text, "html.parser")
        cas = datetime.now().strftime("%d.%m. %H:%M")
        zapis_text = ""

        # Robot projde obě ID jedno po druhém
        for photo_id, jmeno in FOTKY.items():
            # Najde blok fotky (podle ID ve zdrojáku)
            block = soup.find(attrs={"data-id": photo_id}) or soup.find(id=re.compile(photo_id))
            
            if block:
                # Robot přečte text v okolí té fotky
                cely_text = block.get_text(" ", strip=True)
                # Hledá číslo před slovem 'hlas'
                najit_cislo = re.search(r"(\d+)\s*hlas", cely_text)
                
                if najit_cislo:
                    pocet = najit_cislo.group(1)
                    zapis_text += f"{cas} | {jmeno}: {pocet} hlasů\n"
                else:
                    zapis_text += f"{cas} | {jmeno}: Číslo nenalezeno\n"
            else:
                zapis_text += f"{cas} | {jmeno}: ID {photo_id} na stránce nevidím\n"

        # Uložíme výsledek do souboru log_hlasu.txt
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(zapis_text)
        print("Robot úspěšně zkontroloval hlasy.")

    except Exception as e:
        print(f"Něco se pokazilo: {e}")

if __name__ == "__main__":
    hlidej()
