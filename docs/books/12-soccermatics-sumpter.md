# Soccermatics

**David Sumpter — Bloomsbury Sigma, 2016 (subtitle *Mathematical Adventures in the Beautiful Game*; expanded "Pro Edition" paperback 2017 with updated betting results). Sumpter is a professor of applied mathematics at Uppsala University whose research field is collective animal behaviour — fish schools, ant colonies, bird flocks — turned on football.**

---

## Why This Book Is Canon

Most of the canon is written by bettors who learned statistics; *Soccermatics* is written by a working applied mathematician who learned betting. That inversion is exactly why it earns a slot. Where Mack (*Statistical Sports Models in Excel*) shows *how* to build a Poisson goal model and Buchdahl (*Fixed Odds Sports Betting*) shows how to *validate* one, Sumpter shows **why the model family is true in the first place**: he derives, from the structure of the game itself, the two pillars the modern soccer pricing stack rests on — goals as a Poisson process and shot conversion as a logistic function of geometry. A model you can justify generatively is a model you can trust out-of-sample; a model that merely fit last season is not. SharpOds' own soccer engine (`sharpods/models/poisson.py`) is an implementation of machinery this book explains from first principles.

Three further claims to canon status:

1. **It is the popular origin point of expected goals.** Published just as xG was crossing from analytics blogs to television, the book gives the cleanest public account of what a shot model is, why logistic regression on distance and angle is the right form, and why xG is a better measure of a team's underlying rate than the goals it actually scored. Sumpter later turned this material into the *Friends of Tracking* lecture series (2020), where he fits the same logistic xG model live on public data — the book's math has a maintained, verifiable afterlife.
2. **He bet real money and published the results.** In the betting chapters Sumpter stakes part of his book advance on strategies derived in the text — a performance-model strategy, a wisdom-of-the-crowd strategy, and an **odds-bias strategy** built on measured miscalibration in Premier League prices (a weak favourite–longshot bias, and a stronger bias against draws between evenly matched top teams). He reports roughly a 25% return over about half a season, and — critically — is honest that the sample is far too small to prove anything. He revisited the strategy's subsequent performance publicly (his Medium follow-up "If you had followed the betting advice in Soccermatics…"), an accountability standard most betting authors never meet.
3. **It supplies the canon's clearest treatment of randomness versus skill in a low-scoring sport**, and of the betting market as a wisdom-of-the-crowd machine — including the conditions (independence of opinions) under which crowds are sharp and the conditions (information cascades, herding) under which they fail. This is the conceptual bridge between Galton's ox and closing line value.

## Core Thesis

Football looks like chaos and narrative; it is actually a statistically lawful system observed through a thin sample. Goals are rare, approximately independent events, so match scores follow the Poisson distribution and any single result is mostly noise around the teams' true scoring rates. Those rates, in turn, are better measured by the *process* that generates goals — shots, weighted by the geometric probability that each becomes a goal (expected goals) — than by the goals themselves. The betting market is a crowd-wisdom aggregator that estimates these rates impressively well, and its late/closing prices are the best public forecast of a match in existence; but crowds are only as good as the independence of their members, and measurable, persistent biases (favourite–longshot, draw aversion in big matches) survive in the odds. The bettor's edge, therefore, is not "predicting football" — it is modeling the generative process more faithfully than the crowd in specific, measured places, and respecting randomness enough to know that only the long run can confirm you were right.

## Key Concepts

*Organized by theme rather than by the book's chapter sequence.*

### 1. Goals are a Poisson process — and why

The book's foundational demonstration, in the tradition of Moroney's 1950s observation that football scores fit the Poisson distribution. The argument is generative, not merely empirical: a match contains a large number of attacking sequences, each with a small and roughly independent probability of producing a goal, at an approximately constant rate through the 90 minutes. That is precisely the "law of rare events" regime in which the count of successes is Poisson-distributed and the waiting times between goals are exponential. Sumpter checks all of it against Premier League data: the histogram of goals per match sits on top of the Poisson pmf with the same mean (league averages run around 2.5–2.7 goals per match), and inter-goal times are close to exponential (with a mild rise in scoring rate late in matches). Consequences he draws out: 0–0 and 1–0 results carry almost no information about which team was better; freak scorelines occur at roughly the predicted frequency; and the pundit's post-hoc narrative for a one-goal result is mostly noise-fitting.

### 2. Expected goals: logistic shot models by distance and angle

