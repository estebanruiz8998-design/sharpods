"""Fundamental (bottom-up) probability models.

These produce a model probability independent of the betting market. Per the
synthesis of the ten books, fundamental models are the *secondary* signal —
the market consensus (fairline.py) is primary — but they add value when
blended, and they are the only signal available in markets too small or too
new for sharp prices to exist.
"""

from sharpods.models.elo import EloModel
from sharpods.models.poisson import PoissonModel
from sharpods.models.pythagorean import pythagorean_expectation, pythagenpat_exponent
from sharpods.models.montecarlo import simulate_binary, simulate_poisson_match
from sharpods.models.wintotals import (
    poisson_binomial_pmf,
    spread_to_win_probability,
    win_total_ev,
    win_total_probabilities,
)

__all__ = [
    "EloModel",
    "PoissonModel",
    "pythagorean_expectation",
    "pythagenpat_exponent",
    "poisson_binomial_pmf",
    "simulate_binary",
    "simulate_poisson_match",
    "spread_to_win_probability",
    "win_total_ev",
    "win_total_probabilities",
]
