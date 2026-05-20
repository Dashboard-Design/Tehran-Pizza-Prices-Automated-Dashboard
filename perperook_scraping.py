import requests
import json
from pathlib import Path
from datetime import datetime


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
                "price_toman": item.get("price")
            })
    return products

def main():
    # Create data folder
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    data = fetch_perperok_products()

    products = extract_products(data, 2, 26)

    # Save to JSON file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = data_dir / f"perperok_products_{timestamp}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    main()