import pandas as pd
import pytest

from scripts.validate_strategy_001j_u1_membership import validate


def test_empty_membership_is_rejected(tmp_path) -> None:
    path = tmp_path / "membership.csv"
    path.write_text("symbol,effective_from,effective_to\n", encoding="utf-8")
    with pytest.raises(SystemExit, match="membership is empty"):
        validate(path)


def test_overlapping_intervals_are_rejected(tmp_path) -> None:
    path = tmp_path / "membership.csv"
    pd.DataFrame(
        [
            {"symbol": "AAA", "effective_from": "2025-01-01", "effective_to": "2025-06-01"},
            {"symbol": "AAA", "effective_from": "2025-05-15", "effective_to": "2025-12-31"},
        ]
    ).to_csv(path, index=False)
    with pytest.raises(SystemExit, match="Overlapping membership intervals"):
        validate(path)


def test_adjacent_intervals_are_valid(tmp_path) -> None:
    path = tmp_path / "membership.csv"
    pd.DataFrame(
        [
            {"symbol": "AAA", "effective_from": "2025-01-01", "effective_to": "2025-06-01"},
            {"symbol": "AAA", "effective_from": "2025-06-01", "effective_to": "2025-12-31"},
        ]
    ).to_csv(path, index=False)
    validate(path)
