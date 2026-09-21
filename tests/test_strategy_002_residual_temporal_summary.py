from pathlib import Path

import pandas as pd

from scripts.summarize_strategy_002_residual_temporal_conditioning import main


def test_summary_rejects_holdout(tmp_path, monkeypatch):
    breadth = pd.DataFrame(
        [{
            "period": "Q1_time",
            "condition": "prior_negative",
            "component": "close_to_close",
            "horizon_bars": 1,
            "median_instrument_mean": 0.001,
            "positive_instrument_fraction": 1.0,
        }]
    )
    breadth.to_csv(tmp_path / "residual_temporal_conditioning_breadth.csv", index=False)
    pd.Series({
        "holdout_used": True,
        "strategy_pnl_calculated": False,
        "optimization_performed": False,
        "exploratory_start": "2025-09-18",
        "exploratory_end": "2026-06-09",
        "included_instruments": ["A"],
    }).to_json(tmp_path / "run_manifest.json")
    monkeypatch.setattr("sys.argv", ["prog", str(tmp_path)])
    try:
        main()
    except SystemExit as exc:
        assert "holdout_used" in str(exc)
    else:
        raise AssertionError("Expected holdout gate to reject the summary")
