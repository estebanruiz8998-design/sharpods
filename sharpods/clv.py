"""Closing line value — the model's own report card.

Squares & Sharps and Sharper converge on the same epistemological point: over
any sample a bettor can actually collect, win-loss record is dominated by
variance, but *beating the closing line* is measurable immediately and is the
strongest known predictor of long-term profit. The closing price at a sharp
book is the most efficient public estimate of the outcome's probability; if
your bets systematically beat it, you have edge, and if they don't, your
"winning" record is luck on a timer.

SharpOds therefore treats CLV as the primary feedback loop: the engine's
market/model blend weights (fairline.blend_market_and_model) should only move
toward the model as positive CLV accumulates with statistical significance.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from sharpods.odds import devig


@dataclass(frozen=True)
class ClvRecord:
    bet_decimal_odds: float
    closing_decimal_odds: float
    # Closing odds for every outcome of the market, used to devig the close.
    closing_market_odds: tuple[float, ...] = ()
    outcome_index: int = 0

    def clv_pct(self) -> float:
        """Raw CLV: how much better your price was than the close.

        clv = bet_odds / closing_odds - 1. Positive means you beat the close.
        Note this includes the closing vig; prefer no_vig_clv_pct when the
        full closing market is available.
        """
        return self.bet_decimal_odds / self.closing_decimal_odds - 1.0

    def no_vig_clv_pct(self) -> float:
        """CLV measured against the devigged closing price — the true
        benchmark (Buchdahl): clv = bet_odds * fair_closing_prob - 1, i.e.
        the EV of the bet under the hypothesis that the devigged close is the
        truth."""
        if len(self.closing_market_odds) < 2:
            raise ValueError("need full closing market to devig")
        fair = devig(list(self.closing_market_odds), "power")
        return self.bet_decimal_odds * fair[self.outcome_index] - 1.0


@dataclass
class ClvLedger:
    records: list[ClvRecord]

    def mean_clv(self, no_vig: bool = True) -> float:
        if not self.records:
            raise ValueError("empty ledger")
        values = [
            r.no_vig_clv_pct() if no_vig and len(r.closing_market_odds) >= 2 else r.clv_pct()
            for r in self.records
        ]
        return sum(values) / len(values)

    def beat_close_rate(self) -> float:
        if not self.records:
            raise ValueError("empty ledger")
        return sum(1 for r in self.records if r.clv_pct() > 0) / len(self.records)

    def t_statistic(self, no_vig: bool = True) -> float:
        """One-sample t statistic for mean CLV > 0.

        Buchdahl's discipline: do not believe an edge until the record is
        statistically distinguishable from luck. |t| >~ 2 with n >= 30 is the
        conventional threshold for promoting model weight.
        """
        n = len(self.records)
        if n < 2:
            raise ValueError("need at least two records")
        values = [
            r.no_vig_clv_pct() if no_vig and len(r.closing_market_odds) >= 2 else r.clv_pct()
            for r in self.records
        ]
        mean = sum(values) / n
        var = sum((v - mean) ** 2 for v in values) / (n - 1)
        if var == 0.0:
            return math.inf if mean > 0 else 0.0
        return mean / math.sqrt(var / n)

    def verdict(self) -> str:
        n = len(self.records)
        if n < 30:
            return f"insufficient sample (n={n}); keep logging"
        t = self.t_statistic()
        mean = self.mean_clv()
        if t >= 2.0 and mean > 0:
            return f"edge confirmed: mean CLV {mean:+.2%}, t={t:.2f}, n={n}"
        if mean > 0:
            return f"promising but unproven: mean CLV {mean:+.2%}, t={t:.2f}, n={n}"
        return f"no edge vs close: mean CLV {mean:+.2%}, t={t:.2f}, n={n}"
