import pandas as pd

from scripts.build_strategy_001j_broker_liquid_universe import build


def _write(path, multiplier, days=20):
    rows = []
    for day in pd.date_range("2026-01-01", periods=days, freq="B"):
        for minute in ["09:15", "09:20", "09:25"]:
            ts = pd.Timestamp(f"{day.date()} {minute}", tz="Asia/Kolkata")
            rows.append({"timestamp": ts, "close": multiplier, "volume": 1000})
    pd.DataFrame(rows).to_csv(path, index=False)


def test_broker_universe_uses_only_formation_data(tmp_path):
    _write(tmp_path / "AAA.csv", 200)
    _write(tmp_path / "BBB.csv", 100)
    ranking, membership = build(
        tmp_path,
        "2026-01-01T00:00:00+05:30",
        "2026-01-28T23:59:00+05:30",
        "2026-02-28T15:30:00+05:30",
        top_n=1,
        min_days=15,
    )
    assert ranking.iloc[0]["symbol"] == "AAA"
    assert list(membership["symbol"]) == ["AAA"]
    assert membership.iloc[0]["effective_from"] == "2026-01-29T00:04:00+05:30"


def test_broker_universe_does_not_use_strategy_returns(tmp_path):
    _write(tmp_path / "AAA.csv", 200)
    ranking, membership = build(
        tmp_path,
        "2026-01-01T00:00:00+05:30",
        "2026-01-28T23:59:00+05:30",
        "2026-02-28T15:30:00+05:30",
        top_n=1,
        min_days=15,
    )
    assert "strategy_return" not in ranking.columns
    assert "selected_by_return" not in ranking.columns
