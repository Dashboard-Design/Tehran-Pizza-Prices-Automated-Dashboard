import requests
import uuid
import time
from typing import List, Dict

# IDs that together cover the full menu of 30cm pizzas of Shila

# PRODUCT_IDS = [166830, 166832, 166828]

def fetch_products_for_id(product_id = 166830):
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


def scrape() -> List[Dict]:
    PRODUCT_IDS = [166830, 166832, 166828]

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
                    "product_id": pid_key
                }
    items = list(all_products.values())
    return items
