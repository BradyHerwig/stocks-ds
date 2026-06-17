"""Data I/O path helpers."""
from pathlib import Path

from ..config import DATA_PROCESSED, DATA_RAW

DEFAULT_RAW_PRICES_FILE = "prices_AAPL_MSFT_GOOGL+_2018-01-01_latest_1d.parquet"
DEFAULT_FEATURES_FILE = "features_5tickers.parquet"


def raw_prices_path(filename: str = DEFAULT_RAW_PRICES_FILE) -> Path:
    return DATA_RAW / filename


def processed_features_path(filename: str = DEFAULT_FEATURES_FILE) -> Path:
    return DATA_PROCESSED / filename