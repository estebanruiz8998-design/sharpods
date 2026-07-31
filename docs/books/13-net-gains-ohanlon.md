# Net Gains

**Ryan O'Hanlon — Abrams Press, New York, 2022 (ISBN 978-1419758911; full title *Net Gains: Inside the Beautiful Game's Analytics Revolution*)**

---

## Why This Book Is Canon

Ryan O'Hanlon is ESPN's analytics-minded soccer writer (previously The Ringer and FiveThirtyEight-adjacent work, plus the *No Grass in the Clouds* newsletter). *Net Gains* is the definitive journalistic account of soccer's data revolution — the New York Times picked it as one of ten books to read during the 2022 World Cup — built on access to the people who actually ran it: Ian Graham and William Spearman of Liverpool's research group, Sarah Rudd of StatDNA/Arsenal, Luke Bornn (AS Roma), Ted Knutson (StatsBomb), Chris Anderson (*The Numbers Game* co-author who briefly ran Coventry City), and even Ashwin Raman, the Indian teenager hired off Twitter to scout for Dundee United.

Soccer is the largest sports betting market on earth — by most estimates the majority of global handle — and SharpOds' canon so far is overwhelmingly American-sport and market-theory books. *Net Gains* is the soccer entry, and it earns canon status on four counts:

1. **It is the best available history and explanation of expected goals (xG)** — the load-bearing statistic of all modern soccer modeling and pricing — from Charles Reep's 1950s notational analysis through Opta event data to StatsBomb freeze frames and tracking-data models. You cannot price soccer without xG-class inputs; this book explains where they came from, what they measure, and where they break.
2. **It documents that the sharpest soccer models belonged to gamblers before they belonged to clubs.** Matthew Benham (Smartodds; owner of Brentford and FC Midtjylland) and Tony Bloom (Starlizard; owner of Brighton) built fortunes betting soccer with team-strength models, then bought clubs and ran them on the same engines. This is rare direct evidence about which side of the counter held the modeling edge in soccer, and for how long.
3. **It is the extreme case study in luck versus skill.** Soccer is the lowest-scoring major sport; the book is essentially 300 pages on separating repeatable process from goal-count noise — the same decomposition Peta performs on baseball (*Trading Bases*, book 06), pushed to the sport where the noise is largest and the market's mispricing of it lingered longest.
4. **It maps the inefficiencies analytics actually found** — in the transfer market, in set pieces, in shot selection, in the valuation of defenders and keepers — which is a catalogue of what informed models knew before consensus prices did.

## Core Thesis

Soccer produces fewer scoring events than any other major sport — roughly 2.7 goals per match, about one goal per ten shots — so the thing everyone counts (goals, and the league table built from them) is a tiny, wildly noisy sample of the underlying process. The better team loses constantly; researchers Chris Anderson and David Sally estimated match outcomes are roughly half luck. The analytics revolution is the two-decade effort to build progressively better proxies for the repeatable process underneath the outcomes: shot counts, then shot quality (xG), then the value of every on-ball action (possession-value models), then tracking-data models of the 98–99% of the game each player spends off the ball. Whoever measures process while everyone else prices outcomes gets paid — first the betting syndicates (Benham, Bloom), then a handful of clubs (Liverpool, Brentford, Midtjylland, Brighton, Arsenal's StatDNA), and only slowly the rest of the sport. For a bettor, the thesis inverts cleanly: wherever tables, narratives, and goal counts still drive prices, regression to xG-class process metrics is the edge.

## Key Concepts

### 1. Goals are a tiny, noisy sample — soccer's signal problem

The book's foundation. A top-flight team plays 38 league matches and scores perhaps 50–70 goals a season — a season-long sample smaller than one NBA team's scoring events in a week. Scoring runs at ~1.35 goals per team per match, conversion at ~10% of shots, and results are compressed into win/draw/loss with the draw absorbing about a quarter of outcomes. Consequences O'Hanlon draws out:

- **Single matches are barely informative.** Favorites win far less often than in basketball or American football; Anderson and Sally's *The Numbers Game* work (covered through Anderson's story) put the luck share of a match outcome near 50%.
- **The league table lies over short horizons** — Rasmus Ankersen's mantra at Benham's clubs. A handful of deflections, posts, and keeper hot streaks moves a team many table places. Benham's Midtjylland and Brentford famously evaluated themselves on underlying "justice table" metrics rather than actual standings.
- **Soccer is a weak-link game.** Via Anderson and Sally's O-ring argument: because goals are scarce and one error concedes, upgrading your worst regular improves results more than upgrading your star — the opposite of basketball. They also found a goal prevented is worth more in expected points than a goal scored.

