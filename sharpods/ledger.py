"""The operating ledger: settle slates, grade calibration, track CLV.

Sharper's operations chapter and Buchdahl's significance work agree that the
daily discipline — record the prediction before the game, grade it against
the close and the result after — is what separates a model from a tipster.
This module turns that discipline into code around data/track_record.json:

- ``settle_game``   grades one pre-registered fair line against the close
                    and the result;
- ``slate_metrics`` computes the day's Brier scores and fair-vs-close error;
- ``settle_ticket`` books P&L and CLV (raw and no-vig) for a live ticket;
- ``cumulative``    aggregates every settled slate into the running record
                    the daily slip reports.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sharpods.clv import ClvLedger, ClvRecord
from sharpods.odds import devig


def load_record(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def save_record(path: str | Path, record: dict[str, Any]) -> None:
    Path(path).write_text(json.dumps(record, indent=2) + "\n")


def settle_game(
    game: dict[str, Any],
    home_won: bool,
    final: str,
    close_home_decimal: float,
    close_away_decimal: float,
) -> dict[str, Any]:
    """Grade one game entry in place: no-vig close, outcome, scoreline."""
    fair_close = devig([close_home_decimal, close_away_decimal], "power")
    game["close_home_novig"] = round(fair_close[0], 4)
    game["home_won"] = home_won
    game["final"] = final
    return game


def slate_metrics(games: list[dict[str, Any]]) -> dict[str, Any]:
    """Brier (ours vs close) and fair-vs-close error over settled games.

    Only games carrying our_home_fair, close_home_novig, and home_won count;
    unsettled entries are skipped, not guessed at.
    """
    settled = [
        g
        for g in games
        if g.get("our_home_fair") is not None
        and g.get("close_home_novig") is not None
        and g.get("home_won") is not None
    ]
    if not settled:
        raise ValueError("no settled games to grade")
    n = len(settled)
    brier_ours = sum(
        (g["our_home_fair"] - (1.0 if g["home_won"] else 0.0)) ** 2 for g in settled
    ) / n
    brier_close = sum(
        (g["close_home_novig"] - (1.0 if g["home_won"] else 0.0)) ** 2
        for g in settled
    ) / n
    diffs = [abs(g["our_home_fair"] - g["close_home_novig"]) for g in settled]
    return {
        "n": n,
        "brier_ours": round(brier_ours, 4),
        "brier_close": round(brier_close, 4),
        "brier_coinflip": 0.25,
        "mean_abs_fair_vs_close": round(sum(diffs) / n, 4),
        "max_abs_fair_vs_close": round(max(diffs), 4),
    }


def settle_ticket(
    ticket: dict[str, Any],
    won: bool,
    close_side_decimal: float,
    closing_market_odds: tuple[float, ...],
    outcome_index: int,
) -> dict[str, Any]:
    """Book a live ticket: P&L, raw CLV, and no-vig CLV, in place.

    ``close_side_decimal`` is the closing price of the side the ticket is on;
    ``closing_market_odds`` is the full closing market with the ticket's side
    at ``outcome_index`` (needed to devig the close).
    """
    stake = float(ticket["stake"])
    fill = float(ticket["fill_decimal"])
    record = ClvRecord(
        bet_decimal_odds=fill,
        closing_decimal_odds=close_side_decimal,
        closing_market_odds=tuple(closing_market_odds),
        outcome_index=outcome_index,
    )
    ticket["won"] = won
    ticket["pnl"] = round(stake * (fill - 1.0) if won else -stake, 2)
    ticket["clv_raw"] = round(record.clv_pct(), 4)
    ticket["clv_novig"] = round(record.no_vig_clv_pct(), 4)
    ticket["clv"] = "settled"
    return ticket


def cumulative(record: dict[str, Any]) -> dict[str, Any]:
    """The running record across all settled slates: calibration, P&L, CLV.

    CLV verdict comes from clv.ClvLedger once at least two settled tickets
    exist; before that the sample is reported as-is.
    """
    all_games: list[dict[str, Any]] = []
    tickets: list[dict[str, Any]] = []
    for slate in record.get("slates", []):
        all_games.extend(
            g
            for g in slate.get("games", [])
            if g.get("home_won") is not None and g.get("close_home_novig") is not None
        )
        tickets.extend(
            t for t in slate.get("live_tickets", []) if t.get("clv") == "settled"
        )

    out: dict[str, Any] = {"slates_settled": sum(
        1 for s in record.get("slates", []) if s.get("games")
    )}
    if all_games:
        out["calibration"] = slate_metrics(all_games)
    if tickets:
        out["tickets"] = {
            "n": len(tickets),
            "staked": round(sum(float(t["stake"]) for t in tickets), 2),
            "pnl": round(sum(float(t["pnl"]) for t in tickets), 2),
            "record": f"{sum(1 for t in tickets if t['won'])}-"
            f"{sum(1 for t in tickets if not t['won'])}",
            "mean_clv_raw": round(
                sum(float(t["clv_raw"]) for t in tickets) / len(tickets), 4
            ),
            "mean_clv_novig": round(
                sum(float(t["clv_novig"]) for t in tickets) / len(tickets), 4
            ),
        }
        if len(tickets) >= 2:
            ledger = ClvLedger(
                [
                    ClvRecord(
                        bet_decimal_odds=float(t["fill_decimal"]),
                        closing_decimal_odds=float(t["fill_decimal"])
                        / (1.0 + float(t["clv_raw"])),
                    )
                    for t in tickets
                ]
            )
            out["tickets"]["verdict"] = ledger.verdict()
    return out
