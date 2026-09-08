"""NFL scoring-margin model: spread <-> win probability, and spread pricing.

Why this module exists
----------------------
`edges.py` already carries the NFL key-number tables (`NFL_MARGIN_FREQ`),
half-point valuation, Wong teasers and middles — but every one of those
functions takes cover/push probabilities as *inputs*. Nothing in the repo
turned a point spread into probabilities, so NFL spreads were devigged by the
generic two-way machinery as though a push were impossible. On a 3-point line
that discards ~9.8% of the probability mass.

Two things live here:

1. **spread <-> moneyline.** In the NFL the spread is the primary market and
   moneylines are derived from it, often lazily at soft books. A fair
   moneyline computed from a *sharp* spread is therefore genuine information
   about a soft book's posted moneyline — a second market rather than a
   second book, but the same dispersion logic.

2. **cover / push / loss** for a spread bet given a true expected margin, so
   `edges.spread_ev` can finally be called with numbers that came from
   somewhere.

Calibration note (matters, and is not the textbook number)
----------------------------------------------------------
The empirical standard deviation of NFL game margins is about 13.5 points.
Using 13.5 here is WRONG for this purpose: it understates favourites by 2-3
points against the conversion books actually use. Least-squares fitting the
map against the standard devigged conversion table (-3 -> 59.6%, -7 -> 73.3%,
-10 -> 80.0%, -14 -> 87.2%) gives sigma = 11.8, which reproduces the whole
table inside ~1 point. The normal is a convenience, not a claim about the
shape of NFL margins — real margins clump on 3 and 7, which is exactly why
push mass below comes from the empirical table and not from the normal.

Sigma is a keyword everywhere so a future refit is a one-line change, and the
calibration table is pinned in tests/test_football.py.
"""

from __future__ import annotations

import math
from collections.abc import Mapping

from sharpods.edges import NFL_MARGIN_FREQ

__all__ = [
    "NFL_MARGIN_SIGMA",
    "win_probability_from_spread",
    "spread_from_win_probability",
    "fair_moneyline_from_spread",
    "cover_probabilities",
    "push_probability",
]

# Calibrated to the book spread->moneyline table, NOT the raw margin SD.
NFL_MARGIN_SIGMA = 11.8


def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _norm_ppf(p: float) -> float:
    """Inverse normal CDF (Acklam's rational approximation, |err| < 1.15e-9)."""
    if not 0.0 < p < 1.0:
        raise ValueError("p must lie strictly between 0 and 1")
    a = (-3.969683028665376e01, 2.209460984245205e02, -2.759285104469687e02,
         1.383577518672690e02, -3.066479806614716e01, 2.506628277459239e00)
    b = (-5.447609879822406e01, 1.615858368580409e02, -1.556989798598866e02,
         6.680131188771972e01, -1.328068155288572e01)
    c = (-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e00,
         -2.549732539343734e00, 4.374664141464968e00, 2.938163982698783e00)
    d = (7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e00,
         3.754408661907416e00)
    plow, phigh = 0.02425, 1 - 0.02425
    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
               ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if p > phigh:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
                ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    q = p - 0.5
    r = q * q
    return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / \
           (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)


def win_probability_from_spread(
    spread: float, sigma: float = NFL_MARGIN_SIGMA
) -> float:
    """Probability the team wins OUTRIGHT given its point spread.

    `spread` is signed from the team's perspective: -3.5 lays 3.5 points,
    +3.5 receives them. The market's expected margin for the team is
    therefore -spread.

    Ties are folded in at half weight, which is the convention for a
    moneyline that pushes on a tie; NFL ties run about 0.2% so the choice
    moves nothing material.
    """
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    mean = -spread
    p_win = 1.0 - _norm_cdf((0.5 - mean) / sigma)
    p_loss = _norm_cdf((-0.5 - mean) / sigma)
    p_tie = max(0.0, 1.0 - p_win - p_loss)
    return p_win + 0.5 * p_tie


def spread_from_win_probability(
    p_win: float, sigma: float = NFL_MARGIN_SIGMA
) -> float:
    """Inverse of `win_probability_from_spread`: the spread a given win
    probability implies. Useful for turning a model's win probability into a
    number comparable with a posted line."""
    if not 0.0 < p_win < 1.0:
        raise ValueError("p_win must lie strictly between 0 and 1")
    return -sigma * _norm_ppf(p_win)


def fair_moneyline_from_spread(
    spread: float, sigma: float = NFL_MARGIN_SIGMA
) -> float:
    """Fair DECIMAL moneyline implied by a point spread (no vig)."""
    p = win_probability_from_spread(spread, sigma=sigma)
    return 1.0 / p


def push_probability(
    line: float, margin_freqs: Mapping[int, float] = NFL_MARGIN_FREQ
) -> float:
    """Probability a spread bet pushes: the empirical landing frequency of
    that margin, or zero on a half point.

    The empirical table is used deliberately in place of the normal's local
    mass — NFL margins clump on 3 and 7 far harder than any bell curve, which
    is the whole reason Wong's push charts exist. It is a marginal prior, so
    it is most trustworthy where most NFL games live (|line| <= 14) and
    overstates the push at extreme lines.
    """
    if line != int(line):
        return 0.0
    return margin_freqs.get(int(abs(line)), 0.0)


def cover_probabilities(
    line: float,
    true_margin: float,
    sigma: float = NFL_MARGIN_SIGMA,
    margin_freqs: Mapping[int, float] = NFL_MARGIN_FREQ,
) -> tuple[float, float, float]:
    """(p_cover, p_push, p_loss) for a spread bet.

    `line` is the team's posted spread (-3.5 lays 3.5). `true_margin` is the
    margin you actually expect the team to win by — from a model, or from a
    sharper book's line. Feed the result straight into `edges.spread_ev`.

    Whole-number lines take their push mass from the empirical table; the
    surviving cover/loss mass is rescaled to fill what is left, so the three
    always sum to 1.
    """
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    threshold = -line  # team covers when margin > threshold
    p_push = push_probability(line, margin_freqs)

    if p_push == 0.0:
        p_cover = 1.0 - _norm_cdf((threshold - true_margin) / sigma)
        return p_cover, 0.0, 1.0 - p_cover

    # Whole number: split with a continuity correction, then substitute the
    # empirical push mass and rescale the rest proportionally.
    p_cover_raw = 1.0 - _norm_cdf((threshold + 0.5 - true_margin) / sigma)
    p_loss_raw = _norm_cdf((threshold - 0.5 - true_margin) / sigma)
    remaining = p_cover_raw + p_loss_raw
    if remaining <= 0:
        return 0.0, 1.0, 0.0
    scale = (1.0 - p_push) / remaining
    return p_cover_raw * scale, p_push, p_loss_raw * scale
