"""Tests for the derivative-pricing additions from the synthesis spec:
half-point parity, parlays, hedging, promos, middles, win totals."""

import pytest

from sharpods.edges import (
    correlated_parlay_ev,
    free_bet_ev,
    half_point_parity_payout_better,
    half_point_parity_payout_worse,
    hedge_ev_cost,
    hedge_stake_for_lock,
    middle_breakeven,
    parlay_ev,
)
from sharpods.models.wintotals import (
    expected_wins,
    poisson_binomial_pmf,
    spread_to_win_probability,
    win_total_ev,
    win_total_probabilities,
)


class TestHalfPointParity:
    def test_worse_side_demands_higher_payout(self):
        # Giving up push protection on 3 (q ~ 0.10) must be compensated.
        a_prime = half_point_parity_payout_worse(0.909, p_win=0.45, p_push=0.10)
        assert a_prime == pytest.approx(0.909 + 0.10 / 0.45)
        assert a_prime > 0.909

    def test_better_side_costs_payout(self):
        a_dprime = half_point_parity_payout_better(0.909, p_win=0.45, p_push=0.10)
        assert a_dprime == pytest.approx(0.45 * 0.909 / 0.55)
        assert a_dprime < 0.909

    def test_no_push_mass_means_no_adjustment(self):
        assert half_point_parity_payout_worse(0.909, 0.5, 0.0) == pytest.approx(0.909)
        assert half_point_parity_payout_better(0.909, 0.5, 0.0) == pytest.approx(0.909)


class TestParlays:
    def test_standard_two_team_parlay_is_bad(self):
        # Coin-flip legs at the standard 2.6:1 payout (d=3.6): -10% EV.
        assert parlay_ev([0.5, 0.5], 3.6) == pytest.approx(-0.10)

    def test_ev_compounds_multiplicatively_at_fair_odds(self):
        # Legs with +10% EV each at true multiplied odds: 1.1^2 - 1.
        assert parlay_ev([0.55, 0.55], 4.0) == pytest.approx(1.1**2 - 1.0)

    def test_correlated_parlay(self):
        # Book prices legs as independent (d=3.6 for two coin flips) but the
        # true joint probability is 30%.
        assert correlated_parlay_ev(0.30, 3.6) == pytest.approx(0.08)

    def test_validation(self):
        with pytest.raises(ValueError):
            parlay_ev([], 3.6)
        with pytest.raises(ValueError):
            correlated_parlay_ev(0.30, 0.9)


class TestHedging:
    def test_lock_equalizes_profit(self):
        stake = hedge_stake_for_lock(1000.0, 1.90)
        assert stake == pytest.approx(1000.0 / 1.90)
        profit_if_ticket_hits = 1000.0 - stake
        profit_if_hedge_hits = stake * 0.90
        assert profit_if_ticket_hits == pytest.approx(profit_if_hedge_hits)

    def test_hedge_cost_is_the_vig(self):
        stake = hedge_stake_for_lock(1000.0, 1.90)
        cost = hedge_ev_cost(stake, 1.90, complement_fair_probability=0.50)
        # Hedge bet EV per unit: 0.5*1.9 - 1 = -0.05
        assert cost == pytest.approx(stake * 0.05)

    def test_plus_ev_hedge_is_a_scalp(self):
        cost = hedge_ev_cost(100.0, 2.10, complement_fair_probability=0.50)
        assert cost < 0  # negative cost: the hedge side is itself +EV


class TestPromos:
    def test_free_bet_value(self):
        # $100 free bet at 5.0 with fair p=0.19: EV = .19*4*100 = $76.
        assert free_bet_ev(100.0, 5.0, 0.19) == pytest.approx(76.0)

    def test_longshots_convert_better(self):
        short = free_bet_ev(100.0, 1.50, 2.0 / 3.0)
        long = free_bet_ev(100.0, 6.0, 1.0 / 6.0)
        assert long > short


class TestMiddleBreakeven:
    def test_wong_one_in_twentyone(self):
        # Both sides -110: risk 1.1 to win 1.
        be = middle_breakeven(1.1, 1.0, 1.1, 1.0)
        assert be == pytest.approx(0.1 / 2.1, abs=1e-9)

    def test_arb_prices_need_no_middle(self):
        # +105 both sides: any miss still profits.
        assert middle_breakeven(1.0, 1.05, 1.0, 1.05) == 0.0


class TestWinTotals:
    def test_poisson_binomial_two_coin_flips(self):
        pmf = poisson_binomial_pmf([0.5, 0.5])
        assert pmf == pytest.approx([0.25, 0.5, 0.25])

    def test_pmf_sums_to_one(self):
        pmf = poisson_binomial_pmf([0.6, 0.55, 0.45, 0.7, 0.5])
        assert sum(pmf) == pytest.approx(1.0)

    def test_expected_wins(self):
        assert expected_wins([0.6, 0.55, 0.45]) == pytest.approx(1.6)

    def test_half_line_no_push(self):
        over, push, under = win_total_probabilities([0.5, 0.5], 1.5)
        assert push == 0.0
        assert over == pytest.approx(0.25)
        assert under == pytest.approx(0.75)

    def test_integer_line_pushes(self):
        over, push, under = win_total_probabilities([0.5, 0.5], 1.0)
        assert push == pytest.approx(0.5)
        assert over == pytest.approx(0.25)
        assert under == pytest.approx(0.25)

    def test_win_total_ev(self):
        # 17 games at 60% each: expected 10.2 wins; over 9.5 should be +EV
        # at even money, under -EV.
        probs = [0.6] * 17
        ev_over, ev_under = win_total_ev(probs, 9.5, 2.0, 2.0)
        assert ev_over > 0
        assert ev_under < 0

    def test_spread_conversion(self):
        assert spread_to_win_probability(0.0) == pytest.approx(0.5)
        # A -3 favourite: Phi(3/13.5) ~ 58.8%
        p = spread_to_win_probability(-3.0, 13.5)
        assert p == pytest.approx(0.5879, abs=1e-3)
        # Symmetry
        assert spread_to_win_probability(3.0) == pytest.approx(
            1.0 - spread_to_win_probability(-3.0)
        )
