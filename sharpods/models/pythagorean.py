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


def log5(p_a: float, p_b: float) -> float:
    """Bill James' log5 (Mathletics): P(A beats B) from the teams' true win
    fractions. p = pA(1-pB) / (pA(1-pB) + (1-pA)pB). Symmetric, calibrated,
    and exact for Bradley-Terry-style strengths."""
    for p in (p_a, p_b):
        if not 0.0 < p < 1.0:
            raise ValueError(f"win fraction out of range: {p}")
    num = p_a * (1.0 - p_b)
    return num / (num + (1.0 - p_a) * p_b)


def home_log5(p_home: float, p_away: float, home_edge: float = 0.54) -> float:
    """log5 with a home-field adjustment: shift the neutral-site probability
    by the league home-win baseline (MLB ~0.54) in odds space.

    p' = p*h / (p*h + (1-p)(1-h)), h = home_edge. At p = 0.5 this returns
    exactly ``home_edge``.
    """
    if not 0.0 < home_edge < 1.0:
        raise ValueError("home_edge must be in (0, 1)")
    p = log5(p_home, p_away)
    num = p * home_edge
    return num / (num + (1.0 - p) * (1.0 - home_edge))


def pythagorean_matchup(
    home_pf: float, home_pa: float, away_pf: float, away_pa: float,
    home_games: float, away_games: float,
    slope: float = 0.287, home_edge: float = 0.54,
) -> float:
    """The in-house bottom-up pipeline in one call (Mathletics + Trading
    Bases): Pythagenpat expectation per team from points for/against, then
    home-adjusted log5. Returns P(home wins)."""
    hx = pythagenpat_exponent(home_pf, home_pa, home_games, slope)
    ax = pythagenpat_exponent(away_pf, away_pa, away_games, slope)
    p_home = pythagorean_expectation(home_pf, home_pa, hx)
    p_away = pythagorean_expectation(away_pf, away_pa, ax)
    return home_log5(p_home, p_away, home_edge)


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
