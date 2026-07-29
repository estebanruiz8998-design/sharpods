"""Edge detection: where the +EV actually comes from.

This module operationalizes the price-side edges the books describe:

- Line shopping / best price (The Logic of Sports Betting: the cheapest,
  most reliable edge available to anyone).
- Expected value against the consensus fair line (Fixed Odds Sports Betting:
  bet value, not winners).
- Key numbers and half-point values (Sharp Sports Betting: NFL margins mass
  on 3 and 7; a half point is worth its landing frequency, not a flat price).
- Wong teasers (Sharp Sports Betting: 6-point NFL teaser legs that cross
  both 3 and 7 win often enough to beat standard teaser pricing).
- Arbitrage and synthetic hold (The Logic of Sports Betting; Weighing the
  Odds: the best two sides across books sometimes guarantee profit).
- Middles (Weighing the Odds: buy both sides at different numbers; the
  gap landing wins both bets, the cost is the synthetic hold).
- Steam (Sharper: sharp-originated moves carry information; a stale retail
  price after a market-maker move is a bettable lag).
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field

from sharpods.books_registry import BooksRegistry, DEFAULT_REGISTRY
from sharpods.datatypes import MarketSnapshot, Quote, Side

# ---------------------------------------------------------------------------
# Expected value & line shopping
# ---------------------------------------------------------------------------


def expected_value(probability: float, decimal_odds: float) -> float:
    """EV per unit staked: p * d - 1. Positive means +EV."""
    if not 0.0 < probability < 1.0:
        raise ValueError(f"probability out of range: {probability}")
    if decimal_odds <= 1.0:
        raise ValueError(f"decimal odds must exceed 1.0: {decimal_odds}")
    return probability * decimal_odds - 1.0


def best_quote(
    snapshot: MarketSnapshot, side: Side, line: float | None = None
) -> Quote | None:
    """Highest decimal price for a side (at a specific line for spread/total).

    This IS line shopping. Miller & Davidow: over thousands of bets the
    difference between the best and an average price exceeds most models'
    entire edge.
    """
    quotes = snapshot.quotes_for(side, line)
    if not quotes:
        return None
    return max(quotes, key=lambda q: q.decimal_odds)


# ---------------------------------------------------------------------------
# Key numbers and half-point values (NFL)
# ---------------------------------------------------------------------------

# Approximate historical landing frequencies of NFL final-score margins
# (absolute value). Wong's push charts, refreshed by public post-2015 data;
# treat as priors, not constants — scoring-rule changes move them.
NFL_MARGIN_FREQ: dict[int, float] = {
    1: 0.035,
    2: 0.040,
    3: 0.098,
    4: 0.045,
    5: 0.035,
    6: 0.048,
    7: 0.084,
    8: 0.038,
    9: 0.020,
    10: 0.055,
    11: 0.026,
    13: 0.030,
    14: 0.045,
    17: 0.037,
}

KEY_NUMBERS_NFL = (3, 7)


def spread_ev(
    p_cover: float, p_push: float, decimal_odds: float
) -> float:
    """EV of a spread bet with an explicit push probability.

    EV = p_cover*(d-1) - p_loss, where p_loss = 1 - p_cover - p_push and a
    push refunds the stake (profit 0).
    """
    if p_cover < 0 or p_push < 0 or p_cover + p_push > 1.0:
        raise ValueError("invalid cover/push probabilities")
    if decimal_odds <= 1.0:
        raise ValueError("decimal odds must exceed 1.0")
    p_loss = 1.0 - p_cover - p_push
    return p_cover * (decimal_odds - 1.0) - p_loss


def half_point_ev_gain(
    line_from: float,
    line_to: float,
    decimal_odds: float,
    margin_freqs: Mapping[int, float] = NFL_MARGIN_FREQ,
) -> float:
    """EV gained by moving a favourite's spread half a point in its favour
    (e.g. -3.0 -> -2.5, or -3.5 -> -3.0), holding price constant.

    Crossing off an integer margin m:
    - from -m to -(m - 0.5): former pushes at m become wins -> +freq(m)*(d-1)
    - from -(m + 0.5) to -m: former losses at m become pushes -> +freq(m)*1

    Wong's rule follows: a half point is worth the landing frequency of the
    number it crosses — pay for it off 3 and 7, decline it off dead numbers.
    Dog moves are symmetric (call with the dog's line signs flipped).
    """
    if abs(abs(line_from) - abs(line_to)) != 0.5:
        raise ValueError("lines must differ by exactly half a point")
    if abs(line_to) >= abs(line_from):
        raise ValueError("line_to must be the improved (smaller magnitude) line")
    if decimal_odds <= 1.0:
        raise ValueError("decimal odds must exceed 1.0")

    lo, hi = abs(line_to), abs(line_from)
    # The integer being crossed is whichever of lo/hi is whole.
    if lo == int(lo):
        crossed = int(lo)  # e.g. 3.5 -> 3.0 : losses at 3 become pushes
        gain_per_freq = 1.0
    else:
        crossed = int(hi)  # e.g. 3.0 -> 2.5 : pushes at 3 become wins
        gain_per_freq = decimal_odds - 1.0
    freq = margin_freqs.get(crossed, 0.0)
    return freq * gain_per_freq


def half_point_parity_payout_worse(
    net_payout: float, p_win: float, p_push: float
) -> float:
    """Wong's parity price for taking the WORSE side of a half point.

    Moving a dog from +N to +(N-0.5) turns pushes at N into losses; the payout
    that leaves EV unchanged is a' = a + q/w (a = current net payout, w =
    P(win), q = P(push)). Accept the worse number only if paid more than a'.
    """
    if net_payout <= 0 or not 0.0 < p_win < 1.0 or p_push < 0:
        raise ValueError("invalid parity inputs")
    return net_payout + p_push / p_win


def half_point_parity_payout_better(
    net_payout: float, p_win: float, p_push: float
) -> float:
    """Wong's parity price for buying the BETTER side of a half point.

    Moving from +N to +(N+0.5) turns pushes at N into wins; the payout that
    leaves EV unchanged is a'' = w*a/(w+q). Buy the half point only if the
    book charges less than the drop from a to a''.
    """
    if net_payout <= 0 or not 0.0 < p_win < 1.0 or p_push < 0:
        raise ValueError("invalid parity inputs")
    return p_win * net_payout / (p_win + p_push)


# ---------------------------------------------------------------------------
# Parlays (Wong; Weighing the Odds)
# ---------------------------------------------------------------------------


def parlay_ev(leg_probabilities: Sequence[float], decimal_payout: float) -> float:
    """EV of a parlay with independent legs: prod(p_i) * d - 1.

    Wong's result: at true multiplied odds, 1+EV of the parlay is the product
    of the legs' 1+EV — parlays compound edge when legs are +EV and compound
    the vig when they are not. Standard fixed payout charts are -EV for fair
    legs; the engine only emits parlays of individually +EV legs.
    """
    if not leg_probabilities:
        raise ValueError("need at least one leg")
    if decimal_payout <= 1.0:
        raise ValueError("decimal payout must exceed 1.0")
    p_all = 1.0
    for p in leg_probabilities:
        if not 0.0 < p < 1.0:
            raise ValueError(f"leg probability out of range: {p}")
        p_all *= p
    return p_all * decimal_payout - 1.0


def correlated_parlay_ev(joint_probability: float, decimal_payout: float) -> float:
    """EV of a parlay priced by the book as independent when the legs are
    correlated (Yao): bet iff P(A and B) > 1/d. The joint probability must
    come from a joint model (e.g. simulated game scripts), not marginals.
    """
    if not 0.0 < joint_probability < 1.0:
        raise ValueError("joint probability out of range")
    if decimal_payout <= 1.0:
        raise ValueError("decimal payout must exceed 1.0")
    return joint_probability * decimal_payout - 1.0


# ---------------------------------------------------------------------------
# Hedging (Wong; Weighing the Odds)
# ---------------------------------------------------------------------------


def hedge_stake_for_lock(ticket_payout: float, hedge_decimal_odds: float) -> float:
    """Stake on the complement that equalizes profit either way.

    Holding a ticket paying X if the outcome hits, staking h = X / d_h on the
    complement guarantees X - h regardless of result.
    """
    if ticket_payout <= 0 or hedge_decimal_odds <= 1.0:
        raise ValueError("invalid hedge inputs")
    return ticket_payout / hedge_decimal_odds


def hedge_ev_cost(
    hedge_stake: float, hedge_decimal_odds: float, complement_fair_probability: float
) -> float:
    """EV given up by hedging: -stake * EV_of_hedge_bet.

    A hedge is itself a bet; its EV per unit is q*d_h - 1 (usually negative —
    you pay the vig for insurance). Wong and Yao: hedge for bankroll/utility
    reasons only, unless the hedge side is independently +EV (a scalp), in
    which case this function returns a negative cost.
    """
    if hedge_stake < 0:
        raise ValueError("hedge stake must be non-negative")
    if not 0.0 < complement_fair_probability < 1.0:
        raise ValueError("probability out of range")
    if hedge_decimal_odds <= 1.0:
        raise ValueError("invalid hedge odds")
    per_unit_ev = complement_fair_probability * hedge_decimal_odds - 1.0
    return -hedge_stake * per_unit_ev


# ---------------------------------------------------------------------------
# Promos (The Logic of Sports Betting)
# ---------------------------------------------------------------------------


def free_bet_ev(stake: float, decimal_odds: float, fair_probability: float) -> float:
    """Expected cash value of a free bet (stake not returned on a win):
    EV = p * (d - 1) * S. Conversion is maximized on long odds in low-hold
    markets, where (d-1)/d approaches 1 — typically ~70%+ of face value.
    """
    if stake <= 0:
        raise ValueError("stake must be positive")
    if decimal_odds <= 1.0:
        raise ValueError("decimal odds must exceed 1.0")
    if not 0.0 < fair_probability < 1.0:
        raise ValueError("probability out of range")
    return fair_probability * (decimal_odds - 1.0) * stake


# ---------------------------------------------------------------------------
# Wong teasers
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TeaserLeg:
    event_id: str
    side: Side
    original_line: float
    teased_line: float
    quote: Quote


def is_wong_leg(side: Side, line: float, teaser_points: float = 6.0) -> bool:
    """Wong's qualification for a 6-point NFL teaser leg: the tease must move
    the number through BOTH 3 and 7.

    Favourites -7.5 to -8.5 tease to -1.5/-2.5; underdogs +1.5 to +2.5 tease
    to +7.5/+8.5. Anything else crosses at most one key number and does not
    clear standard teaser pricing.
    """
    if teaser_points != 6.0:
        return False
    if side in (Side.HOME, Side.AWAY):
        if line <= 0:  # favourite laying points
            return -8.5 <= line <= -7.5
        return 1.5 <= line <= 2.5  # underdog taking points
    return False


def find_wong_teaser_legs(
    spread_snapshots: Sequence[MarketSnapshot], teaser_points: float = 6.0
) -> list[TeaserLeg]:
    """Scan spread markets for Wong-qualifying teaser legs at each side's
    best available number."""
    legs: list[TeaserLeg] = []
    for snap in spread_snapshots:
        for quote in snap.quotes:
            if quote.line is None:
                continue
            if is_wong_leg(quote.side, quote.line, teaser_points):
                teased = quote.line + teaser_points
                legs.append(
                    TeaserLeg(
                        event_id=snap.event.event_id,
                        side=quote.side,
                        original_line=quote.line,
                        teased_line=teased,
                        quote=quote,
                    )
                )
    return legs


def teaser_breakeven_leg_probability(decimal_odds: float, n_legs: int = 2) -> float:
    """Per-leg win probability needed to break even on an n-leg teaser paying
    ``decimal_odds`` (all legs must win): p = (1/d)^(1/n).

    At the standard two-leg -110 (d=1.909): 72.37%. Wong's data put qualifying
    legs at ~75%, hence the edge.
    """
    if decimal_odds <= 1.0 or n_legs < 1:
        raise ValueError("invalid teaser terms")
    return (1.0 / decimal_odds) ** (1.0 / n_legs)


def teaser_ev(leg_probabilities: Sequence[float], decimal_odds: float) -> float:
    """EV of a teaser whose legs win independently with the given
    probabilities (independence is the standard assumption for legs from
    different games)."""
    if not leg_probabilities:
        raise ValueError("need at least one leg")
    p_all = 1.0
    for p in leg_probabilities:
        if not 0.0 < p < 1.0:
            raise ValueError(f"leg probability out of range: {p}")
        p_all *= p
    return p_all * decimal_odds - 1.0


# ---------------------------------------------------------------------------
# Arbitrage & middles
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Arbitrage:
    quotes: tuple[Quote, ...]
    profit_margin: float  # guaranteed profit per unit of total stake
    stakes: tuple[float, ...]  # fraction of total outlay per leg


def find_arbitrage(
    snapshot: MarketSnapshot, line: float | None = None
) -> Arbitrage | None:
    """Check whether the best price on every side sums to a sub-1.0 book.

    Stakes are proportional to implied probabilities, equalizing payout:
    stake_i = (1/d_i) / sum(1/d_j); guaranteed profit = 1/sum(1/d_j) - 1.
    """
    sides = snapshot.sides()
    if len(sides) < 2:
        return None
    best: list[Quote] = []
    for side in sides:
        q = best_quote(snapshot, side, line)
        if q is None:
            return None
        best.append(q)
    inverse_sum = sum(1.0 / q.decimal_odds for q in best)
    if inverse_sum >= 1.0:
        return None
    stakes = tuple((1.0 / q.decimal_odds) / inverse_sum for q in best)
    return Arbitrage(
        quotes=tuple(best),
        profit_margin=1.0 / inverse_sum - 1.0,
        stakes=stakes,
    )


def middle_breakeven(
    risk_a: float, win_a: float, risk_b: float, win_b: float
) -> float:
    """Hit probability needed for a middle to break even (Wong, generalized).

    Missing the window loses one side and wins the other: net = win - risk of
    the two legs. Hitting wins both. At -110/-110 (risk 1.1 to win 1 each):
    miss costs 0.1, hit wins 2 -> breakeven = 0.1/2.1 ~= 4.76% (1 in 21).
    """
    if min(risk_a, win_a, risk_b, win_b) <= 0:
        raise ValueError("stakes and wins must be positive")
    miss_cost_a = risk_a - win_b  # side B wins, side A loses
    miss_cost_b = risk_b - win_a  # side A wins, side B loses
    avg_miss_cost = (miss_cost_a + miss_cost_b) / 2.0
    hit_gain = win_a + win_b
    if avg_miss_cost <= 0:
        return 0.0  # the two prices arb: every miss still profits
    return avg_miss_cost / (hit_gain + avg_miss_cost)


@dataclass(frozen=True)
class Middle:
    favourite_quote: Quote
    underdog_quote: Quote
    window: tuple[int, ...]  # integer margins that win BOTH bets
    hit_probability: float
    ev: float  # per unit staked on each side (2 units total)


def find_middles(
    snapshot: MarketSnapshot,
    margin_freqs: Mapping[int, float] = NFL_MARGIN_FREQ,
) -> list[Middle]:
    """Find spread middles: favourite at -a and underdog at +b with b > a.

    Margins strictly between a and b win both; landing exactly on a half
    boundary (integer a or b) wins one and pushes the other, treated here as
    EV-neutral relative to the loss case only via the window mass. EV per 2
    units staked ~= p_middle * 2 * (d-1) - (1 - p_middle) * synthetic_cost,
    computed exactly below assuming equal unit stakes at each price.
    """
    fav_quotes = [q for q in snapshot.quotes if q.line is not None and q.line < 0]
    dog_quotes = [q for q in snapshot.quotes if q.line is not None and q.line > 0]
    middles: list[Middle] = []
    for fav in fav_quotes:
        for dog in dog_quotes:
            if fav.side == dog.side:
                continue
            a, b = -fav.line, dog.line  # type: ignore[operator]
            if b <= a:
                continue
            window = tuple(
                m for m in range(int(a) + 1, int(b) + (0 if b == int(b) else 1))
                if a < m < b
            )
            p_mid = sum(margin_freqs.get(m, 0.0) for m in window)
            # Outside the window one bet wins, one loses (ignoring pushes on
            # boundary integers for the conservative estimate).
            d_f, d_d = fav.decimal_odds, dog.decimal_odds
            ev_both = p_mid * ((d_f - 1.0) + (d_d - 1.0))
            ev_split = (1.0 - p_mid) * (
                0.5 * ((d_f - 1.0) - 1.0) + 0.5 * ((d_d - 1.0) - 1.0)
            )
            ev = ev_both + ev_split
            if window:
                middles.append(
                    Middle(
                        favourite_quote=fav,
                        underdog_quote=dog,
                        window=window,
                        hit_probability=p_mid,
                        ev=ev,
                    )
                )
    return sorted(middles, key=lambda m: m.ev, reverse=True)


# ---------------------------------------------------------------------------
# Steam
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SteamSignal:
    book: str
    side: Side
    implied_move: float  # change in implied probability at the moving book
    window_seconds: float
    stale_quotes: tuple[Quote, ...] = field(default=())


def detect_steam(
    history: Sequence[Quote],
    current_snapshot: MarketSnapshot | None = None,
    registry: BooksRegistry = DEFAULT_REGISTRY,
    min_move: float = 0.02,
    window_seconds: float = 300.0,
    min_sharpness: float = 0.8,
) -> list[SteamSignal]:
    """Detect sharp-originated line moves and (optionally) the stale retail
    prices left behind.

    A steam signal fires when a market-maker-grade book's implied probability
    on one side rises by >= ``min_move`` within ``window_seconds``. Sharper's
    warning is encoded in the consumer, not here: chasing steam at the moved
    price is -EV; the play is the *stale* quote at a lagging book, which we
    attach when a current snapshot is provided.
    """
    signals: list[SteamSignal] = []
    by_book_side: dict[tuple[str, Side], list[Quote]] = {}
    for q in history:
        if q.timestamp is None:
            continue
        by_book_side.setdefault((q.book, q.side), []).append(q)

    for (book, side), quotes in by_book_side.items():
        if registry.sharpness(book) < min_sharpness:
            continue
        quotes = sorted(quotes, key=lambda q: q.timestamp)  # type: ignore[arg-type]
        for older in quotes:
            newest = quotes[-1]
            dt = newest.timestamp - older.timestamp  # type: ignore[operator]
            if dt <= 0 or dt > window_seconds:
                continue
            move = (1.0 / newest.decimal_odds) - (1.0 / older.decimal_odds)
            if move >= min_move:
                stale: tuple[Quote, ...] = ()
                if current_snapshot is not None:
                    fresh_implied = 1.0 / newest.decimal_odds
                    stale = tuple(
                        q
                        for q in current_snapshot.quotes_for(side)
                        if q.book != book
                        and (1.0 / q.decimal_odds) <= fresh_implied - min_move
                    )
                signals.append(
                    SteamSignal(
                        book=book,
                        side=side,
                        implied_move=move,
                        window_seconds=dt,
                        stale_quotes=stale,
                    )
                )
                break
    return signals
