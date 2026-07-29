# SharpOds

**A maximum-capacity sports betting model built from the ten best sports betting books ever written.**

SharpOds synthesizes the collected wisdom of the sharp betting canon into one
engine: it ingests a multi-book odds snapshot, constructs a no-vig consensus
fair line from the sharpest books, blends in fundamental model probabilities,
scans every market for price edges — +EV bets, arbitrage, middles, Wong
teasers, steam-stale prices — sizes each play with fractional Kelly under
portfolio caps, and ships a ranked bet card.

## The Ten Books

Each book was analyzed in depth (see [`docs/books/`](docs/books/)) and mapped
into the engine (see [`docs/synthesis.md`](docs/synthesis.md)):

| # | Book | Author | What the model takes |
|---|------|--------|----------------------|
| 1 | *Sharp Sports Betting* | Stanford Wong | Vig math, key numbers, half-point values, Wong teasers |
| 2 | *The Logic of Sports Betting* | Ed Miller & Matthew Davidow | Market-maker vs retail books, line shopping, synthetic hold, devigging |
| 3 | *Weighing the Odds in Sports Betting* | King Yao | Market-based handicapping, hedging, middling, derivative pricing |
| 4 | *Fixed Odds Sports Betting* | Joseph Buchdahl | Value betting, rating systems, staking-plan analysis, significance testing |
| 5 | *Squares & Sharps, Suckers & Sharks* | Joseph Buchdahl | Market efficiency, closing line value as proof of edge, bettor biases |
| 6 | *Trading Bases* | Joe Peta | Cluster luck, Pythagorean projection, portfolio risk discipline |
| 7 | *Statistical Sports Models in Excel* | Andrew Mack | Poisson/Dixon-Coles models, Monte Carlo, backtesting hygiene |
| 8 | *Sharper: A Guide to Modern Sports Betting* | True Pokerjoe | Top-down betting, steam interpretation, CLV as the metric |
| 9 | *Mathletics* | Wayne L. Winston | Pythagorean exponents, power ratings, Elo, win-probability math |
| 10 | *Fortune's Formula* | William Poundstone | Kelly criterion, fractional Kelly, drawdown/risk-of-ruin math |

## The Five Laws (what the books agree on)

1. **The sharp market is the best public estimate of truth.** Devig
   Pinnacle/Circa, not your gut.
2. **Edge comes first from price.** Line shopping beats handicapping;
   the best price across books IS the model's first alpha source.
3. **Bet value, never winners.** A bet exists only when your price beats
   your fair number.
4. **Kelly sizes, fractional Kelly survives.** Full Kelly assumes your
   probabilities are exact; they never are.
5. **Closing line value is the verdict.** Win-loss records lie for years;
   CLV tells the truth in weeks.

## Quickstart

```bash
pip install -e ".[dev]"
pytest                                   # 150+ tests
sharpods data/sample_odds.json --bankroll 10000
```

Output: a ranked bet card with EV, fair odds, Kelly stakes, plus detected
arbitrages, middles, and Wong teaser legs, and per-market diagnostics
(synthetic hold, consensus fair probabilities).

```
RECOMMENDED BETS (2), bankroll 10,000.00:
 1. Lakers @ Celtics | moneyline home | draftkings @ 2.020
    fair p=0.5026 (fair odds 1.990) | EV +1.53% | stake 37.52 (0.38% of roll, 25% Kelly)
...
ARBITRAGE (risk-free at quoted prices):
  nba-2026-lal-bos: home@draftkings 2.020 (50.0%), away@fanduel 2.020 (50.0%) -> +1.00% locked
```

## Pipeline

```
odds snapshot (all books, all markets)
    │
    ├─ 1. FAIR LINE   devig sharp books (power/Shin/…), sharpness-weighted
    │                 logit consensus                    [Books 2, 5, 8]
    ├─ 2. MODEL BLEND Elo / Poisson / Pythagorean / Monte Carlo probabilities,
    │                 market-weighted 75/25              [Books 4, 6, 7, 9]
    ├─ 3. EDGE SCAN   best-price EV, arbitrage, middles, Wong teasers,
    │                 key numbers, steam-stale flags     [Books 1, 2, 3, 8]
    ├─ 4. STAKING     fractional Kelly + per-bet/event/slate caps
    │                                                    [Books 4, 6, 10]
    └─ 5. BET CARD    ranked tickets with rationale + CLV feedback loop
                                                         [Books 5, 8]
```

## Package layout

```
sharpods/
├── odds.py            conversions, overround, five devig methods
├── books_registry.py  sportsbook sharpness weights (market maker vs retail)
├── fairline.py        sharpness-weighted logit consensus; market/model blend
├── models/
│   ├── elo.py         Elo with MOV multiplier and home advantage
│   ├── poisson.py     Poisson + Dixon-Coles score-matrix model
│   ├── pythagorean.py Pythagorean expectation, Pythagenpat, luck wins
│   ├── wintotals.py   Poisson-binomial season win totals; spread↔ML map
│   └── montecarlo.py  seeded simulation with error bars
├── edges.py           EV, line shopping, key numbers + half-point parity,
│                      Wong teasers, parlays (incl. correlated), hedging,
│                      free-bet conversion, arbitrage, middles, steam
├── kelly.py           full/fractional Kelly, growth & Shannon ceiling,
│                      drawdown law, risk-of-ruin math
├── portfolio.py       exposure caps; card ranked by log-growth contribution
├── clv.py             CLV ledger, Buchdahl significance tests, runs test
├── engine.py          the orchestrator; produces the bet card
├── io.py              snapshot JSON loader
└── cli.py             `sharpods` command
```

## What the model refuses to do

Straight from the books' warnings:

- **No fair line without a sharp book.** If no market maker quotes the full
  market, the engine skips it rather than invent a number.
- **No bets below +1% EV.** Sub-threshold edges are estimation noise.
- **No full Kelly.** Default is quarter Kelly with a 2% per-bet cap.
- **No chasing steam.** A move at Pinnacle is information; betting the moved
  price is not. Only *stale* prices left behind are flagged.
- **No unbounded correlated exposure.** Same-event bets share a 3% cap.

## Disclaimer

SharpOds is an educational implementation of published betting theory. Sports
betting involves risk of loss and is not legal in all jurisdictions. Nothing
here is financial advice; historical edges (including Wong teaser pricing and
key-number frequencies) decay as markets adapt.
