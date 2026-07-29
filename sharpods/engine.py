"""The SharpOds engine — the unified "maximum capacity" pipeline.

Stage order (each stage names the books that justify it):

1. Fair line: devig sharp books, sharpness-weighted logit consensus
   (The Logic of Sports Betting; Sharper; Squares & Sharps).
2. Model blend: fold in fundamental-model probabilities, market-weighted
   (Mathletics; Trading Bases; Statistical Sports Models; Fixed Odds).
3. Edge scan: best price vs fair line -> EV; arbitrage; middles; Wong
   teasers; steam-stale flags (Sharp Sports Betting; Weighing the Odds;
   The Logic of Sports Betting; Sharper).
4. Staking: fractional Kelly under portfolio caps (Fortune's Formula;
   Trading Bases; Fixed Odds Sports Betting).
5. Bet card: ranked tickets with rationale, plus structural plays (arbs,
   middles, teasers) and per-market diagnostics.

The engine never bets without a price edge against its own fair number —
"bet value, not winners" (Buchdahl) is enforced structurally, not by policy.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

from sharpods.books_registry import BooksRegistry, DEFAULT_REGISTRY
from sharpods.datatypes import (
    BetCandidate,
    BetTicket,
    FairLine,
    MarketKind,
    MarketSnapshot,
    Quote,
    Side,
)
from sharpods.edges import (
    Arbitrage,
    Middle,
    TeaserLeg,
    best_quote,
    detect_steam,
    expected_value,
    find_arbitrage,
    find_middles,
    find_wong_teaser_legs,
    teaser_breakeven_leg_probability,
)
from sharpods.fairline import blend_market_and_model, market_fair_line
from sharpods.odds import synthetic_hold
from sharpods.portfolio import Portfolio, RiskPolicy


@dataclass
class MarketDiagnostics:
    event_id: str
    kind: MarketKind
    consensus_line: float | None
    fair_line: FairLine | None
    synthetic_hold: float | None


@dataclass
class BetCard:
    tickets: list[BetTicket]
    arbitrages: list[tuple[str, Arbitrage]]
    middles: list[tuple[str, Middle]]
    teaser_legs: list[TeaserLeg]
    diagnostics: list[MarketDiagnostics]
    skipped: list[str] = field(default_factory=list)
    # Every evaluated side, ranked by EV — including sub-threshold ones. The
    # sub-threshold entries carry target_decimal: the day's limit orders.
    candidates: list[BetCandidate] = field(default_factory=list)

    def price_targets(self) -> list[BetCandidate]:
        """Sub-threshold candidates as limit orders, best-first."""
        ticketed = {
            (t.candidate.event.event_id, t.candidate.kind, t.candidate.side)
            for t in self.tickets
        }
        return [
            c
            for c in self.candidates
            if (c.event.event_id, c.kind, c.side) not in ticketed
        ]


@dataclass
class Engine:
    registry: BooksRegistry = field(default_factory=lambda: DEFAULT_REGISTRY)
    policy: RiskPolicy = field(default_factory=RiskPolicy)
    devig_method: str = "power"
    market_weight: float = 0.75
    min_consensus_sharpness: float = 0.5

    def consensus_line(self, snapshot: MarketSnapshot) -> float | None:
        """Pin spreads/totals to one market number so EV compares like with
        like.

        Spread numbers are absolute values (home -3 / away +3 are one
        market at number 3). Preference: the number quoted by the sharpest
        book; ties broken by how many quotes sit at it. Moneylines: None.
        """
        if snapshot.kind == MarketKind.MONEYLINE:
            return None

        def number(line: float) -> float:
            return abs(line) if snapshot.kind == MarketKind.SPREAD else line

        numbers = [number(q.line) for q in snapshot.quotes if q.line is not None]
        if not numbers:
            return None
        counts = Counter(numbers)

        def line_rank(n: float) -> tuple[float, int]:
            sharpest = max(
                (
                    self.registry.sharpness(q.book)
                    for q in snapshot.quotes
                    if q.line is not None and number(q.line) == n
                ),
                default=0.0,
            )
            return sharpest, counts[n]

        return max(counts, key=line_rank)

    def evaluate_market(
        self,
        snapshot: MarketSnapshot,
        model_probabilities: dict[Side, float] | None = None,
        history: list[Quote] | None = None,
    ) -> tuple[list[BetCandidate], MarketDiagnostics]:
        """Stages 1-3 for a single market."""
        line = self.consensus_line(snapshot)
        fair = market_fair_line(
            snapshot,
            registry=self.registry,
            devig_method=self.devig_method,
            min_sharpness=self.min_consensus_sharpness,
            line=line,
        )

        # Synthetic hold across best prices (diagnostic + arb precursor).
        best_prices: list[float] = []
        for side in snapshot.sides():
            q = best_quote(snapshot, side, line)
            if q is not None:
                best_prices.append(q.decimal_odds)
        hold = synthetic_hold(best_prices) if len(best_prices) >= 2 else None

        diagnostics = MarketDiagnostics(
            event_id=snapshot.event.event_id,
            kind=snapshot.kind,
            consensus_line=line,
            fair_line=fair,
            synthetic_hold=hold,
        )
        if fair is None:
            return [], diagnostics

        steam = detect_steam(history or [], snapshot, self.registry)
        steam_sides = {s.side for s in steam}

        candidates: list[BetCandidate] = []
        for side in snapshot.sides():
            probability = fair.probabilities.get(side)
            if probability is None or not 0.0 < probability < 1.0:
                continue
            if model_probabilities and side in model_probabilities:
                probability = blend_market_and_model(
                    probability,
                    model_probabilities[side],
                    market_weight=self.market_weight,
                )
            quote = best_quote(snapshot, side, line)
            if quote is None:
                continue
            ev = expected_value(probability, quote.decimal_odds)
            target = (1.0 + self.policy.min_ev) / probability
            tags = [f"best price of {len(snapshot.quotes_for(side, line))} quotes"]
            if model_probabilities and side in model_probabilities:
                tags.append(
                    f"market/model blend {self.market_weight:.0%}/{1 - self.market_weight:.0%}"
                )
            if side in steam_sides:
                tags.append("sharp steam toward this side; verify price is stale, not moved")
            candidates.append(
                BetCandidate(
                    event=snapshot.event,
                    kind=snapshot.kind,
                    side=side,
                    quote=quote,
                    fair_probability=probability,
                    ev_pct=ev,
                    tags=tags,
                    target_decimal=target,
                )
            )
        return candidates, diagnostics

    def run(
        self,
        snapshots: list[MarketSnapshot],
        bankroll: float,
        model_probabilities: dict[tuple[str, MarketKind, Side], float] | None = None,
        history: dict[tuple[str, MarketKind], list[Quote]] | None = None,
    ) -> BetCard:
        """Full pipeline over a slate of markets."""
        all_candidates: list[BetCandidate] = []
        diagnostics: list[MarketDiagnostics] = []
        arbitrages: list[tuple[str, Arbitrage]] = []
        middles: list[tuple[str, Middle]] = []
        skipped: list[str] = []

        for snap in snapshots:
            model_probs: dict[Side, float] = {}
            if model_probabilities:
                for side in snap.sides():
                    key = (snap.event.event_id, snap.kind, side)
                    if key in model_probabilities:
                        model_probs[side] = model_probabilities[key]

            market_history = None
            if history:
                market_history = history.get((snap.event.event_id, snap.kind))

            candidates, diag = self.evaluate_market(
                snap, model_probs or None, market_history
            )
            diagnostics.append(diag)
            if not candidates and diag.fair_line is None:
                skipped.append(
                    f"{snap.event.event_id}/{snap.kind.value}: no sharp book quotes "
                    "the full market; refusing to invent a fair line"
                )
            all_candidates.extend(candidates)

            arb = find_arbitrage(snap, diag.consensus_line)
            if arb is not None:
                arbitrages.append((snap.event.event_id, arb))
            if snap.kind == MarketKind.SPREAD:
                for mid in find_middles(snap):
                    if mid.ev > 0:
                        middles.append((snap.event.event_id, mid))

        teaser_legs = find_wong_teaser_legs(
            [s for s in snapshots if s.kind == MarketKind.SPREAD]
        )

        portfolio = Portfolio(bankroll=bankroll, policy=self.policy)
        tickets = portfolio.allocate(all_candidates)

        return BetCard(
            tickets=tickets,
            arbitrages=arbitrages,
            middles=middles,
            teaser_legs=teaser_legs,
            diagnostics=diagnostics,
            skipped=skipped,
            candidates=sorted(all_candidates, key=lambda c: c.ev_pct, reverse=True),
        )


def render_bet_card(card: BetCard, bankroll: float) -> str:
    """Human-readable bet card."""
    lines: list[str] = []
    lines.append("=" * 72)
    lines.append("SHARPODS BET CARD")
    lines.append("=" * 72)

    if card.tickets:
        lines.append("")
        lines.append(f"RECOMMENDED BETS ({len(card.tickets)}), bankroll {bankroll:,.2f}:")
        for i, t in enumerate(card.tickets, 1):
            c = t.candidate
            line_txt = f" {c.quote.line:+g}" if c.quote.line is not None else ""
            lines.append(
                f"{i:>2}. {c.event.away} @ {c.event.home} | "
                f"{c.kind.value} {c.side.value}{line_txt} | "
                f"{c.quote.book} @ {c.quote.decimal_odds:.3f}"
            )
            lines.append(
                f"    fair p={c.fair_probability:.4f} (fair odds {c.fair_decimal:.3f}) | "
                f"EV {c.ev_pct:+.2%} | stake {t.stake_amount:,.2f} "
                f"({t.stake_fraction:.2%} of roll, {t.kelly_multiplier:.0%} Kelly)"
            )
            for tag in t.rationale:
                lines.append(f"      - {tag}")
    else:
        lines.append("")
        lines.append("No bets clear the EV threshold. Not betting is a position.")

    targets = card.price_targets()
    if targets:
        lines.append("")
        lines.append("PRICE TARGETS (limit orders — bet only at or above the target):")
        for c in targets[:10]:
            line_txt = f" {c.quote.line:+g}" if c.quote.line is not None else ""
            lines.append(
                f"  {c.event.away} @ {c.event.home} | {c.kind.value} "
                f"{c.side.value}{line_txt} | best {c.quote.decimal_odds:.3f} "
                f"({c.quote.book}) | fair {c.fair_decimal:.3f} | "
                f"bet at >= {c.target_decimal:.3f} | EV now {c.ev_pct:+.2%}"
            )

    if card.arbitrages:
        lines.append("")
        lines.append("ARBITRAGE (risk-free at quoted prices):")
        for event_id, arb in card.arbitrages:
            legs = ", ".join(
                f"{q.side.value}@{q.book} {q.decimal_odds:.3f} ({s:.1%})"
                for q, s in zip(arb.quotes, arb.stakes)
            )
            lines.append(f"  {event_id}: {legs} -> +{arb.profit_margin:.2%} locked")

    if card.middles:
        lines.append("")
        lines.append("MIDDLES (+EV window plays):")
        for event_id, mid in card.middles:
            lines.append(
                f"  {event_id}: fav {mid.favourite_quote.line:+g}@{mid.favourite_quote.book}"
                f" + dog {mid.underdog_quote.line:+g}@{mid.underdog_quote.book}"
                f" | window {mid.window} p={mid.hit_probability:.2%} EV {mid.ev:+.2%}"
            )

    if card.teaser_legs:
        lines.append("")
        be = teaser_breakeven_leg_probability(1.909, 2)
        lines.append(
            f"WONG TEASER LEGS (6pt NFL, cross 3 & 7; pair legs, need >{be:.1%}/leg at -110):"
        )
        for leg in card.teaser_legs:
            lines.append(
                f"  {leg.event_id}: {leg.side.value} {leg.original_line:+g} -> "
                f"{leg.teased_line:+g} ({leg.quote.book})"
            )

    lines.append("")
    lines.append("MARKET DIAGNOSTICS:")
    for d in card.diagnostics:
        hold_txt = f"{d.synthetic_hold:+.2%}" if d.synthetic_hold is not None else "n/a"
        line_txt = f" line {d.consensus_line:+g}" if d.consensus_line is not None else ""
        fair_txt = (
            " | ".join(
                f"{s.value} {p:.4f}" for s, p in d.fair_line.probabilities.items()
            )
            if d.fair_line
            else "no sharp consensus"
        )
        lines.append(
            f"  {d.event_id}/{d.kind.value}{line_txt}: synthetic hold {hold_txt} | {fair_txt}"
        )

    for msg in card.skipped:
        lines.append(f"  SKIPPED {msg}")

    lines.append("=" * 72)
    return "\n".join(lines)
