import pytest

from sharpods.datatypes import Event, MarketKind, MarketSnapshot, Quote, Side
from sharpods.fairline import (
    blend_market_and_model,
    ensemble_probabilities,
    market_fair_line,
)

EVENT = Event(event_id="e1", sport="nfl", home="H", away="A")


def snapshot(quotes):
    return MarketSnapshot(event=EVENT, kind=MarketKind.MONEYLINE, quotes=quotes)


class TestMarketFairLine:
    def test_single_sharp_book(self):
        snap = snapshot(
            [
                Quote("pinnacle", Side.HOME, 1.87),
                Quote("pinnacle", Side.AWAY, 2.05),
            ]
        )
        fair = market_fair_line(snap)
        assert fair is not None
        assert sum(fair.probabilities.values()) == pytest.approx(1.0)
        assert fair.probabilities[Side.HOME] > fair.probabilities[Side.AWAY]
        # Devigged: below raw implied
        assert fair.probabilities[Side.HOME] < 1 / 1.87

    def test_retail_books_excluded_from_consensus(self):
        snap = snapshot(
            [
                Quote("pinnacle", Side.HOME, 1.87),
                Quote("pinnacle", Side.AWAY, 2.05),
                # A wildly wrong retail price must not shift the consensus.
                Quote("barstool", Side.HOME, 3.50),
                Quote("barstool", Side.AWAY, 1.30),
            ]
        )
        fair_with = market_fair_line(snap)
        fair_without = market_fair_line(
            snapshot(
                [
                    Quote("pinnacle", Side.HOME, 1.87),
                    Quote("pinnacle", Side.AWAY, 2.05),
                ]
            )
        )
        assert fair_with.probabilities[Side.HOME] == pytest.approx(
            fair_without.probabilities[Side.HOME]
        )
        assert "barstool" not in fair_with.sources

    def test_no_sharp_books_returns_none(self):
        snap = snapshot(
            [
                Quote("draftkings", Side.HOME, 1.87),
                Quote("draftkings", Side.AWAY, 2.05),
            ]
        )
        assert market_fair_line(snap) is None

    def test_incomplete_sharp_book_ignored(self):
        snap = snapshot(
            [
                Quote("pinnacle", Side.HOME, 1.87),  # no away quote
                Quote("circa", Side.HOME, 1.90),
                Quote("circa", Side.AWAY, 2.02),
            ]
        )
        fair = market_fair_line(snap)
        assert fair is not None
        assert set(fair.sources) == {"circa"}

    def test_weights_favour_sharper_book(self):
        snap = snapshot(
            [
                Quote("pinnacle", Side.HOME, 1.80),
                Quote("pinnacle", Side.AWAY, 2.14),
                Quote("bet365", Side.HOME, 2.10),
                Quote("bet365", Side.AWAY, 1.84),
            ]
        )
        fair = market_fair_line(snap)
        # Pinnacle says home is the favourite; bet365 disagrees. Pinnacle's
        # larger weight must dominate.
        assert fair.probabilities[Side.HOME] > 0.5
        assert fair.sources["pinnacle"] > fair.sources["bet365"]

    def test_three_way_market(self):
        snap = snapshot(
            [
                Quote("pinnacle", Side.HOME, 2.30),
                Quote("pinnacle", Side.DRAW, 3.45),
                Quote("pinnacle", Side.AWAY, 3.30),
            ]
        )
        fair = market_fair_line(snap)
        assert sum(fair.probabilities.values()) == pytest.approx(1.0)
        assert len(fair.probabilities) == 3

    def test_spread_line_pinning_uses_absolute_number(self):
        snap = MarketSnapshot(
            event=EVENT,
            kind=MarketKind.SPREAD,
            quotes=[
                Quote("pinnacle", Side.HOME, 1.925, line=-3.0),
                Quote("pinnacle", Side.AWAY, 1.887, line=3.0),
                Quote("caesars", Side.HOME, 1.952, line=-2.5),
                Quote("caesars", Side.AWAY, 1.87, line=2.5),
            ],
        )
        fair = market_fair_line(snap, line=3.0)
        assert fair is not None
        assert set(fair.sources) == {"pinnacle"}

    def test_fair_decimal(self):
        snap = snapshot(
            [
                Quote("pinnacle", Side.HOME, 2.0),
                Quote("pinnacle", Side.AWAY, 2.0),
            ]
        )
        fair = market_fair_line(snap)
        assert fair.fair_decimal(Side.HOME) == pytest.approx(2.0)


class TestBlending:
    def test_full_market_weight_ignores_model(self):
        assert blend_market_and_model(0.55, 0.90, 1.0) == pytest.approx(0.55)

    def test_blend_between_inputs(self):
        blended = blend_market_and_model(0.50, 0.60, 0.75)
        assert 0.50 < blended < 0.60
        # Closer to the market than the model
        assert abs(blended - 0.50) < abs(blended - 0.60)

    def test_symmetric_blend_sums_to_one(self):
        home = blend_market_and_model(0.55, 0.60, 0.75)
        away = blend_market_and_model(0.45, 0.40, 0.75)
        assert home + away == pytest.approx(1.0)

    def test_invalid_inputs(self):
        with pytest.raises(ValueError):
            blend_market_and_model(0.5, 0.5, 0.0)
        with pytest.raises(ValueError):
            blend_market_and_model(1.5, 0.5)


class TestEnsemble:
    def test_equal_weights_median_behaviour(self):
        p = ensemble_probabilities([0.5, 0.6])
        assert 0.5 < p < 0.6

    def test_weighted(self):
        p = ensemble_probabilities([0.5, 0.6], [3.0, 1.0])
        assert p < ensemble_probabilities([0.5, 0.6], [1.0, 1.0])

    def test_identity(self):
        assert ensemble_probabilities([0.42]) == pytest.approx(0.42)

    def test_errors(self):
        with pytest.raises(ValueError):
            ensemble_probabilities([])
        with pytest.raises(ValueError):
            ensemble_probabilities([0.5], [1.0, 2.0])
