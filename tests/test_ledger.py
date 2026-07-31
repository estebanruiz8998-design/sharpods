import pytest

from sharpods import ledger
from sharpods.odds import devig


class TestSettleGame:
    def test_grades_in_place(self):
        game = {"event_id": "e1", "our_home_fair": 0.55}
        ledger.settle_game(game, home_won=True, final="4-2", close_home_decimal=1.80, close_away_decimal=2.10)
        expected = devig([1.80, 2.10], "power")[0]
        assert game["close_home_novig"] == pytest.approx(expected, abs=1e-4)
        assert game["home_won"] is True
        assert game["final"] == "4-2"


class TestSlateMetrics:
    def test_known_values(self):
        games = [
            {"our_home_fair": 0.6, "close_home_novig": 0.62, "home_won": False},
            {"our_home_fair": 0.5, "close_home_novig": 0.49, "home_won": True},
        ]
        m = ledger.slate_metrics(games)
        assert m["n"] == 2
        assert m["brier_ours"] == pytest.approx((0.36 + 0.25) / 2, abs=1e-4)
        assert m["brier_close"] == pytest.approx((0.62**2 + 0.51**2) / 2, abs=1e-4)
        assert m["mean_abs_fair_vs_close"] == pytest.approx(0.015, abs=1e-4)

    def test_skips_unsettled(self):
        games = [
            {"our_home_fair": 0.6, "close_home_novig": 0.62, "home_won": False},
            {"our_home_fair": 0.5},  # not settled
        ]
        assert ledger.slate_metrics(games)["n"] == 1

    def test_empty_errors(self):
        with pytest.raises(ValueError):
            ledger.slate_metrics([{"our_home_fair": 0.5}])


class TestSettleTicket:
    def _ticket(self):
        return {"stake": 1000.0, "fill_decimal": 1.99}

    def test_win_pnl_and_clv(self):
        t = self._ticket()
        ledger.settle_ticket(t, won=True, close_side_decimal=1.90,
                             closing_market_odds=(1.90, 2.02), outcome_index=0)
        assert t["pnl"] == pytest.approx(990.0)
        assert t["clv_raw"] == pytest.approx(1.99 / 1.90 - 1.0, abs=1e-4)
        fair = devig([1.90, 2.02], "power")[0]
        assert t["clv_novig"] == pytest.approx(1.99 * fair - 1.0, abs=1e-4)
        assert t["clv"] == "settled"

    def test_loss_pnl(self):
        t = self._ticket()
        ledger.settle_ticket(t, won=False, close_side_decimal=2.05,
                             closing_market_odds=(2.05, 1.85), outcome_index=0)
        assert t["pnl"] == pytest.approx(-1000.0)
        # Beat by the close: negative raw CLV
        assert t["clv_raw"] < 0


class TestCumulative:
    def test_aggregates_slates_and_tickets(self):
        record = {
            "slates": [
                {
                    "games": [
                        {"our_home_fair": 0.6, "close_home_novig": 0.61, "home_won": True},
                        {"our_home_fair": 0.4, "close_home_novig": 0.42, "home_won": False},
                    ],
                    "live_tickets": [
                        {"stake": 100.0, "fill_decimal": 2.0, "won": True,
                         "pnl": 100.0, "clv_raw": 0.05, "clv_novig": 0.02, "clv": "settled"},
                        {"stake": 100.0, "fill_decimal": 2.0, "won": False,
                         "pnl": -100.0, "clv_raw": 0.03, "clv_novig": 0.01, "clv": "settled"},
                    ],
                },
            ]
        }
        out = ledger.cumulative(record)
        assert out["calibration"]["n"] == 2
        assert out["tickets"]["n"] == 2
        assert out["tickets"]["pnl"] == pytest.approx(0.0)
        assert out["tickets"]["record"] == "1-1"
        assert out["tickets"]["mean_clv_raw"] == pytest.approx(0.04)
        assert "verdict" in out["tickets"]

    def test_pending_tickets_excluded(self):
        record = {
            "slates": [
                {"games": [], "live_tickets": [
                    {"stake": 100.0, "fill_decimal": 2.0, "clv": "pending close"}
                ]},
            ]
        }
        out = ledger.cumulative(record)
        assert "tickets" not in out

    def test_round_trip_io(self, tmp_path):
        path = tmp_path / "rec.json"
        ledger.save_record(path, {"slates": []})
        assert ledger.load_record(path) == {"slates": []}
