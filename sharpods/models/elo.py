"""Elo power ratings with margin-of-victory and home advantage.

Mathletics (Winston) covers rating systems extensively; the Elo variant here
follows the widely used FiveThirtyEight-style construction: logistic expected
score, K-factor updates, an additive home-advantage term expressed in rating
points, and a margin-of-victory multiplier that dampens autocorrelation
(blowout wins by big favourites should not over-inflate ratings).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field


@dataclass
class EloModel:
    k_factor: float = 20.0
    home_advantage: float = 65.0  # rating points; ~2.5 NFL points equivalent
    initial_rating: float = 1500.0
    scale: float = 400.0
    ratings: dict[str, float] = field(default_factory=dict)

    def rating(self, team: str) -> float:
        return self.ratings.get(team, self.initial_rating)

    def expected_score(self, team: str, opponent: str, is_home: bool = True) -> float:
        """P(team beats opponent) from the logistic Elo curve.

        E = 1 / (1 + 10^(-(R_team + HFA - R_opp) / 400))
        """
        diff = self.rating(team) - self.rating(opponent)
        if is_home:
            diff += self.home_advantage
        else:
            diff -= self.home_advantage
        return 1.0 / (1.0 + 10.0 ** (-diff / self.scale))

    def win_probability(self, home: str, away: str) -> float:
        """P(home wins) — convenience alias for two-way markets."""
        return self.expected_score(home, away, is_home=True)

    def mov_multiplier(self, margin: float, rating_diff_winner: float) -> float:
        """Margin-of-victory multiplier (FiveThirtyEight form):

        ln(|margin| + 1) * 2.2 / (0.001 * elo_diff_winner + 2.2)

        where elo_diff_winner is the winner's pregame rating edge (negative if
        the winner was the underdog). Shrinks credit for blowouts by teams
        that were already heavy favourites.
        """
        return math.log(abs(margin) + 1.0) * 2.2 / (0.001 * rating_diff_winner + 2.2)

    def update(
        self,
        home: str,
        away: str,
        home_score: float,
        away_score: float,
        use_mov: bool = True,
    ) -> tuple[float, float]:
        """Record a result; returns the (home, away) rating deltas applied."""
        expected_home = self.expected_score(home, away, is_home=True)
        if home_score > away_score:
            actual_home = 1.0
        elif home_score < away_score:
            actual_home = 0.0
        else:
            actual_home = 0.5

        multiplier = 1.0
        margin = home_score - away_score
        if use_mov and margin != 0:
            pregame_diff = self.rating(home) + self.home_advantage - self.rating(away)
            winner_diff = pregame_diff if margin > 0 else -pregame_diff
            multiplier = self.mov_multiplier(margin, winner_diff)

        delta = self.k_factor * multiplier * (actual_home - expected_home)
        self.ratings[home] = self.rating(home) + delta
        self.ratings[away] = self.rating(away) - delta
        return delta, -delta

    def spread_estimate(self, home: str, away: str, points_per_rating: float = 0.04) -> float:
        """Translate the rating gap into an expected home margin (a synthetic
        spread). ``points_per_rating`` = points of scoreboard margin per Elo
        point; ~25 Elo per point (0.04) is the standard NFL calibration."""
        diff = self.rating(home) + self.home_advantage - self.rating(away)
        return diff * points_per_rating

    def regress_to_mean(self, fraction: float = 1.0 / 3.0) -> None:
        """Off-season regression toward the mean (Squares & Sharps: skill
        persists but performance regresses; 1/3 toward 1500 is the customary
        between-season adjustment)."""
        for team in list(self.ratings):
            r = self.ratings[team]
            self.ratings[team] = r + (self.initial_rating - r) * fraction
