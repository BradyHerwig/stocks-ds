"""
Stock data loaders.

Start with yfinance for zero-friction prototyping.
Upgrade to Polygon or Finnhub for production-quality data.
"""
from __future__ import annotations

import pandas as pd
from pathlib import Path
from typing import List, Optional, Union
import warnings

from ..config import DATA_RAW, DEFAULT_START_DATE, PARQUET_COMPRESSION

# Lazy imports so the package works even if not all libraries are installed yet
try:
    import yfinance as yf
except ImportError:
    yf = None

try:
    from polygon import RESTClient as PolygonClient
except ImportError:
    PolygonClient = None

try:
    import finnhub
except ImportError:
    finnhub = None


def download_prices(
    tickers: Union[str, List[str]],
    start: str = DEFAULT_START_DATE,
    end: Optional[str] = None,
    interval: str = "1d",
    source: str = "yfinance",
    save_raw: bool = True,
    auto_adjust: bool = True,
) -> pd.DataFrame:
    """
    Download historical price data (OHLCV).

    Parameters
    ----------
    tickers : str or list of str
        Single ticker or list of tickers.
    start : str
        Start date in YYYY-MM-DD format.
    end : str or None
        End date. None = up to today.
    interval : str
        Data frequency: "1d", "1h", "5m", etc. (provider dependent).
    source : {"yfinance", "polygon", "finnhub"}
        Data provider.
    save_raw : bool
        Whether to persist the raw data to data/raw/ as parquet.
    auto_adjust : bool
        Adjust for splits/dividends (yfinance mainly).

    Returns
    -------
    pd.DataFrame
        Multi-index (Date, Ticker) or single-ticker DataFrame with OHLCV columns.
    """
    if isinstance(tickers, str):
        tickers = [tickers]

    tickers = [t.upper() for t in tickers]

    if source == "yfinance":
        if yf is None:
            raise ImportError("yfinance not installed. Run: pip install yfinance")
        df = yf.download(
            tickers,
            start=start,
            end=end,
            interval=interval,
            auto_adjust=auto_adjust,
            progress=False,
            group_by="ticker" if len(tickers) > 1 else "column",
        )

        # Standardize column names and shape
        if len(tickers) == 1:
            df = df.rename(columns=str.lower)
            df["ticker"] = tickers[0]
            df = df.reset_index().set_index(["Date", "ticker"])
        else:
            # yfinance returns columns as (ticker, field) when group_by="ticker"
            df = df.stack(level=0, future_stack=True).rename_axis(["Date", "ticker"])
            df.columns = df.columns.str.lower()

    elif source == "polygon":
        if PolygonClient is None:
            raise ImportError("polygon-api-client not installed.")
        # Note: requires POLYGON_API_KEY in env for real usage
        client = PolygonClient()
        frames = []
        for t in tickers:
            aggs = list(
                client.get_aggs(
                    ticker=t,
                    multiplier=1,
                    timespan=interval.replace("1", "").replace("d", "day").replace("m", "minute"),
                    from_=start,
                    to=end or "today",
                    limit=50000,
                )
            )
            if not aggs:
                continue
            tmp = pd.DataFrame(aggs)
            tmp["ticker"] = t
            tmp["Date"] = pd.to_datetime(tmp["timestamp"], unit="ms").dt.date
            frames.append(tmp)
        if not frames:
            return pd.DataFrame()
        df = pd.concat(frames)
        df = df.rename(
            columns={
                "open": "open",
                "high": "high",
                "low": "low",
                "close": "close",
                "volume": "volume",
            }
        )
        df = df[["Date", "ticker", "open", "high", "low", "close", "volume"]]
        df = df.set_index(["Date", "ticker"])

    elif source == "finnhub":
        if finnhub is None:
            raise ImportError("finnhub-python not installed.")
        # Finnhub example uses resolution strings like "D", "60"
        # This is a simplified implementation; expand as needed.
        warnings.warn("Finnhub loader is a stub — extend with proper candle endpoint.")
        # Placeholder: return empty for now
        df = pd.DataFrame()

    else:
        raise ValueError(f"Unknown source: {source}")

    if save_raw and not df.empty:
        filename = f"prices_{'_'.join(tickers[:3])}{'+' if len(tickers) > 3 else ''}_{start}_{end or 'latest'}_{interval}.parquet"
        out_path = DATA_RAW / filename
        df.to_parquet(out_path, compression=PARQUET_COMPRESSION)
        print(f"Saved raw data → {out_path}")

    return df


def get_ticker_info(ticker: str, source: str = "yfinance") -> dict:
    """Fetch basic company info / metadata."""
    if source == "yfinance":
        if yf is None:
            raise ImportError("yfinance not installed.")
        t = yf.Ticker(ticker)
        return {
            "ticker": ticker,
            "name": t.info.get("shortName"),
            "sector": t.info.get("sector"),
            "industry": t.info.get("industry"),
            "market_cap": t.info.get("marketCap"),
            "exchange": t.info.get("exchange"),
        }
    # Add Polygon / Finnhub implementations as needed
    return {"ticker": ticker}


if __name__ == "__main__":
    # Quick test
    print("Testing yfinance loader...")
    prices = download_prices(["AAPL"], start="2024-01-01", save_raw=False)
    print(prices.head())
    print("\nShape:", prices.shape)
