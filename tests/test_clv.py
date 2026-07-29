import pytest

from sharpods.clv import ClvLedger, ClvRecord


class TestClvRecord:
    def test_beat_the_close(self):
        r = ClvRecord(bet_decimal_odds=2.10, closing_decimal_odds=2.00)
        assert r.clv_pct() == pytest.approx(0.05)

    def test_lost_to_the_close(self):
        r = ClvRecord(bet_decimal_odds=1.90, closing_decimal_odds=2.00)
        assert r.clv_pct() == pytest.approx(-0.05)

    def test_no_vig_clv(self):
        # Bet home at 2.05; market closed 1.87/2.05 -> fair home prob ~< .5228
        r = ClvRecord(
            bet_decimal_odds=2.10,
            closing_decimal_odds=2.05,
            closing_market_odds=(2.05, 1.87),
            outcome_index=0,
        )
        # EV under devigged close: 2.10 * fair_p - 1
        assert r.no_vig_clv_pct() == pytest.approx(2.10 * _fair_first((2.05, 1.87)) - 1)

    def test_no_vig_requires_full_market(self):
        r = ClvRecord(2.0, 1.9)
        with pytest.raises(ValueError):
            r.no_vig_clv_pct()


def _fair_first(market):
    from sharpods.odds import devig

    return devig(list(market), "power")[0]


class TestLedger:
    def test_mean_and_rate(self):
        ledger = ClvLedger(
            [
                ClvRecord(2.10, 2.00),
                ClvRecord(1.95, 2.00),
                ClvRecord(2.06, 2.00),
            ]
        )
        assert ledger.beat_close_rate() == pytest.approx(2 / 3)
        assert ledger.mean_clv(no_vig=False) == pytest.approx(
            (0.05 - 0.025 + 0.03) / 3
        )

    def test_insufficient_sample_verdict(self):
        ledger = ClvLedger([ClvRecord(2.10, 2.00)] * 5)
        assert "insufficient sample" in ledger.verdict()

    def test_edge_confirmed_verdict(self):
        # 40 records, consistently positive with slight variation
        records = [
            ClvRecord(2.00 + 0.02 + (i % 5) * 0.005, 2.00) for i in range(40)
        ]
        ledger = ClvLedger(records)
        assert "edge confirmed" in ledger.verdict()

    def test_no_edge_verdict(self):
        records = [ClvRecord(2.00 - 0.04 + (i % 5) * 0.005, 2.00) for i in range(40)]
        ledger = ClvLedger(records)
        assert "no edge" in ledger.verdict()

    def test_t_statistic_positive(self):
        records = [ClvRecord(2.05 + (i % 3) * 0.01, 2.00) for i in range(30)]
        assert ClvLedger(records).t_statistic(no_vig=False) > 2.0

    def test_empty_ledger_errors(self):
        with pytest.raises(ValueError):
            ClvLedger([]).mean_clv()
