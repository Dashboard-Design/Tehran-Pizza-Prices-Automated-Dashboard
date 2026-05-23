import requests
from typing import List, Dict


def fetch_pizzahot_menu():
    url = "https://www.delino.com/restaurant/menu/fcd56b18-04d0-493e-9f59-be0da058acbb?_=1779235996430"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://meykhosh.delino.com/",
        "Accept-Language": "fa-IR,fa;q=0.9",
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    # Ensure correct encoding for Persian
    resp.encoding = "utf-8"
    return resp.json()


def extract_30cm_pizzas(data):
    categories = data.get("categories", [])
    target_category = None
    for cat in categories:
        if cat.get("title") == "پیتزا دو نفره":
            target_category = cat
            break
    if not target_category:
        raise ValueError("Category 'پیتز دو نفره' not found")

    pizzas = []
    # The food items are inside sub[0].food (as per JSON structure)
    sub_categories = target_category.get("sub", [])
    if sub_categories:
        # Usually first sub-category contains the foods
        foods = sub_categories[0].get("food", [])
        for item in foods:
            pizzas.append({
                "name": item.get("title"),
                "price_toman": item.get("price"),
                "product_id": item.get("id")
            })
    return pizzas


def scrape() -> List[Dict]:
    data = fetch_pizzahot_menu()
    if not data:
        raise Exception("Failed to fetch Pizzahot menu after retries")
    return extract_30cm_pizzas(data)
