import requests
from typing import List, Dict


def fetch_perperok_products():
    url = "https://api.perperook.ir/v1/Product/GetBranchProductPrices/10"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://perperook.ir/",
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    resp.encoding = "utf-8"
    return resp.json()


def extract_products(data, min_id=2, max_id=26):
    products = []
    for item in data:
        pid = item.get("productId")
        if pid is None:
            continue
        if min_id <= pid <= max_id:
            products.append({
                "product_id": pid,
                "name": item.get("productName"),
                "price_toman": int(item.get("price")) / 10
            })
    return products

def scrape() -> List[Dict]:

    data = fetch_perperok_products()
    if not data:
        raise Exception("Failed to fetch Perperook menu after retries")
    return extract_products(data, 2, 26)