### 2. From Charles Reep to xG: the history and meaning of expected goals

O'Hanlon traces the lineage carefully, and it doubles as a cautionary tale about doing this badly. **Charles Reep**, an RAF wing commander, began hand-notating matches in 1950 — the first serious soccer data collection. He concluded that most goals come from moves of three passes or fewer, and preached direct long-ball play; via FA coaching director Charles Hughes, Reep's conclusion deformed English soccer for decades. The analysis was a denominator fallacy: the vast majority of *all* possessions are three passes or fewer, so of course most goals are too — per possession, longer sequences were fine. Reep's one durable finding: it takes roughly nine or ten shots to score a goal, a ratio essentially unchanged since the 1950s. Lesson one of soccer analytics: raw counts without base rates produce confident, wrong, and influential conclusions.

The modern chain: Opta (founded 1996) commercialized event data; the late-2000s blogosphere imported hockey's shot-ratio thinking (Corsi/PDO analogues, e.g. total shots ratio); and shot-quality models emerged in parallel — **Sarah Rudd** at StatDNA (whose 2011 Markov possession model prefigured everything; Arsenal quietly bought StatDNA and Rudd spent a decade as its head of analytics) and **Sam Green at Opta**, whose 2012 blog post assessing Premier League goalscorers popularized the term "expected goals." What xG *is*: a model — trained on hundreds of thousands of historical shots — of the probability that a given shot scores, based on distance, angle, body part, assist type, play pattern (open play, counter, set piece), and, in richer data (StatsBomb freeze frames, tracking), defensive pressure and keeper position. A team's match or season xG is the sum of its shots' probabilities. The average shot is worth ~0.10 xG; a penalty ~0.76–0.79. What it *means*: a measure of chance creation and concession — the process — deliberately stripped of whether the ball happened to go in. Pundits mocked it on arrival; it now underpins club recruitment models and bookmaker pricing alike.

### 3. Goals minus xG regresses: finishing is mostly not persistent at team level

The book's most bettable idea. The gap between goals and xG (over- or under-performance, "finishing" plus keeper performance plus deflection luck) shows almost no season-to-season persistence at team level — the soccer analogue of Peta's cluster luck. The flagship story: **Borussia Dortmund, 2014–15**, Jürgen Klopp's last season. Dortmund sat at or near the bottom of the Bundesliga deep into winter while Ian Graham's Liverpool model rated them the second-best team in Germany by expected goal difference, behind only Bayern — historically horrendous finishing and keeper luck on both ends. They regressed as predicted and climbed to seventh; Graham's analysis that Klopp's Dortmund had been elite-but-unlucky, not declining, underwrote Liverpool's 2015 hire of Klopp — the single most consequential regression-to-xG call in soccer history.

At the *player* level, finishing skill exists (Messi genuinely and durably outperforms xG) but is detectable only over hundreds of shots — far more than most players accumulate in several seasons — so even star strikers' hot conversion runs mostly regress. Liverpool's data case for signing **Mohamed Salah** in 2017 (pushed by the research group when Klopp initially preferred Julian Brandt) rested on Salah's elite shot volume and locations at Roma, not on his conversion rate; his Chelsea "failure" was a scouting-narrative artifact the model ignored. Keeper shot-stopping gets the same treatment via post-shot xG (goals prevented versus expectation given on-target shot placement) — real skill, noisy in small samples.

### 4. What persists: shot volume and shot quality

If finishing doesn't persist, what does? The book's answer, from the hockey-derived research tradition it chronicles: **the ability to generate lots of good shots and concede few** — shot volume and shot quality. Shot ratios stabilize fastest of all team metrics; xG difference (xGD) stabilizes nearly as fast and carries more information per match, making it the best simple blend of repeatability and relevance; goal difference is far slower; points slowest of all. Within a fraction of a season, xGD predicts a team's *future* goals and points better than its actual goals and points do — the empirical backbone (from the public-analytics work of the era, Opta, and club research O'Hanlon reports) of every "justice table." Caveat the book is honest about: xG models carry style biases — teams that defend deep and counter (or that habitually shoot with defenses scrambled) systematically beat generic xG models, so a persistent residual can be *style*, not luck. Treat persistent, mechanism-backed residuals differently from one-season spikes.

