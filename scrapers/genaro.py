import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


async def scrape_gennaro():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://gennaro-pas.ir/menu", wait_until="networkidle")
        await page.wait_for_selector('ion-label:has-text("پیتزا")', timeout=10000)
        html = await page.content()
        await browser.close()

    soup = BeautifulSoup(html, 'html.parser')
    # Find the pizza category as before
    pizza_list = None
    for ion_list in soup.find_all('ion-list'):
        div2 = ion_list.find('div', class_='div2')
        if div2:
            label = div2.find('ion-label')
            if label and label.get_text(strip=True) == "پیتزا":
                pizza_list = ion_list
                break
    if not pizza_list:
        return []

    pizzas = []
    for col in pizza_list.find_all('ion-col'):
        food_card = col.find('a-food-card5')
        if not food_card:
            continue
        name_tag = food_card.find('ion-label', class_='food-title')
        if not name_tag:
            continue
        name = name_tag.get_text(strip=True)
        price_comp = food_card.find('app-product-price')
        if not price_comp:
            continue
        price_label = price_comp.find('ion-label', class_='food-price')
        if not price_label:
            continue
        price_text = price_label.get_text(strip=True)
        if price_text.endswith('ت'):
            price_text = price_text[:-1].strip()
        price_int = int(''.join(ch for ch in price_text if ch.isdigit()))
        pizzas.append({"name": name, "price_toman": price_int})
    return pizzas


def scrape():
    return asyncio.run(scrape_gennaro())


if __name__ == "__main__":
    items = scrape()
    print(f"Found {len(items)} pizzas")
    for item in items[:5]:
        print(f"{item['name']}: {item['price_toman']:,} تومان")