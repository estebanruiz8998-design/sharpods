"""SharpOds — a maximum-capacity sports betting model synthesizing the ten
best sports betting books ever written.

See docs/synthesis.md for the architecture and docs/books/ for the source
analyses. The short version of everything the books teach:

1. The sharp market is the best public estimate of truth — devig it.
2. Edge comes first from price (line shopping), then from information.
3. Bet value against your fair number, never "winners".
4. Kelly sizes the bet; fractional Kelly survives being wrong.
5. Closing line value — not your win rate — is the proof you have an edge.
"""

from sharpods.datatypes import (
    BetCandidate,
    BetTicket,
    Event,
    FairLine,
    MarketKind,
    MarketSnapshot,
    Quote,
    Side,
)
from sharpods.engine import BetCard, Engine, render_bet_card
from sharpods.io import SlateData, load_slate
from sharpods.portfolio import Portfolio, RiskPolicy

__version__ = "0.1.0"

__all__ = [
    "BetCandidate",
    "BetCard",
    "BetTicket",
    "Engine",
    "Event",
    "FairLine",
    "MarketKind",
    "MarketSnapshot",
    "Portfolio",
    "Quote",
    "RiskPolicy",
    "Side",
    "SlateData",
    "load_slate",
    "render_bet_card",
    "__version__",
]