### 5. Beyond xG: possession-value models

xG only scores shots, and shots are the last link of long chains. Luke Bornn's framing in the book: the ball is in play under an hour, and the average player is on the ball for around a minute per match — event-data analytics values players on roughly 1% of what they do. The frontier O'Hanlon documents is assigning goal-probability value to *every* action: Rudd's 2011 Markov model of possession states was the ancestor; descendants include Karun Singh's expected threat (xT), KU Leuven's VAEP, StatsBomb's On-Ball Value, American Soccer Analysis's goals added (g+), and — inside Liverpool — William Spearman's tracking-data **pitch control** models (Spearman is an ex-CERN physicist), which value off-ball movement and space creation. All share one grammar: value of an action = change in P(score soon) minus change in P(concede soon). For team ratings this matters because possession-value differentials capture ball progression and territory that shot-only models miss, and they identify contributors (progressive passers, space creators) whose value never appears in shot or goal columns.

### 6. How clubs actually use analytics

The book's inside-the-building reporting shows adoption was narrow, uneven, and concentrated where the money is:

- **Recruitment is the killer app.** Transfer fees and wages dwarf everything else, so analytics' highest-leverage use is buying undervalued players: Liverpool's Salah-class signings; Brentford's buy-low-sell-high trading (Ollie Watkins, Neal Maupay, Saïd Benrahma types — bought on model metrics from cheaper leagues, sold at multiples); Arsenal's StatDNA-driven scouting; Brighton's Starlizard-informed recruitment from overlooked markets. Ashwin Raman scouting for Dundee United from his bedroom in India is the reductio: the information is in the data feed, not the stadium.
- **Set pieces are the most coachable edge.** Midtjylland (Danish champions 2014–15, in their third season under Benham) and Brentford invested in set-piece routines and long throws because dead-ball situations are discrete, rehearsable, and were league-wide undervalued.
- **Klopp-era Liverpool is the flagship**: FSG (Moneyball owners; John Henry hired Bill James's heirs in Boston) built a physicist-staffed research group under Graham and Michael Edwards that shaped the manager hire, the transfer record, and match preparation en route to the 2019 Champions League and 2020 Premier League titles.
- **Most clubs still weren't doing it.** O'Hanlon is clear that as of 2022 large parts of the sport ran on analytics theater — one analyst, ignored — which is precisely why the edges persisted as long as they did.

### 7. The market inefficiencies analytics found

Two registers, both relevant to SharpOds. **Betting-market inefficiency:** Benham and Bloom beat soccer betting markets (notably deep Asian handicap/totals markets) with quantitative team-strength models for years — profits large enough to buy professional clubs. The syndicates were the sharpest modelers in the sport, ahead of clubs and books; their existence is the book's proof that soccer prices lagged measurable process for a long time, and their absorption into the market is why naive versions of these edges have since shrunk. **On-pitch inefficiencies** (each one a place consensus expectations — and therefore prices and narratives — were wrong): corners are nearly worthless (~2% lead to goals) despite crowds and commentators treating them as chances; long-range shots and high-volume crossing are systematically overvalued relative to working the ball into the box; goals prevented are worth more than goals scored, yet defenders and keepers were priced far below attackers; keepers were judged on save totals rather than post-shot-xG goals prevented; the transfer market overpaid for age (past-peak fame) and league brand while underpaying early-twenties peaks in unfashionable leagues; set-piece design was almost free points. The meta-inefficiency: markets and boardrooms price *goals and tables* (outcomes); models price *chance creation* (process); the gap between them is the recurring trade.

## The Math

*Net Gains* is narrative journalism — it contains stories and findings, not formulas. The rules below state the book's logic precisely, with standard public-analytics parameterizations (flagged where they are calibration choices rather than the book's claims). Notation: per-match rates unless stated; `G`/`GA` goals for/against, `xG`/`xGA` expected goals for/against, `xGD = xG − xGA`, `M` matches played, `n` shots.

**1. Expected goals (definition and calibration requirement)**

