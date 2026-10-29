# Price Scraper & Comparator

## Problem
Local businesses struggle to monitor competitor pricing manually. Checking multiple websites daily is tedious, error-prone, and often leads to missed opportunities when prices drop.

## Solution
A standard-library-only Python CLI that fetches product pages, extracts the price using `html.parser`, and logs the historical data in SQLite. It alerts the user when a price drops below a specified threshold or compared to the previous check.

## Impact
- Replaces manual price checking with a single command.
- Maintains a historical database to track pricing trends.
- Ethical scraping: respects the target server with a custom User-Agent and built-in rate limiting.

## Stack
- Python 3.11+
- `urllib`, `html.parser`, `sqlite3`, `argparse`
- No external dependencies.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
cp .env.example .env
# edit .env with your preferred DB path and User-Agent
```

## Usage
Run against a test sandbox site (`books.toscrape.com`):
```bash
python scraper.py --url "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html" --name "A Light in the Attic" --threshold 50.00
```

Run it again to see the price comparison logic in action.

## Architectural decisions
- **No BeautifulSoup:** The standard library's `html.parser` is perfectly capable of extracting specific tags. Adding a third-party dependency for a single `<p>` tag violates the "zero dependencies" constraint of this project.
- **SQLite for history:** Storing only the current price is useless. Storing the history allows for future features like trend analysis.
- **Ethical scraping:** Includes a 1-second `time.sleep()` and a transparent User-Agent. We target `books.toscrape.com`, an open sandbox designed specifically for this purpose.
- **Fail-fast configuration:** Exits immediately if the HTML structure changes or the network request fails, preventing silent data corruption.

- ## Security Threat Model
This tool is designed strictly as a local CLI. The user executing the command is the sole operator. Therefore, SSRF (Server-Side Request Forgery) is not applicable because the user explicitly provides the target URL. If this code is ever adapted into an HTTP microservice, the URL input **must** be validated against an allowlist of domains to prevent SSRF.
