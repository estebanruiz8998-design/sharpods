# The SharpOds Model: Synthesis of the Ten Books

This document is the unified architecture specification for SharpOds, synthesizing:
Wong (*Sharp Sports Betting*), Miller & Davidow (*The Logic of Sports Betting*), Yao
(*Weighing the Odds*), Buchdahl (*Fixed Odds Sports Betting*; *Squares & Sharps,
Suckers & Sharks*), Peta (*Trading Bases*), Mack (*Statistical Sports Models in
Excel*), Pokerjoe (*Sharper*), Winston (*Mathletics*), and Poundstone (*Fortune's
Formula*).

---

## The Unified Theory

The ten books converge on a single inversion of the amateur's premise: sports betting
is not a prediction contest, it is a price-trading business, and the market itself is
the best handicapper in it. The devigged price at a high-limit market-making book —
Pinnacle- or Circa-class, weighted by the limits they will accept — is the closest
publicly available estimate of true probability, and it is sharpest at close (Miller &
Davidow, Pokerjoe, Buchdahl). SharpOds therefore treats the sharp devigged consensus as
its ground-truth anchor, treats retail and soft-book prices strictly as execution
targets, and defines every edge as a measurable deviation from that anchor: a lagging
copier's stale number, a derivative menu priced by crude rules of thumb, a half point
sold below its key-number mass, a promo with computable face value.

