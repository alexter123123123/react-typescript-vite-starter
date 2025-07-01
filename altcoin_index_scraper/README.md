# Altcoin Index Scraper

This directory contains a simple Python script that fetches the Altcoin Season Index from [Blockchain Center](https://www.blockchaincenter.net/en/altcoin-season-index/) once every 24 hours. The value is appended to `data/altcoin_index_history.csv` with an ISO‑8601 timestamp. Logs are written to `logs/scraper.log`.

## Setup

1. Ensure Python 3.9 or newer is installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the scraper manually:
   ```bash
   python altcoin_index_scraper.py
   ```

## Scheduling

On Linux, you can run the scraper daily via cron. Example (runs at 03:05 UTC every day):

```cron
5 3 * * * /usr/bin/python3 /path/to/altcoin_index_scraper/altcoin_index_scraper.py
```

If using a cloud provider, schedule the script with a job that runs every 24 hours.

## Files

- `altcoin_index_scraper.py` – main script
- `requirements.txt` – Python dependencies
- `data/altcoin_index_history.csv` – output CSV (created automatically)
- `logs/scraper.log` – log file
