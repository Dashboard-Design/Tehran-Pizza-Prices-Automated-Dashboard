import requests
import json
from pathlib import Path
from datetime import datetime

# IDs that together cover the full menu of 30cm pizzas of Shila
PRODUCT_IDS = [166830, 166832, 166828]

def fetch_products_for_id(product_id):
    url = f"https://shilafood.co/Content/JT/4418/siteProductFeatureproductID_{product_id}.txt"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://shilafood.co/order",
    }
    resp = requests.get(url, headers=headers)
    resp.encoding = "utf-8"
    data = resp.json()

    products = []
    # The main product (from the "Product" or "V_Product" field)
    main = data.get("V_Product") or data.get("Product")
    if main and "ProductID" in main:
        products.append(main)

    # The related products list
    related = data.get("productListRepositorySmall", [])
    products.extend(related)

    return products


def main():
    # Create data folder
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    all_products = {}  # deduplicate by ProductID
    for pid in PRODUCT_IDS:
        print(f"Fetching product ID {pid}...")
        prods = fetch_products_for_id(pid)
        for p in prods:
            pid_key = p.get("ProductID")
            if pid_key and pid_key not in all_products:
                # Store only needed fields
                all_products[pid_key] = {
                    "name": p.get("ProductName", ""),
                    "price_toman": p.get("Price", 0),
                    "product_id": pid_key,
                    "menu_id": p.get("MenuID")
                }

    # Convert to list
    items = list(all_products.values())

    # Save to data folder
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = data_dir / f"shila_menu_pizza30cm_{timestamp}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(items)} products to {output_file}")
    for item in items:
        print(f"{item['name']}: {item['price_toman']:,} تومان")


if __name__ == "__main__":
    main()