A goal attempt is a geometry problem. The probability a shot scores falls off sharply with distance and rises with the angle the goal mouth subtends at the shooting position; the correct statistical form is **logistic regression**, because the output must live in [0,1] and saturate at the extremes — the scoring probability approaches 1 as the shooter closes to the open goal line (angle toward 180°) and 0 as the angle closes to nothing. Fit on a season of shots, the model assigns each attempt a probability — its **xG** — and a team's (or player's) xG total is the number of goals its chances "should" have produced. Additional covariates (headers vs feet, assist type, defensive pressure) refine the estimate but distance and angle carry most of the signal.

### 3. Shot quality versus shot volume

xG resolves the older analytics argument between volume metrics (total shots ratio) and quality arguments ("but they were all from 30 yards"). Both matter and xG prices them on one scale: many bad shots and few excellent shots can carry the same expected yield. Sumpter uses shot maps and the fitted model to show how teams differ systematically in the quality of chances they create and concede — a stylistic signature that raw shot counts miss and raw goals drown in noise.

### 4. Why xG predicts future scoring better than past goals

The book's most important idea for a bettor, and a pure sampling-variance argument. Goals are the Poisson-noisy *realization* of a team's chance-creation rate: over even half a season a team's goal total can sit a handful of goals from its true rate just by luck, and conversion rates over/above xG regress hard toward the mean. xG, by contrast, is built from shots — an order of magnitude more events per match than goals — so it converges on the underlying rate far faster. A team that is outscoring its xG is more likely lucky than clinical; a team underscoring it is more likely unlucky than wasteful. When projecting forward, the process measure (xG for/against rates) beats the outcome measure (goals for/against) — the single most load-bearing empirical claim this book contributes to SharpOds' lambda estimation.

### 5. Team performance metrics and structure

Sumpter's day-job toolkit applied to football: passing networks (which pairs of players exchange passes, and network centrality as a measure of dependence on individuals — Barcelona's midfield triangles are the running example), zonal control and pitch geometry (Voronoi-style ideas about space), and flow/synchronization analogies from collective animal behaviour. He is careful about the epistemics: these are largely *descriptive* metrics — superb for characterizing style and structure, much weaker as forward predictors than the rate statistics (xG) above. The book also treats managerial performance and league tables with the same luck-adjustment lens: sacking a manager after a bad run and improving is largely regression to the mean.

### 6. Crowd wisdom and the betting market

The Galton line of argument: aggregated independent estimates outperform experts, and a betting market is a continuously running Galton experiment where the "estimates" are backed by money. Sumpter runs his own crowd experiments and reviews the conditions under which the mechanism works — **independence and diversity of opinions** — and how it breaks: when guessers see previous guesses, information cascades and herding degrade the aggregate. Applied to betting: odds are a crowd forecast of match probabilities and are very well calibrated on the whole — far better calibrated than pundits, whom he tests and finds wanting. Prices sharpen as money arrives, so the **last-minute (closing) odds are the most accurate public prediction available**; a model should be measured against them, and beating the crowd means adding information the crowd has not yet priced, not out-shouting it.

### 7. The odds-bias experiments

The betting chapters' centerpiece. Method: take a large sample of historical odds, convert to implied probabilities, and compare implied probability with the *observed frequency* of each outcome — a calibration analysis of the bookmakers themselves. Sumpter finds Premier League prices carry a **weak favourite–longshot bias** (favourites win slightly more often than their odds imply, so backing short prices loses less/gains more than backing longshots) and a **stronger bias against draws between evenly matched teams**, particularly in matches between the big clubs — the public loves backing a winner in showpiece games, and the draw drifts to value. His strategy backed the outcomes the calibration said were underpriced; staking real money, he reports on the order of a 25% return over roughly half a season, with the explicit caveat that the sample cannot statistically distinguish skill from luck. The durable lesson is the *method* — measure the market's calibration and bet only where miscalibration is demonstrated and persistent — not the specific 2015-era biases, which publication itself erodes.

### 8. Randomness versus skill

How much of football is luck? Sumpter attacks it by simulation: generate seasons from Poisson models and compare the spread of outcomes under luck alone with the observed table. Single matches are heavily luck-dominated (the better team loses routinely — a direct consequence of low scoring; contrast basketball, where hundreds of scoring events let skill express itself within one game); over a 38-game season skill separates the top and bottom, but mid-table ordering and single-season gaps of several points are substantially noise. For the bettor this cashes out as discipline: results-based judgments about teams *or about your own betting record* need far larger samples than intuition suggests, and every evaluation should be phrased as "is this distinguishable from luck?"

## The Math

Every formula below is implementable as stated. `σ(z) = 1/(1+e^(−z))` is the logistic function; odds `d` are decimal.

**1. Poisson goals (the generative core)**

