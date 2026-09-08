"""NFL margin model: spread <-> moneyline, and cover/push/loss pricing."""

import math

import pytest


def _cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

from sharpods.edges import NFL_MARGIN_FREQ, spread_ev
from sharpods.models.football import (
    NFL_MARGIN_SIGMA as _SIGMA,
    NFL_MARGIN_SIGMA,
    cover_probabilities,
    fair_moneyline_from_spread,
    push_probability,
    spread_from_win_probability,
    win_probability_from_spread,
)


# The calibration this module is pinned to. These are the standard book
# spread->moneyline conversions, devigged. Sigma was least-squares fitted to
# reproduce them; if a refit ever moves sigma, this table is what it must
# still satisfy.
BOOK_CONVERSION = {
    3.0: 0.5963,
    3.5: 0.6211,
    4.0: 0.6429,
    6.0: 0.6913,
    7.0: 0.7328,
    10.0: 0.8000,
    14.0: 0.8721,
}


@pytest.mark.parametrize("points,expected", sorted(BOOK_CONVERSION.items()))
def test_reproduces_book_conversion_table_within_one_point(points, expected):
    got = win_probability_from_spread(-points)
    assert abs(got - expected) < 0.011, f"-{points}: {got:.4f} vs {expected:.4f}"


def test_raw_margin_sd_would_understate_favourites():
    """The documented reason sigma is 11.8 and not the textbook 13.5: using
    the raw margin SD prices every favourite short by 2-3 points."""
    for points in (7.0, 10.0, 14.0):
        calibrated = win_probability_from_spread(-points)
        raw_sd = win_probability_from_spread(-points, sigma=13.5)
        assert calibrated - raw_sd > 0.02


def test_pickem_is_a_coin_flip():
    assert win_probability_from_spread(0.0) == pytest.approx(0.5, abs=1e-9)


def test_favourite_and_dog_probabilities_are_complementary():
    for points in (1.5, 3.0, 6.5, 10.0):
        fav = win_probability_from_spread(-points)
        dog = win_probability_from_spread(+points)
        assert fav + dog == pytest.approx(1.0, abs=1e-9)


def test_win_probability_is_monotone_in_the_spread():
    spreads = [3.0, 1.5, 0.0, -1.5, -3.0, -7.0, -14.0]
    probs = [win_probability_from_spread(s) for s in spreads]
    assert probs == sorted(probs)


def test_spread_and_win_probability_round_trip():
    for spread in (-13.5, -7.0, -3.0, -0.5, 0.0, 2.5, 6.0):
        p = win_probability_from_spread(spread)
        assert spread_from_win_probability(p) == pytest.approx(spread, abs=0.05)


def test_fair_moneyline_is_the_reciprocal_of_the_win_probability():
    for spread in (-9.5, -3.0, 4.0):
        p = win_probability_from_spread(spread)
        assert fair_moneyline_from_spread(spread) == pytest.approx(1.0 / p)


def test_push_probability_uses_the_empirical_table_not_the_normal():
    # 3 and 7 are the key numbers; the whole point is that they carry far
    # more mass than a bell curve puts there.
    assert push_probability(-3.0) == NFL_MARGIN_FREQ[3]
    assert push_probability(7.0) == NFL_MARGIN_FREQ[7]
    assert push_probability(-3.0) > 3 * push_probability(-9.0)


def test_half_points_cannot_push():
    for line in (-3.5, -7.5, 2.5, 0.5):
        assert push_probability(line) == 0.0
        _, p_push, _ = cover_probabilities(line, true_margin=3.0)
        assert p_push == 0.0


def test_cover_push_loss_always_sum_to_one():
    for line in (-14.0, -7.0, -3.5, -3.0, 0.0, 2.5, 6.0):
        for margin in (-7.0, 0.0, 3.0, 10.0):
            probs = cover_probabilities(line, margin)
            assert sum(probs) == pytest.approx(1.0, abs=1e-9)
            assert all(p >= 0.0 for p in probs)


