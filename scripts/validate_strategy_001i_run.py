"""Validate integrity of a Strategy 001I prospective paper/shadow run."""

from __future__ import annotations

import argparse

from src.research.strategy_001i_validation import validate_run


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir", help="Path to data/prospective/strategy_001i")
    args = parser.parse_args()

    errors = validate_run(args.output_dir)
    if errors:
        print("Strategy 001I validation FAILED")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("Strategy 001I validation PASSED: no prospective-ledger integrity errors found.")


if __name__ == "__main__":
    main()
