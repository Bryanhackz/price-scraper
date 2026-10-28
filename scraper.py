import argparse
import logging
import sys
import time
import urllib.request
import urllib.error
from contextlib import closing

from config import load_config
from db import connect, get_or_create_product, save_and_compare_price
from parser import extract_price

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("scraper")

def fetch_html(url: str, user_agent: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": user_agent})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode("utf-8")
    except urllib.error.URLError as exc:
        log.error(f"Failed to fetch {url}: {exc}")
        raise

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Track product prices and alert on drops.")
    parser.add_argument("--url", required=True, help="URL of the product to scrape.")
    parser.add_argument("--name", required=True, help="Name of the product.")
    parser.add_argument("--threshold", type=float, default=0.0, help="Alert if price drops below this amount.")
    args = parser.parse_args(argv)

    config = load_config()

    try:
        log.info(f"Fetching {args.url}")
        html = fetch_html(args.url, config.user_agent)
        
        # Respect target server resources to avoid rate-limiting or bans.
        time.sleep(1)
        
        current_price = extract_price(html)
        
        with closing(connect(config.db_path)) as conn:
            product_id = get_or_create_product(conn, args.url, args.name)
            previous_price = save_and_compare_price(conn, product_id, current_price)

    except Exception as exc:
        log.error(f"Scraping failed: {exc}")
        return 1

    log.info(f"Product: {args.name}")
    log.info(f"Current price: {current_price:.2f}")
    
    if previous_price is not None:
        if current_price < previous_price:
            drop = previous_price - current_price
            log.warning(f"PRICE DROP! Down {drop:.2f} from {previous_price:.2f}")
        elif current_price > previous_price:
            log.info(f"Price increased from {previous_price:.2f}")
        else:
            log.info("Price unchanged.")

    if args.threshold > 0 and current_price <= args.threshold:
        log.warning(f"ALERT: Price is below your threshold of {args.threshold:.2f}")

    return 0

if __name__ == "__main__":
    sys.exit(main())