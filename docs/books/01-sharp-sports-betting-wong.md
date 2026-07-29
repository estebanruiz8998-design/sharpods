# Sharp Sports Betting

**Stanford Wong (pen name of John Ferguson) — Pi Yee Press, 2001 (380 pp., ISBN 978-0935926248)**

---

## Why This Book Is Canon

Stanford Wong came to sports betting as an already-legendary blackjack author (*Professional Blackjack*; the term "wonging" — back-counting a blackjack table — is named after him). When he turned that same expected-value discipline on the sports market, the result was the first widely available book that treated sports betting as an exercise in **pricing**, not prediction. Before Wong, popular sports betting books were mostly handicapping folklore. *Sharp Sports Betting* replaced folklore with arithmetic: what the vig actually costs, what a half point is actually worth on each number, what a teaser leg actually has to win, what a season win total is actually a bet on.

Its standing in the sharp community rests on three durable contributions:

1. **The half-point valuation framework.** Wong published push-frequency tables for NFL sides and totals and showed how to convert a push frequency into an equivalent price in cents. This is the origin of the now-universal sharp practice of valuing every half point around the key numbers 3 and 7 instead of accepting the book's flat 10-cents-per-half-point menu.
2. **The "Wong teaser."** The book's basic strategy for 6-point NFL teasers — tease only short underdogs (+1.5 to +2.5) up through both 3 and 7, and mid-range favorites (−7.5 to −8.5) down through both 7 and 3 — was so demonstrably +EV at the prices of the era that the entire industry still calls these "Wong teasers." It is one of the very few named, public, mechanical +EV strategies in sports betting history.
3. **Derivative-market thinking.** Wong's central insight — that the main point-spread market is hard to beat, but the *derivatives* priced off it (teasers, parlays, props, season wins, halves, money-line conversions) are frequently mispriced — is the intellectual template for most modern +EV betting.

The book is on essentially every serious "best sports betting books" list, and its concepts (key numbers, half-point cents values, teaser basic strategy, devigging) are baseline vocabulary at every sharp shop today.

## Core Thesis

You do not beat the sports betting market by out-predicting it on the main lines; you beat it by knowing the exact price of everything and buying only what is offered below fair value. The point-spread market on sides is close to efficient, but the sportsbook's *derived* offerings — teasers, parlays, bought points, props, season win totals, money lines converted from spreads — are priced with crude rules of thumb. A bettor who can compute true probabilities (especially the probability mass sitting on football's key margins, 3 and 7) can identify which of these derived prices are wrong and bet only those, while managing bankroll so that variance never forces him out of the game.

## Key Concepts

### 1. The vig, and what you must beat

Every bet has an implied probability baked into its price. At the standard −110/−110 spread market, each side implies 52.38%, the two sides sum to 104.76%, and the overage is the bookmaker's margin. The bettor's entire job reduces to: **only bet when your true probability exceeds the price's implied probability.** Wong drills the break-even numbers (52.38% at −110, etc.) as the constant hurdle every play must clear.

### 2. Key numbers and the value of a half point

NFL scoring (field goal = 3, touchdown + PAT = 7) concentrates final margins on a few numbers. Historically, roughly **15% of NFL games land exactly on 3** (the most common margin) and roughly **9% land exactly on 7**; 10, 6, 4, and 14 follow at roughly 4–6% each. Conditional on the spread actually being 3, the push rate has measured anywhere from ~10% to ~16% depending on era and sample, because line-3 games are disproportionately close games decided by late field goals.

Wong's contribution is the machinery: a half point is worth exactly the expected value of the outcomes it reallocates (loss→push, or push→win) — nothing more, nothing less. Converted to price, a half point on or off 3 is worth roughly **20–25 cents** of American-odds juice, while books in Wong's era sold every half point for a flat 10 cents. Buying on/off 3 was therefore mechanically +EV, and buying half points on dead numbers (e.g., 8.5→9) was mechanically −EV. Books have since repriced (25 cents or refusal to sell around 3 and 7), which is itself evidence of how right this chapter was.

### 3. Teasers and the Wong teaser

A teaser lets you move the line 6 (or 6.5, 7) points on each of two or more NFL legs in exchange for worse odds. Wong reframed the question: a 6-point teaser is only worth it if the 6 points cross enough probability mass to lift each leg's win rate above the per-leg break-even (72.4% per leg for a two-teamer at −110). Six points starting from a short dog (+1.5 to +2.5, teased to +7.5/+8.5) or a mid favorite (−7.5 to −8.5, teased to −1.5/−2.5) crosses **both 3 and 7** — capturing ~25%+ of margin mass — and those legs historically covered around 75% or better, clearing the hurdle. Teasers that do not cross both key numbers generally do not clear it. This turned teasers from a sucker bet into a basic-strategy chart, exactly as Wong had done for blackjack.

