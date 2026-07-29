"""Poisson goal model with Dixon-Coles adjustment — the workhorse for soccer
match and totals markets (Statistical Sports Models in Excel, ch. on Poisson;
Fixed Odds Sports Betting).

Team attack/defence strengths multiply into expected goals; independent
Poissons give the score matrix; the Dixon-Coles tau term corrects the known
misfit at low scorelines (0-0, 1-0, 0-1, 1-1) caused by score-state dynamics.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


def poisson_pmf(k: int, lam: float) -> float:
    if lam <= 0:
        raise ValueError("lambda must be positive")
    if k < 0:
        return 0.0
    return math.exp(-lam) * lam**k / math.factorial(k)


def dixon_coles_tau(x: int, y: int, lam: float, mu: float, rho: float) -> float:
    """Low-score dependence correction. rho is typically small and negative
    (about -0.1); rho = 0 recovers independence."""
    if x == 0 and y == 0:
        return 1.0 - lam * mu * rho
    if x == 0 and y == 1:
        return 1.0 + lam * rho
    if x == 1 and y == 0:
        return 1.0 + mu * rho
    if x == 1 and y == 1:
        return 1.0 - rho
    return 1.0


@dataclass
class PoissonModel:
    """Score-matrix model for one match.

    home_goals_lambda / away_goals_lambda are expected goals, typically built
    as: league_avg * home_attack * away_defence * home_field_boost.
    """

    home_lambda: float
    away_lambda: float
    rho: float = -0.05  # Dixon-Coles correction; 0 disables
    max_goals: int = 12

    def score_matrix(self) -> list[list[float]]:
        """P(home=i, away=j) for i, j in [0, max_goals], renormalized."""
        matrix = [
            [
                poisson_pmf(i, self.home_lambda)
                * poisson_pmf(j, self.away_lambda)
                * dixon_coles_tau(i, j, self.home_lambda, self.away_lambda, self.rho)
                for j in range(self.max_goals + 1)
            ]
            for i in range(self.max_goals + 1)
        ]
        total = sum(sum(row) for row in matrix)
        return [[p / total for p in row] for row in matrix]

    def outcome_probabilities(self) -> tuple[float, float, float]:
        """(home win, draw, away win)."""
        m = self.score_matrix()
        home = sum(m[i][j] for i in range(len(m)) for j in range(len(m)) if i > j)
        draw = sum(m[i][i] for i in range(len(m)))
        away = 1.0 - home - draw
        return home, draw, away

    def total_goals_probabilities(self, line: float) -> tuple[float, float]:
        """(P(over line), P(under line)). Half-point lines only — integer
        lines push and should be priced as the conditional given no push."""
        if line == int(line):
            raise ValueError("use a half-point line; integer totals can push")
        m = self.score_matrix()
        over = sum(
            m[i][j]
            for i in range(len(m))
            for j in range(len(m))
            if i + j > line
        )
        return over, 1.0 - over

    def both_teams_score(self) -> float:
        m = self.score_matrix()
        return sum(
            m[i][j] for i in range(1, len(m)) for j in range(1, len(m))
        )


def expected_goals(
    league_avg_goals: float,
    attack_strength: float,
    opponent_defence_strength: float,
    home_boost: float = 1.0,
) -> float:
    """Multiplicative expected-goals construction (Mack's Excel formulation):
    lambda = league_avg * attack * opp_defence * home_boost, where strengths
    are ratios of team scoring rates to the league average."""
    lam = league_avg_goals * attack_strength * opponent_defence_strength * home_boost
    if lam <= 0:
        raise ValueError("expected goals must be positive")
    return lam
