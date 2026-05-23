import requests
from typing import List, Dict


def fetch_meykhosh_menu():
    url = "https://restaurant.delino.com/restaurant/menu/401c408c-079c-4810-8fce-f0c3028d6763"
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


def extract_single_pizzas(data):
    categories = data.get("categories", [])
    target_category = None
    for cat in categories:
        if cat.get("title") == "پیتزا تک نفره":
            target_category = cat
            break
    if not target_category:
        raise ValueError("Category 'پیتزا تک نفره' not found")

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
                "id": item.get("id")
            })
    return pizzas


def scrape() -> List[Dict]:
    data = fetch_meykhosh_menu()
    if not data:
        raise Exception("Failed to fetch Meykhosh menu after retries")
    return extract_single_pizzas(data)