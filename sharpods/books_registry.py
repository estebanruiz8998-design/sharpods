"""Sportsbook sharpness registry.

Sharper (Pokerjoe) and The Logic of Sports Betting divide the market into
market-making books — which originate prices, take sharp action, and run thin
margins — and retail books, which copy the market makers, shade prices toward
public demand, and limit winners. The fair-line builder weights each book's
devigged price by its sharpness: the devigged price of a market maker at high
limits is the best available estimate of true probability; a retail book's
price mostly adds noise (but its *availability* is where the +EV bet is
actually placed).

Weights are relative, not calibrated probabilities of correctness; they were
chosen to reflect the consensus ordering in the books and public CLV studies
(Pinnacle/Circa as benchmarks). Override per deployment via ``register``.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BookProfile:
    name: str
    sharpness: float  # relative weight in the consensus fair line, [0, 1]
    market_maker: bool
    notes: str = ""


_DEFAULT_BOOKS: dict[str, BookProfile] = {
    "pinnacle": BookProfile(
        "pinnacle", 1.00, True, "Archetypal market maker; welcomes winners; ~2% ML margin."
    ),
    "circa": BookProfile(
        "circa", 0.95, True, "Vegas market maker; originates NFL lines; high limits."
    ),
    "bookmaker": BookProfile(
        "bookmaker", 0.85, True, "Offshore market maker; early lines."
    ),
    "betcris": BookProfile("betcris", 0.80, True, "Sharp offshore consensus book."),
    "bet365": BookProfile("bet365", 0.55, False, "Huge retail book; fast copier."),
    "draftkings": BookProfile("draftkings", 0.40, False, "US retail; shades to public sides."),
    "fanduel": BookProfile("fanduel", 0.40, False, "US retail; shades to public sides."),
    "betmgm": BookProfile("betmgm", 0.35, False, "US retail."),
    "caesars": BookProfile("caesars", 0.35, False, "US retail."),
    "barstool": BookProfile("barstool", 0.25, False, "Recreational-focused retail."),
}


class BooksRegistry:
    def __init__(self, profiles: dict[str, BookProfile] | None = None) -> None:
        self._profiles = dict(_DEFAULT_BOOKS if profiles is None else profiles)

    def register(self, profile: BookProfile) -> None:
        self._profiles[profile.name.lower()] = profile

    def profile(self, book: str) -> BookProfile:
        key = book.lower()
        if key in self._profiles:
            return self._profiles[key]
        # Unknown books get a conservative retail weight rather than an error:
        # snapshots routinely contain books we have no dossier on, and their
        # prices are still shoppable even if untrusted for consensus.
        return BookProfile(name=key, sharpness=0.20, market_maker=False, notes="unknown book")

    def sharpness(self, book: str) -> float:
        return self.profile(book).sharpness

    def market_makers(self) -> list[str]:
        return [p.name for p in self._profiles.values() if p.market_maker]


DEFAULT_REGISTRY = BooksRegistry()