### 4. Parlays: usually bad, occasionally very good

Standard parlay cards and off-the-board parlays pay less than the fair multiplicative odds (a two-team parlay at 13/5 = 2.6:1 against fair 3:1 for coin-flip legs is a ~10% house edge). But Wong shows the flip side: if the legs are individually +EV, parlaying *compounds* the edge; and **correlated parlays** (outcomes that tend to occur together, e.g., a big favorite covering and the game going over in certain profiles) can be +EV even at standard payouts because the book prices legs as independent.

### 5. Money lines vs. point spreads

The book gives empirical conversion tables between point spreads and money-line win probabilities, so a bettor can tell which of the two markets on the same game is the cheaper way to buy the same opinion. The mapping is not smooth — the same key-number lumpiness that drives half-point values makes spread↔money-line conversion an empirical-table problem, not a formula problem.

### 6. Season win totals

A season win total is a bet on the sum of ~16 (now 17) correlated Bernoulli trials. Wong's method: project a point spread for every game on the schedule, convert each spread to a win probability, sum them for expected wins, and build the full distribution of season wins to price Over/Under against the book's number and juice. He also treats the in-season dynamics: how your position's value evolves as games resolve, and how futures/win-total positions can be hedged with individual game bets.

### 7. Props and basic probability tools

Wong (famous for attacking Super Bowl prop menus) applies elementary probability — binomial and Poisson models, empirical frequencies — to props such as scoring events, showing that thin, casually-priced prop markets are where crude bookmaking rules of thumb are most exposed.

### 8. Hedging and middling

Hedging is presented honestly as **buying insurance at a vig-inclusive price**: it almost always sacrifices EV and is justified only by bankroll/utility considerations or when the hedge side is independently +EV. Middling (holding both sides with a window between the numbers, e.g., +3.5 and −2.5) is the profitable special case: at −110 on both sides you lose only ~0.1 units of vig when the middle misses and win ~2 units when it hits, so a middle needs to land only about 1-in-21 (≈4.8%) to profit — a hurdle a 3-wide window around a key number can clear.

### 9. Money management

Wong's treatment is brief and practical rather than theoretical: bet a small, roughly constant fraction of a dedicated bankroll; size bets so that an ordinary losing streak cannot ruin you; never chase with progressions. Edge determines *whether* to bet; bankroll determines *how much*. (The full Kelly apparatus is developed elsewhere in the literature; Wong's stance here is conservative flat betting at a sustainable fraction.)

### 10. Shopping and market mechanics

Multiple outs, line shopping for the best number and price, understanding limits and when books move numbers — Wong treats access to more prices as a direct, quantifiable increase in EV, since every extra half point or 5 cents is convertible to expectation via the tables above.

## The Math

All prices in American odds `A`. "Net payout" `b` = profit per 1 unit staked: `b = 100/|A|` if `A < 0`, `b = A/100` if `A > 0`.

**1. Implied probability of a price**

```
p_imp(A) = |A| / (|A| + 100)    if A < 0
p_imp(A) = 100 / (A + 100)      if A > 0
```

This is also the break-even win rate. At −110: `p_imp = 110/210 = 0.52381`.

**2. Two-way no-vig (fair) probability — proportional devig**

```
p_fair(side1) = p_imp(A1) / (p_imp(A1) + p_imp(A2))
```

**3. Bookmaker hold (fraction of balanced two-way handle)**

```
hold = 1 − 1 / (p_imp(A1) + p_imp(A2))
```

At −110/−110: `hold = 1 − 1/1.04762 = 4.545%`.

**4. EV of a spread bet with push possibility** (per 1 unit risked; `w` = P(win), `q` = P(push), `l = 1 − w − q`)

```
EV = w·b − l
```

**5. Half-point value — exact parity pricing.** Let `q = P(final margin lands exactly on number N | the line)`. Take a dog at +N with net payout `a` (win prob `w`, push prob `q`, lose prob `l`).

- Off-number on the worse side (+N−0.5, payout `a'`): the margin-N outcome becomes a loss.
  `EV parity:  w·a' − (l+q) = w·a − l   ⇒   a' = a + q/w`
