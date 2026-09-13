from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def test_initial_universe_manifest_is_reproducible_and_has_required_fields():
    path = ROOT / "research" / "universe_candidates.csv"
    df = pd.read_csv(path)

    assert list(df.columns) == ["symbol", "category", "rationale"]
    assert len(df) >= 10
    assert df["symbol"].is_unique
    assert df["symbol"].notna().all()
    assert df["category"].notna().all()
    assert df["rationale"].str.len().gt(0).all()

    categories = set(df["category"])
    assert "broad_market_etf" in categories
    assert "sector_etf" in categories
    assert "large_cap_equity" in categories
