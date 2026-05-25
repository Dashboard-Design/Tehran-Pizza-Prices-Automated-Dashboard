# 🍕 Tehran Pizza Price Tracker

Automated monthly scraping of 30‑cm pizza prices from 14 popular fast‑food chains in Tehran. Data is stored in a SQLite database for trend analysis and can be exported as CSV.

## 📌 Overview

- **Scrapers** – Each restaurant has a dedicated module using either a hidden API or static HTML parsing. All scrapers use only `requests` and `BeautifulSoup` – no browser automation.
- **Orchestrator** – `Pizza_Prices_Pipeline.py` runs all scrapers, handles errors, inserts data into SQLite, and exports a combined CSV.
- **Data storage** – SQLite database (`database/pizza_prices.db`) keeps a historical record. The `data/` folder contains timestamped CSV snapshots.
- **Automation** – Automated and cheduled via cron or GitHub Actions.

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/tehran-pizza-prices.git
cd tehran-pizza-prices
```
### 2. Clone the repository
```
pip install -r requirements.txt
```
### 3. Run the orchestrator
```
python Pizza_Prices_Pipeline.py
```

On first run, it will:
- Create the database/ folder and pizza_prices.db with the required table.
- Run all 14 scrapers.
- Insert all products into the database.
- Export a CSV file with the current snapshot (in data/).

##  📊 Database Schema
| Column         | Type    | Description                         |
|----------------|---------|-------------------------------------|
| `id`           | INTEGER | Primary key, auto‑increment         |
| `restaurant`   | TEXT    | Restaurant name (English slug)      |
| `product_name` | TEXT    | Pizza name (Persian)                |
| `price_toman`  | INTEGER | Price in Iranian Tomans             |
| `collected_at` | DATE    | ISO date of scraping (YYYY-MM-DD)   |


📄 License
MIT License – free to use and modify.

🙏 Acknowledgments
All restaurant websites for providing accessible menu data. Built with Python and the open‑source community.

