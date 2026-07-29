"""Monte Carlo simulation utilities (Statistical Sports Models in Excel;
Trading Bases both simulate seasons/matches to turn ratings into
probabilities with uncertainty attached).

Deterministic seeding is mandatory: reproducibility is a modeling discipline
(you cannot debug or backtest a model whose outputs change run to run).
"""

from __future__ import annotations

import random
from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class SimResult:
    probability: float
    n_trials: int
    standard_error: float

    def confidence_interval(self, z: float = 1.96) -> tuple[float, float]:
        lo = max(0.0, self.probability - z * self.standard_error)
        hi = min(1.0, self.probability + z * self.standard_error)
        return lo, hi


def simulate_binary(
    trial: Callable[[random.Random], bool],
    n_trials: int = 10_000,
    seed: int = 7,
) -> SimResult:
    """Estimate P(event) by running ``trial`` n times.

    ``trial`` receives the RNG and returns True when the event occurs.
    Standard error = sqrt(p(1-p)/n) — report it, per Mack's warning that a
    simulated probability without an error bar invites overconfidence.
    """
    if n_trials <= 0:
        raise ValueError("n_trials must be positive")
    rng = random.Random(seed)
    hits = sum(1 for _ in range(n_trials) if trial(rng))
    p = hits / n_trials
    se = (p * (1.0 - p) / n_trials) ** 0.5
    return SimResult(probability=p, n_trials=n_trials, standard_error=se)


def _poisson_draw(rng: random.Random, lam: float) -> int:
    """Knuth's algorithm — fine for sports-sized lambdas."""
    import math

    threshold = math.exp(-lam)
    k, product = 0, rng.random()
    while product > threshold:
        k += 1
        product *= rng.random()
    return k


def simulate_poisson_match(
    home_lambda: float,
    away_lambda: float,
    n_trials: int = 10_000,
    seed: int = 7,
) -> dict[str, SimResult]:
    """Simulate a match under independent Poisson scoring; returns
    probabilities for home/draw/away as SimResults with error bars."""
    if home_lambda <= 0 or away_lambda <= 0:
        raise ValueError("lambdas must be positive")
    rng = random.Random(seed)
    home_wins = draws = away_wins = 0
    for _ in range(n_trials):
        h = _poisson_draw(rng, home_lambda)
        a = _poisson_draw(rng, away_lambda)
        if h > a:
            home_wins += 1
        elif h == a:
            draws += 1
        else:
            away_wins += 1

    def result(count: int) -> SimResult:
        p = count / n_trials
        se = (p * (1.0 - p) / n_trials) ** 0.5
        return SimResult(probability=p, n_trials=n_trials, standard_error=se)

    return {
        "home": result(home_wins),
        "draw": result(draws),
        "away": result(away_wins),
    }