```
xG_shot = P(goal | distance, angle, body part, assist type, play pattern, pressure)
xG_team(match) = Σ over shots xG_shot
```
- Trained on ≥100k historical shots; must be calibrated: mean predicted ≈ realized conversion (~0.10 overall; penalties ~0.76–0.79).
- Provider models differ (Opta vs. StatsBomb vs. Understat); never mix providers within one time series.

**2. Goals-minus-xG regression (team level): the core rule**

```
FIN_team = (G − xG) / M            (finishing/luck residual, per match; same for GA − xGA)
Projected scoring rate = xG/M + κ_team · FIN_team,   κ_team ≈ 0
```
- Season-to-season team correlation of `FIN` is approximately zero: carry forward **none** of a team's over/under-performance by default. This is the direct analogue of Peta's cluster-luck deletion.
- Exception path: a residual that persists across multiple seasons *with a mechanism* (deep-block counterattacking style, elite set-piece program, a genuine outlier finisher taking a large shot share) should be modeled as a style/personnel covariate in the xG adjustment — never as generic "finishing skill."

**3. Player finishing shrinkage (shot-count based)**

```
FinishSkill_est = (n / (n + k)) · (G_player − xG_player) / n,    k ≈ 300 shots
```
- With k ≈ 300 (calibration choice consistent with public research that finishing skill needs several hundred shots to detect), a 60-shot season keeps ~17% of its residual; almost every player projects at or near league-average finishing. Roster-driven scoring projections should be built on players' xG volume, not their conversion.

**4. Persistence hierarchy: what predicts future goals**

```
Predictive value for future goal difference (given equal sample):
    xGD  >  shot ratio (TSR)  >  GD  >  points
Stabilization speed (small samples):  shot ratio fastest, xGD close behind, GD slow, points slowest
```
Implementation as a sample-size-dependent blend for team strength:

```
Rating input = w(M) · xGD_rate + (1 − w(M)) · GD_rate,   w(M) high and rising: ≈ 0.7 by ~10 matches, ≈ 0.8+ thereafter (calibrate per league)
M < ~6:  underlying rates are all unstable — lean on preseason prior (roster/possession-value based) and the market price.
```
Never rank teams on points or table position: points compound goal-count noise with the win/draw/loss discretization.

