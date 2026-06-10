"""Basic tests for data loaders (expand as you build)."""
import pandas as pd
import pytest

# Example: import your code once the package is installed in editable mode
# from stocks.data.loaders import download_prices


def test_example():
    """Placeholder test — replace with real tests."""
    assert 1 + 1 == 2


def test_parquet_roundtrip(tmp_path):
    """Demonstrate that we can write/read parquet (core for this project)."""
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4.0, 5.0, 6.0]})
    path = tmp_path / "test.parquet"
    df.to_parquet(path, compression="zstd")
    loaded = pd.read_parquet(path)
    pd.testing.assert_frame_equal(df, loaded)
