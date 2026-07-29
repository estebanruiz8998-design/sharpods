import pytest

from sharpods.datatypes import Event, MarketKind, MarketSnapshot, Quote, Side
from sharpods.edges import (
    NFL_MARGIN_FREQ,
    best_quote,
    detect_steam,
    expected_value,
    find_arbitrage,
    find_middles,
    find_wong_teaser_legs,
    half_point_ev_gain,
    is_wong_leg,
    spread_ev,
    teaser_breakeven_leg_probability,
    teaser_ev,
)

EVENT = Event(event_id="e1", sport="nfl", home="H", away="A")


class TestEv:
    def test_positive_and_negative(self):
        assert expected_value(0.55, 2.0) == pytest.approx(0.10)
        assert expected_value(0.45, 2.0) == pytest.approx(-0.10)

    def test_fair_is_zero(self):
        assert expected_value(0.5, 2.0) == pytest.approx(0.0)


class TestBestQuote:
    def test_picks_highest_price(self):
        snap = MarketSnapshot(
            event=EVENT,
            kind=MarketKind.MONEYLINE,
            quotes=[
                Quote("a", Side.HOME, 1.90),
                Quote("b", Side.HOME, 1.95),
                Quote("c", Side.HOME, 1.87),
            ],
        )
        q = best_quote(snap, Side.HOME)
        assert q.book == "b"

    def test_none_when_absent(self):
        snap = MarketSnapshot(event=EVENT, kind=MarketKind.MONEYLINE, quotes=[])
        assert best_quote(snap, Side.HOME) is None


class TestKeyNumbers:
    def test_spread_ev_with_push(self):
        # 50% cover, 10% push at 1.909: EV = .5*.909 - .4 = +0.0545
        assert spread_ev(0.5, 0.1, 1.909) == pytest.approx(0.0545, abs=1e-4)

    def test_half_point_off_three_beats_dead_number(self):
        off_three = half_point_ev_gain(-3.0, -2.5, 1.909)
        off_dead = half_point_ev_gain(-12.5, -12.0, 1.909)
        assert off_three > off_dead
        assert off_three == pytest.approx(NFL_MARGIN_FREQ[3] * 0.909, abs=1e-6)

    def test_half_point_onto_three(self):
        # -3.5 -> -3.0 turns losses at 3 into pushes: worth freq(3) * 1
        gain = half_point_ev_gain(-3.5, -3.0, 1.909)
        assert gain == pytest.approx(NFL_MARGIN_FREQ[3])

    def test_invalid_direction(self):
        with pytest.raises(ValueError):
            half_point_ev_gain(-2.5, -3.0, 1.909)
        with pytest.raises(ValueError):
            half_point_ev_gain(-3.0, -1.5, 1.909)


class TestWongTeasers:
    def test_qualifying_favourites(self):
        assert is_wong_leg(Side.HOME, -7.5)
        assert is_wong_leg(Side.HOME, -8.0)
        assert is_wong_leg(Side.AWAY, -8.5)

    def test_qualifying_underdogs(self):
        assert is_wong_leg(Side.AWAY, 1.5)
        assert is_wong_leg(Side.HOME, 2.5)

    def test_non_qualifying(self):
        assert not is_wong_leg(Side.HOME, -7.0)  # teased to -1: never gets through 7
        assert not is_wong_leg(Side.HOME, -9.0)
        assert not is_wong_leg(Side.AWAY, 3.0)
        assert not is_wong_leg(Side.AWAY, 1.0)

    def test_only_six_point_teasers(self):
        assert not is_wong_leg(Side.HOME, -7.5, teaser_points=7.0)

    def test_finder(self):
        snap = MarketSnapshot(
            event=EVENT,
            kind=MarketKind.SPREAD,
            quotes=[
                Quote("pinnacle", Side.HOME, 1.909, line=-7.5),
                Quote("pinnacle", Side.AWAY, 1.909, line=7.5),
            ],
        )
        legs = find_wong_teaser_legs([snap])
        assert len(legs) == 1
        assert legs[0].side == Side.HOME
        assert legs[0].teased_line == pytest.approx(-1.5)

    def test_breakeven(self):
        assert teaser_breakeven_leg_probability(1.909, 2) == pytest.approx(0.7237, abs=1e-4)

    def test_teaser_ev(self):
        # Two 75% legs at 1.909: EV = .75^2 * 1.909 - 1 = +7.4%
        assert teaser_ev([0.75, 0.75], 1.909) == pytest.approx(0.0738, abs=1e-3)


