"""Command-line entry point: run the full pipeline on an odds snapshot.

    sharpods data/sample_odds.json --bankroll 10000
    python -m sharpods data/sample_odds.json
"""

from __future__ import annotations

import argparse
import sys

from sharpods.engine import Engine, render_bet_card
from sharpods.io import load_slate
from sharpods.portfolio import RiskPolicy


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sharpods",
        description="SharpOds: rank the best bets on the market from an odds snapshot.",
    )
    parser.add_argument("snapshot", help="path to odds snapshot JSON")
    parser.add_argument("--bankroll", type=float, default=10_000.0)
    parser.add_argument(
        "--kelly", type=float, default=0.25, help="fractional Kelly multiplier (default 0.25)"
    )
    parser.add_argument(
        "--min-ev", type=float, default=0.01, help="minimum EV to bet (default 0.01 = 1%%)"
    )
    parser.add_argument(
        "--devig",
        default="power",
        choices=["multiplicative", "additive", "power", "shin", "odds_ratio"],
        help="devig method for the fair line (default power)",
    )
    parser.add_argument(
        "--market-weight",
        type=float,
        default=0.75,
        help="weight on market vs fundamental model in the blend (default 0.75)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    slate = load_slate(args.snapshot)
    engine = Engine(
        registry=slate.registry(),
        policy=RiskPolicy(kelly_multiplier=args.kelly, min_ev=args.min_ev),
        devig_method=args.devig,
        market_weight=args.market_weight,
    )
    card = engine.run(
        slate.snapshots,
        bankroll=args.bankroll,
        model_probabilities=slate.model_probabilities or None,
        history=slate.history or None,
    )
    print(render_bet_card(card, args.bankroll))
    return 0


if __name__ == "__main__":
    sys.exit(main())
