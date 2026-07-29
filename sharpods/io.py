"""Load odds snapshots from JSON.

Format (see data/sample_odds.json):

{
  "events": [
    {
      "event_id": "nfl-2026-w1-kc-buf", "sport": "nfl",
      "home": "Bills", "away": "Chiefs",
      "markets": [
        {"kind": "moneyline",
         "quotes": [{"book": "pinnacle", "side": "home", "decimal_odds": 1.87}]},
        {"kind": "spread",
         "quotes": [{"book": "circa", "side": "home", "line": -2.5,
                     "decimal_odds": 1.909, "timestamp": 1700000000}]}
      ]
    }
  ],
  "model_probabilities": {"nfl-2026-w1-kc-buf:moneyline:home": 0.55},
  "history": {"nfl-2026-w1-kc-buf:moneyline": [
      {"book": "pinnacle", "side": "home", "decimal_odds": 1.95, "timestamp": 1699999000}
  ]}
}
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from sharpods.books_registry import BookProfile, BooksRegistry
from sharpods.datatypes import Event, MarketKind, MarketSnapshot, Quote, Side


@dataclass
class SlateData:
    snapshots: list[MarketSnapshot]
    model_probabilities: dict[tuple[str, MarketKind, Side], float] = field(
        default_factory=dict
    )
    history: dict[tuple[str, MarketKind], list[Quote]] = field(default_factory=dict)
    # Optional per-slate sharpness overrides ("books" section), so degraded
    # snapshots (article/consensus sources instead of real books) document
    # their own anchor quality and runs stay reproducible from the CLI.
    book_profiles: list[BookProfile] = field(default_factory=list)

    def registry(self) -> BooksRegistry:
        reg = BooksRegistry()
        for profile in self.book_profiles:
            reg.register(profile)
        return reg


def _parse_quote(raw: dict) -> Quote:
    return Quote(
        book=str(raw["book"]).lower(),
        side=Side(raw["side"]),
        decimal_odds=float(raw["decimal_odds"]),
        line=float(raw["line"]) if raw.get("line") is not None else None,
        timestamp=float(raw["timestamp"]) if raw.get("timestamp") is not None else None,
    )


def load_slate(path: str | Path) -> SlateData:
    data = json.loads(Path(path).read_text())

    snapshots: list[MarketSnapshot] = []
    for raw_event in data.get("events", []):
        event = Event(
            event_id=raw_event["event_id"],
            sport=raw_event.get("sport", "unknown"),
            home=raw_event["home"],
            away=raw_event["away"],
            league=raw_event.get("league"),
            start_time=raw_event.get("start_time"),
        )
        for raw_market in raw_event.get("markets", []):
            snapshots.append(
                MarketSnapshot(
                    event=event,
                    kind=MarketKind(raw_market["kind"]),
                    quotes=[_parse_quote(q) for q in raw_market.get("quotes", [])],
                )
            )

    model_probabilities: dict[tuple[str, MarketKind, Side], float] = {}
    for key, prob in data.get("model_probabilities", {}).items():
        event_id, kind, side = key.rsplit(":", 2)
        model_probabilities[(event_id, MarketKind(kind), Side(side))] = float(prob)

    history: dict[tuple[str, MarketKind], list[Quote]] = {}
    for key, quotes in data.get("history", {}).items():
        event_id, kind = key.rsplit(":", 1)
        history[(event_id, MarketKind(kind))] = [_parse_quote(q) for q in quotes]

    book_profiles = [
        BookProfile(
            name=str(name).lower(),
            sharpness=float(raw.get("sharpness", 0.2)),
            market_maker=bool(raw.get("market_maker", False)),
            notes=str(raw.get("notes", "")),
        )
        for name, raw in data.get("books", {}).items()
    ]

    return SlateData(
        snapshots=snapshots,
        model_probabilities=model_probabilities,
        history=history,
        book_profiles=book_profiles,
    )
