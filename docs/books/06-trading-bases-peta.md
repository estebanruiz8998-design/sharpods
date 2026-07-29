# Trading Bases: A Story About Wall Street, Gambling, and Baseball

**Joe Peta — Dutton (Penguin Group), New York, 2013 (ISBN 978-0525953647; full subtitle "A Story About Wall Street, Gambling, and Baseball (Not Necessarily in That Order)"); 2014 paperback retitled *Trading Bases: How a Wall Street Trader Made a Fortune Betting on Baseball* (ISBN 978-0451415172)**

---

## Why This Book Is Canon

Joe Peta spent roughly a decade trading equities at Lehman Brothers, moved to Nomura after Lehman's 2008 collapse, and then lost that job too after being struck by an ambulance in Manhattan in January 2011 — an accident that shattered his leg and left him in a wheelchair. Confined to his apartment during the 2011 season, he built a quantitative MLB betting model, raised money from friends, and ran the operation exactly like the hedge funds he had traded for: daily NAV, position limits, investor letters, risk-adjusted performance reporting. The fund returned **+41% on the 2011 season** (with, per the publisher's account, a maximum drawdown of about 5%), and he ran it profitably again in 2012 while writing the book. *Trading Bases* is the narrative and the methodology together.

Its unique contributions to the sharp betting canon:

1. **It is the only canonical book that walks through building a full-season, market-beating projection model for one sport, end to end.** Wong, Yao, Miller/Davidow, and Buchdahl teach market mechanics and betting theory; Peta shows the entire modeling pipeline — from raw team statistics, through luck-stripping, to game-level probabilities and a graded bet card — for MLB, the most model-friendly betting market in American sports (moneyline pricing, 2,430 games a season, the deepest public statistical record in sports).
2. **It coined and operationalized "cluster luck."** The insight that run *totals* are contaminated by the random sequencing of hits — and that the contamination is measurable and mean-reverting — existed in sabermetrics (runs created, BaseRuns, DIPS), but Peta named it, quantified it team by team, and made it the engine of a betting model. The term is now standard vocabulary in baseball analytics and betting.
3. **It imported Wall Street portfolio discipline into sports betting.** Bet sizing as fraction of NAV, drawdown limits, process-versus-outcome evaluation, volatility and Sharpe-style reporting, and the framing of each team as a mispriced security — Peta treats a betting bankroll as a fund with an investment mandate, and shows what that looks like operationally, day by day, for a full season.
4. **It is an honest public track record.** Peta published his projections (the book carries his full 2012 team-by-team forecasts), his daily results, his losing streaks, and his mistakes. Sabermetric reviewers (notably Phil Birnbaum) were able to audit the claimed edge precisely *because* the record was so transparent — a standard of disclosure almost no betting author meets.

## Core Thesis

A baseball team's won-lost record and run totals are noisy outputs of a more stable underlying skill process, and the market prices the noise along with the signal. Strip the luck out — cluster luck in run-scoring, Pythagorean deviation in converting runs to wins — rebuild each team's true talent from the sum of its players' expected contributions (WAR), and you can price every game more accurately than the moneyline does. Then the problem stops being handicapping and becomes portfolio management: bet only when your price and the market's price diverge, size positions as small fractions of capital, expect and survive brutal variance, and judge yourself on process and risk-adjusted return, exactly as a disciplined trading desk would.

## Key Concepts

### 1. Baseball as the ideal betting market

Peta chose MLB deliberately. Moneyline pricing means no point-spread distortion: you bet on who wins, at a price, exactly like buying a stock. The season provides 2,430 games — a sample large enough for a small edge to compound and for skill to be statistically distinguishable from luck within a single year. Odds live in a narrow band (roughly −250 to +200), limiting the favourite–longshot extremes. And baseball's statistical record is uniquely deep and uniquely decomposable: the sport is a sequence of discrete pitcher-batter events, which is why luck can actually be isolated. He frames the 30 franchises as 30 equities whose "earnings" (true talent) he can estimate better than the consensus.

### 2. Cluster luck: sequencing is noise

