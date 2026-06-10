"""Project configuration, paths, and settings."""
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Project root (two levels up from src/stocks/config.py)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Data directories
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
DATA_EXTERNAL = PROJECT_ROOT / "data" / "external"

# Model and report directories
MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

# Ensure directories exist
for d in [DATA_RAW, DATA_PROCESSED, DATA_EXTERNAL, MODELS_DIR, FIGURES_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# API Keys (from environment)
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
FRED_API_KEY = os.getenv("FRED_API_KEY")

# Default tickers / universe example (S&P 500 sample or your list)
DEFAULT_TICKERS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK-B", "JPM", "V",
]

# Time series settings
DEFAULT_START_DATE = "2010-01-01"
DEFAULT_END_DATE = None  # None = today

# Parquet compression for efficient storage
PARQUET_COMPRESSION = "zstd"
