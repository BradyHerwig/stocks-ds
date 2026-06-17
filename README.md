# Stocks ML Data Science Project

Data science / machine learning project for stock market modeling using historical price, volume, fundamentals, and alternative data.

## Data Sources (Recommendations)

### 1. Start Here: yfinance (Easiest, Zero Friction)
- **Library**: `yfinance`
- **Pros**: No API key, simple API, daily + intraday bars, fundamentals, options chains.
- **Cons**: Unofficial (can break), rate limiting, occasional data quality issues, survivorship bias.
- **Best for**: Rapid prototyping, EDA, initial feature engineering, and learning.
- **Example**:
  ```python
  import yfinance as yf
  data = yf.download("AAPL MSFT", start="2015-01-01", end="2025-01-01", auto_adjust=True)
  ```

### 2. Finnhub (Best Generous Free Tier)
- **Website**: https://finnhub.io
- **Free tier**: 60 calls per minute — very usable for development.
- **Strengths**: Real-time quotes, historical candles, company fundamentals, news, earnings, sentiment scores.
- **Python client**: `pip install finnhub-python`
- **Get API key**: Sign up at finnhub.io (free).

### 3. Polygon.io (Best Quality & Reliability for Serious Work)
- **Website**: https://polygon.io (also referenced as Massive in some 2026 materials)
- **Free tier**: Limited (5 calls/min) — enough for exploration. Paid plans start reasonably for real projects.
- **Strengths**: Clean normalized data, excellent historical coverage, aggregates (bars), snapshots, fundamentals, news, options, WebSockets for real-time.
- **Python client**: `pip install polygon-api-client`
- **Highly recommended** by quants for backtesting because data is cleaner and more consistent than yfinance.

### 4. Other Strong Options
- **Twelve Data** — Good free tier (800 calls/day), reliable.
- **EODHD (EOD Historical Data)** — Frequently cited as one of the best Yahoo Finance alternatives. Strong on global stocks + fundamentals.
- **Financial Modeling Prep (FMP)** — Excellent for financial statements, ratios, and historical data.
- **Kaggle** — Static datasets for quick benchmarks or competitions (search "stock prices" or "S&P 500").

### Advice for ML Projects
- **Prototype** with yfinance.
- **Production / serious modeling** → move to Polygon or Finnhub (or combine: prices from Polygon + news/sentiment from Finnhub).
- Always store **raw** data immutably (parquet format is excellent for time series).
- Handle corporate actions (splits, dividends) — most good APIs have `auto_adjust=True` or adjusted columns.
- Watch for **survivorship bias** and **look-ahead bias** in features/labels.
- For fundamentals + macro: combine with FRED (via `fredapi`) or Polygon/FMP statements.
- Consider data versioning later (DVC) once you have valuable datasets.

Store API keys in environment variables (see `.env.example`).

## Project Structure

This follows a practical data-science layout (inspired by Cookiecutter Data Science + modern src layout):

```
stocks/
├── README.md
├── .gitignore
├── requirements.txt
├── .env.example                 # Copy to .env and fill in keys
├── pyproject.toml               # (optional) modern packaging
│
├── data/
│   ├── raw/                     # Immutable original downloads (parquet recommended)
│   ├── processed/               # Cleaned / feature-ready data
│   └── external/                # Third-party static datasets (Kaggle, etc.)
│
├── notebooks/
│   ├── 00_data_acquisition.ipynb
│   ├── 01_eda.ipynb
│   ├── 02_feature_engineering.ipynb
│   └── 03_modeling.ipynb
│
├── src/
│   └── stocks/                  # Reusable Python package
│       ├── __init__.py
│       ├── config.py            # Config, paths, settings
│       ├── data/
│       │   ├── __init__.py
│       │   └── loaders.py       # yfinance, Polygon, Finnhub wrappers
│       ├── features/
│       │   ├── __init__.py
│       │   └── technical.py     # Indicators, transformations
│       ├── models/
│       │   └── ...
│       └── utils/
│           └── io.py            # Save/load parquet, etc.
│
├── scripts/
│   └── download_data.py         # Reproducible data download scripts
│
├── config/                      # YAML/JSON/TOML configs (tickers, params, etc.)
│
├── models/                      # Serialized models (joblib, ONNX, etc.)
│
├── reports/
│   └── figures/                 # Plots for reports/presentations
│
└── tests/
```

### Why this layout?
- `data/raw` is sacred — never modify in place.
- `src/stocks` makes your code importable and testable (`from stocks.data.loaders import ...`).
- Notebooks for exploration; scripts + src for production pipelines.
- Easy to add MLOps later (MLflow, Prefect, etc.).

## Quick Start

1. **Environment**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. **API Keys**
   ```powershell
   copy .env.example .env
   # Edit .env and add your keys
   ```

3. **Explore data**
   Open `notebooks/00_data_acquisition.ipynb`.

4. **Use the package**
   ```python
   from stocks.data.loaders import download_prices
   df = download_prices(["AAPL", "MSFT"], start="2020-01-01")
   ```

## Next Steps Ideas
- Define your universe (S&P 500 constituents? Russell 2000? Custom list).
- Decide prediction target (next-day return, direction, volatility, etc.).
- Feature ideas: technical indicators, volatility regimes, earnings surprises, sentiment, macro variables.
- Proper walk-forward / purged K-fold validation for time series.
- Start simple (linear + XGBoost/LightGBM) before deep learning.

## License
Private / internal project.

Contributions welcome (if this becomes a team repo).
