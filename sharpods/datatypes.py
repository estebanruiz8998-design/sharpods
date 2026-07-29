"""Core data structures shared across the SharpOds pipeline.

Terminology follows the books:

- A *market* is a single two-or-more-way proposition (moneyline, spread at a
  given number, total at a given number).
- A *quote* is one sportsbook's price on one side of a market at a moment in
  time.
- A *snapshot* is the full set of quotes across books for one market, which is
  what the fair-line builder consumes.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field


class MarketKind(str, enum.Enum):
    MONEYLINE = "moneyline"
    SPREAD = "spread"
    TOTAL = "total"


class Side(str, enum.Enum):
    HOME = "home"
    AWAY = "away"
    DRAW = "draw"
    OVER = "over"
    UNDER = "under"


@dataclass(frozen=True)
class Quote:
    """One book's decimal price on one side of a market."""

    book: str
    side: Side
    decimal_odds: float
    # Spread/total line the price applies to (e.g. -3.5, 44.5); None for moneylines.
    line: float | None = None
    timestamp: float | None = None

    def __post_init__(self) -> None:
        if self.decimal_odds <= 1.0:
            raise ValueError(f"decimal odds must exceed 1.0, got {self.decimal_odds}")


@dataclass(frozen=True)
class Event:
    event_id: str
    sport: str
    home: str
    away: str
    league: str | None = None
    start_time: str | None = None


@dataclass
class MarketSnapshot:
    """All current quotes for one market of one event."""

    event: Event
    kind: MarketKind
    quotes: list[Quote] = field(default_factory=list)

    def sides(self) -> list[Side]:
        seen: list[Side] = []
        for q in self.quotes:
            if q.side not in seen:
                seen.append(q.side)
        return seen

    def quotes_for(self, side: Side, line: float | None = None) -> list[Quote]:
        """Quotes for one side, optionally pinned to a line.

        Spread lines are stored from the bet side's perspective (home -3,
        away +3 are the same market number), so spread matching compares
        absolute values. Totals match the line exactly.
        """
        result: list[Quote] = []
        for q in self.quotes:
            if q.side != side:
                continue
            if line is None:
                result.append(q)
                continue
            if q.line is None:
                continue
            if q.line == line or (
                self.kind == MarketKind.SPREAD and abs(q.line) == abs(line)
            ):
                result.append(q)
        return result

    def books(self) -> list[str]:
        seen: list[str] = []
        for q in self.quotes:
            if q.book not in seen:
                seen.append(q.book)
        return seen


@dataclass
class FairLine:
    """Consensus no-vig probabilities for a market, per side."""

    probabilities: dict[Side, float]
    # Diagnostic: which books/weights the consensus was built from.
    sources: dict[str, float] = field(default_factory=dict)
    method: str = "weighted-logit"

    def fair_decimal(self, side: Side) -> float:
        p = self.probabilities[side]
        if not 0.0 < p < 1.0:
            raise ValueError(f"fair probability out of range: {p}")
        return 1.0 / p


@dataclass
class BetCandidate:
    """A priced opportunity: one side of one market at the best available quote."""

    event: Event
    kind: MarketKind
    side: Side
    quote: Quote
    fair_probability: float
    ev_pct: float  # expected value per unit staked, as a fraction (0.05 = +5%)
    tags: list[str] = field(default_factory=list)

    @property
    def fair_decimal(self) -> float:
        return 1.0 / self.fair_probability


@dataclass
class BetTicket:
    """A staked recommendation ready for the bet card."""

    candidate: BetCandidate
    stake_fraction: float  # fraction of bankroll
    stake_amount: float
    kelly_multiplier: float
    rationale: list[str] = field(default_factory=list)
