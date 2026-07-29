import math

import pytest

from sharpods import odds


class TestConversions:
    def test_american_to_decimal_favourite(self):
        assert odds.american_to_decimal(-110) == pytest.approx(1.9091, abs=1e-4)

    def test_american_to_decimal_underdog(self):
        assert odds.american_to_decimal(+150) == pytest.approx(2.50)

    def test_decimal_to_american_round_trip(self):
        for a in (-110, -200, +105, +250, -105):
            d = odds.american_to_decimal(a)
            assert odds.decimal_to_american(d) == pytest.approx(a)

    def test_invalid_american(self):
        with pytest.raises(ValueError):
            odds.american_to_decimal(50)

    def test_implied_round_trip(self):
        p = odds.decimal_to_implied(2.5)
        assert p == pytest.approx(0.4)
        assert odds.implied_to_decimal(p) == pytest.approx(2.5)

    def test_fractional(self):
        assert odds.fractional_to_decimal(5, 1) == pytest.approx(6.0)
        assert odds.fractional_to_decimal(1, 2) == pytest.approx(1.5)


class TestMargins:
    def test_overround_standard_spread(self):
        d = odds.american_to_decimal(-110)
        assert odds.overround([d, d]) == pytest.approx(1.0476, abs=1e-4)

    def test_hold_standard_spread(self):
        d = odds.american_to_decimal(-110)
        assert odds.hold_pct([d, d]) == pytest.approx(0.04545, abs=1e-4)

    def test_synthetic_hold_negative_is_arb(self):
        assert odds.synthetic_hold([2.02, 2.02]) < 0


DEVIG_CASES = [
    [1.909, 1.909],
    [1.87, 2.05],
    [1.30, 4.50, 9.00],  # heavy favourite three-way
    [2.30, 3.45, 3.30],
]


class TestDevig:
    @pytest.mark.parametrize("market", DEVIG_CASES)
    @pytest.mark.parametrize("method", sorted(odds.DEVIG_METHODS))
    def test_probabilities_sum_to_one(self, market, method):
        probs = odds.devig(market, method)
        assert sum(probs) == pytest.approx(1.0, abs=1e-9)
        assert all(0.0 < p < 1.0 for p in probs)

    def test_symmetric_market_gives_half(self):
        for method in odds.DEVIG_METHODS:
            probs = odds.devig([1.909, 1.909], method)
            assert probs[0] == pytest.approx(0.5, abs=1e-9)

    def test_multiplicative_known_value(self):
        probs = odds.devig_multiplicative([1.87, 2.05])
        assert probs[0] == pytest.approx(0.52296, abs=1e-4)

    def test_power_shifts_margin_to_longshots(self):
        # Power devig should assign the favourite a higher probability than
        # multiplicative (margin borne more by the longshot).
        market = [1.30, 4.50, 9.00]
        mult = odds.devig_multiplicative(market)
        power = odds.devig_power(market)
        assert power[0] > mult[0]
        assert power[2] < mult[2]

    def test_shin_shifts_margin_to_longshots(self):
        market = [1.30, 4.50, 9.00]
        mult = odds.devig_multiplicative(market)
        shin = odds.devig_shin(market)
        assert shin[0] > mult[0]
        assert shin[2] < mult[2]

    def test_shin_fair_market_falls_back(self):
        probs = odds.devig_shin([2.0, 2.0])
        assert probs == pytest.approx([0.5, 0.5])

    def test_additive_guard_falls_back_on_longshots(self):
        # Extreme longshot whose implied probability is below the margin share.
        market = [1.01, 101.0, 101.0]
        probs = odds.devig_additive(market)
        assert sum(probs) == pytest.approx(1.0)
        assert all(p > 0 for p in probs)

    def test_ensemble_sums_to_one(self):
        probs = odds.devig_ensemble([1.87, 2.05])
        assert sum(probs) == pytest.approx(1.0, abs=1e-9)

    def test_unknown_method(self):
        with pytest.raises(ValueError):
            odds.devig([1.9, 1.9], "voodoo")

    def test_single_outcome_rejected(self):
        with pytest.raises(ValueError):
            odds.devig([1.9])


class TestDevigOrdering:
    def test_devigged_probability_exceeds_no_margin_case(self):
        """Every method must strip margin: devigged probs are below raw
        implied probs when overround is positive."""
        market = [1.87, 2.05]
        implied = [1 / o for o in market]
        for method in odds.DEVIG_METHODS:
            probs = odds.devig(market, method)
            assert probs[0] < implied[0]
            assert probs[1] < implied[1]
            assert not math.isnan(probs[0])
