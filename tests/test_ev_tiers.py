"""Tiered EV bars inside degraded mode (user-directed change, 2026-08-23).

The ledger's two graded edge classes get lower bars: prices from a venue
outside the anchor consensus (dispersion) bet at 1x min_ev, model-backed
sides at 1.5x; single-anchor market-only sides keep the full degraded
multiplier. Sharp-anchor markets are unchanged.
"""

import pytest

from sharpods.books_registry import BookProfile, BooksRegistry
from sharpods.datatypes import Event, MarketKind, MarketSnapshot, Quote, Side
from sharpods.engine import Engine
from sharpods.portfolio import RiskPolicy

EVENT = Event(event_id="e1", sport="mlb", home="H", away="A")


def make_registry(anchor_sharpness):
    reg = BooksRegistry()
    reg.register(BookProfile(name="anchor", sharpness=anchor_sharpness, market_maker=anchor_sharpness >= 0.8))
    reg.register(BookProfile(name="pm", sharpness=0.45, market_maker=True, notes="shop-only venue"))
    return reg


def make_engine(anchor_sharpness=0.6):
    return Engine(registry=make_registry(anchor_sharpness),
                  policy=RiskPolicy(kelly_multiplier=0.25, min_ev=0.01),
                  devig_method="power", market_weight=0.85)


def snapshot(extra=()):
    quotes = [
        Quote(book="anchor", side=Side.HOME, decimal_odds=1.68),
        Quote(book="anchor", side=Side.AWAY, decimal_odds=2.26),
        *extra,
    ]
    return MarketSnapshot(event=EVENT, kind=MarketKind.MONEYLINE, quotes=quotes)


def by_side(candidates):
    return {c.side: c for c in candidates}


class TestDegradedTiers:
    def test_market_only_single_anchor_keeps_full_bar(self):
        cands, _ = make_engine().evaluate_market(snapshot())
        for c in cands:
            assert c.required_ev == pytest.approx(0.025)

    def test_dispersion_price_bets_at_base_min_ev(self):
        snap = snapshot([Quote(book="pm", side=Side.AWAY, decimal_odds=2.40)])
        cands, _ = make_engine().evaluate_market(snap)
        sides = by_side(cands)
        assert sides[Side.AWAY].quote.book == "pm"
        assert sides[Side.AWAY].required_ev == pytest.approx(0.01)
        # The anchor-priced side keeps the full degraded bar.
        assert sides[Side.HOME].required_ev == pytest.approx(0.025)

    def test_model_backed_side_bets_at_model_tier(self):
        cands, _ = make_engine().evaluate_market(
            snapshot(), model_probabilities={Side.HOME: 0.62}
        )
        sides = by_side(cands)
        assert sides[Side.HOME].required_ev == pytest.approx(0.015)
        assert sides[Side.AWAY].required_ev == pytest.approx(0.025)

    def test_dispersion_beats_model_tier(self):
        snap = snapshot([Quote(book="pm", side=Side.AWAY, decimal_odds=2.40)])
        cands, _ = make_engine().evaluate_market(
            snap, model_probabilities={Side.AWAY: 0.46}
        )
        sides = by_side(cands)
        assert sides[Side.AWAY].required_ev == pytest.approx(0.01)

    def test_sharp_anchor_unchanged(self):
        cands, _ = make_engine(anchor_sharpness=0.9).evaluate_market(snapshot())
        for c in cands:
            assert c.required_ev == pytest.approx(0.01)

    def test_dispersion_value_becomes_a_ticket(self):
        # Anchor devigs away to ~41%; a 2.40 outside price is ~+1.3% EV -
        # above the 1% dispersion bar, so the pipeline must ticket it.
        snap = snapshot([Quote(book="pm", side=Side.AWAY, decimal_odds=2.40)])
        card = make_engine().run([snap], bankroll=10_000)
        assert any(
            t.candidate.side == Side.AWAY and t.candidate.quote.book == "pm"
            for t in card.tickets
        )

    def test_refusal_still_wins_over_tiers(self):
        # Negative cross-source hold on a degraded anchor still refuses the
        # market outright - no tier resurrects it.
        snap = snapshot([Quote(book="pm", side=Side.AWAY, decimal_odds=2.90)])
        cands, diag = make_engine().evaluate_market(snap)
        assert cands == []
        assert "refusing to price" in (diag.unpriceable_reason or "")
