import requests
import uuid
import time
from typing import List, Dict

def fetch_chickenfamily_menu(product_id=182690):
    url = f"https://chickenfamilyco.com/Content/JT/4526/siteProductFeatureproductID_{product_id}.txt"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://chickenfamilyco.com/",
    }
    resp = requests.get(url, headers=headers)
    resp.encoding = "utf-8"
    resp.raise_for_status()
    return resp.json()


def extract_products(data):
    products = []
    main = data.get("V_Product")
    if main:
        products.append({
            "name": main["ProductName"],
            "price_toman": main["Price"],
            "product_id": main["ProductID"]
        })
    related = data.get("productListRepositorySmall", [])
    for item in related:
        if not any(p["product_id"] == item["ProductID"] for p in products):
            products.append({
                "name": item["ProductName"],
                "price_toman": item["Price"],
                "product_id": item["ProductID"]
            })
    return products


def scrape() -> List[Dict]:
    """Return list of products with keys: title, price_toman"""
    data = fetch_chickenfamily_menu()
    if not data:
        raise Exception("Failed to fetch ChickenFamily menu after retries")

    return extract_products(data)
