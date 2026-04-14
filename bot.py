import requests
from bs4 import BeautifulSoup
from datetime import datetime

# ID fotek z tvého kódu
FOTKY = {
    "25583": "Oliver",
    "25017": "Matouš"
}
URL = "https://diteajacasopis.cz/top-100/"
LOG_FILE = "log_hlasu.txt"

def hlidej():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    cas = datetime.now().strftime("%d.%m. %H:%M")
    zapis_text = ""
    
    try:
        # Načteme hlavní stránku (Top 100)
        r = requests.get(URL, headers=headers, timeout=20)
        soup = BeautifulSoup(r.text, "html.parser")
        
        for photo_id, jmeno in FOTKY.items():
            # Hledáme přesně tu značku, co jsi mi poslala: data-post="25017"
            vysledek = soup.find("span", {"data-post": photo_id, "class": "jet-engine-data-post-count"})
            
            if vysledek:
                pocet = vysledek.get_text(strip=True)
                zapis_text += f"{cas} | {jmeno}: {pocet} hlasů\n"
                print(f"--- Najito {jmeno}: {pocet}")
            else:
                # Pokud to nenajde na 1. stránce, zkusíme to najít aspoň v celém kódu
                zapis_text += f"{cas} | {jmeno}: Nenalezeno na 1. straně Top 100\n"
                print(f"--- {jmeno} nenalezen.")

    except Exception as e:
        zapis_text += f"{cas} | Chyba: {e}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(zapis_text)
    print("Hotovo.")

if __name__ == "__main__":
    hlidej()