```
P(X = k) = e^(−λ) · λ^k / k!,   k = 0, 1, 2, …

Rare-events justification: n attacking sequences per match, each scoring with
small probability p, approximately independent  ⇒  X ≈ Poisson(λ = n·p).

Inter-goal waiting times: T ~ Exponential(λ/90)
  P(no goal in next t minutes) = e^(−λ·t/90)

Match model: home ~ Poisson(λ_home), away ~ Poisson(λ_away) with
λ_home + λ_away ≈ 2.5–2.7 in top leagues and λ_home > λ_away (home advantage).
Score matrix, 1X2 / totals / BTTS readouts, and the Dixon–Coles low-score
correction are as already implemented in sharpods/models/poisson.py.

Sanity check the assumption per league: variance/mean of goal counts ≈ 1
(mild overdispersion or late-game rate increase are the known deviations).
```

**2. Logistic xG model (minimum viable form)**

```
Goal-mouth angle for a shot at pitch coordinates (x, y), x = distance from
goal line, y = lateral offset from centre; goal width 7.32 m:

  θ = arctan( 7.32·x / (x² + y² − 3.66²) )     (add π if negative)

xG per shot:  xG = σ( β0 + β1·θ + β2·dist )    dist = √(x² + y²)

Fit β by maximum likelihood on a season of shots (outcome 1 = goal).
Extend with covariates (header, big-chance flag, assist type) only when they
improve out-of-sample log-loss. Team match xG = Σ over its shots.
```

**3. Lambda estimation: blend xG rate with goal rate (xG weighted heavier)**

```
For team t over a decay-weighted window of recent matches:
  goals_rate_t = weighted goals per match
  xg_rate_t    = weighted xG per match

  attack_rate_t = w · xg_rate_t + (1 − w) · goals_rate_t,     w ≈ 0.65–0.8
  (same construction on the conceded side for defence_rate_t)

Rationale (concept 4): xG is the lower-variance estimator of the true rate;
goals retain a sliver of signal (finishing/keeping skill), hence w < 1.
Convert to multiplicative strengths and feed the existing engine:
  attack_t  = attack_rate_t  / league_avg_scored
  defence_t = defence_rate_t / league_avg_conceded
  λ_home = L_home · attack_home · defence_away        (expected_goals() form)
Early season: shrink rates toward league mean (add k pseudo-matches of
league-average production, k ≈ 5–10) and push w toward its upper end.
```

**4. Odds-calibration analysis and bias-exploitation rules**

```
Devig:  p_imp,i = (1/d_i) / Σ_j (1/d_j)

Calibration regression over a large historical sample, per league and
outcome class (home/draw/away):
  fit  logit(P(win)) = γ0 + γ1 · logit(p_imp)     by logistic regression
  Unbiased market ⇔ γ0 = 0, γ1 = 1. Deviations locate the bias:
  γ1 > 1  ⇒ favourite–longshot bias (favourites underpriced).

Sumpter's 2015-era EPL findings: weak favourite–longshot bias, plus draws
underpriced when the teams are evenly matched (|p_home − p_away| small),
especially between top clubs.

Betting rule:  p_cal = σ(γ0 + γ1·logit(p_imp));  bet iff p_cal · d > 1 + τ
(τ = safety margin). Re-estimate γ on a rolling out-of-sample basis and
retire any bias that stops appearing — published biases decay.
```

**5. Luck–skill decomposition by simulation**

```
Simulate the fixture list N ≥ 10,000 times with all teams set to identical
league-average λ  ⇒  distribution of points/finishing positions under pure
luck; its spread (sd of points over a 38-game season is several points) is
the noise floor. A real-table gap smaller than that floor is not evidence of
a skill difference — the same test applies to a betting record's P&L.
```

**6. Crowd-wisdom yardstick**

```
The devigged last-available (closing) price is the sharpest public estimate
of match probabilities. Model health requires beating it out-of-sample
(log-loss vs. devigged close; CLV on placed bets) — identical to the
Mack/Buchdahl CLV gate, here justified as wisdom-of-the-crowd theory.
```

## Strengths and Limitations

**Strengths**

