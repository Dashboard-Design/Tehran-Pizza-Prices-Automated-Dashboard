import requests
from bs4 import BeautifulSoup
from typing import List, Dict

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "fa-IR,fa;q=0.9",
    "Referer": "https://crispy.land/",
}


def fetch_page():
    url = "https://crispy.land/branch/21003"
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    resp.encoding = "utf-8"
    return resp.text


def extract_pizzas(html: str) -> List[Dict]:
    soup = BeautifulSoup(html, 'html.parser')
    pizzas = []

    # Find all product articles that belong to the pizza category
    # Each article has classes like "w-grid-item product_category-pizza product_category-all"
    pizza_articles = soup.select('article.w-grid-item.product_category-pizza')

    for article in pizza_articles:
        # Product name
        title_tag = article.select_one('h2.post_title a')
        if not title_tag:
            continue
        name = title_tag.get_text(strip=True)

        # Price – located inside .amx-price__final .amx-price__amount
        price_span = article.select_one('.amx-price__final .amx-price__amount')
        if not price_span:
            continue
        price_text = price_span.get_text(strip=True).replace(',', '')
        try:
            price_rials = int(price_text)
            price_toman = price_rials // 10  # Convert Rials to Tomans
        except ValueError:
            continue

        pizzas.append({
            "name": name,
            "price_toman": price_toman
        })

    return pizzas


def scrape() -> List[Dict]:
    html = fetch_page()
    return extract_pizzas(html)

# For testing purposes
# if __name__ == "__main__":
#     items = scrape()
#     print(f"Found {len(items)} pizzas")
#     for item in items[:5]:
#         print(f"{item['name']}: {item['price_toman']:,} تومان")