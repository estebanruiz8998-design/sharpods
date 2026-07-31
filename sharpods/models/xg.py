"""Expected goals (xG): the stable scoring signal for soccer lambdas.

Soccermatics (Sumpter) supplies the machinery: goals are Poisson, shots can
be valued with a simple logistic model of distance and angle, and a team's
xG rate is a better predictor of its future scoring than its goal rate.
Net Gains (O'Hanlon) supplies the correction: at team level, finishing —
goals minus xG — is mostly NOT a persistent skill, so scoring-rate
estimates should shrink toward xG, and heavy over/under-performers are
regression (and market-mispricing) candidates. This is Peta's cluster-luck
argument (Trading Bases) rebuilt for soccer.

Pipeline: shot data -> xg_from_shots -> team xG rates -> blend_goals_xg ->
lambda for models.poisson.PoissonModel.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class Shot:
    """One shot: distance from goal centre (metres) and the angle (radians)
    subtended by the goal mouth at the shot location."""

    distance_m: float
    angle_rad: float


# Default logistic coefficients for a Sumpter-style two-feature xG model.
# These approximate published simple fits (intercept, per-metre distance
# penalty, per-radian angle bonus); they are CALIBRATION PARAMETERS to be
# refit on real shot data, not constants of nature.
XG_INTERCEPT = -0.90
XG_DISTANCE_COEF = -0.145
XG_ANGLE_COEF = 1.35


def shot_xg(
    shot: Shot,
    intercept: float = XG_INTERCEPT,
    distance_coef: float = XG_DISTANCE_COEF,
    angle_coef: float = XG_ANGLE_COEF,
) -> float:
    """P(goal | shot) from the logistic model:

    xG = 1 / (1 + exp(-(b0 + b1*distance + b2*angle)))

    Sumpter's insight is not the exact coefficients but the shape: scoring
    probability decays with distance and rises with the visible goal angle.
    """
    if shot.distance_m < 0 or not 0.0 <= shot.angle_rad <= math.pi:
        raise ValueError("invalid shot geometry")
    z = intercept + distance_coef * shot.distance_m + angle_coef * shot.angle_rad
    return 1.0 / (1.0 + math.exp(-z))


def goal_angle(distance_m: float, lateral_offset_m: float, goal_width_m: float = 7.32) -> float:
    """Angle subtended by the goal mouth at a shot location ``distance_m``
    out from the goal line and ``lateral_offset_m`` from the centre of the
    goal (Sumpter's geometry)."""
    if distance_m <= 0:
        raise ValueError("distance must be positive")
    half = goal_width_m / 2.0
    left = math.atan2(lateral_offset_m + half, distance_m)
    right = math.atan2(lateral_offset_m - half, distance_m)
    return abs(left - right)


def xg_from_shots(shots: Iterable[Shot], **coefs: float) -> float:
    """Total expected goals for a collection of shots."""
    return sum(shot_xg(s, **coefs) for s in shots)


def blend_goals_xg(
    goals_rate: float, xg_rate: float, xg_weight: float = 0.7
) -> float:
    """Scoring-rate estimate shrunk toward xG.

    lambda = w * xG_rate + (1 - w) * goals_rate, with w defaulting to 0.7:
    both books put xG's predictive weight well above raw goals at team
    level (finishing over/under-performance regresses). Feed the result to
    models.poisson.expected_goals / PoissonModel.
    """
    if goals_rate < 0 or xg_rate < 0:
        raise ValueError("rates must be non-negative")
    if not 0.0 <= xg_weight <= 1.0:
        raise ValueError("xg_weight must be in [0, 1]")
    return xg_weight * xg_rate + (1.0 - xg_weight) * goals_rate


def finishing_luck(goals: float, xg: float) -> float:
    """Goals scored minus expected goals — O'Hanlon's regression flag.

    Strongly positive: the team's goal record flatters its chance creation
    and the market may be overrating it (soccer's cluster luck). Strongly
    negative: undervalued chance creation. Use per equal exposure (e.g. a
    season); the sign, not the third decimal, is the signal.
    """
    if xg < 0 or goals < 0:
        raise ValueError("inputs must be non-negative")
    return goals - xg


def overperformance_ratio(goals: float, xg: float) -> float:
    """goals / xG — the scale-free version of finishing_luck; ~1.0 is
    sustainable, far above 1 regresses down, far below regresses up."""
    if xg <= 0:
        raise ValueError("xG must be positive")
    if goals < 0:
        raise ValueError("goals must be non-negative")
    return goals / xg


def team_lambdas_from_xg(
    home_xg_rate: float,
    home_goals_rate: float,
    away_xg_rate: float,
    away_goals_rate: float,
    xg_weight: float = 0.7,
    home_boost: float = 1.1,
) -> tuple[float, float]:
    """Convenience: xG-shrunk expected-goals pair for a match, ready for
    PoissonModel(home_lambda, away_lambda). ``home_boost`` is the standard
    multiplicative home-field scoring bump."""
    home = blend_goals_xg(home_goals_rate, home_xg_rate, xg_weight) * home_boost
    away = blend_goals_xg(away_goals_rate, away_xg_rate, xg_weight)
    if home <= 0 or away <= 0:
        raise ValueError("lambdas must be positive; check the input rates")
    return home, away


__all__ = [
    "Shot",
    "shot_xg",
    "goal_angle",
    "xg_from_shots",
    "blend_goals_xg",
    "finishing_luck",
    "overperformance_ratio",
    "team_lambdas_from_xg",
]
