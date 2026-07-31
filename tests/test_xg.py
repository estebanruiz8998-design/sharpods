import math

import pytest

from sharpods.models.poisson import PoissonModel
from sharpods.models.xg import (
    Shot,
    blend_goals_xg,
    finishing_luck,
    goal_angle,
    overperformance_ratio,
    shot_xg,
    team_lambdas_from_xg,
    xg_from_shots,
)


class TestShotXg:
    def test_probability_bounds(self):
        assert 0.0 < shot_xg(Shot(11.0, 0.6)) < 1.0

    def test_closer_is_better(self):
        near = shot_xg(Shot(6.0, 0.8))
        far = shot_xg(Shot(25.0, 0.8))
        assert near > far

    def test_wider_angle_is_better(self):
        wide = shot_xg(Shot(11.0, 0.9))
        narrow = shot_xg(Shot(11.0, 0.2))
        assert wide > narrow

    def test_penalty_spot_is_high_value(self):
        # ~11m out, centred: angle ~0.64 rad; should be a strong chance
        # relative to a 25m screamer.
        pen = shot_xg(Shot(11.0, goal_angle(11.0, 0.0)))
        long_shot = shot_xg(Shot(25.0, goal_angle(25.0, 0.0)))
        assert pen > 3 * long_shot

    def test_invalid_geometry(self):
        with pytest.raises(ValueError):
            shot_xg(Shot(-1.0, 0.5))
        with pytest.raises(ValueError):
            shot_xg(Shot(10.0, 4.0))


class TestGoalAngle:
    def test_centred_close_is_wide(self):
        assert goal_angle(6.0, 0.0) > goal_angle(20.0, 0.0)

    def test_offset_narrows_angle(self):
        assert goal_angle(11.0, 0.0) > goal_angle(11.0, 12.0)

    def test_symmetric_in_offset(self):
        assert goal_angle(11.0, 5.0) == pytest.approx(goal_angle(11.0, -5.0))


class TestRates:
    def test_xg_from_shots_sums(self):
        shots = [Shot(11.0, 0.6), Shot(18.0, 0.4)]
        assert xg_from_shots(shots) == pytest.approx(
            shot_xg(shots[0]) + shot_xg(shots[1])
        )

    def test_blend_weights_xg_heavier_by_default(self):
        # goals 2.0/game, xG 1.4/game: estimate sits nearer xG.
        lam = blend_goals_xg(2.0, 1.4)
        assert lam == pytest.approx(0.7 * 1.4 + 0.3 * 2.0)
        assert abs(lam - 1.4) < abs(lam - 2.0)

    def test_blend_bounds(self):
        with pytest.raises(ValueError):
            blend_goals_xg(1.0, 1.0, xg_weight=1.5)
        with pytest.raises(ValueError):
            blend_goals_xg(-0.1, 1.0)

    def test_finishing_luck_sign(self):
        assert finishing_luck(60, 48.5) > 0  # overperforming: regress down
        assert finishing_luck(30, 41.0) < 0  # underperforming: regress up

    def test_overperformance_ratio(self):
        assert overperformance_ratio(60, 48.0) == pytest.approx(1.25)
        with pytest.raises(ValueError):
            overperformance_ratio(10, 0.0)


class TestMatchPipeline:
    def test_lambdas_feed_poisson(self):
        home, away = team_lambdas_from_xg(
            home_xg_rate=1.6, home_goals_rate=2.0,
            away_xg_rate=1.1, away_goals_rate=0.9,
        )
        # Home shrunk toward 1.6 then boosted; away shrunk toward 1.1.
        assert home == pytest.approx((0.7 * 1.6 + 0.3 * 2.0) * 1.1)
        assert away == pytest.approx(0.7 * 1.1 + 0.3 * 0.9)
        h, d, a = PoissonModel(home, away).outcome_probabilities()
        assert h + d + a == pytest.approx(1.0, abs=1e-9)
        assert h > a


class TestStarRating:
    def test_tiers(self):
        from sharpods.portfolio import star_rating

        assert star_rating(0.009, 0.01) == 0
        assert star_rating(0.012, 0.01) == 1
        assert star_rating(0.017, 0.01) == 2
        assert star_rating(0.025, 0.01) == 3
        assert star_rating(0.033, 0.01) == 4
        assert star_rating(0.05, 0.01) == 5

    def test_requires_positive_bar(self):
        from sharpods.portfolio import star_rating

        with pytest.raises(ValueError):
            star_rating(0.05, 0.0)

    def test_tickets_carry_stars(self):
        from sharpods.datatypes import (
            BetCandidate, Event, MarketKind, Quote, Side,
        )
        from sharpods.portfolio import Portfolio

        cand = BetCandidate(
            event=Event(event_id="e1", sport="mlb", home="H", away="A"),
            kind=MarketKind.MONEYLINE,
            side=Side.HOME,
            quote=Quote("pinnacle", Side.HOME, 2.0),
            fair_probability=0.52,
            ev_pct=0.04,
            required_ev=0.01,
        )
        tickets = Portfolio(bankroll=10_000).allocate([cand])
        assert tickets[0].stars == 5
        assert any("conviction" in r for r in tickets[0].rationale)
