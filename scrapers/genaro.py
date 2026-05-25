import requests
import json
from typing import List, Dict

# API endpoint
API_URL = "https://api15.live-menu.ir/api/Menu/Config5/"

# Headers (copied from the curl)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Referer": "https://gennaro-krsh.ir/",
    "sec-ch-ua": '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}

# Payload (taken from your DevTools)
PAYLOAD = {
    "url": "gennaro-krsh.ir",
    "hashCode": "YzxrT0c33aj3d4OHtbT3o7jCXMNpEp",
    "cuGid": None,
    "language": "fa",
    "oGid": "25A45DCC-463C-473A-A314-F2BE8635DFDD",
    "food": True,
    "ccscore": True,
    "favorite": True,
    "popular": False,
    "home": False,
    "referrer": None,
}

def fetch_menu() -> Dict:
    """POST to the API and return JSON response."""
    resp = requests.post(API_URL, json=PAYLOAD, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return resp.json()

def extract_pizzas(data: Dict) -> List[Dict]:
    """Extract pizza names and prices from the JSON."""
    for category in data.get("food", []):
        if category.get("g") == "پیتزا":
            # The 'p' field is a JSON string
            products = json.loads(category.get("p", "[]"))
            pizzas = []
            for prod in products:
                name = prod.get("t")
                if not name:
                    continue
                # Price is in thousands of Tomans (e.g., 750 = 750,000)
                price_thousands = prod.get("p", 0)
                price_toman = price_thousands * 1000
                pizzas.append({"name": name, "price_toman": price_toman})
            return pizzas
    return []

def scrape() -> List[Dict]:
    data = fetch_menu()
    return extract_pizzas(data)

# For testing purposes
# if __name__ == "__main__":
#     items = scrape()
#     print(f"Found {len(items)} pizzas")
#     for item in items[:5]:
#         print(f"{item['name']}: {item['price_toman']:,} تومان")