"""End-to-end tests: sample slate through the full pipeline."""

from pathlib import Path

import pytest

from sharpods.cli import main as cli_main
from sharpods.datatypes import MarketKind, Side
from sharpods.engine import Engine, render_bet_card
from sharpods.io import load_slate

SAMPLE = Path(__file__).resolve().parent.parent / "data" / "sample_odds.json"


@pytest.fixture(scope="module")
def slate():
    return load_slate(SAMPLE)


@pytest.fixture(scope="module")
def card(slate):
    engine = Engine()
    return engine.run(
        slate.snapshots,
        bankroll=10_000,
        model_probabilities=slate.model_probabilities,
        history=slate.history,
    )


class TestIo:
    def test_loads_all_markets(self, slate):
        assert len(slate.snapshots) == 6
        kinds = {(s.event.event_id, s.kind) for s in slate.snapshots}
        assert ("nfl-2026-w9-kc-buf", MarketKind.MONEYLINE) in kinds
        assert ("epl-2026-ars-liv", MarketKind.MONEYLINE) in kinds

    def test_model_probability_keys(self, slate):
        key = ("nfl-2026-w9-kc-buf", MarketKind.MONEYLINE, Side.HOME)
        assert slate.model_probabilities[key] == pytest.approx(0.545)

    def test_history_parsed(self, slate):
        hist = slate.history[("nfl-2026-w9-kc-buf", MarketKind.MONEYLINE)]
        assert len(hist) == 2


class TestPipeline:
    def test_finds_the_planted_value_bets(self, card):
        picks = {
            (t.candidate.event.event_id, t.candidate.side, t.candidate.quote.book)
            for t in card.tickets
        }
        # The stale betmgm price on the Chiefs after pinnacle steamed to the Bills.
        assert ("nfl-2026-w9-kc-buf", Side.AWAY, "betmgm") in picks
        # DraftKings' off-market Celtics price.
        assert ("nba-2026-lal-bos", Side.HOME, "draftkings") in picks

    def test_no_negative_ev_tickets(self, card):
        assert all(t.candidate.ev_pct >= 0.01 for t in card.tickets)

    def test_efficient_markets_produce_no_bets(self, card):
        # Totals and spreads in the sample are priced tight to consensus.
        for ticket in card.tickets:
            assert ticket.candidate.kind == MarketKind.MONEYLINE

    def test_tickets_ranked_by_log_growth(self, card):
        from sharpods.kelly import expected_log_growth

        growths = [
            expected_log_growth(
                t.candidate.fair_probability,
                t.candidate.quote.decimal_odds,
                t.stake_fraction,
            )
            for t in card.tickets
        ]
        assert growths == sorted(growths, reverse=True)

    def test_stakes_respect_caps(self, card):
        for t in card.tickets:
            assert 0 < t.stake_fraction <= 0.02
        assert sum(t.stake_fraction for t in card.tickets) <= 0.20

    def test_finds_arbitrages(self, card):
        arb_events = {event_id for event_id, _ in card.arbitrages}
        # betmgm's stale Chiefs price arbs against circa's Bills price,
        # and draftkings/fanduel disagree on the NBA game.
        assert "nba-2026-lal-bos" in arb_events
        assert "nfl-2026-w9-kc-buf" in arb_events
        for _, arb in card.arbitrages:
            assert arb.profit_margin > 0
            assert sum(arb.stakes) == pytest.approx(1.0)

    def test_finds_the_middle(self, card):
        assert any(event_id == "nfl-2026-w9-dal-phi" for event_id, _ in card.middles)
        _, mid = next(m for m in card.middles if m[0] == "nfl-2026-w9-dal-phi")
        assert mid.window == (3,)

    def test_finds_wong_teaser_legs(self, card):
        by_event = {}
        for leg in card.teaser_legs:
            by_event.setdefault(leg.event_id, []).append(leg)
        # Bills -7.5 (three books quote it) and Cowboys +2.5 (caesars).
        assert "nfl-2026-w9-kc-buf" in by_event
        assert "nfl-2026-w9-dal-phi" in by_event
        cowboys_leg = by_event["nfl-2026-w9-dal-phi"][0]
        assert cowboys_leg.original_line == pytest.approx(2.5)
        assert cowboys_leg.teased_line == pytest.approx(8.5)

    def test_diagnostics_cover_every_market(self, card, slate):
        assert len(card.diagnostics) == len(slate.snapshots)

    def test_spread_consensus_line_is_absolute(self, card):
        diag = next(
            d
            for d in card.diagnostics
            if d.event_id == "nfl-2026-w9-dal-phi" and d.kind == MarketKind.SPREAD
        )
        assert diag.consensus_line == pytest.approx(3.0)
        assert set(diag.fair_line.sources) == {"pinnacle"}


class TestModelBlend:
    def test_model_shifts_probability_toward_model(self, slate):
        base = Engine(market_weight=1.0).run(slate.snapshots, 10_000)
        blended = Engine(market_weight=0.75).run(
            slate.snapshots, 10_000, model_probabilities=slate.model_probabilities
        )

        def home_prob(card):
            for t in card.tickets:
                if (
                    t.candidate.event.event_id == "nfl-2026-w9-kc-buf"
                    and t.candidate.side == Side.AWAY
                ):
                    return t.candidate.fair_probability
            return None

        p_base, p_blend = home_prob(base), home_prob(blended)
        assert p_base is not None and p_blend is not None
        # Model says away 0.455 < market fair; blend must pull the away
        # probability below the pure-market number.
        assert p_blend < p_base


