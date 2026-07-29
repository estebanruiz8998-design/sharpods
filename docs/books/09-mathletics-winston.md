# Mathletics: How Gamblers, Managers, and Sports Enthusiasts Use Mathematics

**Wayne L. Winston — Princeton University Press, 2009 (full first-edition title: *…in Baseball, Basketball, and Football*; second edition 2022, retitled *How Gamblers, Managers, and Fans Use Mathematics in Sports*, co-authored with Scott Nestler and Konstantinos Pelechrinis)**

---

## Why This Book Is Canon

*Mathletics* is the canon's **quantitative textbook**. The other books in this series are written by bettors about betting; Winston is an academic operations researcher — MIT-trained, Yale PhD, longtime professor of decision sciences at Indiana University's Kelley School of Business — who spent years inside professional sports as a consultant to Mark Cuban's Dallas Mavericks, where he and Jeff Sagarin built the WINVAL adjusted plus-minus system. The book is 50-odd short chapters, each posing one question ("Why is the Pythagorean theorem true for baseball?", "How do bookmakers really set lines?", "Was that collapse really improbable?") and answering it with a model the reader can rebuild in Excel. Part IV, "Playing with Money, and Other Topics for Serious Sports Fans" (chapters 38–46 of the first edition: Sports Gambling 101; Freakonomics Meets the Bookmaker; Rating Sports Teams; the parity, RPI, and point-ratings-to-probabilities chapters; the Kelly chapter; Ranking Great Sports Collapses), is the most direct bridge in print between academic sports statistics and the betting window.

Its unique contributions to a betting canon:

1. **The rating-system toolkit, done properly.** Least-squares (Massey-style) power ratings with a fitted home edge, solved by optimization rather than folklore — the machinery behind Sagarin-type ratings that bettors had used as a black box for decades.
2. **The margin-distribution bridge from ratings to prices.** Winston's normal-distribution model of game margins (σ ≈ 14 points NFL, ≈ 12 NBA around the predicted margin) converts any point rating into a win probability, a moneyline, a spread-cover probability, a teaser-leg probability, or a live in-game win probability — one distribution, every price.
3. **Sport-specific Pythagorean exponents** popularized for a wide audience: James's 2 for baseball, and Daryl Morey's 2.37 (NFL) and 13.91 (NBA), with the interpretation that scoring-ratio-implied wins beat actual wins as a forecast of future wins.
4. **The Levitt result on bookmaker behavior** — books do not simply balance action; they shade lines against known bettor biases — placed squarely in front of a mainstream audience.
5. **Institutional credibility.** Reviewed favorably by the MAA and widely adopted in university sports-analytics courses, it legitimized the entire enterprise; a generation of quant bettors and team analysts (the book predates the analytics-department boom) started here.

## Core Thesis

Nearly every interesting question in sports — who is better, by how much, what should we expect next, and what is a fair price — reduces to a tractable mathematical model that an intelligent amateur can build with regression, probability distributions, and a spreadsheet. Teams' true quality is best expressed as a **point rating** estimated by least squares from scoring margins; game outcomes are that rating differential plus home edge plus roughly normal noise; therefore probabilities for every derivative question (win, cover, tease, comeback, season total) fall out of one statistical framework. Applied to gambling, the same framework shows precisely why the standard menu (parlays, teasers, −110 spreads) is priced against the bettor, how accurate the market's lines really are, and that any sustainable edge must come from a model that out-predicts the line plus the vig — with Kelly's growth criterion governing how much to stake when it does.

## Key Concepts

*The treatment below is organized by theme, following the book's four parts (Baseball; Football; Basketball; Playing with Money).*

### 1. Pythagorean expectation with sport-specific exponents

