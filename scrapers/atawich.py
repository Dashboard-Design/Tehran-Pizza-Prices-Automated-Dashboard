import requests
import time
from typing import List, Dict

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://atawich.com/",
    "Origin": "https://atawich.com",
}


def fetch_product(product_id: int, session: requests.Session) -> Dict:
    """
    Fetch product data from the API endpoint.
    The slug (%D9%BE%DB%8C%D8%AA%D8%B2%D8%A7) is 'pizza' in URL‑encoded Persian.
    """
    url = f"https://atawich.com/p/{product_id}/%D9%BE%DB%8C%D8%AA%D8%B2%D8%A7?lazyLoad=true"
    resp = session.get(url, headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()
    product = data.get("Product")
    if not product:
        raise ValueError(f"No product data for ID {product_id}")
    return {
        "name": product["ProductName"],
        "price_toman": int(data["BasePrice"]),  # BasePrice is a string like "878000"
        "product_id": product["ProductID"],
    }


def scrape(product_ids: List[int] = None, delay_seconds: float = 1.0) -> List[Dict]:
    """
    Fetch products for given IDs. If product_ids is None, use a default list.
    delay_seconds: pause between requests to be polite to the server.
    """
    if product_ids is None:
        # Default list of product IDs
        product_ids = [104245, 32221, 32211, 32214, 32219, 32224, 32227, 109544, 71382]

    session = requests.Session()
    # Visit homepage once to get cookies (optional but safe)
    session.get("https://atawich.com/", headers=HEADERS)

    products = []
    for i, pid in enumerate(product_ids):
        print(f"Fetching product ID {pid}...")
        try:
            prod = fetch_product(pid, session)
            products.append(prod)
        except Exception as e:
            print(f"Error fetching ID {pid}: {e}")
        # Wait between requests (except after the last one)
        if i < len(product_ids) - 1:
            time.sleep(delay_seconds)
    return products

# for testing
# if __name__ == "__main__":
#     items = scrape()  # uses default product_ids and 1 second delay
#     print(f"\nFetched {len(items)} products")
#     for item in items:
#         print(f"{item['name']}: {item['price_toman']:,} تومان")