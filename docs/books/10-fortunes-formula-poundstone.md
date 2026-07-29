# Fortune's Formula: The Untold Story of the Scientific Betting System That Beat the Casinos and Wall Street

**William Poundstone — Hill and Wang (Farrar, Straus and Giroux), New York, 2005 (hardcover ISBN 978-0809045990; paperback 2006, ISBN 978-0809046379)**

---

## Why This Book Is Canon

*Fortune's Formula* is the book that made the **Kelly criterion** part of the working vocabulary of every serious bettor. Before 2005, Kelly staking lived in a 1956 Bell Labs paper, a handful of academic exchanges, and the practice of a small circle of blackjack players and quantitative traders. Poundstone — a science writer with a physics background — turned that material into the definitive popular account, and the sharp community adopted it as the canonical text on **bankroll management and bet sizing**. When Wong, Buchdahl, Miller, or any modern staking article says "bet edge over odds" or "use fractional Kelly," this book is the common cultural reference behind the phrase. Ed Thorp, the central living figure of the story, has repeatedly cited the book approvingly as an accurate account of the history he lived.

Its unique contributions to the betting canon:

1. **It is the only book on this list about *sizing* rather than *picking*.** The other nine books are mostly about finding edges. Poundstone's subject is what to do once you have one: the mathematics of growing a bankroll at the maximum sustainable rate, and the precise sense in which betting too much converts a winning strategy into a losing one.
2. **It grounds Kelly in information theory, not folklore.** The book explains *why* the formula works — the deep identity between the rate at which you can grow money and the rate at which you receive information the market lacks (Kelly's `G_max = R`). This reframing — *an edge is information; bet size should be a function of information quality* — is the intellectual foundation of quantitative betting.
3. **It documents the failure modes with real bodies.** The proportional-betting math is bracketed by two cautionary histories: the mob-run racing wire (edges from faster information, and what happens to those who hold them) and Long-Term Capital Management (what happens to brilliant people who overbet a genuine edge with 25-to-1 leverage). No other popular book makes the overbetting lesson as visceral.
4. **It presents the strongest case *against* Kelly fairly.** Poundstone gives the Samuelson/Merton critique a full and honest hearing. A bettor who has only read cheerleading for Kelly does not actually understand Kelly; this book is where most practitioners first met the counterarguments.

The book was widely acclaimed on publication and remains the standard recommendation — alongside Thorp's own technical papers — for anyone asking "how much should I bet?"

Within the SharpOds canon it is the capstone of the money-management layer. Wong and Miller/Davidow establish where edges live; Buchdahl establishes how to validate them statistically; Peta and Mack show how to build the models that produce `p`. Poundstone's book is the reason the output of all of that work is a *bet fraction* rather than a unit count: it supplies the objective function (log growth), the sizing formula (edge/odds), and the two boundary conditions (never above full Kelly; never a fixed stake that cannot shrink with the bankroll) that the rest of the system plugs into.

## Core Thesis

A gambler or investor with a genuine edge should bet a fixed *fraction* of current bankroll determined by the size of the edge relative to the odds (`f* = edge/odds`), because that policy — and only that policy — maximizes the long-run compound (geometric) growth rate of wealth while making total ruin impossible. Betting less sacrifices growth; betting more first adds only variance and then, past twice the Kelly fraction, produces certain long-run decline *even with the edge intact*. The formula falls out of Shannon's information theory: money grows at the rate at which you receive reliable information the market has not priced. The book's history — from wire-service mobsters through Thorp's blackjack and Princeton-Newport, to LTCM's collapse — is one long demonstration that edges come from privileged information and that the fatal error of smart people is not bad handicapping but overbetting.

## Key Concepts

### 1. Information is the edge (Shannon, Kelly, and the wire)

The book opens with the mob-controlled racing wire (Annenberg's Nationwide News Service, the murder of James Ragen, Bugsy Siegel's Trans-America): whoever gets race results *first* can past-post bookmakers — profit from an information channel faster than the official one. Claude Shannon's 1948 information theory quantified channels; John L. Kelly Jr., a Bell Labs physicist, connected the two in his 1956 paper "A New Interpretation of Information Rate" (Bell System Technical Journal — reportedly retitled from "Information Theory and Gambling" to soothe AT&T). Kelly's motivating example came from the quiz-show scandals era: a bettor learning outcomes of *The $64,000 Question* before the West Coast broadcast. His startling result: a gambler with a private wire transmitting winners can compound wealth at a rate equal to the **information rate of the channel** (`G_max = R`). Noise (wrong tips) reduces the growth rate exactly as it reduces channel capacity. For SharpOds the moral is structural: **a betting model is an information channel, and its sustainable growth rate is bounded by how much true information it adds over the market price**. Kelly himself never bet a dollar with his formula; he died in 1965 at 41.

### 2. The Kelly criterion: edge over odds

For a binary bet paying net odds `b` (profit per unit staked; decimal odds minus 1) with true win probability `p`:

```
f* = (b·p − q) / b        (q = 1 − p)
```

The numerator `b·p − q` is the **edge** (expected profit per unit staked); the denominator is the **odds**. Hence the famous mnemonic **"edge/odds"**. Equivalently `f* = p − q/b`. If the edge is zero or negative, bet nothing. For an even-money bet this reduces to `f* = p − q` — a 55% coin-flip edge means betting 10% of bankroll. Crucially, `f*` is a fraction of *current* bankroll: stakes shrink automatically in drawdowns and grow in upswings, which is why a Kelly bettor can never be fully ruined by any finite losing streak (in the idealized, infinitely divisible-bankroll model).

In sportsbook terms: at decimal odds `d`, `b = d − 1`; at American odds `+A`, `b = A/100`; at `−A`, `b = 100/A`. A model probability of 54% on a −110 side (`b ≈ 0.909`) gives `f* = (0.909·0.54 − 0.46)/0.909 ≈ 3.4%` of bankroll — realistic point-spread edges translate into low-single-digit stake fractions even at *full* Kelly, which is why any staking scheme routinely recommending 5–10% of bankroll on standard-priced sides is overbetting on its face.

### 3. Why logarithms: geometric versus arithmetic mean

Kelly betting is exactly the policy that maximizes the **expected logarithm of wealth** per bet — equivalently, the geometric mean of wealth relatives. Poundstone traces the idea to Daniel Bernoulli's 1738 resolution of the St. Petersburg paradox and to Henry Latané's 1950s "geometric mean criterion." The core fact: repeated multiplicative outcomes compound by their *geometric* mean, which is dragged below the arithmetic mean by variance (`g ≈ μ − σ²/2`). Maximizing expected wealth (arithmetic mean) tells you to bet everything every time — a policy that ends in ruin with probability approaching 1. Maximizing expected *log* wealth optimizes what actually accumulates. This is the book's deepest practical lesson: **for a compounding bankroll, EV per bet is the wrong objective function; expected log-growth is the right one.**

### 4. What Kelly optimality actually guarantees (Breiman's theorems)

Poundstone reports the rigorous results (Leo Breiman, 1961): the Kelly bettor (a) achieves a higher long-run growth rate than any "essentially different" strategy with probability 1 — given enough time, her bankroll exceeds a rival's by any factor you name; (b) minimizes the expected time to reach any sufficiently distant wealth goal; (c) never risks total ruin, since only a fraction of bankroll is ever staked. Expected time to double the bankroll is approximately `ln(2)/g` where `g` is the growth rate per bet.

### 5. The price: variance and drawdowns; fractional Kelly

Full Kelly is a wild ride, and the book is blunt about it. Exact results for the full-Kelly bettor: the probability of *ever* dropping to a fraction `x` of the starting bankroll is `x` itself — a 50% chance of halving at some point, a 1-in-10 chance of losing 90%. The chance of halving the bankroll *before* doubling it is 1/3. These are properties of the optimal strategy, not signs of failure. Practitioners' answer — used by Thorp himself, who has written that he typically operated at around half Kelly or less — is **fractional Kelly**: bet `c·f*` with `c < 1`. Half Kelly (`c = 0.5`) delivers about **75% of the maximum growth rate with half the volatility**, and collapses the drawdown distribution (probability of ever falling to fraction `x` becomes `x^(2/c − 1)` — for half Kelly, `x³`: the chance of ever halving drops from 1/2 to 1/8). Because real-world win probabilities are *estimates*, fractional Kelly also buys insurance against the far more dangerous error of unknowingly betting past true Kelly.

### 6. Overbetting: the asymmetric sin

The growth-rate curve `g(f)` is an inverted parabola (exactly, in the continuous approximation): rising from 0 at `f = 0` to its maximum at `f*`, falling back to **zero growth at `2f*`**, and *negative* beyond. Betting double Kelly earns nothing in the long run while enduring maximal swings; betting more than double Kelly drives wealth to zero with probability 1 — **with a winning strategy**. The curve's asymmetry is the operational takeaway: betting 1.5× Kelly yields the same growth as 0.5× Kelly but with roughly nine times the variance. Under-betting costs a little growth; over-betting costs everything. Since edge estimates are noisy and biased upward (selection effects: you bet when your model disagrees with the market, which is exactly when your model is most likely wrong), *systematic* overbetting is the default failure mode of quantitative bettors — the book's single most important warning.

### 7. Diversification and simultaneous bets (Thorp in practice)

Thorp's career is the proof of concept: Kelly-sized blackjack betting (stakes proportional to the count-indicated advantage) funded by Manny Kimmel's $10,000 bankroll, turning it into $21,000 over one 1961 weekend; then *Beat the Dealer* (1962); then warrant and convertible hedging in *Beat the Market* (1967); then Princeton-Newport Partners (1969–1988), which compounded near 15% annually net with no losing year until Giuliani's RICO-era raid (aimed at Drexel-related stock parking; PNP dissolved, and the convictions of its principals were later overturned). PNP's practical Kelly lesson: **many small, simultaneous, low-correlation positions allow larger total exposure at the same risk** — the joint Kelly solution across bets is not the sum of individual Kelly fractions. Correlated bets must share one Kelly budget; independent bets each get slightly less than their standalone fraction but sum to more aggregate action. (The book treats this qualitatively; the precise portfolio mathematics is in Thorp's later technical papers.)

### 8. Shannon's demon: growth from volatility

Shannon's famous MIT lecture: take a maximally volatile asset (doubles or halves each period, zero expected log-growth), hold half your wealth in it, and **rebalance to 50/50 every period**. The rebalanced portfolio grows about 6% per period out of an asset going nowhere — buying dips and selling rips mechanically harvests volatility. Shannon never traded the scheme (transaction costs), and his actual fortune came from concentrated buy-and-hold in companies he understood deeply (Teledyne, Motorola, HP — returns around 28% a year). But the demon illustrates the same log-optimal principle as Kelly: **constant-fraction exposure to a favorable-or-volatile process, continuously re-anchored to current wealth, is what compounds.** Also in this thread: Shannon and Thorp's 1961 wearable roulette computer — the first literal conversion of physics information into casino edge.

### 9. The Samuelson war

Paul Samuelson and Robert Merton attacked the Kelly school (Latané, Markowitz's flirtation, Thorp, later Cover) for decades, most famously in Samuelson's 1979 journal article written entirely in words of one syllable ("Why we should not make mean log of wealth big though years to act are long"). The critique is mathematically correct: maximizing `E[log W]` is optimal only for an agent with logarithmic utility; the "long run" argument involves a fallacy of large numbers; a more risk-averse agent rationally prefers fractional Kelly or less *forever*, not just as an approximation. The Kelly camp's response: almost-sure growth dominance and ruin-avoidance are properties most real bettors actually want, whatever their textbook utility function. Poundstone adjudicates honestly: Kelly is not a law of nature; it is the *upper bound* on rational aggressiveness. Everything above full Kelly is provably irrational for every investor; where to sit below it is a genuine preference.

### 10. Blowing up: LTCM as the anti-Kelly

The book closes the argument with Long-Term Capital Management: Nobel laureates (Merton and Scholes — the very critics of Kelly's "excessive risk-taking" framing), real statistical edges, and leverage near 30:1 on a few billion of capital — an effective betting fraction far beyond `2f*`. In 1998 the fund lost over 90% in months and required a Fed-brokered bailout. Thorp, who had declined to invest, ran comparable strategies for decades without a losing year at a fraction of the leverage. The juxtaposition is the book's thesis in one image: **the difference between the best track record in the business and a crater is not the edge; it is the fraction bet.**

### 11. What Kelly replaces: fixed stakes, martingales, and gambler's ruin

The book's mathematical backdrop is the classical **gambler's ruin** problem: a bettor wagering *fixed* amounts, even with an edge, faces a real probability of busting before the edge asserts itself — for even-money bets with win probability `p > 1/2` and a bankroll of `B` betting units, the ruin probability is `(q/p)^B`, which is small only when the bankroll is many units deep. With *no* edge, fixed-stake betting guarantees eventual ruin against an adversary with deeper pockets, and loss-chasing progressions (martingale: double after every loss) merely trade many small wins for rare catastrophic busts — the expected value never budges. Proportional (Kelly) betting dissolves the classical problem: stakes scale down with losses, so the idealized Kelly bettor's ruin probability is zero, and the *relevant* risk metric shifts from "probability of busting" to the drawdown distribution of Concept 5. This reframing — from ruin-avoidance to growth-versus-drawdown trade-off — is the conceptual jump that separates modern bankroll management from staking-plan folklore.

## The Math

All formulas in plain notation. `W` = current bankroll; stakes are always fractions of *current* bankroll.

1. **Kelly fraction, single binary bet.**
   `f* = (b·p − q) / b`
   where `b` = net odds (decimal odds − 1; profit per unit staked), `p` = true win probability, `q = 1 − p`. Bet `f*·W`. Bet 0 if `b·p − q ≤ 0`. Equivalent forms: `f* = p − q/b` ; "edge/odds" with edge `= b·p − q`.

2. **Expected log-growth per bet.**
   `g(f) = p·ln(1 + b·f) + q·ln(1 − f)`
   Maximized at `f = f*`. Even-money maximum: `g_max = ln 2 + p·ln p + q·ln q` (nats per bet).

3. **Kelly–Shannon identity.** For fair even-money odds with binary side information correct with probability `p`, the maximum doubling rate is
   `G_max = 1 − H(p)` bits per bet, `H(p) = −p·log2(p) − q·log2(q)`.
   In general the maximum growth rate equals the information rate `R` of the gambler's private channel.

4. **Multi-outcome with fair odds ("bet your beliefs").** With mutually exclusive outcomes at fair decimal odds `d_i`, stake `f_i = p_i` on each outcome `i`; growth rate `g = Σ_i p_i·ln(p_i·d_i)`. (With a track take, bet only a subset — solved by water-filling; Kelly's original paper.)

5. **Continuous (Gaussian) approximation** (Thorp's formulation for markets): for an asset with expected excess return `μ` per period and variance `σ²`, the growth-optimal exposure is
   `f* = μ / σ²`, with `g(f) = r + f·μ − f²·σ²/2` and `g_max = r + μ²/(2σ²)` (`r` = risk-free rate).

6. **Variance drag.** Geometric growth ≈ arithmetic mean − half the variance: `g ≈ μ − σ²/2`.

7. **Fractional Kelly.** Betting `c·f*` (0 < c ≤ 1) yields excess growth
   `g(c) = (2c − c²)·g_max_excess`
   (continuous approximation; `g_max_excess = μ²/(2σ²)`), with log-wealth volatility scaled by `c`. Half Kelly: 75% of maximal growth, half the volatility.

8. **Drawdown law.** Betting fraction `c` of full Kelly, the probability of *ever* falling to fraction `x` of the starting bankroll (before growing without bound) is
   `P(min W ≤ x·W₀) = x^(2/c − 1)`, `0 < x < 1`.
   Full Kelly (`c = 1`): `P = x`. Half Kelly: `P = x³`. Full Kelly doubles before halving with probability 2/3.

9. **Overbetting boundary.** `g(2f*) = r` (zero excess growth at exactly twice Kelly, continuous case); for `f > 2f*`, `g < r` and for `g(f) < 0` wealth → 0 with probability 1. Symmetry: `g(c) = g(2 − c)` — 1.5× Kelly grows like 0.5× Kelly with (1.5/0.5)² = 9× the variance.

10. **Doubling time.** Median/expected time to double ≈ `ln 2 / g`. Kelly minimizes expected time to any sufficiently distant wealth goal (Breiman 1961).

11. **Simultaneous bets.** Choose fractions `(f_1, …, f_n)` maximizing `E[ln(1 + Σ_i f_i·X_i)]` subject to `Σ_i f_i ≤ 1`, where `X_i` = net return per unit staked on bet `i`. Continuous approximation with covariance matrix `C` and mean excess-return vector `M`: `F* = C⁻¹·M`. Independent bets: each `f_i` slightly below its standalone Kelly; correlated bets share one budget.

12. **Shannon's demon (constant-proportion rebalancing).** Holding constant fraction `w` in an asset with period return `R`, rebalancing each period: `g = E[ln(1 + w·R)]`. For the double-or-halve coin-flip asset at `w = 1/2`: `g = 0.5·ln(1.5) + 0.5·ln(0.75) ≈ 0.0589` ≈ 6% per period from a zero-growth asset.

13. **Gambler's ruin (fixed-stake baseline).** Betting one fixed unit per even-money bet with win probability `p > 1/2`, starting bankroll of `B` units, against an effectively infinite adversary: `P(ruin) = ((1 − p)/p)^B`. With `p ≤ 1/2`, ruin is certain. This is the risk profile Kelly's proportional staking eliminates, and the reason SharpOds never sizes in fixed units.

## Strengths and Limitations

**Strengths**

- **The definitive treatment of the *only* part of betting that is solved.** Edge-finding is empirical and forever contested; given an edge and a probability estimate, optimal sizing is mathematics, and this book states it correctly, with its costs and failure modes, in a form practitioners actually absorbed.
- **Intellectual honesty.** Poundstone presents Samuelson's critique at full strength, reports Kelly's own formula's dependence on *true* probabilities, and never sells Kelly as a way to manufacture edge. Compare the staking-plan snake oil (Martingale et al.) that Buchdahl had to debunk: this book is the antidote at the source.
- **The overbetting asymmetry is taught unforgettably** — through the `g(f)` parabola, the drawdown laws, and LTCM. This is the lesson most quantitative bettors learn too late.
- **Historically reliable.** The Shannon/Kelly/Thorp/PNP history has been corroborated by Thorp's own memoir (*A Man for All Markets*, 2017) and technical writings.
- **It gives quantitative bettors their epistemology.** The information-channel framing (edge = information the market lacks; growth bounded by channel capacity) generalizes beyond any single formula and motivates measuring a model by calibration and log-score rather than win rate — exactly the evaluation stack a modern betting model needs.

**Limitations and what has aged or been superseded**

- **It is a history, not a manual.** There are no worked staking tables, no treatment of odds formats, no devigging, no estimation of `p`. Kelly sizing is only as good as the probability fed into it — and the book (correctly, but briefly) leaves the estimation problem to others. In SharpOds terms: this book supplies the objective function and the sizing layer; Buchdahl/Miller/Wong supply `p`.
- **Simultaneous and correlated betting is under-specified.** The practical portfolio-Kelly mathematics (Thorp 2006 "The Kelly Criterion in Blackjack, Sports Betting, and the Stock Market"; MacLean–Thorp–Ziemba 2011) postdates or goes beyond the book and must be pulled from those sources for implementation.
- **Parameter uncertainty is handled informally.** The book motivates fractional Kelly as volatility-taming; the modern justification is sharper: with *estimated* edges, full Kelly computed from a noisy/optimistic `p̂` is expected overbetting, and shrinkage of `p̂` toward the market price plus a fractional multiplier is the principled response (later Buchdahl's *Monte Carlo or Bust*, and the Bayesian-Kelly literature).
- **Idealizations:** infinitely divisible stakes (real minimum bets reintroduce a small ruin probability), unlimited re-betting at fixed edge (real books limit and ban winners), and no transaction costs. None break the framework; all shave the constants.
- **The Samuelson point stands.** Kelly is not "optimal" full stop; it is growth-optimal. A model may rationally target below-Kelly aggressiveness permanently. Modern practice (and SharpOds) treats full Kelly as a hard ceiling, not a target.
- **Sports-betting frictions are out of scope.** The book's exemplars could re-bet a stable edge thousands of times (blackjack hands, convertible positions). A sports bettor faces lumpy, clustered opportunities (whole slates settling simultaneously), stake limits that bind before Kelly fractions do at scale, and account longevity risk at recreational books — all of which push practical sizing further below the theoretical fraction and make the joint-bet formulation (Math item 11) the operative one, not the single-bet formula the book is famous for.

## What SharpOds Takes From This Book

1. **Objective function: expected log-growth of bankroll, not expected value.** Bet selection, sizing, and portfolio construction all maximize `E[Δ ln W]`. EV determines *whether* an opportunity exists; log-growth determines *whether and how much* to bet. Two bets with equal EV are not equal: the one at shorter odds contributes more growth per unit of variance.
2. **Sizing layer: fractional Kelly on devigged edges.** Stake `= c · max(0, (b·p̂ − q̂)/b) · W_current`, where `p̂` is the model's probability *after* shrinkage toward the sharp-market devigged consensus (see directive 3), `b` is the best available net price, and `W_current` is live bankroll (never starting bankroll — stakes must breathe with the roll).
3. **Default `c = 0.25`, ceiling `c = 0.5`, and never above `c = 1` under any override.** Rationale from the book's math: the growth penalty is asymmetric (1.5× Kelly = 0.5× Kelly's growth at ~9× the variance), and estimated edges are optimistic precisely when the model most disagrees with the market. `c` may rise toward 0.5 only as out-of-sample calibration evidence (CLV capture, closing-line beat rate, realized vs. predicted hit rates) accumulates.
4. **Shrink `p̂` toward the market before sizing.** Kelly with the *true* `p` is optimal; Kelly with an overestimated `p` is overbetting in disguise. SharpOds computes `p_bet = λ·p_model + (1 − λ)·p_market_devig` with `λ` set by the model's demonstrated calibration on that market type, and feeds `p_bet` — not raw `p_model` — into the Kelly formula.
5. **Joint sizing for simultaneous exposure.** Concurrent bets are sized by maximizing `E[ln(1 + Σ f_i X_i)]` numerically (or `F = C⁻¹M` as a fast approximation), not by summing standalone Kelly fractions. Same-game and correlated positions (side + total, futures + series prices) share a single Kelly budget via their covariance; a hard cap keeps total amount at-risk below the level at which estimated portfolio `g` stops increasing.
6. **Drawdown-based calibration audit.** The drawdown law `P(dip to x·W₀) = x^(2/c − 1)` is a falsifiable prediction. SharpOds continuously compares realized drawdown quantiles against the theoretical distribution for its chosen `c`; drawdowns statistically in excess of prediction are treated as evidence of overstated edge and trigger automatic reduction of `λ` and `c` — the system assumes overbetting before it assumes bad luck.
7. **Ruin guardrails for the discrete world.** Because minimum stakes break the "never ruined" idealization, sizing suspends (falls back to flat minimum or no bet) when `f*·W_current` approaches the minimum bet, and the bankroll figure fed to Kelly excludes any funds not actually deployable.
8. **Report growth rate, not ROI, as the headline metric.** Following the book's central identity, SharpOds evaluates itself on realized `g` (log-growth per bet and per period) and on information-theoretic edge measures (calibration and log-score against closing prices — the model's "channel capacity"), since these, not per-bet ROI, bound sustainable compounding.
