import requests
import uuid
import time
from typing import List, Dict

def fetch_menu(retries=3):
    udid = str(uuid.uuid4())
    url = f"https://apigw.snappfood.ir/menu-read-model/37jgem?lat=35.774&long=51.418&optionalClient=PWA&client=PWA&deviceType=PWA&appVersion=6.0.0&UDID={udid}&Bonyan=true&X_ABT=%7B%22backend_delivery_fee_feature%22:false,%22backend_commission_sort_feature%22:false,%22backend_sort_home_carousel%22:false,%22backend_sort_food_party%22:false,%22backend_sort_vendor_search%22:false,%22backend_best_offer_badge_on_vendor_card%22:false,%22backend_modified_vps_in_product_search%22:false,%22backend_active_pro_filter_as_default%22:false,%22backend_jimbo_on_card_eta_color%22:false,%22backend_service_fee_feature%22:true,%22backend_food_vendor_list_default_sorting%22:0,%22backend_party_nonfood_feature%22:false,%22backend_group_order%22:true,%22backend_m41_feature%22:false,%22backend_offbox_on_supertype_section%22:false,%22backend_caffe_vendor_list_default_sorting%22:0,%22backend_juice_vendor_list_default_sorting%22:0,%22backend_confectionery_vendor_list_default_sorting%22:0,%22backend_cpc_search_v2_feature%22:false,%22backend_reorder_ux_improvement_feature%22:false,%22backend_order_history_query_feature%22:false,%22backend_ranker_service_feature%22:false%7D"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "fa-IR,fa;q=0.9",
        "Referer": "https://snappfood.ir/",
        "x-device-type": "PWA",
        "x-app-version": "6.0.0",
        "origin": "https://snappfood.ir",
    }
    session = requests.Session()
    try:
        session.get("https://snappfood.ir/", timeout=10)
    except:
        pass

    for attempt in range(retries):
        try:
            resp = session.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"Baguette attempt {attempt + 1} failed: {e}")
            time.sleep(2 ** attempt)
    return None


def extract_italian_pizzas(data):
    categories = data.get("data", {}).get("menuCategories", [])
    target = next((cat for cat in categories if cat.get("title") == "پیتزا با خمیر نازک - یک نفره"), None)
    if not target:
        raise ValueError("Category 'پیتزا با خمیر نازک - یک نفره' not found")
    pizzas = []
    for product in target.get("products", []):
        name = product.get("title")
        variations = product.get("variations", [])
        if variations:
            price = variations[0].get("price")
            pizzas.append({"name": name, "price_toman": price})
    return pizzas


def scrape() -> List[Dict]:
    """Return list of products with keys: title, price_toman"""
    data = fetch_menu()
    if not data:
        raise Exception("Failed to fetch baguette menu after retries")
    return extract_italian_pizzas(data)