Edge comes from two channels, and the books rank them clearly. The first and most
reliable channel is **price**: exhaustive line shopping drives the synthetic hold of
the bettor's personal market toward zero or below (Miller & Davidow), while top-down
scanning fires whenever any book's price beats the sharp fair probability by more than
a threshold (Pokerjoe, Buchdahl's wisdom-of-crowd trigger). The second channel is
**models**: distribution-first probability machines — Poisson score matrices, Massey
and Elo ratings mapped through empirical margin distributions, Pythagorean and
luck-stripped bottom-up team projections (Mack, Winston, Peta) — deployed where markets
are soft (derivatives, props, niche leagues, early numbers) rather than head-on against
efficient main-line closers. Crucially, no model output is ever trusted raw: model
probabilities are shrunk toward the market anchor, with the model's weight earned only
by its demonstrated record (Peta's 75% shrink per Birnbaum's audit; Buchdahl's
blend-by-CLV directive; Poundstone's warning that Kelly with an overestimated p is
overbetting in disguise).

The proof of edge is **closing line value**, not profit and loss. Bet-level outcomes
are so luck-dominated that thousands of bets are needed before a P&L record carries
statistical information (Buchdahl's t-statistic and minimum-n formulas), while
consistently beating the devigged sharp close predicts realized returns nearly
one-for-one and converges in hundreds of bets (Buchdahl, Miller & Davidow, Mack,
Pokerjoe). SharpOds therefore grades every bet, every strategy, and every model
component on mean CLV with confidence intervals, quarantines anything whose rolling CLV
goes non-positive regardless of recent profit, shrinks every performance estimate
toward the population mean before acting on it, and architecturally forbids
"resulting" — no component may condition stakes or weights on recent win/loss
sequences.

**Kelly is the throttle, never the engine.** Staking cannot create edge — expected
profit is yield times turnover under every staking plan (Buchdahl) — but staking is
how edges compound or die. SharpOds sizes every bet as a fraction of *current* bankroll
via fractional Kelly (default 0.25×, ceiling 0.5×), computed on the shrunk probability
and the best available price, with simultaneous and correlated bets sized jointly
against one Kelly budget (Poundstone). The asymmetry of overbetting is enforced as a
hard guardrail: 1.5× Kelly earns 0.5× Kelly's growth at nine times the variance, and
beyond 2× Kelly growth turns negative even with the edge intact. Realized drawdowns are
continuously audited against the theoretical law P(dip to x·W₀) = x^(2/c−1); excess
drawdown is treated as evidence of overstated edge, not bad luck.

Finally, **discipline is the moat**. Every book documents how winners destroy
themselves: chasing steam into the moved number, paying retail hold on parlays, buying
half points above their key-number value, betting for action, sizing up after losses,
believing a hot streak. SharpOds encodes the discipline structurally — hard EV gates on
every emission, bans on loss-linked sizing and momentum features, account capacity
managed as capital, fund-style accounting with NAV, drawdown limits and written review
triggers (Peta) — so that the engine is incapable of the errors the books catalogue,
rather than merely advised against them.

---

## Principle-to-Component Matrix

| Book | Concept | Component | How Applied |
|---|---|---|---|
| Wong | Vig / break-even implied probability | `odds.py` | Every price converted to implied probability; hard gate: emit only when fair prob exceeds it plus threshold |
| Wong | Key numbers (NFL 3 ≈ 15% of games incl. spread-conditioning, 7 ≈ 9%) | `models/margins.py` | Rolling empirical margin distribution conditional on closing spread, re-fit per season; drives all derivative pricing |
| Wong | Half-point valuation by outcome reallocation (a′ = a + q/w; a″ = wa/(w+q)) | `edges.py` | `halfpoint_value()` prices every point buy/sell and alt line at parity; buy only below parity |
| Wong | Wong teaser (6-pt legs crossing 3 and 7) | `edges.py` | Candidate filter dogs +1.5..+2.5 / favs −7.5..−8.5; each leg re-qualified on current margin data at actual price (−120/−130 aware) |
| Wong | Teaser per-leg break-even r = p_imp^(1/n) | `edges.py` | `teaser_breakeven()`; auto-reject teasers whose empirical leg cover probs fall below hurdle |
| Wong | Season win totals via Poisson-binomial DP | `models/montecarlo.py` + `edges.py` | Exact DP convolution of per-game win probs; priced vs devigged market both sides with correlation haircut and league win-sum consistency |
| Wong | Parlays: −EV at standard payouts, +EV legs compound | `edges.py` | Emit only parlays of individually +EV legs or correlated combos beating multiplicative price |
| Wong | Hedging = buying insurance at vig-inclusive price | `edges.py` | `hedge_stake()` computes lock stake and EV cost; default EV-max (no auto-hedge); surface cost, hedge only on utility triggers |
| Wong | Middling: ~4.8% hit rate suffices at −110/−110 | `edges.py` | `middle_breakeven()` vs window mass from margin distribution; auto-flag qualifying middles |
| Wong | Money management: flat small fraction, never chase; RoR = ((1−p)/p)^N | `kelly.py` | Ruin-probability check on unit size; architecture bans loss-chasing |
| Wong | Line shopping: each half point / 5 cents has computable EV | `fairline.py` + `edges.py` | Best-price synthetic market; EV of price improvements computed, not assumed |
| Wong | Derivatives-first scanning priority | `engine.py` | Scan order: teasers, alt lines, point buys, props, win totals, spread-vs-ML before main-line picks |
| Wong | Poisson prop pricing P(X≥1) = 1 − e^(−λ) | `models/poisson.py` | Count-type prop pricer |
| Wong | Spread → win probability Φ(s/σ) | `models/margins.py` | Cold-start fallback only; empirical margin distribution preferred |
| Miller & Davidow | Market makers vs retail copiers | `books_registry.py` | Every book classified; p_fair computed only from market-maker prices weighted by limits; retail = execution targets |
| Miller & Davidow | Closing line as best public probability estimate | `fairline.py` + `clv.py` | Devigged MM close is truth benchmark for grading and anchor for pricing |
| Miller & Davidow | Hold per market; hurdle varies by bet type | `odds.py` + `books_registry.py` | `hold()` stored on every market snapshot; routes bets to lowest effective margin |
| Miller & Davidow | Synthetic hold across books; B_syn < 1 = arb | `fairline.py` | `synthetic_market()` takes best price per side; flags near-arb (<1% hold) and arb |
| Miller & Davidow | Devigging (proportional + power/additive/Shin for longshot bias) | `odds.py` | Four devig methods implemented; selected per market shape |
| Miller & Davidow | CLV as the honest scorecard | `clv.py` | `clv_ev()` logged per bet vs devigged MM close; positive limit-weighted CLV required to keep strategies enabled |
| Miller & Davidow | Line moves: MM move = information, retail move = copying | `edges.py` | `classify_move()`; MM move updates p_fair, retail move triggers stale-line scan |
| Miller & Davidow | Derivative markets attackable by consistency checks | `fairline.py` + `edges.py` | Fair derivative prices derived from sharp primary; inconsistent postings bet |
| Miller & Davidow | Half-point value = mass on the number crossed | `edges.py` | dEV = P_k (loss→push), P_k(d−1) (push→win); never pay above dEV |
| Miller & Davidow | Account access is capital | `books_registry.py` | Per-book limits, limit history, expected account-lifetime cost in routing |
| Miller & Davidow | Promos / free bets are quantifiable +EV | `edges.py` | `free_bet_ev()`; convert on high-odds low-hold markets (~70%+ of face) |
| Miller & Davidow | Top-down bet trigger p_fair·d_best − 1 > θ | `edges.py` | The primary bet generator; θ scaled up where anchor confidence is low |
| Yao | Relative-value player: main line is the underlying, menu is derivatives | `fairline.py` | Derivative fair-pricing layer anchored to devigged sharp main line |
| Yao | Push removal p′ = p_w/(p_w+p_l) | `odds.py` | The low-level utility for comparing bets across numbers on one EV scale |
| Yao | Living push-percentage tables P_k (era-split at 2015 NFL PAT change) | `models/margins.py` | Per-league/market/era key-number mass tables feeding all half-point math |
| Yao | Scalping: Σ(1/d) < 1 across books | `edges.py` | `find_arbs()` standing scanner with stakes ∝ implied probability |
| Yao | Middle break-even (J−100)/(J+100) | `edges.py` | Middle scanner prioritizing windows containing 3 and 7, push-term aware |
| Yao | Hedge EV cost = h(1 − q·d_h); fair-or-better hedge = scalp | `edges.py` | Price every hedge; cost ≤ 0 → maximize as scalp; else require utility justification |
| Yao | Correlated parlays: bet iff P(A∩B) > 1/d_par | `edges.py` | Joint distributions for same-game side/total and 1H/full-game combos |
| Yao | Team totals from spread and total: (T±S)/2 | `fairline.py` | Anchor for team totals and derived props |
| Yao | 1H/2H/quarter derivative consistency (1H ≈ r × game) | `fairline.py` | Per-league period-share ratios; bet when |posted − fair| > vig + buffer |
| Yao | Spread–moneyline equivalence via f(m\|S) | `models/margins.py` | Cheapest-instrument routing between spread and ML expressions |
| Yao | Futures booksum 120–160%; replication test | `edges.py` | Reject futures whose replicating game-bet sequence is cheaper |
| Yao | Bet timing by market maturity | `engine.py` | Attack derivative menus/openers early; bet main markets late |
| Buchdahl (Fixed Odds) | Overround as structural tax | `odds.py` | `booksum()`/`overround()`; blind-bettor loss rate 1/B − 1 as null hypothesis |
| Buchdahl (Fixed Odds) | Value is the only selection criterion (p·d > 1 + τ) | `edges.py` | Sole bet gate; strike rate is display metadata only |
| Buchdahl (Fixed Odds) | Margin-weights-proportional-to-odds devig | `odds.py` | `devig_margin_weights()` for 3+ outcome / favourite-longshot markets; plain normalization reserved for symmetric two-ways |
| Buchdahl (Fixed Odds) | Goal-superiority rating (last-6 goal diff, calibrated) | `models/ratings.py` | Cheap baseline feature and stale-line flag; never outranks sharp-price probabilities |
| Buchdahl (Fixed Odds) | Accumulators compound margins and edges | `edges.py` | Emit only when every leg independently passes value gate |
| Buchdahl (Fixed Odds) | Staking plans cannot change edge sign; recovery plans ruin | `kelly.py` | Level/percentage/fixed-profit implemented; loss-linked sizing structurally impossible |
| Buchdahl (Fixed Odds) | Significance test t = Y√n/√(d̄−1); minimum n | `clv.py` | Gates "profitable" labels; auto-quarantine on negative-drifting t |
| Buchdahl (Fixed Odds) | Per-bet volatility √(d−1); P(profit) horizons | `clv.py` | Reported with every strategy before deployment |
| Buchdahl (Fixed Odds) | Tipsters as testable products | `clv.py` | External signals need timestamps, achievable odds, passing t-stat before nonzero weight |
| Buchdahl (Squares & Sharps) | Sharp devigged close ≈ unbiased crowd forecast | `fairline.py` | The anchor doctrine: sharp consensus is baseline truth for every market |
| Buchdahl (Squares & Sharps) | Wisdom-of-crowd trigger r = d_best/d_fair > 1 + τ | `edges.py` | Primary bet generator (same machinery as top-down trigger); r − 1 logged as EV |
| Buchdahl (Squares & Sharps) | CLV converges in hundreds of bets vs thousands for P&L | `clv.py` | CLV is primary KPI ahead of P&L; profit without positive CLV presumed luck |
| Buchdahl (Squares & Sharps) | Favourite-longshot bias + probability weighting w(p) | `books_registry.py` | Soft-book mispricing prior: scanner steered toward favourites; +EV longshots at soft books treated as suspect |
| Buchdahl (Squares & Sharps) | Luck-skill decomposition; shrinkage κ = Var(skill)/Var(total) | `clv.py` | All performance estimates shrunk before use; leaderboards ranked on shrunken values |
| Buchdahl (Squares & Sharps) | Model blending w·p_model + (1−w)·p_anchor, w earned by CLV | `fairline.py` | Models start as feature generators (w≈0); weight grows only with demonstrated CLV |
| Buchdahl (Squares & Sharps) | Process over outcome; ban resulting | `engine.py` + `clv.py` | No component conditions on recent W/L; review ordering by CLV and calibration |
| Peta | Cluster luck via BaseRuns residual | `models/pythagorean.py` | Actual RS/RA replaced by BaseRuns-expected before projection; residual gets zero forward weight |
| Peta | Pythagorean deviation is luck | `models/pythagorean.py` | Pythagenpat conversion; actual-vs-Pythag divergence flagged as regression candidate |
| Peta | Bottom-up talent: wins = 47.7 + ΣWAR (regressed) | `models/pythagorean.py` | Preseason team priors from projected (not raw) WAR with roster deltas |
| Peta | Game-day starter annualization (5× starter WAR) | `models/pythagorean.py` | Converts season strength to tonight's strength per actual starter |
| Peta | Log5 with home advantage via odds ratio (h ≈ 0.54) | `models/pythagorean.py` | Two team strengths → single-game home win probability |
| Peta | In-season blending k/(k+G), k ≈ 60–70 | `models/pythagorean.py` | Smooth preseason-to-observed weight shift on luck-stripped results |
| Peta | Market shrinkage λ ≈ 0.25 (Birnbaum audit) | `fairline.py` | Model-market gaps shrunk ~75% toward market before edge computation |
| Peta | Fund management: NAV, drawdown limits, Sharpe, process reviews | `portfolio.py` | Daily NAV accounting, drawdown alerts triggering model review not tilt |
| Peta | Sport selection: model where luck is measurable and games are many | `engine.py` | Deployment prioritizes MLB-like structures (moneylines, 2,430 games, decomposable stats) |
| Mack | Distribution-first modeling | `models/` | Each sport engine declares its generative distribution; all market prices derive from that one fit |
| Mack | Poisson score matrix (attack/defense strengths) | `models/poisson.py` | One matrix prices 1X2, totals, correct score, BTTS, Asian handicaps |
| Mack | Bivariate Poisson (Karlis–Ntzoufras λ₃) | `models/poisson.py` | Fixes underpricing of draws/low-scoring games via score covariance |
| Mack | Massey least-squares ratings + Φ(m/σ) | `models/ratings.py` + `models/margins.py` | Ridge-regularized baseline for margin sports; σ re-fit per season from residuals |
| Mack | Normal model for high-scoring sports | `models/margins.py` | Independent normal scores price sides and totals (NBA/NFL/AFL) |
| Mack | Logistic regression by MLE | `models/ratings.py` | Direct win-probability models from team statistics |
| Mack | Monte Carlo as universal fallback pricer (N ≥ 10,000, SE reported) | `models/montecarlo.py` | Prices any derivative/path-dependent market lacking closed form |
| Mack | Overfitting discipline: parsimony, walk-forward, pre-committed criteria | `clv.py` + `engine.py` | Feature caps, never-shuffled splits, deployment criteria fixed before backtest |
| Mack | Market-softness allocation | `engine.py` | Per-market efficiency metrics steer modeling effort to niche/derivative markets |
| Mack | CLV as model kill switch | `clv.py` | Rolling non-positive CLV quarantines a live model regardless of P&L |
| Pokerjoe | The market is the best handicapper | `fairline.py` | Default assumption: sharp line right, model wrong; deviations must clear vig + threshold |
| Pokerjoe | Top-down stale-line scanner (θ ≥ 0.01) | `edges.py` | Continuous EV scan of every screen price vs sharp fair probability |
| Pokerjoe | Steam-follow gate: never bet the moved number | `edges.py` | After MM move, follow only where laggards still clear EV gate; require persistence / multi-book confirmation |
| Pokerjoe | Move weighting by where/when/limits | `books_registry.py` | Moves weighted by the max bet accepted at the moving book at that moment |
| Pokerjoe | CLV as only short-term truth | `clv.py` | Signals with rolling mean CLV ≤ 0 disabled; expected ROI reported as mean CLV |
| Pokerjoe | Half-point value Δp = f(N)/2 | `edges.py` | Alternate-line/point-buy/teaser/middle valuation off margin-landing distribution |
| Pokerjoe | Flat staking 1–2% floor, thin edge × high volume | `kelly.py` | Flat bet-to-risk floor policy; sizing capped well below full Kelly |
| Pokerjoe | Accounts and limits as depletable capital | `books_registry.py` | Route +EV extraction to soft books, price discovery to sharp books |
| Winston | Pythagorean with sport exponents (MLB ~2, NFL 2.37, NBA 13.91) | `models/pythagorean.py` | Regression-to-mean prior for futures and win totals; Pythag wins fed instead of actual wins |
| Winston | Massey ratings: recency weights, blowout caps, fitted home edge | `models/ratings.py` | Baseline spread prediction; any replacement must beat it out-of-sample on margin MAE |
| Winston | Normal margin model with key-number patch | `models/margins.py` | σ per sport (~14 NFL, ~12 NBA); discrete empirical mass at 3/7 overlaid on the normal |
| Winston | Parlay/teaser arithmetic (10–12.5% house edge; 72.38% teaser hurdle) | `edges.py` | Auto-reject standard offers; joint probabilities for same-game legs, never independence-by-default |
| Winston | Elo with margin multiplier | `models/elo.py` | Online-updating rating ensembled with Massey; Elo-gap-to-points mapping |
| Winston | Brownian in-game win probability | `models/margins.py` | Live-pricing fallback and divergence alarm for live models |
| Winston | Levitt line-shading: books exploit bias, don't balance | `models/ratings.py` | Public-bias correction terms (favorites, overs, glamour teams) as decay-tested features |
| Winston | Pace × efficiency, RAPM; linear weights | `models/ratings.py` / `models/pythagorean.py` | NBA totals decomposition and injury repricing; MLB run-expectation inputs |
| Winston | RPI anti-pattern; runs-test streakiness screen | `clv.py` | Momentum features blocked unless passing runs test; unweighted composites banned as inputs |
| Winston | Kelly as growth-optimal management | `kelly.py` | Sizing on +EV bets; overbetting destroys growth |
| Poundstone | Kelly f* = edge/odds maximizes log growth, precludes ruin | `kelly.py` | Core stake computation on current (never starting) bankroll |
| Poundstone | Fractional Kelly (c = 0.5 keeps 75% of growth at half volatility) | `kelly.py` | Default c = 0.25, ceiling 0.5, raised only on out-of-sample evidence |
| Poundstone | Overbetting asymmetry; 2× Kelly = zero growth | `kelly.py` | Hard guardrail: effective stake never exceeds full Kelly under any override |
| Poundstone | Simultaneous/correlated Kelly: max E[ln(1+Σfᵢxᵢ)], F = C⁻¹M | `portfolio.py` | Concurrent bets share one Kelly budget via covariance; never sum standalone fractions |
| Poundstone | Variance drag g ≈ μ − σ²/2 | `kelly.py` | Bets ranked by log-growth contribution, not raw EV |
| Poundstone | Drawdown law P(dip to x) = x^(2/c−1) | `portfolio.py` | Continuous audit; excess drawdowns trigger λ and c reductions |
| Poundstone | Edge is information (G_max = R; 1 − H(p)) | `kelly.py` + `clv.py` | Growth ceiling; models measured by log-score/calibration against closes |
| Poundstone | Gambler's ruin of fixed staking; Shannon's demon rebalancing | `kelly.py` | Proportional staking re-anchored to live bankroll every bet |

---

## Pipeline Architecture

Target package: `sharpods/` with `odds.py`, `books_registry.py`,
`models/` (`elo.py`, `poisson.py`, `pythagorean.py`, `montecarlo.py`, plus two
book-justified additions: `ratings.py` for Massey/logistic/goal-superiority and
`margins.py` for margin distributions, key numbers and normal-model conversions),
`fairline.py`, `edges.py`, `kelly.py`, `portfolio.py`, `clv.py`, `engine.py`, with
`datatypes.py`/`io.py`/`cli.py` as infrastructure. The two model additions are
justified because Massey ratings appear independently in Mack and Winston, and the
empirical margin/key-number distribution is the shared pricing substrate demanded by
Wong, Yao, Miller & Davidow, Pokerjoe and Winston — it must be a first-class model, not
a constant table inside `edges.py`.

### Stage 1 — Ingest & Normalize (`io.py`, `datatypes.py`, `odds.py`)
- **Inputs:** raw odds feeds (American/decimal/fractional), market metadata, limits, timestamps.
- **Outputs:** normalized `Quote`/`Market` objects; all prices in decimal; implied probabilities and per-market booksum/hold attached.
- **Algorithms:** American↔decimal conversion; implied probability; booksum, overround, hold.
- **Books:** Miller & Davidow (normalize to decimal before any computation), Buchdahl, Pokerjoe, Wong, Winston.

### Stage 2 — Book Classification & Weighting (`books_registry.py`)
- **Inputs:** book identities, current limits, historical hold, limit history.
- **Outputs:** per-book sharpness weight; market-maker vs retail flag; per-book routing metadata (account-lifetime cost, soft-book bias prior).
- **Algorithms:** limit-weighted sharpness scoring; probability-weighting w(p) soft-book distortion prior; move-weighting by max accepted bet.
- **Books:** Miller & Davidow (originators vs copiers), Pokerjoe (weight by limits; accounts as capital), Buchdahl *Squares & Sharps* (FLB/probability weighting).

### Stage 3 — Devig & Sharp Anchor (`odds.py` → `fairline.py`)
- **Inputs:** market-maker quotes only, weighted by limits.
- **Outputs:** `p_fair` per outcome per market (the anchor); synthetic best-price market across all books with synthetic hold.
- **Algorithms:** proportional devig for symmetric two-ways; margin-weights-proportional-to-odds for 3+ outcomes / favourite-longshot structure; power, additive and Shin devig selected per market shape; synthetic booksum B_syn and hold H_syn.
- **Books:** Wong, Miller & Davidow, both Buchdahl volumes, Pokerjoe, Peta.

### Stage 4 — Model Probabilities (`models/`)
- **Inputs:** historical scores, team/player stats, schedules, rosters.
- **Outputs:** independent `p_model` per outcome, with declared generative distribution and calibration record.
- **Algorithms:** Poisson score matrix + bivariate Poisson (soccer/hockey); ridge Massey + Elo ensemble mapped through per-sport margin distributions (margin sports); Pythagorean/Pythagenpat, BaseRuns luck-stripping, WAR bottom-up, log5, in-season blending (MLB); logistic regression; Monte Carlo (N ≥ 10,000, SE reported) for anything without closed form; Brownian live win probability as fallback/alarm.
- **Books:** Mack (distribution-first), Winston (ratings, normal margin model, Elo, in-game), Peta (luck-stripping and bottom-up MLB), Buchdahl *Fixed Odds* (goal superiority baseline).

### Stage 5 — Blend & Shrink (`fairline.py`)
- **Inputs:** `p_fair` anchor, `p_model` per model, each model's CLV/calibration record.
- **Outputs:** `p_used = w·p_model + (1−w)·p_fair` with w per model per market type (starting near 0; Peta-class team models start at λ ≈ 0.25).
- **Algorithms:** CLV-earned blend weights; Birnbaum-style shrinkage; models failing to beat the close remain feature generators.
- **Books:** Buchdahl *Squares & Sharps*, Peta, Poundstone (shrink before sizing), Mack.

### Stage 6 — Derivative Fair Pricing (`fairline.py` + `models/margins.py`, `models/poisson.py`)
- **Inputs:** anchored main-line `p_used`, empirical margin/score distributions.
- **Outputs:** fair prices for 1H/2H/quarters, team totals, alternate lines, spread↔moneyline equivalents, props, win totals, futures.
- **Algorithms:** team totals (T±S)/2; period-share ratios per league; f(m|S) spread↔ML tables; Poisson-binomial DP for season wins; Poisson prop pricing; futures replication test.
- **Books:** Yao (the derivative doctrine), Wong, Miller & Davidow, Winston.

### Stage 7 — Edge Scan (`edges.py`)
- **Inputs:** `p_used`/derivative fair prices, synthetic best-price market, live quote stream, key-number masses.
- **Outputs:** typed `EdgeCandidate`s: value bets, half-point buys, teasers, correlated parlays, middles, arbs/scalps, steam-follows, stale derivatives, win totals, futures-vs-replication, free-bet conversions.
- **Algorithms:** top-down trigger p_fair·d_best − 1 > θ (θ ≥ 0.01, scaled by anchor confidence); half-point parity and P_k valuation; teaser per-leg hurdle p_imp^(1/n) with Wong candidate filter re-qualified on current data; middle hurdle (J−100)/(J+100); arb condition Σ1/d < 1 with stakes ∝ 1/d; hedge EV cost h(1−q·d_h); move-source classification and steam-follow gate; correlated-parlay joint probability test.
- **Books:** all ten — this is where every pricing insight converges into emission logic.

### Stage 8 — Gating & Validation (`clv.py` policies applied in `engine.py`)
- **Inputs:** edge candidates, per-strategy CLV records, significance statistics.
- **Outputs:** candidates surviving the value gate, quarantine list, strategy enable/disable flags.
- **Algorithms:** p·d > 1 + τ hard gate; t-statistic and minimum-n enforcement; rolling-CLV kill switch; shrinkage of performance estimates; runs-test screen on momentum features.
- **Books:** both Buchdahl volumes, Mack, Pokerjoe, Winston.

### Stage 9 — Staking (`kelly.py`)
- **Inputs:** surviving candidates with `p_bet` (shrunk), best price, live deployable bankroll.
- **Outputs:** stake per bet = c·f*·W_current, c default 0.25, capped at 0.5; flat floor and minimum-stake/ruin guardrails.
- **Algorithms:** Kelly fraction; fractional-Kelly growth trade-off; expected log-growth evaluation; overbetting boundary enforcement; staking-plan library with recovery plans structurally excluded.
- **Books:** Poundstone (the core), Buchdahl *Fixed Odds*, Winston, Mack, Peta, Wong, Pokerjoe.

### Stage 10 — Portfolio Construction (`portfolio.py`)
- **Inputs:** individually sized candidates, covariance estimates (same-game, same-team, futures-vs-series overlaps), current exposures, NAV.
- **Outputs:** jointly optimized stakes; exposure caps (2–3% NAV per game); total at-risk capped where portfolio log-growth stops increasing.
- **Algorithms:** simultaneous Kelly max E[ln(1+Σfᵢxᵢ)] (numeric) and F = C⁻¹M approximation; correlation budgeting; drawdown-law audit x^(2/c−1); fund accounting (NAV, max drawdown, Sharpe).
- **Books:** Poundstone, Peta.

### Stage 11 — Bet Card Emission (`engine.py`)
- **Inputs:** portfolio-adjusted stakes, candidate metadata.
- **Outputs:** ranked bet card ordered by expected log-growth contribution (not raw EV), with price, fair probability, EV, stake, edge type, and book routing; derivatives-first scan ordering; market-maturity timing tags.
- **Books:** Poundstone (ranking), Wong and Yao (derivatives-first, timing), Pokerjoe (routing).

### Stage 12 — CLV Logging & Audit Feedback (`clv.py`)
- **Inputs:** every emitted bet's taken price; devigged closing price; settled results.
- **Outputs:** per-bet CLV, per-strategy mean CLV with confidence intervals, t-statistics, luck-accounting displays, calibration/log-score, updated blend weights w and Kelly fraction c — closing the loop into Stages 5 and 9.
- **Books:** Miller & Davidow, both Buchdahl volumes, Mack, Pokerjoe, Poundstone (information metrics), Peta (the metric he lacked).

---

## Key Formulas Consolidated

Deduplicated; each formula lives in exactly one module. Decimal odds `d` throughout;
American odds `A`; net odds `b = d − 1`.

### odds.py — prices and probabilities
1. **American ↔ decimal** (Miller & Davidow, Pokerjoe, Wong): `d = 1 + A/100` if A > 0; `d = 1 + 100/|A|` if A < 0. Inverse: `A = 100(d−1)` if d ≥ 2 else `−100/(d−1)`.
2. **Implied probability / break-even** (all ten): `p_imp = 1/d`; at −110, 0.52381.
3. **Booksum, overround, hold** (Miller & Davidow, Buchdahl, Pokerjoe): `B = Σ 1/dᵢ`; overround = B − 1; hold `H = 1 − 1/B`; blind-bettor return = 1/B − 1.
4. **Proportional devig** (Wong, Miller & Davidow, Pokerjoe, Peta, Winston): `p_fair,i = (1/dᵢ)/B`.
5. **Margin-weights-proportional-to-odds devig** (Buchdahl ×2): `M = B − 1`; `d_fair,i = n·dᵢ/(n − M·dᵢ)`; check: 1.909/1.909 → 2.00. Mandatory for 3+ outcomes or favourite-longshot structure.
6. **Power devig** (Miller & Davidow directive): solve k such that `Σ (1/dᵢ)^k = 1`; `p_fair,i = (1/dᵢ)^k`. **Additive**: `p_fair,i = 1/dᵢ − (B−1)/n`. **Shin**: solve for insider fraction z; corrects longshot bias.
7. **EV per unit** (all ten): `EV = p·d − 1`; with pushes (Wong, Yao): `EV = p_w(d−1) − p_l`.
8. **Push removal** (Yao): `p′ = p_w/(p_w + p_l)`; bet +EV iff `p′ > 1/d`. The universal cross-number comparison utility.

### books_registry.py — the market's microstructure
9. **Probability weighting function** (Buchdahl *Squares & Sharps*, TK 1992): `w(p) = p^γ/(p^γ + (1−p)^γ)^(1/γ)`, γ ≈ 0.61; with prospect-theory value function `v(x) = x^0.88` (gains), `−2.25(−x)^0.88` (losses). Used as a *prior on soft-book mispricing*, never as a pricing tool.

### models/margins.py — margin distributions and conversions
10. **Empirical margin distribution** (Wong, Yao, Pokerjoe): `f(m|S)` per league conditional on closing spread, era-split (NFL at 2015 PAT change); key masses NFL P₃ ≈ 0.09–0.10, P₇ ≈ 0.05–0.06.
11. **Normal margin model** (Winston, Mack, Wong fallback): `P(win) = Φ(m̂/σ)`; `P(cover s) = Φ((m̂−s)/σ)`; σ ≈ 13.5–14 NFL, ~12 NBA, ~10 NCAAB, re-fit per season from rating residuals; discrete empirical mass patched at 3 and 7.
12. **Normal score model, high-scoring sports** (Mack): H ~ N(μ_H, σ_H²), A ~ N(μ_A, σ_A²); `P(home win) = Φ((μ_H−μ_A)/√(σ_H²+σ_A²))`; `P(over T) = 1 − Φ((T−(μ_H+μ_A))/√(σ_H²+σ_A²))`.
13. **Spread ↔ moneyline equivalence** (Yao, Wong, Winston): `p_ML = P(m > 0 | S)` from f(m|S); implied margin from prob: `m = σ·Φ⁻¹(p)`.
14. **Brownian in-game win probability** (Winston): lead L, fraction f remaining, full-game margin μ: `P(win) = Φ((L + μ·f)/(σ·√f))`.

### models/ratings.py — rating and regression models
15. **Massey least squares** (Mack, Winston): `margin_g = h + rᵢ − rⱼ + e_g`, minimize Σe² s.t. Σr = 0; ridge penalty, exponential recency weights, blowout cap ~20–24; predicted spread `m̂ = h + rᵢ − rⱼ`.
16. **Goal-superiority rating** (Buchdahl *Fixed Odds*): last-6 goal-difference differential, mapped to (p_H, p_D, p_A) by per-league regression-smoothed frequencies, normalized.
17. **Logistic regression by MLE** (Mack): `p = 1/(1+e^(−Xβ))`; maximize `LL = Σ[y ln p + (1−y) ln(1−p)]`.
18. **Possessions / efficiency / RAPM** (Winston): `Poss ≈ FGA − ORB + TO + 0.44·FTA`; `OffEff = 100·Pts/Poss`; ridge regression of stint margin on player indicators.

### models/elo.py
19. **Elo with margin multiplier** (Winston 2nd ed.): `E_A = 1/(1+10^(−(R_A−R_B+HFA)/400))`; `R_A += K·M·(S_A − E_A)`; `M = ln(|margin|+1)·2.2/(0.001·ΔR_winner + 2.2)`; K ≈ 20 NFL/NBA, 4–6 MLB; Elo gap mapped to points via empirical slope.

### models/poisson.py
20. **Poisson scoreline matrix** (Mack): `P(X=k) = e^(−λ)λ^k/k!`; `λ_home = L_home·att_home·def_away` (mirrored away); matrix S(i,j) prices 1X2, totals, correct score, BTTS, handicaps.
21. **Bivariate Poisson** (Mack, Karlis–Ntzoufras): X = X₁+X₃, Y = X₂+X₃; `Cov(X,Y) = λ₃`; corrects draw/under underpricing.
22. **Poisson prop pricing** (Wong): `P(X≥1) = 1 − e^(−λ)` with λ = expected event count.

### models/pythagorean.py — team strength and luck-stripping
23. **Pythagorean / Pythagenpat** (Winston, Peta): `W% = PF^x/(PF^x + PA^x)`; x = 1.83–2 MLB, 2.37 NFL, 13.91 NBA; Pythagenpat `x = ((PF+PA)/G)^0.287`; deviation from actual = non-persistent luck.
24. **BaseRuns cluster luck** (Peta): `A = H+BB−HR`; `B = (1.4TB − 0.6H − 3HR + 0.1BB)·1.02`; `C = AB−H`; `D = HR`; `BaseRuns = AB/(B+C)·B + D` (i.e., A·B/(B+C) + D); cluster luck = R_actual − BaseRuns, zero forward weight.
25. **WAR-to-wins** (Peta): wins ≈ 47.7 + ΣWAR (regressed projections); ΔWins = ΣWAR_in − ΣWAR_out; runs-per-win `RPW = 1.5·(runs/game both teams) + 3`.
26. **Starter annualization** (Peta): `W_tonight = W_proj − ΣWAR_rotation + 5·WAR_starter`; `p_raw = W_tonight/162`.
27. **Log5 with home edge** (Peta): `OR = [p_A/(1−p_A)]·[(1−p_B)/p_B]·[h/(1−h)]`, h ≈ 0.54; `p_home = OR/(1+OR)`.
28. **In-season blending** (Peta): `p_blend = (k·p_pre + G·p_obs_adj)/(k + G)`, k ≈ 60–70.
29. **Linear weights** (Winston): runs ≈ 0.5·1B + 0.7·2B + 1.0·3B + 1.4·HR + 0.33·(BB+HBP) + 0.2·SB − 0.4·CS.

### models/montecarlo.py
30. **Poisson-binomial DP** (Wong, Yao): `f₀ = [1]`; `fᵢ(k) = fᵢ₋₁(k−1)·pᵢ + fᵢ₋₁(k)·(1−pᵢ)`; exact season-win pmf; normal approximation μ = Σpᵢ, σ² = Σpᵢ(1−pᵢ) as fallback.
31. **Monte Carlo estimation** (Mack): inverse-transform sampling; N ≥ 10,000; `SE = √(p̂(1−p̂)/N)` reported with every estimate.

### fairline.py — the anchor and its derivatives
32. **Synthetic market** (Miller & Davidow): `dᵢ* = max over books of dᵢ`; `B_syn = Σ 1/dᵢ*`; `H_syn = 1 − 1/B_syn`; B_syn < 1 ⇒ arbitrage.
33. **Model-market blend / shrinkage** (Peta, Buchdahl *S&S*, Poundstone, Mack): `p_used = w·p_model + (1−w)·p_fair`; w starts ≈ 0 (team models λ ≈ 0.25 per Birnbaum) and is earned by CLV record.
34. **Team totals from main lines** (Yao): favorite fair points = (T+S)/2, dog = (T−S)/2.
35. **Derivative consistency** (Yao): fair 1H line = r·game line, r per league from period-score history (NFL 1H total ≈ 45–48% of game total); bet when |posted − fair| > derivative vig + error buffer.

### edges.py — edge detection and pricing
36. **Top-down value trigger** (Miller & Davidow, Pokerjoe, Buchdahl ×2 — the wisdom-of-crowd trigger and value ratio are the same gate): bet iff `p_fair·d_best − 1 > θ`, θ ≥ 0.01–0.05 scaled by anchor confidence and market liquidity.
37. **Half-point / key-number value** (Wong parity form; Yao/Miller/Pokerjoe mass form — equivalent): loss→push `ΔEV = P_k`; push→win `ΔEV = P_k(d−1)`; full point through k `ΔEV = P_k·d`; Wong parity: worse side `a′ = a + q/w`, better side `a″ = w·a/(w+q)`. Buy iff price charged < ΔEV.
38. **Teaser evaluation** (Wong, Winston): per-leg break-even `r = p_imp(A)^(1/n)` (−110 two-team: 0.7237; −120: 0.7386; −130: 0.7518); `EV = Πrᵢ·(1+b) − 1` with rᵢ from current margin data; Wong candidate set (dogs +1.5..+2.5, favs −7.5..−8.5 crossing 3 and 7) must re-qualify at the offered price.
39. **Parlay / accumulator EV** (Wong, Yao, Winston, Buchdahl): fair payout `Π(1/pᵢ) − 1`; `EV = Πpᵢ·(1+B) − 1`; at true odds `1+EV = Π(1+EVᵢ)`; correlated: bet iff `P(A∩B) > 1/d_par` from the joint model.
40. **Middle break-even** (Wong, Yao, Pokerjoe): both sides at −J: `P_be = (J−100)/(J+100)` (4.76% at −110/−110); general form (R−W)/(R+W); bet iff window mass from f(m|S) > P_be (+ push term when the window contains a whole number).
41. **Arbitrage / scalp** (Miller & Davidow, Yao, Buchdahl, Pokerjoe): condition `Σ 1/dᵢ* < 1`; stakes `sᵢ = (1/dᵢ*)/B_syn`; guaranteed profit `1/B_syn − 1`.
42. **Hedge pricing** (Wong, Yao): lock stake `h* = X/d_h` guaranteeing `X(d_h−1)/d_h`; EV cost `h(1 − q·d_h)` with devigged q; cost ≤ 0 ⇒ scalp, maximize; else hedge only on utility triggers.
43. **Steam-follow gate** (Pokerjoe, Miller & Davidow): after MM move to devigged p_new, follow only at books with `p_new·d − 1 > θ`; never bet the moved number; require persistence or multi-book agreement.
44. **Futures replication test** (Yao): futures booksum commonly 1.2–1.6; reject a future if the replicating sequence of game moneylines is cheaper.
45. **Free-bet conversion** (Miller & Davidow): `EV = p(d−1)·S`; at efficient prices `EV = S(d−1)/d`, increasing in d.

### kelly.py — staking
46. **Kelly fraction** (Poundstone, Buchdahl, Winston, Mack, Peta): `f* = (p·d − 1)/(d − 1) = (bp − q)/b = edge/odds`; stake `c·f*·W_current`, c = 0.25 default, 0.5 ceiling; zero if edge ≤ 0.
47. **Expected log-growth** (Poundstone): `g(f) = p·ln(1+bf) + q·ln(1−f)`; ranking metric for the bet card; variance drag `g ≈ μ − σ²/2`.
48. **Fractional-Kelly trade-off** (Poundstone): betting c·f* keeps `(2c − c²)` of maximal excess growth at c× volatility; c = 0.5 → 75% of growth, half the volatility.
49. **Overbetting boundary** (Poundstone): `g(2f*) = 0` excess; beyond 2× Kelly growth is negative; `g(c) = g(2−c)` symmetry (1.5× = 0.5× growth at ~9× variance). Hard cap: never above 1× Kelly.
50. **Information bound** (Poundstone/Kelly-Shannon): `G_max = 1 − H(p)` bits per bet for binary side information; sustainable growth ≤ information rate of the model's channel.
51. **Multi-outcome Kelly** (Poundstone): at fair odds, `fᵢ = pᵢ` (bet your beliefs); with margin, water-filling subset solution; doubling time ≈ `ln 2 / g`.
52. **Ruin arithmetic** (Wong, Poundstone): fixed-stake RoR = `((1−p)/p)^B`; ruin certain at p ≤ ½; proportional staking dissolves ruin — the justification for never sizing in fixed units.
53. **Staking-plan library** (Buchdahl *Fixed Odds*): level, percentage-bank, square-root, fixed-profit implemented for simulation; E[profit] = yield × turnover under all; loss-recovery (Martingale-family) structurally excluded.

### portfolio.py — joint sizing and fund accounting
54. **Simultaneous Kelly** (Poundstone): maximize `E[ln(1 + Σfᵢxᵢ)]` s.t. Σfᵢ ≤ 1; continuous approximation `F* = C⁻¹M`; single-asset Gaussian case `f* = μ/σ²`; correlated bets share one budget.
55. **Drawdown law** (Poundstone): at fraction c of full Kelly, `P(ever dip to x·W₀) = x^(2/c−1)`; full Kelly halves before doubling with prob 1/3. Audit trigger: realized drawdowns beyond predicted quantiles ⇒ reduce λ and c.
56. **Fund accounting** (Peta): `NAV_t = NAV_{t−1} + settled P&L`; max drawdown = max peak-to-trough/peak; Sharpe ≈ mean/σ of daily returns × √(days); exposure cap 2–3% NAV per game; pre-committed drawdown level triggers written model review.

### clv.py — validation and audit
57. **Closing line value** (Miller & Davidow, Buchdahl *S&S*, Mack, Pokerjoe): `CLV_EV = p_close·d_bet − 1` with p_close devigged from the market-maker close; probability form `p_close − 1/d_bet`; expected long-run ROI ≈ mean CLV.
58. **Significance test** (Buchdahl ×2): `t = (Y − Y₀)·√n/√(d̄ − 1)`; one-tailed p = 1 − Φ(t) (Student-t small n); minimum sample `n ≥ t*²·(d̄−1)/Y²` (t* = 1.64 @95%, 2.33 @99%).
59. **Volatility and profit horizon** (Buchdahl): per-bet σ = `d·√(p(1−p))` ≈ `√(d̄−1)`; `P(profit after n) ≈ Φ(Y√n/σ)`; run with Y = −margin for the luck-only baseline displayed beside every record.
60. **Luck-skill decomposition and shrinkage** (Buchdahl *S&S*): `Var(luck) ≈ (d̄−1)/n`; `Var(skill) = max(0, Var(obs) − Var(luck))`; `κ = Var(skill)/Var(total)`; `E[future] = μ_pop + κ(observed − μ_pop)`; `SE(p̂) = √(p(1−p)/n)`.
61. **Calibration / log-score** (Poundstone directive, Mack): log-score vs devigged closes measures the model's information rate — the channel capacity that bounds compounding.
62. **Runs test** (Winston): `E[runs] = 2WL/n + 1`; z-screen; |z| < 2 ⇒ momentum/streak features blocked from the model.

---

## What the Model Refuses to Do

Anti-patterns the ten books converge on, enforced structurally, not advisorily:

1. **No steam chasing.** Never bet the number a sharp move produced — the value is absorbed into the new price (Pokerjoe). Follow a move only at lagging books that still clear the EV gate, with persistence/multi-book confirmation against head-fakes.
2. **No betting into efficient closers without price advantage.** The devigged sharp close is presumed right; head-on main-line picks without a price edge are refused. Scanning priority is derivatives-first (Wong, Yao, Mack).
3. **No full Kelly, ever.** Fraction c capped at 0.5, default 0.25; no override may push effective stake above 1× Kelly; probabilities are shrunk toward the market before sizing because Kelly on an overestimated p is overbetting in disguise (Poundstone, Peta, Buchdahl).
4. **No parlays or teasers at retail hold.** Standard-payout parlays (10–12.5% house edge) and blind 6-point teasers (legs ~67% vs 72.4% hurdle) are auto-rejected; only individually +EV legs, correlated combos beating the joint price, or re-qualified key-number teasers are emitted (Winston, Wong, Yao, Buchdahl).
5. **No loss-linked sizing.** Martingale/recovery/chase logic is architecturally impossible: no code path may read cumulative losses into a stake (Buchdahl, Wong). Stakes re-anchor to current bankroll only.
6. **No resulting.** No component conditions on recent win/loss sequences; strategies are ordered and judged by CLV, calibration and shrunken estimates, never short-run ROI (Buchdahl *S&S*, Pokerjoe, Peta).
7. **No "profitable" labels without significance.** A strategy may not be reported profitable below the minimum-n from `n ≥ t*²(d̄−1)/Y²`; every record displays its probability of arising from pure luck (Buchdahl).
8. **No raw model probabilities into sizing.** Models earn weight only through demonstrated CLV; a model that cannot beat the close is a feature generator, not a probability source (Buchdahl *S&S*, Mack, Peta).
9. **No flat-cents half-point pricing and no overpaying key numbers.** Every half point is priced by outcome-reallocation parity / empirical mass; buying above ΔEV is refused (Wong, Yao, Miller & Davidow).
10. **No retail prices in the truth estimate.** Soft-book quotes are execution targets only; p_fair comes exclusively from limit-weighted market-maker prices (Miller & Davidow, Pokerjoe).
11. **No plain-normalization devig where favourite-longshot structure exists** — margin-weights (or power/Shin) devig is mandatory there; and apparent +EV longshots at soft books are treated as suspect, since that is where books bury margin (Buchdahl ×2).
12. **No momentum/streak features without a passing runs test; no RPI-style unweighted composites as inputs** (Winston).
13. **No default independence for same-game combinations.** Joint distributions price correlated legs; independence-by-default is refused (Winston, Yao, Wong).
14. **No hedging by default.** Hedges are priced insurance; the engine surfaces the EV cost and hedges only on bankroll-utility triggers or when the hedge is itself +EV (a scalp) (Wong, Yao).
15. **No ignoring account capacity.** Limits and account longevity are depletable capital; routing includes expected account-lifetime cost, and extraction/discovery roles are kept separate (Pokerjoe, Miller & Davidow).
16. **No unbounded backtest optimism.** Feature caps, walk-forward (never shuffled) validation, and deployment criteria pre-committed before the backtest runs (Mack).
