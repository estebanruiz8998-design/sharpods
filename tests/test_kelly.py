import pytest

from sharpods import kelly


class TestKellyFraction:
    def test_textbook_case(self):
        # p=0.55 at evens: f* = (1*0.55 - 0.45)/1 = 0.10
        assert kelly.kelly_fraction(0.55, 2.0) == pytest.approx(0.10)

    def test_no_edge_returns_zero(self):
        assert kelly.kelly_fraction(0.50, 2.0) == 0.0
        assert kelly.kelly_fraction(0.40, 2.0) == 0.0

    def test_underdog_odds(self):
        # p=0.30 at 4.0: b=3, f* = (3*0.3 - 0.7)/3 = 0.0667
        assert kelly.kelly_fraction(0.30, 4.0) == pytest.approx(0.2 / 3.0)

    def test_fractional_kelly(self):
        full = kelly.kelly_fraction(0.55, 2.0)
        assert kelly.fractional_kelly(0.55, 2.0, 0.25) == pytest.approx(full * 0.25)

    def test_invalid_multiplier(self):
        with pytest.raises(ValueError):
            kelly.fractional_kelly(0.55, 2.0, 0.0)
        with pytest.raises(ValueError):
            kelly.fractional_kelly(0.55, 2.0, 1.5)


class TestGrowth:
    def test_growth_positive_at_kelly(self):
        f = kelly.kelly_fraction(0.55, 2.0)
        assert kelly.expected_log_growth(0.55, 2.0, f) > 0

    def test_full_kelly_beats_other_fractions(self):
        f_star = kelly.kelly_fraction(0.55, 2.0)
        g_star = kelly.expected_log_growth(0.55, 2.0, f_star)
        for f in (f_star / 2, f_star * 1.5):
            assert g_star > kelly.expected_log_growth(0.55, 2.0, f)

    def test_double_kelly_growth_near_zero(self):
        f_star = kelly.kelly_fraction(0.55, 2.0)
        g = kelly.expected_log_growth(0.55, 2.0, 2 * f_star)
        assert abs(g) < 1e-3

    def test_zero_fraction_zero_growth(self):
        assert kelly.expected_log_growth(0.55, 2.0, 0.0) == 0.0


class TestRisk:
    def test_halving_probability_full_kelly(self):
        assert kelly.probability_of_halving(1.0) == pytest.approx(0.5)

    def test_halving_probability_half_kelly(self):
        assert kelly.probability_of_halving(0.5) == pytest.approx(0.125)

    def test_halving_decreases_with_multiplier(self):
        assert kelly.probability_of_halving(0.25) < kelly.probability_of_halving(0.5)


class TestSimultaneous:
    def test_no_scaling_when_under_cap(self):
        fractions = kelly.simultaneous_kelly([0.55, 0.55], [2.0, 2.0], 0.25, 0.25)
        assert fractions == pytest.approx([0.025, 0.025])

    def test_scaling_when_over_cap(self):
        # 10 strong edges at quarter Kelly would want 0.25 total; cap at 0.10.
        probs = [0.60] * 10
        odds_ = [2.0] * 10
        fractions = kelly.simultaneous_kelly(probs, odds_, 0.25, cap_total=0.10)
        assert sum(fractions) == pytest.approx(0.10)
        # Relative sizing preserved (all equal here).
        assert len(set(round(f, 12) for f in fractions)) == 1

    def test_mismatched_inputs(self):
        with pytest.raises(ValueError):
            kelly.simultaneous_kelly([0.5], [2.0, 2.0])


class TestAdvise:
    def test_cap_binds(self):
        advice = kelly.advise_stake(0.70, 2.0, 10_000, multiplier=1.0, max_fraction=0.02)
        assert advice.fraction == pytest.approx(0.02)
        assert advice.amount == pytest.approx(200.0)
        assert advice.full_kelly_fraction == pytest.approx(0.40)

    def test_quarter_kelly_under_cap(self):
        advice = kelly.advise_stake(0.55, 2.0, 10_000, multiplier=0.25, max_fraction=0.05)
        assert advice.fraction == pytest.approx(0.025)
        assert advice.expected_growth > 0

    def test_invalid_bankroll(self):
        with pytest.raises(ValueError):
            kelly.advise_stake(0.55, 2.0, 0)
