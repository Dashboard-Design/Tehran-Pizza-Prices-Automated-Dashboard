"""
Orchestrator for all pizza price scrapers.
Runs each scraper, stores results in SQLite, and optionally exports a CSV.
"""

import sqlite3
import csv
import sys
from os import name
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Callable

# Import all scrapers (each must have a scrape() function)
from scrapers import shila, meykhosh, perperook, chickenfamily, sib360, baguette, atawich, khatoonpizza, haida, pizzahot

# Define restaurants with their scraper module and a display name
# Add more restaurants here as you complete them
RESTAURANTS = [
    {"name": "shila", "module": shila},
    {"name": "meykhosh", "module": meykhosh},
    {"name": "perperok", "module": perperook},
    {"name": "chickenfamily", "module": chickenfamily},
    {"name": "sib360", "module": sib360},
    {"name": "baguette", "module": baguette},
    {"name": "atawich", "module": atawich},
    {"name": "pizzahot", "module": pizzahot},
    {"name": "khatoonpizza", "module": khatoonpizza },
    {"name": "haida", "module": haida}
]

# ----------------------------------------------------------------------
# Database setup
# ----------------------------------------------------------------------
DB_DIR = Path("database")
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / "pizza_prices.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant TEXT,
            product_name TEXT,
            price_toman INTEGER,
            collected_at DATE
        )
    """)
    conn.commit()
    return conn

def insert_products(conn, restaurant: str, products: List[Dict], date_str: str):
    cursor = conn.cursor()
    for p in products:
        # Each scraper returns dict with 'name' (or 'title') and 'price_toman'
        name = p.get("name") or p.get("title")
        price = p.get("price_toman")
        if name and price is not None:
            cursor.execute(
                "INSERT INTO prices (restaurant, product_name, price_toman, collected_at) VALUES (?, ?, ?, ?)",
                (restaurant, name, price, date_str)
            )
    conn.commit()

# ----------------------------------------------------------------------
# CSV export (optional)
# ----------------------------------------------------------------------
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def export_to_csv(all_data: List[Dict], timestamp: str):
    """Export all products from all restaurants into one CSV file."""
    csv_file = DATA_DIR / f"prices_{timestamp}.csv"
    with open(csv_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["restaurant", "product_name", "price_toman", "collected_at"])
        for row in all_data:
            writer.writerow([row["restaurant"], row["product_name"], row["price_toman"], row["collected_at"]])
    print(f"📄 Exported CSV to {csv_file}")

# ----------------------------------------------------------------------
# Main orchestrator
# ----------------------------------------------------------------------
def main():
    print("=" * 60)
    print("Starting pizza price collection pipeline")
    print("=" * 60)

    run_date = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    conn = init_db()
    all_rows_for_csv = []  # collect for optional CSV export

    failed_restaurants = []

    for rest in RESTAURANTS:
        name = rest["name"]
        module = rest["module"]
        print(f"\n--- Scraping {name.upper()} ---")
        try:
            products = module.scrape()   # expects list of dicts with name/title and price_toman
            if not products:
                print(f"⚠️ No products returned for {name}")
                continue
            insert_products(conn, name, products, run_date)
            # Prepare for CSV
            for p in products:
                all_rows_for_csv.append({
                    "restaurant": name,
                    "product_name": p.get("name") or p.get("title"),
                    "price_toman": p.get("price_toman"),
                    "collected_at": run_date
                })
            print(f"✅ {name}: {len(products)} products inserted")
        except Exception as e:
            print(f"❌ FAILED {name}: {e}")
            failed_restaurants.append(name)

    conn.close()

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    successful = len(RESTAURANTS) - len(failed_restaurants)
    print(f"Successful: {successful}/{len(RESTAURANTS)}")
    if failed_restaurants:
        print(f"Failed: {', '.join(failed_restaurants)}")
        sys.exit(1)   # optional: mark workflow as failed if any scraper errors
    else:
        print("All restaurants scraped successfully!")

    # Optional: export CSV
    if all_rows_for_csv:
        export_to_csv(all_rows_for_csv, timestamp)

if __name__ == "__main__":
    main()