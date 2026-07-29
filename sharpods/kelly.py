"""Kelly criterion staking — Fortune's Formula (Poundstone) made operational.

Core results the module encodes:

- Full Kelly maximizes long-run geometric growth of the bankroll:
  f* = (p*b - q) / b = edge / (decimal_odds - 1) for a binary bet.
- Full Kelly is violently volatile: there is a 1/2 chance of halving the
  bankroll at some point, a 1/n chance of ever dropping to 1/n. Practitioners
  (Thorp, Buchdahl, Peta) therefore bet a *fraction* of Kelly; 0.25-0.5 is
  the range the books converge on.
- Betting more than full Kelly is never rational: 2x Kelly has zero expected
  growth, and beyond that growth is negative even with a real edge.
- With simultaneous bets, individual Kelly fractions must be scaled down
  because they compete for the same bankroll.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass


def kelly_fraction(probability: float, decimal_odds: float) -> float:
    """Full-Kelly optimal fraction for a single binary bet.

    f* = (b*p - q) / b, with b = decimal_odds - 1, q = 1 - p.
    Returns 0.0 when there is no edge (never bet a negative-EV spot).
    """
    _check_probability(probability)
    _check_decimal(decimal_odds)
    b = decimal_odds - 1.0
    q = 1.0 - probability
    f = (b * probability - q) / b
    return max(0.0, f)


def fractional_kelly(
    probability: float, decimal_odds: float, multiplier: float = 0.25
) -> float:
    """Fractional Kelly — the practitioners' consensus throttle.

    A multiplier of 0.25 ("quarter Kelly") gives up ~25% of the growth rate
    in exchange for cutting variance by ~75% (growth is locally quadratic in
    the fraction, variance is linear); it also defends against the certainty
    that our probability estimates are imperfect (overestimated edges make
    nominal full Kelly effectively over-Kelly).
    """
    if not 0.0 < multiplier <= 1.0:
        raise ValueError(f"multiplier must be in (0, 1], got {multiplier}")
    return kelly_fraction(probability, decimal_odds) * multiplier


def expected_log_growth(
    probability: float, decimal_odds: float, fraction: float
) -> float:
    """Expected log-growth per bet at a given staking fraction.

    g(f) = p * ln(1 + f*b) + q * ln(1 - f)
    Maximized at f = f*; zero at f = 0 and (approximately) at f = 2f*.
    """
    _check_probability(probability)
    _check_decimal(decimal_odds)
    if not 0.0 <= fraction < 1.0:
        raise ValueError(f"fraction must be in [0, 1), got {fraction}")
    if fraction == 0.0:
        return 0.0
    b = decimal_odds - 1.0
    q = 1.0 - probability
    return probability * math.log1p(fraction * b) + q * math.log1p(-fraction)


def probability_of_halving(kelly_multiplier: float) -> float:
    """P(bankroll ever falls to half) when betting a constant fraction of Kelly.

    Classic continuous-approximation result: betting c×Kelly, the chance of
    ever reaching fraction x of the starting bankroll is x^(2/c - 1).
    Full Kelly (c=1): 0.5. Half Kelly (c=0.5): 0.125. Quarter: ~0.0078.
    """
    if not 0.0 < kelly_multiplier <= 1.0:
        raise ValueError("kelly multiplier must be in (0, 1]")
    return 0.5 ** (2.0 / kelly_multiplier - 1.0)


def simultaneous_kelly(
    probabilities: Sequence[float],
    decimal_odds: Sequence[float],
    multiplier: float = 0.25,
    cap_total: float = 0.25,
) -> list[float]:
    """Approximate Kelly staking for simultaneous independent bets.

    Exact simultaneous Kelly requires optimizing over all outcome
    combinations; the standard practical approximation (Thorp) computes each
    bet's individual fractional Kelly and, if the sum exceeds ``cap_total``
    of bankroll, scales all stakes down proportionally so total exposure
    stays bounded. This preserves relative sizing while respecting the joint
    bankroll constraint.
    """
    if len(probabilities) != len(decimal_odds):
        raise ValueError("probabilities and odds must align")
    fractions = [
        fractional_kelly(p, o, multiplier)
        for p, o in zip(probabilities, decimal_odds)
    ]
    total = sum(fractions)
    if total > cap_total and total > 0.0:
        scale = cap_total / total
        fractions = [f * scale for f in fractions]
    return fractions


@dataclass(frozen=True)
class StakeAdvice:
    fraction: float
    amount: float
    full_kelly_fraction: float
    multiplier: float
    expected_growth: float


def advise_stake(
    probability: float,
    decimal_odds: float,
    bankroll: float,
    multiplier: float = 0.25,
    max_fraction: float = 0.02,
) -> StakeAdvice:
    """Produce a stake recommendation with a hard per-bet cap.

    ``max_fraction`` is the risk-office override from Trading Bases (Peta ran
    fixed small position sizes): no single bet exceeds this fraction of the
    bankroll no matter what Kelly says, defending against model overconfidence.
    """
    if bankroll <= 0:
        raise ValueError("bankroll must be positive")
    full = kelly_fraction(probability, decimal_odds)
    frac = min(full * multiplier, max_fraction)
    return StakeAdvice(
        fraction=frac,
        amount=bankroll * frac,
        full_kelly_fraction=full,
        multiplier=multiplier,
        expected_growth=expected_log_growth(probability, decimal_odds, frac),
    )


def _check_probability(p: float) -> None:
    if not 0.0 < p < 1.0:
        raise ValueError(f"probability must be in (0, 1), got {p}")


def _check_decimal(decimal_odds: float) -> None:
    if decimal_odds <= 1.0:
        raise ValueError(f"decimal odds must exceed 1.0, got {decimal_odds}")
