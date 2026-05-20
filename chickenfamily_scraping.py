import requests
import json
from pathlib import Path
from datetime import datetime


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


def main():
    data = fetch_chickenfamily_menu(182690)  # or any product ID in that menu
    products = extract_products(data)

    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = data_dir / f"chickenfamily_ItallianPizza_{timestamp}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(products)} products to {output_file}")


if __name__ == "__main__":
    main()