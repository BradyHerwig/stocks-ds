"""
Technical indicator and feature engineering helpers.

Start simple (returns, volatility, moving averages) and expand.
Consider using the 'ta' library or pandas-ta for many indicators.
"""
from __future__ import annotations
import pandas as pd
import numpy as np


def add_returns(df: pd.DataFrame, price_col: str = "close") -> pd.DataFrame:
    """Add simple and log returns."""
    df = df.copy()
    df["return"] = df[price_col].pct_change()
    df["log_return"] = np.log(df[price_col] / df[price_col].shift(1))
    return df


def add_volatility(df: pd.DataFrame, window: int = 20, price_col: str = "close") -> pd.DataFrame:
    """Rolling realized volatility (annualized, assuming daily data)."""
    df = df.copy()
    ret = df[price_col].pct_change()
    df[f"vol_{window}d"] = ret.rolling(window).std() * np.sqrt(252)
    return df


def add_moving_averages(
    df: pd.DataFrame, windows: list[int] = (10, 20, 50, 200), price_col: str = "close"
) -> pd.DataFrame:
    """Simple moving averages."""
    df = df.copy()
    for w in windows:
        df[f"sma_{w}"] = df[price_col].rolling(w).mean()
    return df


def add_rsi(df: pd.DataFrame, period: int = 14, price_col: str = "close") -> pd.DataFrame:
    """Relative Strength Index (simple implementation)."""
    df = df.copy()
    delta = df[price_col].diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    df[f"rsi_{period}"] = 100 - (100 / (1 + rs))
    return df


# Example usage inside a notebook or pipeline:
# df = add_returns(df)
# df = add_volatility(df)
# df = add_moving_averages(df)
# df = add_rsi(df)
