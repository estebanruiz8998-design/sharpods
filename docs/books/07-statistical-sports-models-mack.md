# Statistical Sports Models in Excel

**Andrew Mack — self-published (Amazon KDP), July 2019 (ISBN 978-1079013450); companion downloadable Excel workbooks; Volume 2 followed in 2020**

---

## Why This Book Is Canon

Every other book in the sharp-betting canon tells you *why* markets can be beaten — Wong and Miller/Davidow explain market structure, Buchdahl explains value and validation. Mack's book is the canon's **"how" manual**: it is the first widely read book that walks a reader end-to-end through actually *building* working betting models — data in, probabilities out, compared against real prices — using a tool every reader already owns (Excel), with downloadable companion spreadsheets covering the **NFL, NBA, NHL, AFL, and English Premier League**. The spreadsheets are, as reviewers put it, the meat and bones of the book: you learn by opening the model and tracing every cell.

Its standing in the community is unusually consistent. It periodically topped Amazon's sports-betting bestseller lists in multiple countries, earned a favorable review on Pinnacle's Betting Resources (the sharpest bookmaker's own education arm), and remains the default first answer on betting Twitter and r/algobetting to the question "I understand value — how do I actually build a model?" Mack himself is a credentialed practitioner rather than a pundit: a professional sports bettor and quantitative retail trader, founder of the private research firm Mack Analytics (known online as @Gingfacekillah), who later added an MSc in data science and went on to write *Statistical Sports Models in Excel Volume 2* (2020, player props and derivatives) and *Bayesian Sports Models in R* (2024) — a trajectory that itself maps the field's evolution from spreadsheets to modern probabilistic programming.

Unique contributions to the canon:

1. **The distribution-first mindset.** Choose the probability distribution that matches the sport's scoring process — Poisson-family for low-scoring count sports (soccer, hockey), normal for high-scoring aggregates (basketball, American/Australian football) — then let the distribution generate every market price from one fitted set of parameters.
2. **The full modeling pipeline as a repeatable loop**: collect data → fit a simple structural model → convert outputs to fair odds → compare against the devigged market → bet only demonstrated edges → track, backtest, refine.
3. **The market as the yardstick.** Mack is blunt that sharp closing prices are the best publicly available estimate of true probability, so a model earns trust by systematically beating the (vig-free) closing line — not by cherry-picked winning streaks.
4. **Honest difficulty-setting.** The opening of the book establishes that modeling is hard, most models fail, edges are small and live mostly in less efficient corners of the market (niche leagues like the AFL, derivative markets) — an antidote to the genre's get-rich tone.

## Core Thesis

You do not beat a betting market by predicting winners; you beat it by producing **better-calibrated probabilities than the price** in spots where the market is soft. A disciplined amateur can build such probability machines with nothing more than Excel if they (a) pick a distribution that matches how the sport actually generates scores, (b) keep the model parsimonious enough not to memorize noise, (c) convert every output into fair odds and compare it to the devigged market, and (d) accept the sharp closing line as the referee: a model that cannot consistently beat vig-free closing prices out-of-sample is a losing model no matter what its recent P&L says. Modeling is a process business — iterate, validate, size stakes fractionally, and hunt where the market's attention is thinnest.

## Key Concepts

*The book's exact chapter structure is organized around one working model per sport; the treatment below is organized by theme.*

### 1. The market-efficiency spectrum and niche selection

Markets vary in sharpness with liquidity and attention. Main lines in the NFL and EPL are brutally efficient; smaller leagues (Mack's own AFL success is the running example), lower divisions, and derivative markets (totals, team totals, alternate lines) are progressively softer. Strategic consequence: model where your marginal information can matter. A mediocre model of a soft market beats an excellent model of an efficient one.

### 2. Closing line value (CLV) as the model's report card

Because the sharp close (canonically Pinnacle's) aggregates the entire market's information, beating it systematically is both the best early evidence of edge and a far faster diagnostic than P&L, whose signal drowns in variance over any human-scale sample. Mack's validation stance: track the price you took against the devigged closing price on every bet; positive average CLV with reasonable consistency is a necessary condition for believing in the model. This position — inherited from the professional community and given a practical tracking implementation here — is the connective tissue between Mack and the Miller/Davidow strand of the canon.

### 3. Distribution-first modeling

The central technical idea. Ask first: *what statistical process generates this sport's scores?*

- **Low-scoring count sports** (soccer goals, NHL goals, many props): Poisson family. Scores are small non-negative integers; a Poisson with the right mean reproduces the whole scoreline distribution.
- **High-scoring sports** (NFL, NBA, AFL points): the sum of many scoring events is approximately **normal**; model team scores or margins/totals as normal random variables with estimated means and standard deviations.

Once the distribution is chosen and parameterized, *every* market — moneyline, spread/handicap, total, correct score — is just a region of the same distribution. One model, all prices.

### 4. The Poisson goal model (soccer/hockey)

The workhorse, built in the book on EPL data. Team strengths are multiplicative factors relative to league average:

- Attack strength = team's average goals scored ÷ league average goals scored.
- Defense strength = team's average goals conceded ÷ league average goals conceded.
- Expected goals for each side = the relevant league scoring baseline × own attack × opponent defense, with home advantage entering through separate home/away baselines (or an explicit multiplier).

Independent Poisson draws at these two means generate a **score matrix** — the probability of every exact scoreline — from which 1X2, over/under, correct score, both-teams-to-score, and Asian handicap probabilities are read off by summing cells. Fair odds are reciprocals; edges are found by comparison with devigged market prices.

### 5. The correlation problem and the bivariate Poisson

Mack is explicit that the independence assumption is the basic model's known flaw: real match scores are mildly correlated (game state changes behavior), and the independent-Poisson matrix underprices draws and low-scoring outcomes. The remedy he presents is the **bivariate Poisson** (the Karlis–Ntzoufras construction): give the two teams a shared latent scoring component so their scores covary, with the covariance a third fitted parameter. This is the same defect Dixon–Coles patch with their low-score adjustment; Mack's choice of the bivariate Poisson is the more general, if heavier, fix, and he shows it can be evaluated in a spreadsheet.

### 6. Least-squares power ratings (Massey) for margin sports

For sports where margin of victory is the natural signal (NFL is the book's example), Mack builds **Massey-style least-squares ratings**: each game's margin is modeled as home rating minus away rating plus home-field advantage; the ratings that minimize squared prediction error across all games are found by regression (LINEST) or Solver, with an identifiability constraint (ratings sum to zero). The rating difference plus HFA is a predicted point spread; the spread converts to a win probability through the normal CDF using the empirical standard deviation of margin errors (on the order of 13–14 points in the NFL). This is the classic bridge from "power rating" folklore to actual statistics.

### 7. Logistic regression, fit with Solver

For direct win-probability modeling from team statistics (efficiency differentials, rest, venue — the NBA treatment leans this way), Mack teaches **logistic regression fitted by maximum likelihood in Excel**: set up the logit formula, compute each game's log-likelihood, and let Solver choose coefficients maximizing the total. This demystifies MLE — the reader watches the optimizer do what statistical packages hide — and gives a template for any binary-outcome model.

### 8. Monte Carlo simulation

When a market has no clean closed form (derivatives, distributions of season outcomes, anything path-dependent), simulate: draw random scores from the fitted distributions via inverse-transform sampling (`RAND()` through the inverse CDF), replay the game thousands of times, and estimate any probability as the fraction of simulations in which the event occurs. Mack emphasizes simulation as the modeler's universal fallback and shows how simulation error shrinks with the number of trials.

### 9. Odds mechanics, devigging, and expected value

The standard toolkit, treated operationally: implied probability as the reciprocal of decimal odds; removing the overround by normalization to compare like with like; expected value per unit as `p·d − 1`; bet only when model probability times price clears 1 by a margin of safety. Nothing here is original to Mack — the point is that the book wires these conversions into every spreadsheet so the model's *native output is a fair price*, not a pick.

### 10. Staking: Kelly and its fractions

Mack presents the Kelly criterion as the growth-optimal stake and immediately discounts it for practice: model probabilities are estimates, Kelly is brutally sensitive to overestimated edges, therefore bet **fractional Kelly** (quarter to half) or flat stakes. The estimation-error argument, not risk appetite, is the operative justification.

### 11. Backtesting, overfitting, and parsimony

The book's most repeated warnings. Fit on one sample, judge on another (hold-out or walk-forward); a model tuned until its historical P&L looks great has usually memorized noise; every added parameter is another chance to fool yourself. Prefer few, theoretically motivated inputs. Judge models on out-of-sample yield, calibration, and CLV over samples large enough that variance cannot masquerade as skill. Related: regression to the mean — extreme observed team performance is part luck and should be shrunk toward the average when projecting forward.

### 12. Process over results

A losing week proves nothing; a winning month proves little. The modeler's obligations are to the process: log every bet with the taken and closing price, review honestly, iterate deliberately, and let sample size — not emotion — decide when the model has spoken.

## The Math

All odds are decimal (`d` = total return per unit staked). `p` = model probability. Every formula below is implementable directly.

**1. Implied probability, devig (normalization), fair odds, EV**

```
p_imp,i  = 1/d_i
B        = Σ_j 1/d_j                     (book sum over the market's outcomes)
p_fair,i = (1/d_i) / B                   (multiplicative devig)
d_fair   = 1/p_model
EV per unit = p·d − 1                    bet iff p·d > 1 + τ  (τ = safety threshold)
```

**2. Poisson scoreline model (soccer/hockey)**

```
Poisson pmf:  P(X = k) = e^(−λ) · λ^k / k!        k = 0, 1, 2, …

attack_i  = (avg goals scored by team i)   / (league avg goals scored)
defense_i = (avg goals conceded by team i) / (league avg goals conceded)

λ_home = L_home · attack_home · defense_away
λ_away = L_away · attack_away · defense_home
   where L_home, L_away = league average goals by home/away sides
   (home advantage is carried by L_home > L_away, or an explicit multiplier γ on λ_home)

Score matrix (independence): S(i,j) = P(H = i) · P(A = j),  i, j = 0…K (K ≈ 10)

P(home win) = Σ_{i>j} S(i,j)     P(draw) = Σ_{i=j} S(i,j)     P(away win) = Σ_{i<j} S(i,j)
P(over 2.5) = Σ_{i+j ≥ 3} S(i,j)         P(correct score m–n) = S(m,n)
Asian/European handicaps: sum S(i,j) over the region defined by the adjusted margin.
```

**3. Bivariate Poisson (correlated scores; Karlis–Ntzoufras form)**

```
X = X1 + X3,  Y = X2 + X3,  X1~Pois(λ1), X2~Pois(λ2), X3~Pois(λ3) independent

P(X = x, Y = y) = e^(−(λ1+λ2+λ3)) · (λ1^x / x!) · (λ2^y / y!) ·
                  Σ_{k=0}^{min(x,y)} C(x,k) · C(y,k) · k! · (λ3 / (λ1·λ2))^k

E[X] = λ1 + λ3,  E[Y] = λ2 + λ3,  Cov(X,Y) = λ3
Setting λ3 = 0 recovers the independent model. Fit λ1, λ2, λ3 by maximum
likelihood (Solver) or set λ3 from historical score covariance.
```

**4. Massey least-squares ratings and margin → probability**

```
For each game g:  margin_g = r_home(g) − r_away(g) + h + ε_g
   r_t = rating of team t, h = home-field advantage, ε = error

Fit: minimize Σ_g ε_g²  subject to Σ_t r_t = 0
   (equivalently solve the normal equations X'X r = X'y, or use LINEST/Solver)

Predicted spread:  m̂ = r_i − r_j + h        (i at home)
Win probability:   P(i wins) = Φ(m̂ / σ)
   Φ = standard normal CDF; σ = std dev of margin prediction errors,
   estimated from residuals (NFL ≈ 13–14 points; estimate per sport, don't assume)
Push-aware spread probabilities: P(cover s) = Φ((m̂ − s)/σ) with discreteness
handled empirically around key numbers.
```

**5. Normal model for high-scoring sports (NBA/NFL/AFL totals and sides)**

```
Team scores: H ~ N(μ_H, σ_H²),  A ~ N(μ_A, σ_A²), independence assumed
P(home win)  = Φ( (μ_H − μ_A) / sqrt(σ_H² + σ_A²) )
P(over T)    = 1 − Φ( (T − (μ_H + μ_A)) / sqrt(σ_H² + σ_A²) )
```

**6. Logistic regression by maximum likelihood (Solver)**

```
p_g = 1 / (1 + e^(−z_g)),   z_g = β0 + β1·x_g1 + … + βk·x_gk
LL  = Σ_g [ y_g · ln(p_g) + (1 − y_g) · ln(1 − p_g) ]      y_g ∈ {0,1}
Choose β to maximize LL (Excel: Solver, GRG Nonlinear, on the LL cell).
```

**7. Monte Carlo estimation**

```
Draw u = RAND() ∈ (0,1); score = F⁻¹(u) for the fitted distribution
  (normal: NORM.INV(u, μ, σ); Poisson: smallest k with CDF(k) ≥ u)
Repeat N times (N ≥ 10,000); for any event E:
  p̂(E) = (# simulations where E occurs) / N
  standard error = sqrt( p̂(1 − p̂) / N )
```

**8. Kelly staking**

```
f* = (p·d − 1) / (d − 1)        fraction of bankroll at decimal odds d
Practice: bet c · f* with c ≈ 0.25–0.5 (fractional Kelly), because p is an
estimate and overestimated edges make full Kelly over-bet catastrophically.
```

**9. Closing line value**

```
CLV per bet = (d_taken / d_close_fair) − 1
   d_close_fair = devigged closing price of the same outcome (formula 1)
Model health check: mean CLV > 0 sustained across a meaningful sample of bets
is required evidence of edge; persistent CLV ≤ 0 condemns the model regardless
of recent profit.
```

## Strengths and Limitations

**Strengths**

- **It closes the theory–practice gap.** No other canon book leaves the reader with running models for five sports. The companion spreadsheets make every formula auditable cell by cell — the best pedagogy in the genre.
- **Distribution-first thinking is the right foundation** and transfers unchanged to any modern stack: the Poisson score matrix and normal-margin machinery in this book are the same structural cores inside professional pricing engines.
- **Correct incentives throughout**: parsimony over complexity, out-of-sample over in-sample, CLV over P&L, fractional Kelly over bravado, soft niches over sharp majors. The book teaches the *epistemics* of modeling, not just mechanics.
- **Honesty about difficulty.** Mack repeatedly says most models will not beat the close, and frames that as normal, not failure.

**Limitations and what has aged**

- **Excel is the wrong production platform, and Mack now agrees.** Spreadsheets cannot handle modern data volumes, automated refits, or API-driven bet placement; Solver's GRG optimizer is fragile for MLE at scale. Mack's own later work (*Bayesian Sports Models in R*, 2024) migrates to R/MCMC — treat Excel here as pedagogy, not architecture.
- **Point estimates without uncertainty.** Every parameter (attack strengths, ratings, β's) is a single number; there is no parameter uncertainty, no shrinkage priors, no predictive distributions over parameters. Bayesian hierarchical models — now standard, including in Mack's sequel — dominate this approach, especially early-season and for small samples.
- **Model families have been superseded in places.** Goals-based Poisson inputs are now routinely replaced or augmented by expected-goals (xG) data; Dixon–Coles time-decay weighting handles form better than fixed-window averages; regularized (ridge) and state-space ratings outperform vanilla Massey; gradient boosting beats hand-specified logistic regressions on rich feature sets. The book's structures remain valid skeletons; its estimation choices are dated.
- **Team-level main markets only.** Player props, derivatives, and live betting — where most soft edges now live — are deferred to Volume 2 and beyond. Nothing on limits, market access, or beard/exchange logistics.
- **Statistical depth is intentionally thin.** Reviewers fairly note that explanations of *why* techniques work are brisk; a reader can follow the recipes without acquiring the statistics to extend them safely.

## What SharpOds Takes From This Book

Mack supplies SharpOds' **model-construction layer**: the actual probability engines and the validation harness around them.

1. **Implement the Poisson score-matrix engine (formula 2) as the core pricer for soccer and hockey**, upgraded per the aging notes: inputs from xG-blended team strengths rather than raw goal averages, Dixon–Coles-style time-decay weighting on the fitting window, and a correlation correction (bivariate Poisson λ3 or Dixon–Coles ρ, fitted by MLE per league) so draws and unders are not systematically underpriced. All derivative soccer/hockey markets (totals, AH, correct score, BTTS) must price off this one matrix — never off separate ad-hoc models.
2. **Implement Massey least-squares ratings (formula 4) as the baseline power rating for every margin sport** (NFL, NBA, CFB, AFL), with home advantage as a fitted term, ridge regularization added, and margin→probability conversion through a normal CDF whose σ is re-estimated each season from residuals. This baseline is the benchmark every fancier rating (Elo variants, state-space) must beat out-of-sample before replacing it.
3. **Adopt CLV as the mandatory model gate (formula 9).** Every logged bet stores the taken price and the devigged Pinnacle close; a model must show positive mean CLV over its validation sample before real staking, and any live model whose rolling CLV goes non-positive over its trailing window is automatically quarantined for refit — regardless of P&L.
4. **Enforce distribution-first pricing.** Each sport's engine must declare its generative distribution (Poisson-family for counts, normal for high-scoring aggregates) and derive *all* market prices from that one fitted distribution; closed-form where available, Monte Carlo (formula 7, N ≥ 10,000 with reported standard errors) for anything path-dependent or derivative.
5. **Enforce Mack's overfitting discipline in the pipeline itself**: hard cap on features per model, walk-forward (never shuffled) validation splits, and deployment criteria stated *before* backtesting (minimum out-of-sample sample size, calibration error bounds, CLV threshold) so the backtest cannot be tuned into a curve-fit.
6. **Stake by fractional Kelly (formula 8) at c = 0.25–0.30**, computed on the edge after shrinking the model probability toward the devigged market probability — Mack's estimation-error argument implies never staking on the raw model number alone.
7. **Weight development toward market softness**: prioritize engines for lower-liquidity leagues and derivative markets over main lines of major leagues, and record per-market efficiency estimates (average |model − devigged close|, realized CLV available) to steer where the next modeling hour is spent.
8. **Treat Excel-era estimation as scaffolding**: implement each Mack model first as specified (it is simple, auditable, and a correctness benchmark), then let regularized/Bayesian upgrades compete against it — an upgrade ships only when it beats the Mack baseline on out-of-sample log-loss and CLV.