Peta's signature concept. Run scoring depends not just on how many hits, walks, and extra-base hits a team produces, but on how they *cluster*: ten singles spread across nine innings can score zero runs; three of them bunched in one inning score two or three. Hitters demonstrably control their rates of reaching base and hitting for power; no one controls the sequencing. So Peta computes each team's **expected runs** from its underlying rate stats (in the book, a regression built on on-base and slugging components — effectively "hits per run"), and calls the gap between actual and expected runs **cluster luck**, on both sides of the ball (runs scored and runs allowed). Cluster luck has essentially zero year-over-year persistence, so a team that scored 60 runs more than its components justify should be projected off the *component* number, not the actual one. His flagship demonstration: the 2010 Rays' offense was heavily cluster-lucky, and his model called for them to score roughly 100 fewer runs in 2011 — they scored 95 fewer. Modern implementations of the same idea use David Smyth's **BaseRuns** estimator (the approach FanGraphs uses), which is cleaner than Peta's regression and is the recommended substitute.

### 3. Pythagorean expectation: converting runs to wins, and one-run-game luck

The second luck filter is Bill James's Pythagorean theorem: a team's expected winning percentage is determined by its runs scored and runs allowed (see The Math). Deviations between actual record and Pythagorean record — driven largely by one-run-game results and bullpen timing — are, like cluster luck, overwhelmingly non-persistent. A 90-win team that "should" have won 84 games by run differential is an 84-win team for projection purposes. Stacking the two filters gives Peta's core cleansing operation: **actual record → Pythagorean record → cluster-luck-adjusted Pythagorean record**, which is the best simple estimate of what last season's roster truly was.

### 4. WAR-based roster adjustment: from last year's team to this year's team

Last season's cleansed record describes last season's roster. Peta then adjusts for offseason player movement using **Wins Above Replacement**: sum the WAR of departing players, sum the WAR of arriving players, and shift the team's projected win total by the difference (with the standard sabermetric identity that a full-replacement roster wins roughly 47–48 games, so team wins ≈ replacement baseline + total WAR, and ~10 runs of value ≈ 1 win). A noted and conceded weakness: Peta used players' *prior-season actual* WAR rather than regressed projections — he states explicitly that he assumed the previous 162 games were the best indicator of the next season, with no regression to the mean, no aging curve, and no injury modeling. This is the part of the pipeline modern practice most clearly supersedes (see Strengths and Limitations).

### 5. The daily game model: starter annualization and matchup probability

Season win projections become game probabilities in two steps. First, the **starting pitcher adjustment**: a team's season-strength number embeds its whole rotation, but tonight only one starter matters. Peta's device is annualization — remove the rotation's aggregate contribution and add back today's starter *as if he pitched every day*: since a starter makes roughly one of every five starts, his full-season WAR is multiplied by ~5 when he's the one on the mound. A .400 team with an ace going can genuinely be a .500+ team tonight. Second, the two adjusted team strengths are combined into a head-to-head win probability (a log5/Bill James matchup calculation) with home-field advantage applied (MLB home teams win ~54% over the long run). As the season progresses, Peta gradually blends actual current-season performance into the preseason projection, so that by season's end the model runs almost entirely on the current year's (luck-adjusted) data.

### 6. Betting only the divergence, and sizing like a risk manager

The model's probability is compared with the moneyline's implied (devigged) probability; a bet exists only when the divergence clears a threshold, and the stake scales with the size of the edge. Peta explicitly invokes Kelly-style thinking — balancing ruin risk against compound growth, betting fractions of a growing bankroll — but implements it conservatively and somewhat informally, with tiered stakes that were tiny fractions of NAV (Birnbaum noted bets as small as 0.1% of bankroll and argued the sizing was inefficiently timid given the claimed edges). The portfolio framing is the point: dozens of small, roughly independent positions per week, no position large enough to threaten the fund, no chasing, no doubling after losses.

### 7. Running it as a fund: NAV, drawdown, Sharpe, process over outcome

Peta ran the operation with hedge-fund mechanics: outside capital from friends, a daily marked NAV, periodic investor letters, and performance reported in risk-adjusted terms (volatility and Sharpe-ratio framing borrowed directly from his equity-desk life) rather than in tout-style win percentages. The Wall Street chapters double as the book's risk-management curriculum: the Lehman collapse as a lesson in leverage and correlated exposure; the trading-desk lesson that a good process losing money is not a bad decision, and a bad process winning money is not a good one; the insistence that variance must be pre-committed to — his fund's worst drawdown stayed near 5% by design, not luck.

### 8. Respecting the market

Though the book predates the popularization of closing-line-value discipline, Peta treats the betting market as a mostly efficient consensus that is beatable only at the margin and only with information handled better than the consensus handles it. He looks for structural reasons the line is off (market inertia on luck-inflated teams, public overreaction to name-brand rosters) rather than assuming wholesale market stupidity. Post-publication audits sharpened this point: Birnbaum's analysis concluded that when Peta's price diverged from the market's by 4%, the true expected edge was closer to 1% — i.e., the market deserved roughly three-quarters of the weight — and that a meaningful share of the 41% return was variance (in Birnbaum's simulation, about 25 of 1,000 zero-skill seasons cleared +28.8%). The method was judged genuinely profitable, but with an edge perhaps a quarter of its naive size.