- **Generative justification, not curve-fitting.** The canon's other soccer treatments assert that Poisson works; Sumpter derives *why* it must, from rare-events structure — which tells you in advance where it will bend (score-state effects, late-game rates) and why patches like Dixon–Coles are needed. Same for the logistic form of xG: the functional form is argued from the geometry, not chosen by software default.
- **The best public explanation of xG's predictive superiority over goals** — the sampling-variance argument in concept 4 is the intellectual foundation for xG-based lambda estimation, and it has held up empirically for a decade.
- **Real-money honesty.** He stakes his own advance, reports the result, flags the sample-size problem himself, and publicly tracks the strategy afterward. That epistemic hygiene — treating his own 25% half-season return as unproven — models exactly the standard SharpOds holds itself to.
- **The calibration methodology for finding odds biases is fully portable**: implied probability vs. observed frequency, per league, per outcome class, is a reusable market-monitoring instrument regardless of whether Sumpter's specific 2015 biases survive.
- **Crowd-wisdom framing of the market** gives principled grounding for closing-line discipline: the close is sharp *because* it aggregates independent, money-weighted opinions — and the same theory predicts where it can fail (herded, cascade-driven markets; outcomes the public dislikes backing, like big-match draws).

**Limitations and what has aged**

- **It is popular science.** No code, few explicit fitted coefficients, no datasets; every number must be re-derived before use. The book teaches judgment and structure, not a pipeline — it needs Mack (implementation) and Buchdahl (validation) alongside it.
- **The betting experiment is anecdotal by design.** Half a season at ~25% is well inside the luck band that his own randomness chapter defines; he says so, but a careless reader can still walk away with a "proven strategy" that was never proven.
- **The published biases are decayed edges.** Favourite–longshot and big-match draw biases have been public since 2016 and heavily arbitraged; his own follow-up tracking exists precisely because persistence was the open question. Treat them as hypotheses to re-verify on current data, never as standing rules.
- **Pre-tracking-data era.** The 2016 shot models use event data (location, body part); modern xG adds freeze-frame defender positions, pressure, and keeper placement. The logistic distance/angle skeleton remains the right baseline but is no longer the frontier.
- **Descriptive metrics oversold by association.** Passing networks and geometric style measures are intellectually beautiful and predictively weak; the book is honest about this, but they should not leak into a pricing model without out-of-sample proof.
- **No staking, no market mechanics.** Nothing on Kelly, vig structure, limits, line shopping, or execution — the practical betting layer must come entirely from the rest of the canon.

## What SharpOds Takes From This Book

Sumpter supplies the **generative justification and the input layer** for the soccer engine that Mack's blueprint and `sharpods/models/poisson.py` already give structural form.

1. **Estimate Poisson lambdas from xG rates blended with goal rates, xG weighted heavier (formula 3).** This is the book's single most actionable directive: team attack/defence rates entering `expected_goals()` must be computed as `w·xG_rate + (1−w)·goals_rate` with `w ≈ 0.7` (tuned per league by out-of-sample log-loss), over a decay-weighted window, because xG is the lower-variance measurement of the true scoring rate. Raw goals-only strengths are a legacy fallback, never the default.
2. **Build the logistic xG model (formula 2) as a first-class SharpOds component**, with goal-mouth angle and distance as the mandatory baseline features and ML-fit coefficients per league; richer features must beat the baseline on held-out log-loss to ship. Team xG for/against per match becomes the canonical team-strength input feeding directive 1.
3. **Regress finishing to the mean.** Team-level over/under-performance of xG is presumed luck: shrink conversion deviations aggressively toward league average when projecting, and flag any team whose price the market appears to have set off its goal record rather than its xG record — that gap is exactly where concept 4 says value lives.
4. **Validate the Poisson assumption per league (formula 1's sanity check)** — variance/mean of goal counts, exponential inter-goal times — as an automated diagnostic; material overdispersion or score-state effects justify the Dixon–Coles rho (already implemented) or a negative-binomial escalation, decided by evidence rather than fashion.
5. **Stand up a permanent odds-calibration monitor (formula 4)**: rolling logistic calibration of devigged market probabilities against outcomes, per league and outcome class. Sumpter's specific biases (favourite–longshot; draws in evenly matched top-club fixtures) are seeded as *hypotheses* the monitor tests on current data; any detected bias must persist out-of-sample across seasons before a bias-exploitation rule (bet when `p_cal·d > 1 + τ`) is enabled, and rules auto-retire when the bias fades.
6. **Adopt the crowd-wisdom reading of the closing line (formula 6)**: the devigged close is the sharpest public probability, so SharpOds' models are graded against it (log-loss and CLV), and the system should expect edges precisely where crowd-wisdom preconditions fail — herded public money, unfashionable outcomes, and information the crowd hasn't priced — rather than uniformly.
7. **Enforce luck-aware evaluation everywhere (formula 5)**: before any conclusion — about a team's form, a model tweak, or a strategy's P&L — compute the luck-only noise floor by simulation and require the observed effect to clear it. Sumpter's own refusal to claim victory on a 25% half-season return is the house standard for interpreting SharpOds' results.
