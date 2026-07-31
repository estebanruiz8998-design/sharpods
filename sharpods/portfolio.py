"""Portfolio and exposure discipline — the fund-management layer.

Peta (Trading Bases) ran his betting like a long/short fund; Walters
(Gambler) ran the most successful betting operation on record on the same
skeleton: many small diversified positions, hard caps that no conviction
level overrides (Walters' ceiling was ~3% of bankroll at maximum
conviction; ours is stricter), and a method that changes only on ledger
evidence, never after a bad weekend. Kelly (Fortune's Formula) sizes
individual bets; this module bounds the *joint* exposure:

- per-bet cap (model overconfidence guard; Walters' conviction ceiling),
- per-event cap (same-game bets are correlated: a spread and a moneyline on
  the same team are nearly the same bet),
- per-slate cap (simultaneous bets share one bankroll — Thorp's scaling),
- minimum edge threshold (transaction-cost and estimation-noise floor).

Walters' star system survives as ``star_rating``: a 1-5 conviction tier
from how far the edge clears its required bar — communication and audit
trail, not sizing, because Kelly already scales stake with edge.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from sharpods.datatypes import BetCandidate, BetTicket
from sharpods.kelly import expected_log_growth, kelly_fraction


def star_rating(ev: float, required_ev: float) -> int:
    """Walters-style conviction tier: how many times the edge clears the
    required EV bar. 0 stars = below the bar (no bet); 5 = 4x the bar or
    better. Monotone in edge quality, capped so no rating can talk the
    portfolio past its exposure limits."""
    if required_ev <= 0:
        raise ValueError("required_ev must be positive")
    if ev < required_ev:
        return 0
    ratio = ev / required_ev
    if ratio >= 4.0:
        return 5
    if ratio >= 3.0:
        return 4
    if ratio >= 2.0:
        return 3
    if ratio >= 1.5:
        return 2
    return 1


@dataclass
class RiskPolicy:
    kelly_multiplier: float = 0.25
    max_bet_fraction: float = 0.02
    max_event_fraction: float = 0.03
    max_slate_fraction: float = 0.20
    min_ev: float = 0.01  # ignore edges under 1%: inside estimation noise

    def __post_init__(self) -> None:
        if not 0.0 < self.kelly_multiplier <= 1.0:
            raise ValueError("kelly_multiplier must be in (0, 1]")
        for name in ("max_bet_fraction", "max_event_fraction", "max_slate_fraction"):
            v = getattr(self, name)
            if not 0.0 < v <= 1.0:
                raise ValueError(f"{name} must be in (0, 1]")


@dataclass
class Portfolio:
    bankroll: float
    policy: RiskPolicy = field(default_factory=RiskPolicy)

    def allocate(self, candidates: list[BetCandidate]) -> list[BetTicket]:
        """Turn ranked candidates into staked tickets under all caps.

        Candidates are processed best-EV first; later (weaker) bets get
        whatever room the caps have left. This greedy order matches the
        books' guidance: when bankroll constraints bind, keep the biggest
        edges at full size rather than shaving everything equally.
        """
        if self.bankroll <= 0:
            raise ValueError("bankroll must be positive")
        tickets: list[BetTicket] = []
        event_exposure: dict[str, float] = {}
        slate_exposure = 0.0

        for cand in sorted(candidates, key=lambda c: c.ev_pct, reverse=True):
            # A candidate may demand more than the policy floor (degraded
            # fair-line anchor); the stricter bar wins.
            if cand.ev_pct < max(self.policy.min_ev, cand.required_ev):
                continue
            full = kelly_fraction(cand.fair_probability, cand.quote.decimal_odds)
            frac = full * self.policy.kelly_multiplier
            frac = min(frac, self.policy.max_bet_fraction)

            eid = cand.event.event_id
            event_room = self.policy.max_event_fraction - event_exposure.get(eid, 0.0)
            slate_room = self.policy.max_slate_fraction - slate_exposure
            frac = min(frac, max(0.0, event_room), max(0.0, slate_room))
            if frac <= 0.0:
                continue

            rationale = list(cand.tags)
            if frac < full * self.policy.kelly_multiplier:
                rationale.append("stake reduced by exposure caps")
            required = max(self.policy.min_ev, cand.required_ev)
            stars = star_rating(cand.ev_pct, required)
            rationale.append(
                f"conviction {'★' * stars} ({cand.ev_pct / required:.1f}x the EV bar)"
            )

            tickets.append(
                BetTicket(
                    candidate=cand,
                    stake_fraction=frac,
                    stake_amount=round(self.bankroll * frac, 2),
                    kelly_multiplier=self.policy.kelly_multiplier,
                    rationale=rationale,
                    stars=stars,
                )
            )
            event_exposure[eid] = event_exposure.get(eid, 0.0) + frac
            slate_exposure += frac

        # Final card order: expected log-growth contribution at the allocated
        # stake, not raw EV — at equal EV, variance drag favours the shorter
        # price (Fortune's Formula; the synthesis' ranking rule).
        tickets.sort(
            key=lambda t: expected_log_growth(
                t.candidate.fair_probability,
                t.candidate.quote.decimal_odds,
                t.stake_fraction,
            ),
            reverse=True,
        )
        return tickets
