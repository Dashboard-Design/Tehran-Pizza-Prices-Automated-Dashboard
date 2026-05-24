import requests
from typing import List, Dict

def fetch_harmonykitchen_menu():
    url = "https://restaurant.delino.com/restaurant/menu/5571d769-98e4-4f40-b457-1f829e8a6aa7"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://www.harmonykitchen.ir/",
        "Accept-Language": "fa-IR,fa;q=0.9",
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    # Ensure correct encoding for Persian
    resp.encoding = "utf-8"
    return resp.json()


def extract_pizzas(data):
    categories = data.get("categories", [])
    target_category = None
    for cat in categories:
        if cat.get("title") == "پیتزا":
            target_category = cat
            break
    if not target_category:
        raise ValueError("Category 'پیتزا ' not found")

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
    data = fetch_harmonykitchen_menu()
    if not data:
        raise Exception("Failed to fetch HarmonyKitchen menu after retries")
    print(f"Successfully fetched HarmonyKitchen menu")
    for i in extract_pizzas(data):
        print(i)
    return extract_pizzas(data)

scrape()