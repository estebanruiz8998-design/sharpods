import pytest

from sharpods.datatypes import BetCandidate, Event, MarketKind, Quote, Side
from sharpods.portfolio import Portfolio, RiskPolicy


def candidate(event_id="e1", ev=0.05, prob=0.55, odds=2.0, side=Side.HOME):
    return BetCandidate(
        event=Event(event_id=event_id, sport="nfl", home="H", away="A"),
        kind=MarketKind.MONEYLINE,
        side=side,
        quote=Quote("pinnacle", side, odds),
        fair_probability=prob,
        ev_pct=ev,
    )


class TestRiskPolicy:
    def test_validation(self):
        with pytest.raises(ValueError):
            RiskPolicy(kelly_multiplier=0.0)
        with pytest.raises(ValueError):
            RiskPolicy(max_bet_fraction=1.5)


class TestPortfolio:
    def test_stakes_positive_ev_only(self):
        portfolio = Portfolio(bankroll=10_000)
        tickets = portfolio.allocate([candidate(ev=0.05), candidate(ev=-0.02, prob=0.45)])
        assert len(tickets) == 1
        assert tickets[0].candidate.ev_pct == pytest.approx(0.05)

    def test_min_ev_threshold(self):
        portfolio = Portfolio(bankroll=10_000, policy=RiskPolicy(min_ev=0.03))
        tickets = portfolio.allocate([candidate(ev=0.02)])
        assert tickets == []

    def test_per_bet_cap(self):
        # Huge edge: quarter Kelly would exceed 2%; cap binds.
        portfolio = Portfolio(bankroll=10_000)
        tickets = portfolio.allocate([candidate(ev=0.40, prob=0.70, odds=2.0)])
        assert tickets[0].stake_fraction == pytest.approx(0.02)
        assert tickets[0].stake_amount == pytest.approx(200.0)

    def test_event_cap_limits_correlated_bets(self):
        policy = RiskPolicy(max_bet_fraction=0.02, max_event_fraction=0.03)
        portfolio = Portfolio(bankroll=10_000, policy=policy)
        cands = [
            candidate(event_id="same", ev=0.40, prob=0.70, side=Side.HOME),
            candidate(event_id="same", ev=0.39, prob=0.70, side=Side.AWAY),
            candidate(event_id="same", ev=0.38, prob=0.70, side=Side.OVER),
        ]
        tickets = portfolio.allocate(cands)
        total = sum(t.stake_fraction for t in tickets)
        assert total <= 0.03 + 1e-9

    def test_slate_cap(self):
        policy = RiskPolicy(max_slate_fraction=0.05, max_bet_fraction=0.02)
        portfolio = Portfolio(bankroll=10_000, policy=policy)
        cands = [
            candidate(event_id=f"e{i}", ev=0.40, prob=0.70) for i in range(10)
        ]
        tickets = portfolio.allocate(cands)
        total = sum(t.stake_fraction for t in tickets)
        assert total <= 0.05 + 1e-9

    def test_best_ev_first(self):
        portfolio = Portfolio(bankroll=10_000)
        tickets = portfolio.allocate(
            [candidate(event_id="low", ev=0.02, prob=0.51), candidate(event_id="high", ev=0.06, prob=0.53)]
        )
        assert tickets[0].candidate.event.event_id == "high"

    def test_invalid_bankroll(self):
        with pytest.raises(ValueError):
            Portfolio(bankroll=0).allocate([candidate()])
