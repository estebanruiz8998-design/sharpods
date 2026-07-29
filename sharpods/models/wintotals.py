"""Season win totals and spread <-> win-probability conversion.

Sharp Sports Betting (Wong) prices season win totals as the distribution of a
sum of independent per-game win probabilities — a Poisson-binomial — with the
per-game probabilities derived from projected spreads. Mathletics (Winston)
supplies the spread-to-probability map: game margin ~ Normal(spread, sigma),
with sigma ~ 13.5-14 for the NFL.
"""

from __future__ import annotations

import math
from collections.abc import Sequence

# Historical standard deviations of the final margin around the spread.
MARGIN_SIGMA = {
    "nfl": 13.5,
    "nba": 11.5,
    "ncaaf": 16.0,
    "ncaab": 10.5,
}


def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def spread_to_win_probability(spread: float, sigma: float = 13.5) -> float:
    """P(team wins) from its point spread (negative = favourite).

    Margin ~ Normal(-spread, sigma) for the team laying `spread` points, so
    P(win) = Phi(-spread / sigma). Winston's caveat applies: near key numbers
    an empirical margin distribution beats the normal; use this for win
    totals and moneyline sanity checks, not half-point pricing.
    """
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    return _norm_cdf(-spread / sigma)


def poisson_binomial_pmf(win_probabilities: Sequence[float]) -> list[float]:
    """Exact distribution of total wins across independent games.

    Dynamic program (Wong's season-total construction):
    f_0 = [1]; f_i(k) = f_{i-1}(k-1) * p_i + f_{i-1}(k) * (1 - p_i).
    Returns pmf[k] = P(exactly k wins) for k in [0, n].
    """
    pmf = [1.0]
    for p in win_probabilities:
        if not 0.0 <= p <= 1.0:
            raise ValueError(f"win probability out of range: {p}")
        nxt = [0.0] * (len(pmf) + 1)
        for k, mass in enumerate(pmf):
            nxt[k] += mass * (1.0 - p)
            nxt[k + 1] += mass * p
        pmf = nxt
    return pmf


def win_total_probabilities(
    win_probabilities: Sequence[float], line: float
) -> tuple[float, float, float]:
    """(P(over), P(push), P(under)) for a season win-total line.

    Half-point lines cannot push; integer lines push on exactly `line` wins.
    """
    if not win_probabilities:
        raise ValueError("need at least one game")
    pmf = poisson_binomial_pmf(win_probabilities)
    over = sum(mass for k, mass in enumerate(pmf) if k > line)
    push = sum(mass for k, mass in enumerate(pmf) if k == line)
    under = 1.0 - over - push
    return over, push, under


def expected_wins(win_probabilities: Sequence[float]) -> float:
    """mu = sum(p_i); with variance sum(p_i * (1 - p_i)) under independence."""
    return sum(win_probabilities)


def win_total_ev(
    win_probabilities: Sequence[float],
    line: float,
    over_decimal_odds: float,
    under_decimal_odds: float,
) -> tuple[float, float]:
    """(EV of over, EV of under) at the quoted prices; pushes refund."""
    if over_decimal_odds <= 1.0 or under_decimal_odds <= 1.0:
        raise ValueError("decimal odds must exceed 1.0")
    over, push, under = win_total_probabilities(win_probabilities, line)
    ev_over = over * (over_decimal_odds - 1.0) - under
    ev_under = under * (under_decimal_odds - 1.0) - over
    return ev_over, ev_under