## The Math

Notation: `RS` = runs scored, `RA` = runs allowed, `G` = games, `W%` = winning percentage. Odds conversions use American odds `L` and decimal odds `d`.

**1. Pythagorean expectation (Bill James), and modern exponents**

```
W% = RS^x / (RS^x + RA^x)
Expected wins = 162 * W%
```
- Classic James: `x = 2`; refined fixed exponent: `x = 1.83`.
- Pythagenpat (preferred, run-environment-aware): `x = ((RS + RA) / G)^0.287`.
- Luck residual: `Pythag deviation = actual wins − expected wins` (non-persistent; forecast value ≈ 0).

**2. Cluster luck**

```
CL_offense = RS_actual − RS_expected
CL_defense = RA_actual − RA_expected
```
where `RS_expected` (and `RA_expected`, computed from opponents' events against the team) comes from a component run estimator. Peta used a regression of team runs on OBP/SLG-type components; implement instead with **BaseRuns** (simple team-season form):

```
A = H + BB − HR                      (baserunners)
B = (1.4*TB − 0.6*H − 3*HR + 0.1*BB) * 1.02   (advancement)
C = AB − H                           (outs)
D = HR
BaseRuns = A * B / (B + C) + D
```
Projection rule: replace `RS_actual`/`RA_actual` with `RS_expected`/`RA_expected` everywhere downstream; treat `CL` as noise with zero carry-forward.

**3. WAR-to-wins identity and roster adjustment**

```
Team wins ≈ 47.7 + Σ WAR_i          (replacement-level team ≈ .294 W%, i.e. ~47.7 wins)
ΔWins(offseason) = Σ WAR_incoming − Σ WAR_outgoing
Runs-to-wins: ΔWins ≈ ΔRuns / RPW,  RPW ≈ 9–10  (Tango: RPW = 1.5*(league runs per game, both teams) + 3)
```
Peta used prior-season actual WAR for `WAR_i`; superseded practice is to use regressed projections (see Limitations).

**4. Game-day starter annualization**

```
W_team_ex_rotation = W_projected − Σ WAR_rotation
W_team_tonight = W_team_ex_rotation + 5 * WAR_starter
p_raw = W_team_tonight / 162
```
The factor 5 annualizes the starter (he normally provides ~1/5 of team starts); `WAR_starter` should be a full-season (projected) figure. Apply to both teams.

**5. Log5 matchup with home-field advantage**

```
Log5:  p(A beats B) = pA*(1−pB) / (pA*(1−pB) + pB*(1−pA))
```
Home advantage via odds ratio, with `h ≈ 0.54` (long-run MLB home win rate):

```
OR = [pA/(1−pA)] * [(1−pB)/pB] * [h/(1−h)]
p_home = OR / (1 + OR)
```

**6. In-season blending of projection and results**

Peta describes a gradual mix from 100% preseason projection to ~100% current-season (luck-adjusted) data. Standard implementation — pad the observed record with `k` games of the prior:

```
p_blend = (k * p_preseason + G_played * p_observed_adjusted) / (k + G_played),   k ≈ 60–70
```

**7. Moneyline conversion and devigging**

```
Implied probability:  q = |L| / (|L| + 100)   if L < 0
                      q = 100 / (L + 100)     if L > 0
Decimal odds:         d = 1 + 100/|L| (L<0);  d = 1 + L/100 (L>0)
Two-way devig (multiplicative): q_fair_i = q_i / (q_home + q_away)
```

**8. Market-shrunk edge and bet trigger (Birnbaum correction)**

```
p_final = λ * p_model + (1 − λ) * q_fair          (λ ≈ 0.25 for a Peta-class model)
Edge = p_final * d − 1
Bet iff Edge > threshold (threshold > 0 after vig; e.g. 1–2%)
```

**9. Kelly sizing (referenced by Peta; implement fractionally)**

```
f* = (p*d − 1) / (d − 1)      fraction of bankroll at decimal odds d
Stake = c * f*,  c ≈ 0.25–0.5 (fractional Kelly), with a hard per-game cap on NAV at risk
```

**10. Fund accounting**

```
NAV_t = NAV_{t−1} + Σ (settled P&L of day t)
Return = (NAV_end / NAV_start) − 1
Max drawdown = max over t of (peak NAV to date − NAV_t) / peak NAV
Sharpe ≈ (mean daily return − rf) / stdev(daily return) * sqrt(days per season)
```

## Strengths and Limitations

**Strengths**

- **The luck-decomposition pipeline is real and still works.** Cluster luck (BaseRuns residuals) and Pythagorean deviation remain among the most robust mean-reversion signals in baseball; they are the backbone of every serious public MLB projection today.
- **The portfolio discipline is timeless.** Daily NAV, pre-committed sizing, drawdown tolerance, process-over-outcome review — no other canonical book demonstrates the operational side of betting-as-fund-management this concretely.
- **Radical transparency.** Full projections and full results published; the model is falsifiable and was in fact independently audited.
- **Sport selection logic** (moneyline market, huge sample, decomposable statistics) is a genuinely transferable meta-lesson for choosing where to deploy a model.

**Limitations and what has aged poorly**

- **No regression to the mean in player inputs.** Peta fed prior-season raw WAR forward, by his own admission. Modern projection systems (ZiPS, Steamer, PECOTA, THE BAT) regress, age-adjust, and blend multiple seasons; they strictly dominate this step. Reviewers flagged this at publication and it remains the model's clearest technical flaw.
- **The claimed edge was overstated by variance.** Birnbaum's audit: model-market divergences needed ~75% shrinkage toward the market (a 4-point gap ≈ 1 point of real edge), and roughly 2.5% of zero-skill simulated seasons beat +28.8% — the +41% season was skill *plus* a favourable draw. The method beat the market; it did not beat it by 41% a year in expectation.
- **WAR is a blunt game-level instrument.** It is cumulative, mixes noisy defensive components, and ignores matchup detail. Modern game models price the actual lineup versus the actual starter with platoon splits, park factors, weather, umpire, bullpen availability, and catcher framing — granularity Peta's team-level model never had.
- **Sizing was ad hoc.** Tiered stakes down to 0.1% of NAV are not an optimal response to a quantified edge; the book gestures at Kelly without implementing it.
- **The market has hardened.** 2011 MLB lines were softer than today's; sharp books now price from projection systems themselves, and limits/segmentation punish winners faster. A pure Peta-2011 replica should be presumed to have no edge against 2020s closing lines.
- **No closing-line-value framework.** Peta evaluates by P&L alone; the CLV discipline of Miller/Davidow and Buchdahl is the superior day-to-day skill diagnostic and postdates his season.

## What SharpOds Takes From This Book

1. **Luck-strip every team input before it touches a projection.** For MLB: replace actual RS/RA with BaseRuns-expected RS/RA (Formula 2), then convert to expected record with Pythagenpat (`x = ((RS+RA)/G)^0.287`). Carry forward zero weight on cluster-luck and Pythag residuals. Apply the same "decompose, find the non-persistent component, delete it" pattern in every sport we model.
2. **Build team priors bottom-up from player value: `wins = 47.7 + Σ WAR`,** but source `WAR` from regressed multi-season projections (Steamer/ZiPS-class), never raw prior-season figures — adopting Peta's architecture while fixing his acknowledged no-regression flaw.
3. **Price the game, not the team:** remove the rotation aggregate, annualize tonight's starter at 5× projected WAR (Formula 4), combine strengths via log5 with home advantage `h ≈ 0.54` applied through the odds ratio (Formula 5).
4. **Blend to the season as it happens:** weight preseason priors versus observed (luck-adjusted) results by `k/(k+G)` padding with `k ≈ 60–70` games, so early-season lines are challenged with priors and late-season lines with cleansed actuals.
5. **Shrink toward the market before betting.** Final probability = `0.25 * p_model + 0.75 * q_fair(devigged)` as the starting calibration for any Peta-class team model, per Birnbaum's audit; re-estimate λ out-of-sample per sport. Bet only when the shrunk edge still clears the vig plus a 1–2% threshold.
6. **Size like the fund, not the tout:** fractional Kelly (25–50%) on the shrunk edge, hard cap per game (≤2–3% of NAV), minimum-stake floor to avoid meaningless dust positions, and an explicit pre-committed max-drawdown tolerance that triggers review, not tilt.
7. **Account like a fund:** daily NAV, full bet-level logs, rolling Sharpe and max drawdown, and periodic written performance reviews — with CLV added as the primary process metric Peta lacked.
8. **Deploy models where the market structure favors them,** per Peta's sport-selection logic: prefer moneyline (win-probability) markets with large seasons and decomposable event-level statistics, where luck can be measured and priors compound over thousands of bets.