class TestArbitrage:
    def test_detects_arb(self):
        snap = MarketSnapshot(
            event=EVENT,
            kind=MarketKind.MONEYLINE,
            quotes=[
                Quote("a", Side.HOME, 2.02),
                Quote("b", Side.AWAY, 2.02),
            ],
        )
        arb = find_arbitrage(snap)
        assert arb is not None
        assert arb.profit_margin == pytest.approx(2.02 / 2 - 1, abs=1e-9)
        assert sum(arb.stakes) == pytest.approx(1.0)
        # Equal odds -> equal stakes
        assert arb.stakes[0] == pytest.approx(arb.stakes[1])

    def test_no_arb_at_normal_prices(self):
        snap = MarketSnapshot(
            event=EVENT,
            kind=MarketKind.MONEYLINE,
            quotes=[
                Quote("a", Side.HOME, 1.909),
                Quote("b", Side.AWAY, 1.909),
            ],
        )
        assert find_arbitrage(snap) is None

    def test_arb_payout_equalized(self):
        snap = MarketSnapshot(
            event=EVENT,
            kind=MarketKind.MONEYLINE,
            quotes=[
                Quote("a", Side.HOME, 2.10),
                Quote("b", Side.AWAY, 2.00),
            ],
        )
        arb = find_arbitrage(snap)
        payout_home = arb.stakes[0] * 2.10
        payout_away = arb.stakes[1] * 2.00
        assert payout_home == pytest.approx(payout_away)


class TestMiddles:
    def test_finds_middle_around_three(self):
        snap = MarketSnapshot(
            event=EVENT,
            kind=MarketKind.SPREAD,
            quotes=[
                Quote("caesars", Side.HOME, 1.952, line=-2.5),
                Quote("barstool", Side.AWAY, 1.87, line=3.5),
            ],
        )
        middles = find_middles(snap)
        assert len(middles) == 1
        mid = middles[0]
        assert mid.window == (3,)
        assert mid.hit_probability == pytest.approx(NFL_MARGIN_FREQ[3])
        assert mid.ev > 0

    def test_no_middle_same_number(self):
        snap = MarketSnapshot(
            event=EVENT,
            kind=MarketKind.SPREAD,
            quotes=[
                Quote("a", Side.HOME, 1.909, line=-7.5),
                Quote("b", Side.AWAY, 1.909, line=7.5),
            ],
        )
        assert find_middles(snap) == []


class TestSteam:
    def test_detects_sharp_move(self):
        history = [
            Quote("pinnacle", Side.HOME, 1.95, timestamp=1000.0),
            Quote("pinnacle", Side.HOME, 1.87, timestamp=1200.0),
        ]
        signals = detect_steam(history)
        assert len(signals) == 1
        assert signals[0].book == "pinnacle"
        assert signals[0].implied_move > 0.02

    def test_ignores_retail_moves(self):
        history = [
            Quote("barstool", Side.HOME, 1.95, timestamp=1000.0),
            Quote("barstool", Side.HOME, 1.80, timestamp=1200.0),
        ]
        assert detect_steam(history) == []

    def test_ignores_slow_drift(self):
        history = [
            Quote("pinnacle", Side.HOME, 1.95, timestamp=1000.0),
            Quote("pinnacle", Side.HOME, 1.87, timestamp=9000.0),
        ]
        assert detect_steam(history) == []

    def test_flags_stale_quotes(self):
        history = [
            Quote("pinnacle", Side.HOME, 2.10, timestamp=1000.0),
            Quote("pinnacle", Side.HOME, 1.87, timestamp=1200.0),
        ]
        current = MarketSnapshot(
            event=EVENT,
            kind=MarketKind.MONEYLINE,
            quotes=[
                Quote("pinnacle", Side.HOME, 1.87),
                Quote("betmgm", Side.HOME, 2.08),  # hasn't moved yet
            ],
        )
        signals = detect_steam(history, current)
        assert len(signals) == 1
        assert [q.book for q in signals[0].stale_quotes] == ["betmgm"]
