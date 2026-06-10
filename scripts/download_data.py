"""
Reproducible data download script.

Usage examples:
    python scripts/download_data.py --tickers AAPL MSFT NVDA --start 2020-01-01
    python scripts/download_data.py --tickers-file config/sp500.txt --source polygon
"""
import argparse
from pathlib import Path
import sys

# Make src importable when running the script directly
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from stocks.data.loaders import download_prices
from stocks.config import DEFAULT_TICKERS


def main():
    parser = argparse.ArgumentParser(description="Download stock price data")
    parser.add_argument("--tickers", nargs="+", default=DEFAULT_TICKERS[:5],
                        help="List of tickers to download")
    parser.add_argument("--tickers-file", type=Path,
                        help="Path to a text file with one ticker per line")
    parser.add_argument("--start", default="2015-01-01", help="Start date YYYY-MM-DD")
    parser.add_argument("--end", default=None, help="End date YYYY-MM-DD (default: today)")
    parser.add_argument("--interval", default="1d", help="Bar interval (1d, 1h, 5m, ...)")
    parser.add_argument("--source", default="yfinance",
                        choices=["yfinance", "polygon", "finnhub"],
                        help="Data source")
    parser.add_argument("--no-save", action="store_true", help="Do not persist raw parquet")

    args = parser.parse_args()

    if args.tickers_file:
        tickers = [line.strip() for line in args.tickers_file.read_text().splitlines()
                   if line.strip() and not line.startswith("#")]
    else:
        tickers = args.tickers

    print(f"Downloading {len(tickers)} tickers from {args.source} ...")
    df = download_prices(
        tickers=tickers,
        start=args.start,
        end=args.end,
        interval=args.interval,
        source=args.source,
        save_raw=not args.no_save,
    )

    print(f"\nDownloaded shape: {df.shape}")
    print(df.tail(3) if not df.empty else "No data returned.")


if __name__ == "__main__":
    main()
