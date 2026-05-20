import requests
import json
from pathlib import Path
from datetime import datetime


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
                "title": item.get("title"),
                "price_toman": item.get("price"),
                "id": item.get("id"),
                "available": item.get("available", False)
            })
    return pizzas


def main():
    # Create data folder if not exists
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    data = fetch_meykhosh_menu()

    pizzas = extract_single_pizzas(data)
    print(f"Found {len(pizzas)} items in 'پیتزا تک نفره'")

    # Save to JSON file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = data_dir / f"meykhosh_single_pizzas_{timestamp}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(pizzas, f, indent=2, ensure_ascii=False)

    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    main()