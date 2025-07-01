#!/usr/bin/env python3
"""Fetch Altcoin Season Index and append to CSV."""
import csv
import logging
from datetime import datetime, timezone
from pathlib import Path
import sys
import time

import requests
from bs4 import BeautifulSoup

URL = "https://www.blockchaincenter.net/en/altcoin-season-index/"
CSV_PATH = Path(__file__).with_parent.joinpath("data", "altcoin_index_history.csv")
LOG_PATH = Path(__file__).with_parent.joinpath("logs", "scraper.log")

LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def fetch_html(url: str, max_retries: int = 3, timeout: int = 10) -> str:
    delay = 1
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(
                url,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/114.0 Safari/537.36"
                    )
                },
                timeout=timeout,
            )
            response.raise_for_status()
            return response.text
        except Exception as exc:
            logging.warning("Attempt %s failed: %s", attempt, exc)
            if attempt == max_retries:
                raise
            time.sleep(delay)
            delay *= 2

def extract_value(html: str) -> int:
    soup = BeautifulSoup(html, "html.parser")
    div = soup.select_one('div[style*="font-size:88px"]')
    if div is None:
        raise ValueError("Target div not found")
    return int(div.get_text(strip=True))

def append_to_csv(value: int) -> None:
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    write_header = not CSV_PATH.exists()
    with CSV_PATH.open("a", newline="") as fp:
        writer = csv.writer(fp)
        if write_header:
            writer.writerow(["timestamp", "value"])
        writer.writerow([
            datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(),
            value,
        ])

def main() -> None:
    logging.info("Scraper started")
    try:
        html = fetch_html(URL)
        value = extract_value(html)
        append_to_csv(value)
        logging.info("Scraper finished successfully: %s", value)
    except Exception as exc:
        logging.exception("Scraper failed: %s", exc)
        sys.exit(1)

if __name__ == "__main__":
    main()
