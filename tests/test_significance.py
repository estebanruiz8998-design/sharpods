"""Tests for the Kelly growth-theory additions and Buchdahl's
record-significance toolkit."""

import pytest

from sharpods import kelly
from sharpods.clv import (
    luck_p_value,
    min_sample_size,
    runs_test_z,
    yield_t_statistic,
)


class TestKellyGrowthTheory:
    def test_fractional_tradeoff_half_kelly(self):
        assert kelly.fractional_tradeoff(0.5) == pytest.approx(0.75)
        assert kelly.fractional_tradeoff(1.0) == pytest.approx(1.0)

    def test_max_growth_zero_without_edge(self):
        assert kelly.max_growth_rate(0.5) == pytest.approx(0.0, abs=1e-12)

    def test_max_growth_equals_growth_at_full_kelly(self):
        # The Kelly-Shannon identity: G_max = g(f*) for even-money bets.
        p = 0.55
        f_star = kelly.kelly_fraction(p, 2.0)
        assert kelly.max_growth_rate(p) == pytest.approx(
            kelly.expected_log_growth(p, 2.0, f_star), abs=1e-12
        )

    def test_doubling_time(self):
        g = kelly.expected_log_growth(0.55, 2.0, kelly.kelly_fraction(0.55, 2.0))
        n = kelly.doubling_time(g)
        assert n == pytest.approx(0.6931 / g, abs=0.01)
        assert 130 < n < 145  # ~138 bets at p=0.55 even money

    def test_fixed_stake_ruin(self):
        assert kelly.ruin_probability_fixed_stake(0.55, 10) == pytest.approx(
            (0.45 / 0.55) ** 10
        )
        # No edge: ruin certain.
        assert kelly.ruin_probability_fixed_stake(0.5, 100) == 1.0
        # Bigger bankroll, smaller ruin.
        assert kelly.ruin_probability_fixed_stake(
            0.55, 50
        ) < kelly.ruin_probability_fixed_stake(0.55, 10)


class TestRecordSignificance:
    def test_t_statistic_known_value(self):
        t = yield_t_statistic(0.05, 978, 1.909)
        assert t == pytest.approx(1.64, abs=0.01)

    def test_min_sample_size_matches_t(self):
        n = min_sample_size(0.05, 1.909, t_star=1.64)
        assert n == 978
        # And a smaller yield needs a much larger sample.
        assert min_sample_size(0.02, 1.909) > 6000

    def test_luck_p_value(self):
        # A significant record has a small luck probability.
        assert luck_p_value(0.05, 978, 1.909) == pytest.approx(0.0505, abs=0.002)
        # A tiny sample proves nothing.
        assert luck_p_value(0.05, 10, 1.909) > 0.4


class TestRunsTest:
    def test_alternating_sequence_flags(self):
        z = runs_test_z([1, 0] * 20)
        assert z > 2.0  # far too many runs to be independent

    def test_streaky_sequence_flags_negative(self):
        z = runs_test_z([1] * 20 + [0] * 20)
        assert z < -2.0  # far too few runs

    def test_degenerate_sequences(self):
        assert runs_test_z([1, 1, 1]) == 0.0
        assert runs_test_z([]) == 0.0
