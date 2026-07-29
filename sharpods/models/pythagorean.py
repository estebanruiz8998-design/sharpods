"""Pythagorean expectation — true team strength from points scored/allowed.

Mathletics (Winston) and Trading Bases (Peta) both lean on Pythagorean win
percentage as a luck-stripped measure of team quality: teams whose actual
record beats their Pythagorean record have usually been lucky (in Peta's MLB
framing, "cluster luck") and should be expected to regress.
"""

from __future__ import annotations

# Sport-specific exponents established in the literature (Winston, ch. 1;
# subsequent public research for NBA/NHL/soccer).
SPORT_EXPONENTS = {
    "mlb": 1.83,
    "nfl": 2.37,
    "nba": 13.91,
    "nhl": 2.15,
    "soccer": 1.35,
}


def pythagorean_expectation(
    points_for: float, points_against: float, exponent: float = 2.0
) -> float:
    """Expected win fraction = PF^x / (PF^x + PA^x)."""
    if points_for < 0 or points_against < 0:
        raise ValueError("points must be non-negative")
    if points_for == 0 and points_against == 0:
        return 0.5
    if points_for == 0:
        return 0.0
    if points_against == 0:
        return 1.0
    pf = points_for**exponent
    pa = points_against**exponent
    return pf / (pf + pa)


def pythagenpat_exponent(
    points_for: float, points_against: float, games: float, slope: float = 0.287
) -> float:
    """Pythagenpat: exponent adapted to scoring environment,
    x = ((PF + PA) / G) ^ slope. Higher-scoring environments earn larger
    exponents; more accurate than a fixed exponent across eras and leagues."""
    if games <= 0:
        raise ValueError("games must be positive")
    rpg = (points_for + points_against) / games
    if rpg <= 0:
        raise ValueError("scoring rate must be positive")
    return rpg**slope


def luck_wins(
    actual_wins: float,
    points_for: float,
    points_against: float,
    games: float,
    exponent: float,
) -> float:
    """Actual wins minus Pythagorean-expected wins — Peta's regression flag.

    A strongly positive number marks a team the market may be overrating
    (record flatters the underlying performance); negative marks a potential
    undervalued team.
    """
    expected = pythagorean_expectation(points_for, points_against, exponent) * games
    return actual_wins - expected