class TestRendering:
    def test_render_contains_key_sections(self, card):
        text = render_bet_card(card, 10_000)
        assert "SHARPODS BET CARD" in text
        assert "RECOMMENDED BETS" in text
        assert "ARBITRAGE" in text
        assert "MIDDLES" in text
        assert "WONG TEASER LEGS" in text
        assert "MARKET DIAGNOSTICS" in text

    def test_cli_end_to_end(self, capsys):
        assert cli_main([str(SAMPLE), "--bankroll", "5000"]) == 0
        out = capsys.readouterr().out
        assert "SHARPODS BET CARD" in out


class TestRefusals:
    def test_no_fair_line_without_sharp_books(self):
        from sharpods.datatypes import Event, MarketSnapshot, Quote

        snap = MarketSnapshot(
            event=Event(event_id="retail-only", sport="nfl", home="H", away="A"),
            kind=MarketKind.MONEYLINE,
            quotes=[
                Quote("draftkings", Side.HOME, 2.30),
                Quote("fanduel", Side.AWAY, 1.75),
            ],
        )
        card = Engine().run([snap], 10_000)
        assert card.tickets == []
        assert any("refusing to invent a fair line" in s for s in card.skipped)


class TestPriceTargets:
    def test_every_candidate_carries_a_target(self, card):
        assert card.candidates, "engine should surface evaluated candidates"
        for c in card.candidates:
            assert c.target_decimal is not None
            # Target is exactly the price that yields min_ev at the fair prob.
            assert c.fair_probability * c.target_decimal - 1.0 == pytest.approx(0.01)

    def test_candidates_ranked_by_ev(self, card):
        evs = [c.ev_pct for c in card.candidates]
        assert evs == sorted(evs, reverse=True)

    def test_targets_exclude_ticketed_sides(self, card):
        ticketed = {
            (t.candidate.event.event_id, t.candidate.kind, t.candidate.side)
            for t in card.tickets
        }
        for c in card.price_targets():
            assert (c.event.event_id, c.kind, c.side) not in ticketed

    def test_render_shows_limit_orders(self, card):
        text = render_bet_card(card, 10_000)
        assert "PRICE TARGETS" in text
        assert "bet at >=" in text


class TestDegradedAnchor:
    """Live-run lesson (2026-07-29): consensus-grade anchors carry ~2pt
    probability noise, so the EV bar scales up when no market maker anchors
    the fair line."""

    def _snapshot(self, home_odds, away_odds, book="bet365"):
        from sharpods.datatypes import Event, MarketSnapshot, Quote

        return MarketSnapshot(
            event=Event(event_id="degraded", sport="mlb", home="H", away="A"),
            kind=MarketKind.MONEYLINE,
            quotes=[
                Quote(book, Side.HOME, home_odds),
                Quote(book, Side.AWAY, away_odds),
            ],
        )

    def test_dispersion_price_tickets_at_the_floor_on_soft_anchor(self):
        # bet365 (sharpness 0.55) anchors; fair home prob is 0.500, so 2.03
        # at FanDuel is a +1.5% edge. Pre-2026-08-23 policy held this below
        # the 2.5% degraded bar; the user-directed tier change (see
        # Engine.dispersion_ev_multiplier) bets prices from OUTSIDE the
        # anchor consensus at the 1% floor — the ledger's only positive-CLV
        # fills were exactly this shape.
        snap = self._snapshot(1.909, 1.909)
        snap.quotes.append(
            __import__("sharpods.datatypes", fromlist=["Quote"]).Quote(
                "fanduel", Side.HOME, 2.03
            )
        )
        card = Engine().run([snap], 10_000)
        assert len(card.tickets) == 1
        cand = card.tickets[0].candidate
        assert cand.quote.book == "fanduel"
        assert cand.required_ev == pytest.approx(0.01)
        # The anchor-priced away side still carries the full degraded bar.
        away = next(c for c in card.candidates if c.side == Side.AWAY)
        assert away.required_ev == pytest.approx(0.025)

    def test_big_edge_still_tickets_on_soft_anchor(self):
        # 2.06 at fair 0.500 is +3.0% EV, above the 2.5% bar, and the
        # cross-source hold stays positive (no conflict refusal).
        snap = self._snapshot(1.909, 1.909)
        snap.quotes.append(
            __import__("sharpods.datatypes", fromlist=["Quote"]).Quote(
                "fanduel", Side.HOME, 2.06
            )
        )
        card = Engine().run([snap], 10_000)
        assert len(card.tickets) == 1
        assert card.tickets[0].candidate.ev_pct > 0.025

    def test_negative_hold_refuses_degraded_market(self):
        # A cross-source "arb" on soft anchors is conflicting quotes, not
        # value: no candidates, no arb listing, an explicit skip reason.
        snap = self._snapshot(1.909, 1.909)
        snap.quotes.append(
            __import__("sharpods.datatypes", fromlist=["Quote"]).Quote(
                "fanduel", Side.HOME, 2.12
            )
        )
        card = Engine().run([snap], 10_000)
        assert card.tickets == []
        assert card.candidates == []
        assert card.arbitrages == []
        assert any("conflicting quotes" in s for s in card.skipped)

    def test_sharp_anchor_negative_hold_still_arbs(self, card):
        # Pinnacle-anchored sample slate keeps its genuine arbs.
        assert len(card.arbitrages) == 2

    def test_sharp_anchor_keeps_normal_bar(self, card):
        # Sample slate is pinnacle-anchored: requirements stay at the floor.
        for c in card.candidates:
            assert c.required_ev == pytest.approx(0.01)

    def test_targets_reflect_raised_bar(self):
        snap = self._snapshot(1.909, 1.909)
        card = Engine().run([snap], 10_000)
        for c in card.candidates:
            assert c.fair_probability * c.target_decimal - 1.0 == pytest.approx(0.025)