Chapter 1 ("Baseball's Pythagorean Theorem") establishes the book's method in miniature: take James's rule that win fraction ≈ R² / (R² + 1) where R is the ratio of runs scored to runs allowed, test it against decades of MLB data (the exponent 2 predicts season wins with a mean absolute error of about two percentage points, roughly three wins per 162; Winston's own best-fit exponent is close to 1.9), and then generalize: Morey's fitted exponents are **2.37 for the NFL** and **13.91 for the NBA** (large because a given scoring ratio is far more informative in a high-scoring sport). The betting payload: **Pythagorean record predicts future record better than actual record does**, so teams whose win-loss record outruns their scoring ratio are regression candidates — a systematic signal for futures, season win totals, and early-season power priors. Later refinements (Pythagenpat's environment-dependent exponent) sharpen but do not change the idea.

### 2. Least-squares (Massey-type) power ratings and the home edge

Chapter 40 ("Rating Sports Teams") is the technical heart for bettors. Model each game's margin as

> home margin = home edge + (home team rating − away team rating) + error

and choose the ratings (and home edge) minimizing the sum of squared errors — solvable with Excel Solver or one regression, with ratings normalized to mean zero so a rating is "points better than average." Winston fits these for the NFL, NBA, and college sports, reports a **home edge of roughly 3 points in the NFL and NBA** (a bit higher in college), and emphasizes two production details: **weight recent games more heavily** (team quality drifts within a season) and consider **capping blowout margins** so garbage time doesn't distort ratings. He is candid about the punchline: his ratings' mean absolute prediction error comes out at about 13.5–14 points per NFL game — essentially indistinguishable from the Las Vegas line, which he shows is both accurate and nearly unbiased. The market is the benchmark to tie, not a soft target.

### 3. From point ratings to probabilities: the normal margin model

Chapter 43 supplies the conversion layer. Around any predicted margin, actual margins are approximately normal with a sport-specific standard deviation — **about 14 points in the NFL, about 12 in the NBA** (college hoops runs ≈ 10). Then the probability a team favored by m points wins outright is Φ(m/σ); fair moneylines follow from that probability; the probability of covering any alternate number s is Φ((m − s)/σ). This one approximation prices spreads from moneylines and vice versa, evaluates buying/selling points, and (see below) exposes teaser and parlay pricing. Its known defect — margins are discrete with mass spikes at key numbers (3 and 7 in the NFL) — is exactly where the continuous model must be patched with empirical margin frequencies.

### 4. Sports Gambling 101: vig, parlays, and teasers

Chapter 38 covers mechanics with the arithmetic made explicit: laying −110 means risking 11 to win 10, so the breakeven win rate is 11/21 ≈ **52.4%**; a bettor with no edge loses the vig at a rate of about 4.5% of dollars bet. American moneylines convert to implied probabilities, and the overround (the two sides' implied probabilities summing past 1) is the book's margin. **Parlays**: a two-team parlay at the standard 13/5 payout against fair odds of 3/1 (for 50/50 legs) gives the house 10%; three-team at 6/1 versus fair 7/1 gives 12.5% — multiplying negative-edge bets compounds the edge against you. **Teasers**: moving the line 6 points looks generous, but through the normal margin model a 6-point tease lifts a 50% leg only to about Φ(6/14) ≈ 66–67%, while a two-team teaser at −110 needs each leg at √0.5238 ≈ **72.4%** — standard teasers are firmly −EV. (The exception the community later formalized as the Wong teaser — legs that cross both 3 and 7 — is a key-number effect invisible to the continuous model, which is precisely Winston's point about where the approximation breaks.)

### 5. How bookmakers actually set lines (Freakonomics Meets the Bookmaker)

Chapter 39 presents Steven Levitt's 2004 study: contrary to textbook lore, books do **not** move lines to balance action 50/50. They exploit predictable bettor biases — the public overbets favorites and glamour sides — by shading lines and letting the imbalance ride, because the biased money loses more than balanced action would earn in vig. Consequences for a modeler: (a) the closing line is a strong but not perfectly unbiased estimator — small systematic biases (historically, home underdogs covering slightly over 50%) can persist because they are profitable for the book to leave in; (b) beating the market means beating a price deliberately set where the public is most wrong, so contrarian value concentrates against popular sides; (c) any such documented bias decays once publicized — Winston's own framing warns these edges are small and transient.

### 6. Kelly money management

Chapter 44 ("Optimal Money Management: The Kelly Growth Criteria") derives the stake that maximizes expected logarithmic growth of the bankroll: bet the fraction f* = (edge)/(odds) of your bankroll — for a bet winning with probability p at b-to-1 payoff, f* = (bp − q)/b. Winston explains the properties that matter: Kelly maximizes long-run geometric growth, never risks ruin (stakes shrink with the bankroll), and overbetting beyond Kelly strictly reduces growth while inflating variance — the asymmetry that justifies the professional practice of betting a *fraction* of Kelly when p is only an estimate.

### 7. In-game win probability and the mathematics of collapses

Several threads make up the book's live-betting toolkit. In baseball, **Player Win Averages** (the Mills brothers' idea) values every event by the change in win probability from a state table — the ancestor of modern WPA and of live pricing by state. In football, Winston builds **state-and-value models** (expected points by down, distance, and field position, computed by dynamic-programming logic) and uses them for fourth-down, two-point-conversion, and play-calling questions in the spirit of Romer — the machinery a live totals/spread model needs. And in "Ranking Great Sports Collapses" (chapter 45) he quantifies comebacks: season-level collapses via the probability of losing a lead given per-game win probabilities and games remaining (simulation/binomial logic), and in-game leads via the normal/Brownian-motion approximation (popularized by Hal Stern): a lead of L points with fraction f of the game left, for a team expected to win the whole game by μ, survives with probability Φ((L + μf)/(σ√f)). Related basketball chapters analyze end-game strategy (e.g., when to foul, when a trailing team should take threes).

### 8. Player valuation and per-possession thinking

The baseball part builds Runs Created, **linear weights** (regression of team runs on singles, doubles, triples, homers, walks, steals), Monte Carlo simulation of innings to value hitters, DIPS-style pitcher evaluation, park factors, and replacement value. The basketball part is built on **points per 100 possessions** (offensive/defensive efficiency, which Winston stresses over raw per-game stats because pace confounds them) and **adjusted plus-minus** (WINVAL): regress score margin per stint on indicators for the ten players on the floor, so each player's coefficient is his net point impact holding teammates and opponents fixed. For a betting model these are the input layers for totals, derivatives, and injury/lineup repricing: efficiency-per-possession × pace is the correct decomposition of a basketball total, and adjusted plus-minus is the correct currency for "how many points is this player's absence worth?"

### 9. Rating-system criticism: RPI, parity, and payroll

Chapter 42 dissects the NCAA's **RPI** (0.25 × win% + 0.50 × opponents' win% + 0.25 × opponents' opponents' win%) and shows why it is inferior: it ignores margin of victory and game location and is gameable through scheduling — least-squares/Sagarin-type ratings dominate it. Chapter 41 measures **parity** by comparing the spread of team ratings to the randomness of single games, finding the NFL far more compressed than the NBA (where the better team wins much more often). Chapter 46 finds the payroll–wins relationship real but loose. The transferable lesson: judge any rating input by out-of-sample predictive error against margins, not by pedigree.

### 10. Forensics: hot hands, biased whistles, fixed games

Winston devotes chapters to streakiness (runs-test analysis in the Gilovich–Vallone–Tversky tradition, concluding evidence for momentum/hot hands is weak to nonexistent), the Price–Wolfers own-race referee-bias study, Wolfers's point-shaving analysis of college basketball spreads, and the Donaghy affair. For a bettor the punchlines are: do not price momentum (but do fade lines that do); small officiating and situational biases (fatigue, back-to-backs, rest — which Winston also quantifies for the NBA) are real, measurable, and belong in a model as features rather than narratives.

### 11. What the second edition adds (2022)

With Nestler and Pelechrinis, the second edition modernizes the toolkit: chapters on soccer, golf, volleyball, and e-sports; gambling Calcuttas; player-tracking/camera data; **Bayesian inference and ridge regression** (the fix that turned adjusted plus-minus into RAPM); expanded win-probability and rating material, including Elo-style dynamic ratings and logistic-regression win models that had become the community standard in the intervening decade; and updated daily-fantasy/betting-market context post-PASPA. For SharpOds the second edition is the better spec of "the same book, with the estimation techniques the field actually uses now."

## The Math

Notation: PF/PA = points (runs) for/against; R = PF/PA; m = predicted margin; σ = sport-specific margin SD; Φ = standard normal CDF; p = win probability; d = decimal odds.

**1. Pythagorean expectation (sport-specific exponent x)**

```
Win% = PF^x / (PF^x + PA^x) = R^x / (R^x + 1)
x: MLB ≈ 2 (Winston's best fit ≈ 1.9), NFL ≈ 2.37, NBA ≈ 13.91 (Morey)
Pythagenpat refinement: x = ((PF + PA)/G)^0.287   (G = games; use for MLB run environments)
Predicted wins = Win% × season games. Regression signal: (actual wins − Pythag wins)
is mostly luck; forecast future performance from Pythag, not actual, record.
```

**2. Least-squares (Massey) power ratings with home edge**

```
For each game g (home team i, away team j):
   margin_g = h + r_i − r_j + ε_g
Fit r (all teams) and h by minimizing Σ_g ε_g²  subject to Σ_t r_t = 0.
Options Winston endorses: exponential recency weighting w_g = φ^(days ago) with φ < 1,
and truncating |margin| at a cap (≈ 20–24 pts) to limit blowout influence.
Predicted spread of a new game: m̂ = h + r_i − r_j   (i at home)
Home edge h ≈ 3 points (NFL, NBA); re-fit per league and season.
Residual SD σ from the fit: NFL ≈ 14, NBA ≈ 12, NCAAB ≈ 10 — re-estimate, don't assume.
```

**3. Ratings/spreads to probabilities (normal margin model)**

```
P(team favored by m wins outright)      = Φ(m / σ)
P(favorite of m covers spread s)        = Φ((m − s) / σ)     [continuous approx.]
Fair decimal moneyline for that team    = 1 / Φ(m / σ)
Spread ↔ moneyline conversion: given a market moneyline prob p, implied margin m = σ · Φ⁻¹(p).
Correction: for NFL spreads near key numbers (3, 7), replace the continuous normal with
empirical margin mass; the normal misprices pushes and hooks there.
```

**4. Odds, vig, and breakeven**

```
American → implied probability: p = A/(A+100) for −A;  p = 100/(B+100) for +B
Breakeven at −110: p_be = 110/210 = 0.5238
Devig a two-way market: p_fair,i = p_imp,i / (p_imp,1 + p_imp,2)
EV per unit staked at decimal d: EV = p·d − 1
```

**5. Parlay pricing**

```
Fair payout for n independent legs with probs p_1…p_n:  d_fair = Π (1/p_i)
House edge = 1 − (offered payout + 1) / (fair payout + 1)   [for "X/1"-quoted payouts]
Standard −110 legs (p = 0.5): 2-team pays 13/5 vs fair 3/1 → edge 10%;
3-team pays 6/1 vs fair 7/1 → edge 12.5%.
Correlated legs (same-game): replace Π p_i with joint probability from the margin/total model.
```

**6. Teaser evaluation**

```
Teaser leg win probability (t-point tease of a fair line): p_leg ≈ Φ(t / σ)
   NFL, t = 6, σ = 14: p_leg ≈ Φ(0.43) ≈ 0.666
Two-team teaser at −110 requires p_leg ≥ sqrt(0.5238) = 0.7238  → standard teasers are −EV.
Decision rule: price each teased leg off the *empirical* margin distribution; only bet
when Π p_leg,empirical > breakeven (legs crossing both 3 and 7 are the historical exception).
```

**7. Kelly criterion (Optimal Money Management)**

```
Bet paying b-to-1, win prob p, q = 1 − p:  f* = (b·p − q) / b = p − q/b
Decimal-odds form: f* = (p·d − 1) / (d − 1)
Growth rate at fraction f: g(f) = p·ln(1 + b·f) + q·ln(1 − f); f* maximizes g.
Properties: f* > 0 iff EV > 0; betting 2f* zeroes growth; stake fractional Kelly
(c·f*, c ≈ 0.25–0.5) because p is an estimate.
```

**8. In-game win probability (normal / Brownian approximation)**

```
Lead L for team A, fraction f of game remaining, full-game predicted margin μ for A:
   P(A wins) = Φ( (L + μ·f) / (σ · sqrt(f)) )
σ = full-game margin SD (formula 2). At f = 1, L = 0 this reduces to formula 3.
Use per-possession/state models (expected points by down-distance-field position;
baseball base-out-inning win expectancy tables i.e. Player Win Averages) when
state granularity matters; the Brownian formula is the fallback pricer.
```

**9. Elo-style dynamic rating (second-edition-era complement to formula 2)**

```
Expected score: E_A = 1 / (1 + 10^(−(R_A − R_B + HFA_elo)/400))
Update after result S_A ∈ {0, ½, 1}:  R_A ← R_A + K · M · (S_A − E_A)
K per sport (NFL ≈ 20, NBA ≈ 20, MLB ≈ 4–6); M = margin multiplier,
e.g. M = ln(|margin| + 1) · (2.2 / (0.001·ΔR_winner + 2.2))  (FiveThirtyEight form).
Map rating gap to points via the empirical points-per-Elo slope, then price via formula 3.
```

**10. Ratings Percentage Index (known-bad benchmark)**

```
RPI = 0.25·WP + 0.50·OWP + 0.25·OOWP
(WP = team win%, OWP = opponents' win% excluding games vs the team, OOWP = opponents' OWP.)
Included as an anti-pattern: no margin, no venue, gameable — never use as a model input;
use it only to model how committees/selection processes behave.
```

**11. Linear weights and per-possession efficiency (input layers)**

```
Team runs ≈ β0 + β_1B·1B + β_2B·2B + β_3B·3B + β_HR·HR + β_BB·(BB+HBP) + β_SB·SB + β_CS·CS
(fit on team-seasons; canonical fits ≈ 0.5, 0.7, 1.0, 1.4, 0.33, +0.2, −0.4)
Basketball: OffEff = 100·Pts/Poss;  Poss ≈ FGA − ORB + TO + 0.44·FTA
Game total ≈ pace_estimate × (OffEff_A vs DefEff_B blend + OffEff_B vs DefEff_A blend)/100
Adjusted +/− (WINVAL): stint margin per possession regressed on on-court player indicators;
modern practice adds ridge penalty λ‖β‖² (RAPM).
```

**12. Runs test for streakiness (hot-hand screen)**

```
Sequence of W wins and L losses, n = W + L:
E[runs] = 2WL/n + 1;   Var[runs] = 2WL(2WL − n) / (n²(n − 1));   z = (observed − E)/sqrt(Var)
|z| < 2 for nearly all teams/players ⇒ no exploitable streakiness; do not price momentum.
```

## Strengths and Limitations

**Strengths**

- **The most complete single-volume toolkit in the canon.** Ratings, probability conversion, gambling arithmetic, valuation, in-game states, and money management in one place, every model reproducible in a spreadsheet. It is the reference the other canon books implicitly assume.
- **Authority.** Winston built real systems for a real NBA franchise (WINVAL); the book's methods are the published layer of professional practice circa 2009, not speculation.
- **Correct market epistemics for its era.** Winston demonstrates rather than asserts that Vegas lines are accurate and nearly unbiased, that the standard betting menu is priced against you, and that parlays/teasers compound the house edge — and he shows the computations.
- **The margin-distribution insight** — one normal model priced off a power rating generating every derivative probability — remains the architecture of most production pricing engines; only the estimators around it have changed.
- **Intellectual honesty**: chapters that debunk (hot hand, RPI, momentum narratives) are as prominent as chapters that build.

**Limitations and what has aged**

- **It is a textbook, not a betting manual.** There is no treatment of closing line value, line shopping, devigging as a workflow, bet timing, limits, or record-keeping discipline — the operational layer belongs to Wong, Miller/Davidow, and Buchdahl. Winston tells you how to compute a fair price, not how to run a betting operation.
- **Estimation methods are pre-modern.** OLS point estimates without regularization or uncertainty; WINVAL-style adjusted +/- was superseded by ridge/Bayesian RAPM (a fix the 2022 edition itself adopts); static least-squares ratings are now typically replaced or ensembled with Elo/state-space (Kalman) ratings that update online; logistic/gradient-boosted in-game models outperform the Brownian approximation, which survives as a sanity check and cold-start fallback.
- **Fixed Pythagorean exponents** were refined by Pythagenpat (environment-dependent exponent); rule changes (NFL extra-point distance, pace-and-space NBA, three-point volume) shift home edges, σ values, and key-number masses, so every constant in the book (h ≈ 3, σ ≈ 14/12, teaser cover rates) must be re-fit, not copied — indeed the measured NBA home edge has drifted well below 3 since 2009.
- **The continuous normal margin model misprices key numbers**, which Winston acknowledges implicitly; empirical margin distributions are mandatory for NFL spread derivatives.
- **2009 data throughout the first edition**, and the gambling landscape it describes (Nevada-centric, pre-PASPA-repeal, no liquid exchanges or same-game parlays) is historical; the second edition modernizes content but still stops short of market microstructure.
- Excel/Solver as the implementation vehicle is pedagogy, not architecture.

## What SharpOds Takes From This Book

Winston supplies SharpOds' **ratings-and-conversion layer**: how team strength becomes a price for every market.

1. **Implement the Massey least-squares rating engine (formula 2) for every margin sport**, with fitted (not assumed) home edge per league-season, exponential recency weighting, blowout capping, and ridge regularization; normalize ratings to mean zero so rating units are points. Run it alongside an Elo engine (formula 9); ensemble them, and require any fancier rating to beat both out-of-sample on margin MAE before promotion.
2. **Route every price through the margin-distribution layer (formula 3)**: maintain per-sport, per-season estimates of σ (re-fit from rating residuals; expect ≈ 13–14 NFL, ≈ 11–12 NBA, ≈ 10 NCAAB) and price moneylines, spreads, alternate lines, and live states from the same distribution — with the NFL using an empirical discrete margin distribution around key numbers 3 and 7 instead of the raw normal.
3. **Use sport-specific Pythagorean records (formula 1) as the regression-to-mean prior**: exponents 1.83–2.0 MLB (Pythagenpat), 2.37 NFL, 13.91 NBA; feed Pythag wins (never actual wins) into season-total and futures pricing, and flag teams with |actual − Pythag| ≥ ~2 SD as fade/back candidates at market prices that anchor on actual record.
4. **Build the derivative-pricing guardrails from formulas 5–6**: every parlay/teaser is priced from joint leg probabilities (correlated legs via the joint margin/total model, never independence-by-default); auto-reject any teaser whose empirically priced legs fall below the breakeven (0.7238 per leg for two-team −110), and only surface teaser bets where the empirical cover probability clears breakeven plus a margin — i.e., key-number-crossing legs.
5. **Ship the Brownian in-game model (formula 8) as the live-pricing fallback and sanity check**: any ML live model whose output diverges from Φ((L + μf)/(σ√f)) by more than a tolerance without a state-based reason (possession, red zone, foul situation) gets flagged before quoting.
6. **Encode the Levitt lesson as a feature, not a slogan**: model the *direction of public bias* per market (favorites, overs, glamour teams) and treat the closing line as a strong prior that can carry small persistent shading; SharpOds' bias-correction terms must be fit on data and decay-tested, since published biases (e.g., the old home-dog edge) demonstrably shrink after publication.
7. **Adopt Winston's input decompositions**: basketball totals priced as pace × per-100 efficiency matchups with adjusted plus-minus (ridge/RAPM) driving injury and lineup repricing; MLB run expectation from linear-weights-style event values; football situational values from an expected-points state model (formula 11 and concept 7).
8. **Institutionalize the debunking chapters**: no momentum/streak features without passing a runs-test-style screen (formula 12) on historical data; RPI and any unweighted win-percentage composite are banned as model inputs (allowed only when modeling committee behavior); rest/fatigue and schedule-spot effects are included as fitted features because Winston shows they are real and quantifiable.