- Off-number on the better side (+N+0.5, payout `a''`): the margin-N outcome becomes a win.
  `EV parity:  (w+q)·a'' − l = w·a − l   ⇒   a'' = w·a / (w+q)`
- Convert net payout back to American: `A = +100·a` if `a ≥ 1`, else `A = −100/a`.
- **Decision rule: buy (or sell) the half point iff the price charged is better than the parity price.** With `q ≈ 0.10` on the number 3 and `w ≈ 0.45`, parity ≈ 20–25 cents; the historical 10-cent menu price made buying on/off 3 +EV, and made buying across dead numbers (q ≈ 1–2%) −EV.

**6. Teaser break-even per leg** (n-team teaser paying American `A`)

```
r_breakeven = p_imp(A)^(1/n)
```

Two-team at −110: `sqrt(0.52381) = 0.7237` (72.4% per leg). At −120: `sqrt(0.54545) = 0.7386`. At −130: `sqrt(0.56522) = 0.7518`.

**7. Teaser EV** (legs with true cover probabilities `r_1..r_n`, treated as independent, net payout `b`)

```
EV = (Π r_i)·(1 + b) − 1
```

**8. Wong teaser selection rule (as published, 2001).** NFL only, 6-point, two-team teasers: tease underdogs +1.5 to +2.5 up to +7.5..+8.5, and favorites −7.5 to −8.5 down to −1.5..−2.5, so every leg crosses both 3 and 7. Wong's era data put such legs at ~75%+ cover rates vs. the 72.4% hurdle at −110. (See Limitations for current status.)

**9. Spread → win probability** (for money-line comparison and season wins)

```
P(team wins) ≈ Φ(s / σ),   s = points team is better than opponent (incl. home edge), σ ≈ 13.5–14 for NFL
```

Wong himself uses empirical tables rather than the normal curve; the normal approximation is the implementable fallback, with the empirical margin distribution preferred because of key-number mass.

**10. Season win total distribution** (game win probs `p_1..p_G` from projected spreads)

```
Expected wins:  μ = Σ p_i
Variance (independence approx.):  σ²_W = Σ p_i(1 − p_i)
Exact distribution: Poisson-binomial via DP convolution:
  f_0 = [1];  f_i(k) = f_{i−1}(k−1)·p_i + f_{i−1}(k)·(1−p_i)
P(Over t) = Σ_{k > t} f_G(k);  bet Over iff P(Over t) > p_imp(A_over), after devig.
```

**11. Hedge sizing** (ticket pays `X` if outcome O occurs; hedge on not-O at net odds `b_h`)

```
Equal-profit hedge stake:  h = X / (1 + b_h)
Guaranteed payout: X·b_h / (1 + b_h)
```

Hedging burns EV equal to the vig in `b_h`; do it for utility, not for expectation.

