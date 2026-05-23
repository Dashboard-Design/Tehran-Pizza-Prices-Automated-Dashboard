import requests
import re
from typing import List, Dict


def fetch_baguette_js():
    url = "https://baguette.ir/static/menu.js?v=1779493637"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/javascript, */*",
        "Referer": "https://baguette.ir/",
    }
    resp = requests.get(url, headers=headers)
    resp.encoding = "utf-8"  # The file is UTF-8; the garbled display earlier was a viewer issue
    return resp.text


def extract_products_by_category(js_text, category_index=0):
    """
    Extract all products belonging to a specific category index.
    Each product block looks like:
        x=[];
        x[0]=0;
        x[1]="product name";
        x[2]=price;
        x[3]="description";
        x[4]="image_url";
        products.push(x);
    """
    # Split the text by "products.push(x);" to get each product block
    blocks = js_text.split("products.push(x);")
    products = []
    for block in blocks:
        # Find the category assignment
        cat_match = re.search(r'x\[0\]\s*=\s*(\d+)', block)
        if not cat_match:
            continue
        cat = int(cat_match.group(1))
        if cat != category_index:
            continue

        # Find name
        name_match = re.search(r'x\[1\]\s*=\s*"([^"]*)"', block)
        # Find price
        price_match = re.search(r'x\[2\]\s*=\s*(\d+)', block)
        if name_match and price_match:
            name = name_match.group(1)
            price_rials = int(price_match.group(1))
            price_toman = price_rials // 10  # convert to Tomans
            products.append({
                "name": name,
                "price_toman": price_toman
            })
    return products


def scrape(category_index=0) -> List[Dict]:
    js = fetch_baguette_js()
    products = extract_products_by_category(js, category_index)
    if not products:
        # Debug: print available categories
        print("No products found for category index", category_index)
        # Optionally list all category indices found
        cats_found = set()
        blocks = js.split("products.push(x);")
        for block in blocks:
            m = re.search(r'x\[0\]\s*=\s*(\d+)', block)
            if m:
                cats_found.add(int(m.group(1)))
        print("Available category indices in the file:", sorted(cats_found))
        raise ValueError(f"No products for index {category_index}")
    return products