import requests
import json
from datetime import datetime

# ID a jména
FOTKY = {
    "25583": "Oliver",
    "25017": "Matouš"
}
LOG_FILE = "log_hlasu.txt"

def hlidej():
    # Tento odkaz je "mozek" jejich databáze
    api_url = "https://diteajacasopis.cz/wp-admin/admin-ajax.php"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    
    cas = datetime.now().strftime("%d.%m. %H:%M")
    zapis_text = ""

    for photo_id, jmeno in FOTKY.items():
        # Tyhle parametry jsem vytáhl přímo z jejich systému
        payload = {
            "action": "jet_engine_get_posts_count",
            "store": "oblibene",
            "post_id": photo_id
        }
        
        try:
            # Musíme to poslat jako POST požadavek
            r = requests.post(api_url, data=payload, headers=headers, timeout=20)
            
            if r.status_code == 200:
                res_data = r.json()
                # Odpověď vypadá jako {"success":true,"data":{"count":"390"}}
                if res_data.get("success"):
                    pocet = res_data["data"]["count"]
                    zapis_text += f"{cas} | {jmeno}: {pocet} hlasů\n"
                    print(f"Úspěch: {jmeno} má {pocet} hlasů")
                else:
                    zapis_text += f"{cas} | {jmeno}: Web odmítl vydat data\n"
            else:
                zapis_text += f"{cas} | {jmeno}: Chyba serveru {r.status_code}\n"
        except Exception as e:
            zapis_text += f"{cas} | {jmeno}: Chyba: {str(e)}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(zapis_text)
    print("Hotovo.")

if __name__ == "__main__":
    hlidej()
