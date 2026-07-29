"""Consensus fair-line construction — the heart of the top-down approach.

The synthesis of Sharper, The Logic of Sports Betting, and Squares & Sharps:
the single best estimate of an outcome's true probability is the devigged
price of the sharpest market, refined by (a) blending across sharp books
weighted by sharpness and (b) optionally blending in a fundamental model's
probability, precision-weighted, in log-odds space.

Blending happens in logit space because probabilities are bounded and edges
live in log-odds: averaging logits respects the geometry (a 50%→52% move and
a 95%→96% move are comparable logit shifts, not comparable probability
shifts).
"""

from __future__ import annotations

import math
from collections.abc import Sequence

from sharpods.books_registry import BooksRegistry, DEFAULT_REGISTRY
from sharpods.datatypes import FairLine, MarketSnapshot, Side
from sharpods.odds import devig


def _logit(p: float) -> float:
    return math.log(p / (1.0 - p))


def _inv_logit(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def market_fair_line(
    snapshot: MarketSnapshot,
    registry: BooksRegistry = DEFAULT_REGISTRY,
    devig_method: str = "power",
    min_sharpness: float = 0.5,
    line: float | None = None,
) -> FairLine | None:
    """Build the consensus no-vig probabilities for one market.

    Only books at or above ``min_sharpness`` contribute — retail prices are
    for betting into, not for learning from (Sharper). Each contributing book
    must quote *every* side of the market (devigging needs the full book).
    Books' devigged probabilities are combined side-by-side as a
    sharpness-weighted average in logit space, then renormalized.

    For spreads/totals pass ``line`` to pin all quotes to one number; mixing
    quotes at different numbers would blend different propositions.

    Returns None when no sufficiently sharp book quotes the full market.
    """
    sides = snapshot.sides()
    if len(sides) < 2:
        return None

    per_book: dict[str, list[float]] = {}
    weights: dict[str, float] = {}
    for book in snapshot.books():
        sharpness = registry.sharpness(book)
        if sharpness < min_sharpness:
            continue
        odds: list[float] = []
        complete = True
        for side in sides:
            quotes = snapshot.quotes_for(side, line)
            match = [q for q in quotes if q.book == book]
            if not match:
                complete = False
                break
            odds.append(match[0].decimal_odds)
        if not complete:
            continue
        per_book[book] = devig(odds, devig_method)
        weights[book] = sharpness

    if not per_book:
        return None

    total_weight = sum(weights.values())
    consensus: dict[Side, float] = {}
    for i, side in enumerate(sides):
        logit_sum = sum(
            weights[book] * _logit(per_book[book][i]) for book in per_book
        )
        consensus[side] = _inv_logit(logit_sum / total_weight)

    norm = sum(consensus.values())
    for side in consensus:
        consensus[side] /= norm

    return FairLine(
        probabilities=consensus,
        sources={book: weights[book] / total_weight for book in per_book},
        method=f"weighted-logit/{devig_method}",
        anchor_sharpness=max(weights.values()),
    )


def blend_market_and_model(
    market_probability: float,
    model_probability: float,
    market_weight: float = 0.75,
) -> float:
    """Precision-weighted blend of market and fundamental-model probabilities
    in logit space.

    Default 75/25 toward the market: Squares & Sharps shows sharp closing
    prices are extraordinarily well calibrated, so a solo fundamental model
    earns a minority voice. Raise the model's share only with demonstrated
    CLV (clv.py provides the evidence loop).
    """
    if not 0.0 < market_weight <= 1.0:
        raise ValueError("market_weight must be in (0, 1]")
    for p in (market_probability, model_probability):
        if not 0.0 < p < 1.0:
            raise ValueError(f"probability out of range: {p}")
    blended_logit = market_weight * _logit(market_probability) + (
        1.0 - market_weight
    ) * _logit(model_probability)
    return _inv_logit(blended_logit)


def ensemble_probabilities(
    probabilities: Sequence[float], weights: Sequence[float] | None = None
) -> float:
    """Weighted logit-space ensemble of any number of probability estimates
    for the same outcome (e.g. Elo + Poisson + market)."""
    if not probabilities:
        raise ValueError("need at least one probability")
    if weights is None:
        weights = [1.0] * len(probabilities)
    if len(weights) != len(probabilities):
        raise ValueError("weights must align with probabilities")
    total = sum(weights)
    if total <= 0:
        raise ValueError("weights must sum positive")
    blended = sum(w * _logit(p) for p, w in zip(probabilities, weights)) / total
    return _inv_logit(blended)
