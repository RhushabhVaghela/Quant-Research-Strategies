from pathlib import Path

import pandas as pd
import pytest

from scripts.fetch_research_universe_kite_data import _load_symbols, _output_path


def test_load_symbols_requires_symbol_column(tmp_path: Path) -> None:
    path = tmp_path / "symbols.csv"
    pd.DataFrame({"ticker": ["AAA"]}).to_csv(path, index=False)

    with pytest.raises(ValueError, match="symbol"):
        _load_symbols(path)


def test_load_symbols_normalizes_and_deduplicates(tmp_path: Path) -> None:
    path = tmp_path / "symbols.csv"
    pd.DataFrame({"symbol": [" aaa ", "AAA", "bbb", None]}).to_csv(path, index=False)

    assert _load_symbols(path) == ["AAA", "BBB"]


def test_output_path_matches_universe_audit_filename_contract(tmp_path: Path) -> None:
    assert _output_path(tmp_path, "NIFTYBEES").name == "NSE_NIFTYBEES_5minute.csv"