def test_fairly_priced_whole_number_line_is_symmetric_around_the_push():
    """A -3 laid into a true 3-point edge: cover and loss must be equal, and
    the push must carry the empirical key-number mass."""
    p_cover, p_push, p_loss = cover_probabilities(-3.0, true_margin=3.0)
    assert p_cover == pytest.approx(p_loss, abs=1e-9)
    assert p_push == pytest.approx(NFL_MARGIN_FREQ[3])
    assert p_cover == pytest.approx((1.0 - NFL_MARGIN_FREQ[3]) / 2.0, abs=1e-9)


def test_fairly_priced_half_point_line_is_a_coin_flip():
    p_cover, p_push, p_loss = cover_probabilities(-3.5, true_margin=3.5)
    assert p_push == 0.0
    assert p_cover == pytest.approx(0.5, abs=1e-9)
    assert p_loss == pytest.approx(0.5, abs=1e-9)


def test_a_better_true_margin_raises_cover_probability():
    weak = cover_probabilities(-3.0, true_margin=3.0)[0]
    strong = cover_probabilities(-3.0, true_margin=6.0)[0]
    assert strong > weak


def test_push_mass_shrinks_the_edge_in_both_directions():
    """The bug this module fixes, stated correctly.

    A push is a no-action outcome, so substituting real push mass for a naive
    two-way split pulls EV *toward zero* whichever way the bet leans. Getting
    the sign of that error right matters: at a fairly-priced -3 the push
    HELPS (it refunds stake that a coin-flip model would have lost at -110),
    while on a bet with a real edge it HURTS (it strips mass off the winning
    side). Either way, pricing a key number as a two-way 50/50 is wrong.
    """
    price = 1.909  # -110

    # Fairly priced: push converts symmetric mass into refunds, and at -110 a
    # refund is worth more than the 0.909 a win pays.
    p_cover, p_push, _ = cover_probabilities(-3.0, true_margin=3.0)
    honest_fair = spread_ev(p_cover, p_push, price)
    naive_fair = spread_ev(0.5, 0.0, price)
    assert honest_fair > naive_fair
    assert honest_fair < 0 and naive_fair < 0  # both still losers at -110

    # Real edge: the same push mass now eats winning outcomes.
    p_cover_e, p_push_e, _ = cover_probabilities(-3.0, true_margin=10.0)
    honest_edge = spread_ev(p_cover_e, p_push_e, price)
    naive_cover = 1.0 - _cdf((3.0 - 10.0) / NFL_MARGIN_SIGMA)
    naive_edge = spread_ev(naive_cover, 0.0, price)
    assert honest_edge < naive_edge
    assert honest_edge > 0  # still a good bet, just less good than naive says

    # And the effect is not trivially small at a key number.
    assert abs(honest_edge - naive_edge) > 0.02


def test_spread_implied_moneyline_can_disagree_with_a_posted_moneyline():
    """The dispersion this module exists to surface: a sharp -3 spread implies
    about 1.67, so a soft book posting 1.85 on the same side is a real
    cross-market gap, not noise."""
    fair = fair_moneyline_from_spread(-3.0)
    assert fair == pytest.approx(1.666, abs=0.01)
    soft_book_price = 1.85
    edge = soft_book_price / fair - 1.0
    assert edge > 0.10


def test_sigma_is_a_keyword_so_a_refit_is_one_line():
    assert win_probability_from_spread(-7.0, sigma=13.5) != win_probability_from_spread(-7.0)
    assert NFL_MARGIN_SIGMA == pytest.approx(11.8)


def test_rejects_nonsense_inputs():
    with pytest.raises(ValueError):
        win_probability_from_spread(-3.0, sigma=0.0)
    with pytest.raises(ValueError):
        spread_from_win_probability(0.0)
    with pytest.raises(ValueError):
        spread_from_win_probability(1.0)
    with pytest.raises(ValueError):
        cover_probabilities(-3.0, 3.0, sigma=-1.0)
