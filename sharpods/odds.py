"""Odds conversion and vig removal (devigging).

The Logic of Sports Betting (Miller & Davidow) and Buchdahl's work establish
that a sportsbook's quoted prices embed a margin (the vig / overround), and
that recovering the book's true opinion requires stripping that margin. No
single devig method is correct in all cases:

- *Multiplicative* (proportional) assumes the margin is applied evenly across
  outcomes. Simple, but understates the favourite's true probability when the
  favourite-longshot bias is present.
- *Additive* assumes an equal absolute margin per outcome. Can produce
  negative probabilities for longshots; guarded here.
- *Power* raises each implied probability to a common exponent k solved so
  probabilities sum to 1. Pushes more of the margin onto longshots, which
  matches observed favourite-longshot bias better than multiplicative.
- *Shin* models the margin as protection against insider trading; the implied
  z (insider fraction) shifts margin toward longshots. Widely considered the
  best theoretically grounded method for markets with informed money.
- *Odds ratio* (Buchdahl's preferred practical method) applies the margin in
  proportion to each outcome's odds.

SharpOds defaults to power devig for two-way markets and Shin for three-way,
per Buchdahl's empirical comparisons in "Squares & Sharps" and his wisdom-of-
crowds articles, but every method is exposed so the engine can ensemble them.
"""

from __future__ import annotations

import math
from collections.abc import Sequence

# ---------------------------------------------------------------------------
# Conversions
# ---------------------------------------------------------------------------


def american_to_decimal(american: float) -> float:
    """Convert American odds (e.g. -110, +150) to decimal odds."""
    if american == 0 or -100 < american < 100:
        raise ValueError(f"invalid American odds: {american}")
    if american > 0:
        return 1.0 + american / 100.0
    return 1.0 + 100.0 / abs(american)


def decimal_to_american(decimal_odds: float) -> float:
    """Convert decimal odds to American odds."""
    _check_decimal(decimal_odds)
    if decimal_odds >= 2.0:
        return (decimal_odds - 1.0) * 100.0
    return -100.0 / (decimal_odds - 1.0)


def decimal_to_implied(decimal_odds: float) -> float:
    """Implied (vig-inclusive) probability of decimal odds."""
    _check_decimal(decimal_odds)
    return 1.0 / decimal_odds


def implied_to_decimal(probability: float) -> float:
    _check_probability(probability)
    return 1.0 / probability


def fractional_to_decimal(numerator: float, denominator: float) -> float:
    if denominator <= 0 or numerator < 0:
        raise ValueError("invalid fractional odds")
    return 1.0 + numerator / denominator


def _check_decimal(decimal_odds: float) -> None:
    if decimal_odds <= 1.0:
        raise ValueError(f"decimal odds must exceed 1.0, got {decimal_odds}")


def _check_probability(p: float) -> None:
    if not 0.0 < p < 1.0:
        raise ValueError(f"probability must be in (0, 1), got {p}")


# ---------------------------------------------------------------------------
# Margin measures
# ---------------------------------------------------------------------------


def overround(decimal_odds: Sequence[float]) -> float:
    """Sum of implied probabilities across all outcomes (a.k.a. the book).

    1.0 means a fair market; 1.045 means a 4.5% overround.
    """
    _check_market(decimal_odds)
    return sum(1.0 / o for o in decimal_odds)


def vig(decimal_odds: Sequence[float]) -> float:
    """Margin as a fraction of the total implied book: (overround - 1) / overround."""
    ov = overround(decimal_odds)
    return (ov - 1.0) / ov


def hold_pct(decimal_odds: Sequence[float]) -> float:
    """Book hold: expected fraction of balanced two-sided handle kept by the book.

    Miller & Davidow use this to compare how expensive markets are. For a
    standard -110/-110 spread market this is ~4.54%.
    """
    return vig(decimal_odds)


def synthetic_hold(best_decimal_odds: Sequence[float]) -> float:
    """Hold computed from the best available price on each outcome across ALL books.

    The Logic of Sports Betting: line shopping creates a 'synthetic book' whose
    hold is far lower than any single book's — sometimes negative (an arb).
    """
    return vig(best_decimal_odds)


# ---------------------------------------------------------------------------
# Devig methods — all take decimal odds for every outcome of one market and
# return no-vig probabilities summing to 1.
# ---------------------------------------------------------------------------


def devig_multiplicative(decimal_odds: Sequence[float]) -> list[float]:
    """Proportional devig: normalize implied probabilities to sum to 1."""
    _check_market(decimal_odds)
    implied = [1.0 / o for o in decimal_odds]
    total = sum(implied)
    return [p / total for p in implied]


