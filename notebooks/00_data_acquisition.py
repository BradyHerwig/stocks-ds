"""
Notebook-style script: Data Acquisition (convert to .ipynb later or run cell-by-cell).

Run:
    python notebooks/00_data_acquisition.py
"""
# %%
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pandas as pd
import matplotlib.pyplot as plt

from stocks.data.loaders import download_prices, get_ticker_info
from stocks.config import DEFAULT_TICKERS

# %%
# 1. Download a small set of tickers with yfinance (easiest starting point)
print("Downloading sample prices...")
prices = download_prices(
    tickers=["AAPL", "MSFT", "NVDA"],
    start="2020-01-01",
    source="yfinance",
    save_raw=True,
)

print(prices.head())
print("\nIndex levels:", prices.index.names)
print("Columns:", prices.columns.tolist())

# %%
# 2. Basic exploration
print("\nDate range:", prices.index.get_level_values("Date").min(), "→",
      prices.index.get_level_values("Date").max())

# Pivot close prices for easy plotting
close = prices["close"].unstack("ticker")
close.plot(figsize=(10, 5), title="Adjusted Close Prices")
plt.grid(True)
plt.show()

# %%
# 3. Fetch metadata for one ticker
info = get_ticker_info("AAPL")
print("\nAAPL info:", info)

# %%
# 4. Next steps ideas
# - Download your full universe from config/example_tickers.txt
# - Add fundamentals via Polygon or Finnhub
# - Build a proper pipeline that updates incrementally
# - Save processed features to data/processed/

print("\nData acquisition starter complete.")