**5. PDO-style luck flag (hockey import the book's history runs through)**

```
PDO = (G / shots_for) + (1 − GA / shots_against)      (finishing% + save-side%)
```
- Regresses toward the league mean (≈ 1.0 in this form). Teams > ~1σ above league mean are overperformance flags (fade candidates); below, back candidates. Use as a screen; xG residuals (Rule 2) are the sharper version of the same signal.

**6. Sample-size cautions (make the noise concrete)**

```
Season goals ≈ 55  ⇒  Poisson SD ≈ √55 ≈ 7.4 goals of pure luck per season side
⇒ a team's seasonal GD carries ~±10 goals of noise ⇒ roughly ±7–10 table points
```
- A quarter-season (~9–10 matches, ~13 goals scored) is ~±3.6 goals of noise on the scored side alone — early tables are mostly noise. Single-match xG totals are themselves small samples of shots (a 2.5-xG match can be one penalty plus chaff); for match post-mortems and "deserved result" estimates, simulate the shot list (Rule 7) rather than comparing xG totals.

**7. xG points / "justice table" (Midtjylland–Brentford evaluation tool)**

```
For each match: Monte Carlo each shot as Bernoulli(xG_shot) → scoreline distribution
→ P(win), P(draw), P(loss) → xPts = 3·P(win) + 1·P(draw)
Justice table = Σ xPts;  Gap = actual points − Σ xPts
```
- `Gap` is the mispricing screen: large positive gaps = teams the table (and narrative-following prices) overrate; large negative gaps = underrated. Evaluate teams, managers, and our own bets on xPts, not points.

**8. From xG rates to prices**

```
λ_home = base · att_home(xG-based) · def_away(xGA-based) · home_adv ;  λ_away analogous
Score matrix via Poisson (Dixon–Coles low-score correction) → 1X2, AH, totals
```
- The book supplies the *input discipline* (xG-based attack/defense ratings, luck-stripped); the pricing machinery is Buchdahl (book 04) and Mack (book 07). Blend the model price with the devigged market price before betting (Peta/Birnbaum shrinkage, book 06) — the Benham/Bloom lesson is that even the best soccer models bet marginal divergences against liquid closers, not headline disagreements.

## Strengths and Limitations

**Strengths**

- **The definitive synthesis of soccer analytics' first two decades**, reported from primary sources — Graham, Spearman, Rudd, Bornn, Knutson, Anderson — rather than reconstructed secondhand. The Dortmund/Klopp and Salah cases are the canonical worked examples of xG regression driving real, expensive, correct decisions.
- **Conceptually rigorous about luck.** The book never oversells: it is explicit that soccer outcomes are heavily random, that xG is a proxy with provider variance and style biases, and that finishing narratives are mostly noise. The Reep chapter is the best cautionary tale about denominators in the whole canon.
- **Unique market evidence.** No other canon book documents billion-scale betting operations (Smartodds, Starlizard) whose models demonstrably beat soccer markets long enough to buy the league's clubs.
- **Current (2022)** — it describes the data landscape (event + tracking, possession value) SharpOds actually faces, not a vanished era.

**Limitations**

- **No math, no method.** It is journalism: zero formulas, no datasets, no betting procedure, no parameter values. Every quantity in The Math above must be sourced and calibrated from public research and our own data; the book supplies logic and priors only.
- **The inefficiencies are partly harvested.** Precisely because Benham, Bloom, and the clubs won, xG-class models are now inside bookmaker pricing; naive "fade the xG over-performer" is substantially absorbed at closing prices in major leagues. Residual edge lives in speed (early lines, lineup news), minor leagues, style-bias corrections, and possession-value inputs the market lags.
- **Survivorship and access bias.** Liverpool, Brentford, Brighton, and Midtjylland are the successes; clubs that bought analytics and failed get less ink, so the effect size of "analytics wins" is overstated by construction.
- **xG heterogeneity is underplayed.** Cross-provider differences of 10–20% on the same team-season are routine; the book treats "xG" as one thing. A model must pin one provider (or build in-house) and recalibrate on provider changes.
- **Team-level focus leaves player-to-team aggregation open.** How to roll possession-value player ratings into match-level team strengths (with lineup news) is the live modeling problem the book gestures at but cannot solve for us.

## What SharpOds Takes From This Book

1. **Build soccer team strength from xG, never goals.** Attack rating from schedule-adjusted xG rate, defense from xGA rate; goals enter only through the shrunk blend of Rule 4 (`w ≈ 0.7–0.8` on xGD by mid-season, market/prior-dominant before ~6 matches). Points and table position are display artifacts, not inputs.
2. **Treat goals-minus-xG as cluster luck: carry-forward ≈ 0 at team level.** Identical pattern to Peta's BaseRuns residual deletion — decompose, identify the non-persistent component, delete it. Allow persistent residuals back in only as explicit style/personnel covariates (counterattacking depth, set-piece program, outlier finisher share) with multi-season evidence.
3. **Flag heavy xG over/under-performers as market-mispricing candidates.** Maintain the justice table (Rule 7) league-wide: fade teams whose points run well ahead of xPts (match odds, futures, season totals) and back teams running behind — weighting the signal highest early season, after managerial-change narratives, and in competitions where closing prices are least sharp (lower divisions, cups, minor leagues).
4. **Shrink all finishing.** Player scoring projections use xG volume with conversion shrunk by `n/(n+300)` (Rule 3); keeper projections use multi-season post-shot-xG goals prevented, heavily shrunk. Applies directly to goalscorer props and team-total derivatives.
5. **Price matches through Poisson/Dixon–Coles on xG-derived rates** (Rule 8), then shrink toward the devigged close before betting — treat liquid soccer closers as Benham/Bloom-grade opposition and demand an information reason (lineups, style change, cross-league transfer, set-piece coaching hire) for any large divergence.
6. **Respect Poisson noise budgets** (Rule 6) in every evaluation: never re-rate a team, a model, or our own performance on goal counts a √n test can't distinguish from luck; evaluate on xPts and CLV.
7. **Prefer possession-value inputs where available** (xT/VAEP/g+-class) to capture progression and off-ball value shot-only xG misses — the book's frontier is our input roadmap — and fall back to shot ratios only in tiny samples.
8. **Hunt Reep-class fallacies in our own shop.** Every SharpOds finding must state its denominator and base rate; any conclusion from raw event counts without per-possession or per-opportunity normalization is presumed wrong until proven otherwise — the revolution's founding error is the easiest one to repeat.
