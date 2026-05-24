import requests
from bs4 import BeautifulSoup
from typing import List, Dict

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "fa-IR,fa;q=0.9",
    "Referer": "https://gennaro-pas.ir/",
}


def fetch_page():
    url = "https://gennaro-pas.ir/menu"
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    resp.encoding = "utf-8"
    return resp.text


def extract_pizzas(html: str) -> List[Dict]:
    soup = BeautifulSoup(html, 'html.parser')
    pizzas = []

    # Find all ion-list elements
    ion_lists = soup.find_all('ion-list')

    for ion_list in ion_lists:
        # Look for the "پیتزا" header inside this ion-list
        header_div = ion_list.find('div', class_='div2')
        if not header_div:
            continue
        header_label = header_div.find('ion-label')
        if not header_label or header_label.get_text(strip=True) != "پیتزا":
            continue

        # Found the pizza category – now extract products
        # Products are inside ion-col elements within this ion-list
        product_cols = ion_list.find_all('ion-col')
        for col in product_cols:
            # Each product is inside an <a-food-card5> component
            food_card = col.find('a-food-card5')
            if not food_card:
                continue

            # Product name
            name_tag = food_card.find('ion-label', class_='food-title')
            if not name_tag:
                continue
            name = name_tag.get_text(strip=True)

            # Price – inside <app-product-price>
            price_comp = food_card.find('app-product-price')
            if not price_comp:
                continue

            # The final price is in an <ion-label class="food-price"> inside a div with class "container2"
            # Note: There may be an <ion-label class="offPrice"> for the original price (strikethrough)
            price_label = price_comp.find('ion-label', class_='food-price')
            if price_label:
                # Remove commas and convert to int (prices are in Tomans)
                price_text = price_label.get_text(strip=True).replace(',', '').split()[0]
                try:
                    price = int(price_text)
                except:
                    price = 0
            else:
                price = 0

            pizzas.append({
                "name": name,
                "price_toman": price
            })
        break  # Found the pizza category, no need to continue searching

    return pizzas


def scrape() -> List[Dict]:
    html = fetch_page()
    return extract_pizzas(html)


if __name__ == "__main__":
    items = scrape()
    print(f"Found {len(items)} pizzas")
    for item in items[:10]:
        print(f"{item['name']}: {item['price_toman']:,} تومان")