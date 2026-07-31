import pytest

from sharpods.models import (
    EloModel,
    PoissonModel,
    pythagenpat_exponent,
    pythagorean_expectation,
    simulate_binary,
    simulate_poisson_match,
)
from sharpods.models.poisson import expected_goals, poisson_pmf


class TestElo:
    def test_equal_ratings_home_edge(self):
        elo = EloModel()
        p = elo.win_probability("A", "B")
        assert p > 0.5  # home advantage
        assert p == pytest.approx(1 / (1 + 10 ** (-65 / 400)))

    def test_symmetry_without_home_edge(self):
        elo = EloModel(home_advantage=0.0)
        assert elo.win_probability("A", "B") == pytest.approx(0.5)

    def test_update_moves_ratings_toward_winner(self):
        elo = EloModel()
        elo.update("A", "B", 27, 17)
        assert elo.rating("A") > 1500
        assert elo.rating("B") < 1500

    def test_update_zero_sum(self):
        elo = EloModel()
        elo.update("A", "B", 27, 17)
        assert elo.rating("A") + elo.rating("B") == pytest.approx(3000)

    def test_upset_moves_more_than_expected_win(self):
        elo = EloModel(home_advantage=0.0, ratings={"A": 1700, "B": 1300})
        favourite_win = EloModel(home_advantage=0.0, ratings={"A": 1700, "B": 1300})
        favourite_win.update("A", "B", 21, 20, use_mov=False)
        upset = EloModel(home_advantage=0.0, ratings={"A": 1700, "B": 1300})
        upset.update("B", "A", 21, 20, use_mov=False)
        gain_favourite = favourite_win.rating("A") - 1700
        gain_underdog = upset.rating("B") - 1300
        assert gain_underdog > gain_favourite

    def test_spread_estimate_sign(self):
        elo = EloModel(ratings={"A": 1600, "B": 1500})
        assert elo.spread_estimate("A", "B") > 0

    def test_regression_to_mean(self):
        elo = EloModel(ratings={"A": 1650.0})
        elo.regress_to_mean(1 / 3)
        assert elo.rating("A") == pytest.approx(1600.0)


class TestPoisson:
    def test_pmf_sums_to_one(self):
        total = sum(poisson_pmf(k, 2.5) for k in range(60))
        assert total == pytest.approx(1.0, abs=1e-9)

    def test_outcomes_sum_to_one(self):
        model = PoissonModel(home_lambda=1.6, away_lambda=1.2)
        h, d, a = model.outcome_probabilities()
        assert h + d + a == pytest.approx(1.0, abs=1e-9)
        assert h > a  # stronger attack should win more often

    def test_dixon_coles_raises_draw_probability(self):
        independent = PoissonModel(1.3, 1.1, rho=0.0)
        corrected = PoissonModel(1.3, 1.1, rho=-0.10)
        assert corrected.outcome_probabilities()[1] > independent.outcome_probabilities()[1]

    def test_totals_probabilities(self):
        model = PoissonModel(1.6, 1.2, rho=0.0)
        over, under = model.total_goals_probabilities(2.5)
        assert over + under == pytest.approx(1.0, abs=1e-9)
        # E[goals]=2.8 > 2.5, so over should be favoured
        assert over > 0.5

    def test_integer_total_rejected(self):
        model = PoissonModel(1.6, 1.2)
        with pytest.raises(ValueError):
            model.total_goals_probabilities(3.0)

    def test_btts(self):
        model = PoissonModel(1.6, 1.2, rho=0.0)
        p = model.both_teams_score()
        expected = (1 - poisson_pmf(0, 1.6)) * (1 - poisson_pmf(0, 1.2))
        assert p == pytest.approx(expected, abs=0.01)

    def test_expected_goals_construction(self):
        lam = expected_goals(1.35, attack_strength=1.2, opponent_defence_strength=0.9, home_boost=1.1)
        assert lam == pytest.approx(1.35 * 1.2 * 0.9 * 1.1)


class TestPythagorean:
    def test_even_team(self):
        assert pythagorean_expectation(700, 700, 1.83) == pytest.approx(0.5)

    def test_known_mlb_case(self):
        # 800 scored / 700 allowed at x=1.83 -> about .561
        expected = 800**1.83 / (800**1.83 + 700**1.83)
        assert pythagorean_expectation(800, 700, 1.83) == pytest.approx(expected)
        assert 0.55 < expected < 0.58

    def test_degenerate_cases(self):
        assert pythagorean_expectation(0, 0) == 0.5
        assert pythagorean_expectation(0, 10) == 0.0
        assert pythagorean_expectation(10, 0) == 1.0

    def test_pythagenpat_scales_with_scoring(self):
        low = pythagenpat_exponent(300, 300, 162)
        high = pythagenpat_exponent(900, 900, 162)
        assert high > low


class TestMonteCarlo:
    def test_deterministic_with_seed(self):
        r1 = simulate_binary(lambda rng: rng.random() < 0.6, 5000, seed=42)
        r2 = simulate_binary(lambda rng: rng.random() < 0.6, 5000, seed=42)
        assert r1.probability == r2.probability

    def test_converges_to_truth(self):
        r = simulate_binary(lambda rng: rng.random() < 0.6, 20_000, seed=7)
        assert r.probability == pytest.approx(0.6, abs=0.02)
        lo, hi = r.confidence_interval()
        assert lo < 0.6 < hi

    def test_poisson_match_agrees_with_analytic(self):
        sim = simulate_poisson_match(1.6, 1.2, n_trials=30_000, seed=3)
        analytic = PoissonModel(1.6, 1.2, rho=0.0).outcome_probabilities()
        assert sim["home"].probability == pytest.approx(analytic[0], abs=0.02)
        assert sim["draw"].probability == pytest.approx(analytic[1], abs=0.02)
        total = sum(r.probability for r in sim.values())
        assert total == pytest.approx(1.0)


class TestLog5:
    def test_symmetric_even(self):
        from sharpods.models.pythagorean import log5

        assert log5(0.5, 0.5) == pytest.approx(0.5)
        assert log5(0.6, 0.6) == pytest.approx(0.5)

    def test_known_value(self):
        from sharpods.models.pythagorean import log5

        # .600 team vs .400 team: p = .6*.6/(.6*.6+.4*.4) = .36/.52
        assert log5(0.6, 0.4) == pytest.approx(0.36 / 0.52)

    def test_complement(self):
        from sharpods.models.pythagorean import log5

        assert log5(0.55, 0.48) + log5(0.48, 0.55) == pytest.approx(1.0)

    def test_home_edge_at_even(self):
        from sharpods.models.pythagorean import home_log5

        assert home_log5(0.5, 0.5) == pytest.approx(0.54)
        assert home_log5(0.5, 0.5, home_edge=0.5) == pytest.approx(0.5)

    def test_matchup_pipeline(self):
        from sharpods.models.pythagorean import pythagorean_matchup

        # Stronger home team by run differential must exceed the bare
        # home edge; a mirror matchup must be its complement-ish.
        p = pythagorean_matchup(560, 480, 480, 560, 108, 108)
        assert p > 0.54
        q = pythagorean_matchup(480, 560, 560, 480, 108, 108)
        assert q < 0.54

    def test_bounds(self):
        from sharpods.models.pythagorean import log5

        with pytest.raises(ValueError):
            log5(0.0, 0.5)