**12. Middle break-even** (both sides at −110; win both = +2 units, miss = −0.0909... ≈ −0.1 units on the losing side's vig)

```
p_middle > 0.1 / 2.1 ≈ 0.0476  (≈ 1 in 21)
```

Generalized: `p_mid·(b1 + b2) > (1 − p_mid)·(1 − min(b1,b2))`-style parity computed from the two actual prices.

**13. Parlay fair value and EV** (independent legs, true probs `p_i`, parlay net payout `B`)

```
Fair net payout:  B_fair = Π(1/p_i) − 1
EV = (Π p_i)·(1 + B) − 1
```

Two-team card at 13/5 with 50% legs: `EV = 0.25·3.6 − 1 = −10%`. If a book computes parlay payouts by multiplying money-line prices, then `1 + EV_parlay = Π(1 + EV_i)`: parlays of +EV legs compound edge.

**14. Poisson prop pricing** (count-type props with event rate `λ`)

```
P(X = k) = e^(−λ)·λ^k / k!;  P(X ≥ 1) = 1 − e^(−λ)
```

**15. Risk-of-ruin sanity bound for flat betting** (even-money-ish bets, win prob `p`, bankroll of `N` units)

```
RoR ≈ ((1−p)/p)^N
```

Used to justify keeping unit size a small fraction of bankroll (Wong's guidance is conservative flat staking; Kelly `f* = (p·b − (1−p))/b` is the theoretical ceiling developed more fully elsewhere).

## Strengths and Limitations

**Strengths**

- **Pricing over prediction.** The book's frame — compute fair value for every derivative, bet only mispriced ones — is the correct frame, and it predates the mainstream by a decade-plus.
- **Everything is implementable.** Push tables, parity pricing, break-even roots, win-total convolutions: there is almost nothing in the book that cannot be turned directly into code. That is vanishingly rare for a 2001 gambling book.
- **Intellectual honesty.** Wong presents data, shows the arithmetic, and refuses to sell handicapping magic. Hedging is called what it is (paying vig for insurance); parlays are −EV except in stated conditions.

**Limitations and what has aged**

- **The Wong teaser edge has been repriced away, mostly.** Books moved two-team 6-point teasers from −110 to −120/−130, raising the per-leg hurdle from 72.4% to 73.9–75.2%, right against the strategy's historical performance. The 2015 extra-point rule change (33-yard PATs) and the analytics-era rise in 2-point tries and aggressive fourth downs thinned the mass on 3 and 7 somewhat. Modern public studies (e.g., Unabated, Action Network) find blind Wong teasers roughly break-even at −120 and losing at −130; the *method* (compare Πrᵢ to the price) survives, the *chart* does not auto-print money.
- **Half-point menus were fixed.** Books now charge 25 cents (or refuse sales) around 3 and 7. The valuation machinery still matters — for alternate lines, comparing books, and identifying stale menus — but the printed free lunch is gone.
- **Era-bound data.** All push/margin frequencies are from pre-2001 NFL football (16-game seasons, no overtime rule changes, old PAT). Any implementation must re-estimate the margin distribution on rolling modern data rather than use the book's tables.
- **Independence assumptions.** Season win totals and teaser legs are treated as (approximately) independent; modern practice models schedule correlation (teams play each other; league wins sum to a constant) and same-week correlations.
- **Thin on modeling and staking theory.** There is no power-rating/handicapping model, no market-timing (CLV) framework, and only rudimentary bankroll theory — later books (Miller's *The Logic of Sports Betting*, the Kelly literature, in-play/market-microstructure work) supersede it on those fronts.
- **Pre-modern market.** No betting exchanges, no live betting, no screen-scraped odds, no limits arms race. The market Wong beat was slower and softer than today's.

## What SharpOds Takes From This Book

1. **Price hurdle as a hard gate.** Every candidate bet is converted to implied probability via `p_imp(A)`; a bet is emitted only if the model's fair probability exceeds `p_imp` (after devigging the sharpest reference line via formula 2) by the configured edge threshold. −110 means the model must show > 52.38% — no exceptions, no "leans."
2. **Maintain a live empirical NFL margin distribution, conditional on closing spread**, re-fit each season on a rolling window. This single table drives half-point values, teaser leg probabilities, middle windows, and spread↔money-line conversion. Use `Φ(s/13.5)` only as a cold-start fallback; never hard-code Wong's 2001 push frequencies.
3. **Value every half point and alternate line by outcome-reallocation parity (formula 5), not by flat cents.** Buy/sell points only when the book's charge is on the profitable side of parity; flag any book whose menu misprices a key number.
4. **Teaser module = Wong's method, not Wong's chart.** For each candidate 6-point teaser leg, compute the teased cover probability from the margin distribution; bet two-team teasers only when `Π r_i · (1+b) − 1` exceeds the edge threshold at the *actual offered price* (−120/−130 aware). Legs crossing both 3 and 7 (dogs +1.5..+2.5, favs −7.5..−8.5) are the priority candidate set, but must re-qualify on current data.
5. **Season win totals via Poisson-binomial convolution** (formula 10) over game-by-game win probabilities derived from projected spreads for the full schedule; compare exact `P(Over)` to the devigged market price on both sides; apply a correlation haircut and enforce league-wide win-sum consistency across all team projections.
6. **Hedging policy: EV-max by default.** The engine never auto-hedges; it computes `h = X/(1+b_h)` and surfaces the EV cost of the hedge, hedging only when a bankroll-utility rule (drawdown/exposure cap) triggers or the hedge side is independently +EV. Middles are auto-flagged when the window probability from the margin table exceeds the price-derived hurdle (≈4.8% at −110/−110).
7. **Parlay logic: fair value is the product of devigged single-leg probabilities.** Emit parlays only from legs that are individually +EV (edge compounds) or from correlated combinations where the model's joint probability beats the multiplicative price.
8. **Derivatives-first scanning priority.** Following Wong's core thesis, allocate model attention where crude pricing rules live: teasers, alternate lines, bought points, props, win totals, and cross-market (spread vs. money line) inconsistencies — rather than trying to out-pick the efficient main spread market head-on.