def devig_additive(decimal_odds: Sequence[float]) -> list[float]:
    """Additive devig: subtract an equal share of the margin from each outcome.

    Falls back to multiplicative if any probability would go non-positive
    (which happens with longshots), per standard practice.
    """
    _check_market(decimal_odds)
    implied = [1.0 / o for o in decimal_odds]
    margin = (sum(implied) - 1.0) / len(implied)
    adjusted = [p - margin for p in implied]
    if any(p <= 0.0 for p in adjusted):
        return devig_multiplicative(decimal_odds)
    return adjusted


def devig_power(decimal_odds: Sequence[float], tol: float = 1e-12) -> list[float]:
    """Power devig: solve for k such that sum(implied_i ** k) == 1.

    k > 1 when there is positive margin; raising sub-1 probabilities to k > 1
    shrinks longshots proportionally more, matching favourite-longshot bias.
    Solved by bisection — the objective is monotone decreasing in k.
    """
    _check_market(decimal_odds)
    implied = [1.0 / o for o in decimal_odds]

    def total(k: float) -> float:
        return sum(p**k for p in implied)

    lo, hi = 0.5, 1.0
    while total(hi) > 1.0:
        hi *= 2.0
        if hi > 1e6:
            raise ArithmeticError("power devig failed to bracket")
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if total(mid) > 1.0:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    k = (lo + hi) / 2.0
    probs = [p**k for p in implied]
    total_p = sum(probs)
    return [p / total_p for p in probs]


def devig_shin(decimal_odds: Sequence[float], tol: float = 1e-12) -> list[float]:
    """Shin devig: models margin as insurance against insider bettors.

    Solves for z (the insider fraction) such that the Shin probabilities sum
    to 1:  p_i = (sqrt(z^2 + 4(1-z) * pi_i^2 / B) - z) / (2(1-z))
    where pi_i are implied probabilities and B = sum(pi_i).
    """
    _check_market(decimal_odds)
    implied = [1.0 / o for o in decimal_odds]
    book = sum(implied)
    if book <= 1.0:
        return devig_multiplicative(decimal_odds)

    def shin_probs(z: float) -> list[float]:
        return [
            (math.sqrt(z * z + 4.0 * (1.0 - z) * (pi * pi) / book) - z)
            / (2.0 * (1.0 - z))
            for pi in implied
        ]

    lo, hi = 0.0, 0.5
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if sum(shin_probs(mid)) > 1.0:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    z = (lo + hi) / 2.0
    probs = shin_probs(z)
    total_p = sum(probs)
    return [p / total_p for p in probs]


def devig_odds_ratio(decimal_odds: Sequence[float], tol: float = 1e-12) -> list[float]:
    """Buchdahl's odds-ratio devig.

    Solves for c such that sum(pi_i / (c + pi_i - c*pi_i)) == 1, i.e. the
    margin is applied via the odds-ratio function OR(p) = p / (p + c(1-p)).
    """
    _check_market(decimal_odds)
    implied = [1.0 / o for o in decimal_odds]

    def total(c: float) -> float:
        return sum(pi / (c + pi - c * pi) for pi in implied)

    lo, hi = 1.0, 1.0
    while total(hi) > 1.0:
        hi *= 2.0
        if hi > 1e9:
            raise ArithmeticError("odds-ratio devig failed to bracket")
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if total(mid) > 1.0:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    c = (lo + hi) / 2.0
    probs = [pi / (c + pi - c * pi) for pi in implied]
    total_p = sum(probs)
    return [p / total_p for p in probs]


DEVIG_METHODS = {
    "multiplicative": devig_multiplicative,
    "additive": devig_additive,
    "power": devig_power,
    "shin": devig_shin,
    "odds_ratio": devig_odds_ratio,
}


def devig(decimal_odds: Sequence[float], method: str = "power") -> list[float]:
    """Devig a market with a named method. See module docstring for guidance."""
    try:
        fn = DEVIG_METHODS[method]
    except KeyError:
        raise ValueError(
            f"unknown devig method {method!r}; choose from {sorted(DEVIG_METHODS)}"
        ) from None
    return fn(decimal_odds)


def devig_ensemble(
    decimal_odds: Sequence[float],
    methods: Sequence[str] = ("multiplicative", "power", "shin"),
) -> list[float]:
    """Average of several devig methods — a hedge against model error in the
    margin structure, per Buchdahl's observation that no method dominates in
    all markets."""
    results = [devig(decimal_odds, m) for m in methods]
    n = len(decimal_odds)
    avg = [sum(r[i] for r in results) / len(results) for i in range(n)]
    total = sum(avg)
    return [p / total for p in avg]


def _check_market(decimal_odds: Sequence[float]) -> None:
    if len(decimal_odds) < 2:
        raise ValueError("a market needs at least two outcomes")
    for o in decimal_odds:
        _check_decimal(o)
