# The Logic of Sports Betting

**Ed Miller & Matthew Davidow, 2019** (self-published, May 17, 2019; followed by the 2023 sequel *Interception: The Secrets of Modern Sports Betting*)

Miller is a bestselling poker/gambling author (300,000+ copies sold, e.g. *Small Stakes Hold 'em* with Sklansky and Malmuth) with experience on the oddsmaking side; Davidow is a professional sports modeler who co-founded two private sports analytics firms and has beaten major markets for 15+ years.

---

## Why This Book Is Canon

Published one year after the *Murphy v. NCAA* repeal of PASPA opened the US market, *The Logic of Sports Betting* became the default "read this first" recommendation in the sharp community — cited approvingly by Pinnacle's own educational arm, by the Unabated/Circa orbit of professional bettors, and on virtually every credible "best sports betting books" list since 2019.

Its unique contribution is **market microstructure**. Almost every prior betting book was about handicapping (building a better opinion about teams). Miller and Davidow instead explain *how the sportsbook industry actually works*: who originates prices, who copies them, how vig is embedded, why winners get limited, and why the structure of the market itself — not superior sports knowledge — is where most accessible edge lives. They demolished two pieces of folklore that had survived for decades:

1. **The "balanced book" myth** — the idea that books try to get 50/50 action and collect vig risk-free. Real books, especially market makers, take positions and trade.
2. **The "pick winners" frame** — the idea that betting is about being right about teams. The book reframes every bet as a **trade against a price**, making sports betting legible as a financial-markets problem.

Concepts the book either coined or brought into mainstream betting vocabulary: **market-maker vs. retail sportsbooks**, **synthetic hold**, and the systematic attack on **derivative markets**. For SharpOds, this is the market-structure spec: it defines where trustworthy prices come from and how to measure the cost of betting.

## Core Thesis

Sports betting is a trading game, not a picking game. Betting lines are prices discovered by a market: a small number of market-making books originate lines, sharp money corrects them, and everyone else copies. The (devigged) price at a high-limit market maker — especially at close — is the best publicly available estimate of true probability, and a bettor's job is not to out-predict the game but to systematically buy prices that are better than that estimate: by shopping every line across many books (driving synthetic hold toward or below zero), by exploiting the copying lag and derivative-pricing errors of retail books, and by validating everything against closing line value rather than short-term results.

## Key Concepts

### 1. Two kinds of sportsbooks: market makers and retail books

- **Market makers** (the book's archetypes: Pinnacle, CRIS/Bookmaker, and offshore originators; today Circa is the US example) post lines first, at low margins and high limits, and *welcome* sharp action because sharp bets are information — they are paid, in effect, to have their prices corrected. Their business is price discovery plus volume.
- **Retail books** (DraftKings, FanDuel, Caesars, etc.) do not originate prices. They copy market makers (or license third-party feeds), add extra margin, compete on marketing and promotions, and manage risk by **limiting or banning winning customers** rather than by pricing well.
- Consequence: **not all prices carry the same information.** A move at a market maker reflects new information (sharp money); a move at a retail book usually reflects copying ("moving on air"). Retail books are structurally vulnerable in the window between a market-maker move and their copy — the **stale line** — which is precisely why they limit winners.

### 2. Where lines come from (price discovery)

Openers are provisional, posted at low limits as a probe. Sharp bettors hit errors, the market maker adjusts, limits rise as confidence grows, and the line converges toward an efficient price. By closing time the line has absorbed the maximum information — injuries, weather, sharp models, betting-syndicate opinion. Hence the **closing line at a market maker is the sharpest single number in the market**, and beating it consistently is the practical definition of edge.

### 3. Hold: the price of betting

The book teaches bettors to compute, for any market, how much margin is baked into the odds (the "booksum" or overround, and the hold derived from it — full math below). Key practical points:

- A standard −110/−110 spread market holds ≈ 4.5%; a bettor flipping coins at −110 loses ≈ 4.55% of every dollar risked.
- Hold varies enormously by bet type: mainline sides/totals are cheapest; parlays, teasers, player props, and futures carry far higher hold (futures booksums of 120–160% are common). **Hold is the hurdle your edge must clear**, so know it before betting anything.

### 4. Synthetic hold and line shopping — the #1 accessible edge

The single most famous idea in the book. You are not forced to bet both sides at one book: with accounts at many books you can take the *best* price on each side, constructing a **synthetic market** whose hold is lower than any individual book's — often near 0%, sometimes negative (an arbitrage). The authors' "0% synthetic hold" framing is the crux of their recommended baseline strategy: **line shopping does not make your opinions better, it makes every opinion cheaper to express**, converting many losing bettors into breakeven ones and breakeven bettors into winners. A corollary: the count and diversity of your betting accounts ("outs") is itself capital.

### 5. Devigging: recovering true probability from a price

Because quoted odds embed margin, implied probabilities in a market sum to more than 1. Removing the vig (the book uses the simple proportional method — normalize implied probabilities to sum to 1) yields the market's **fair probability** for each outcome. Applied to a sharp market maker's line, this devigged probability is the best public estimate of the true probability, and therefore:

- the correct **benchmark for any model** (if your model disagrees with the devigged sharp close, the default assumption is that your model is wrong);
- the correct **input for EV calculations** against softer books' prices (the "top-down" method: devig the sharp line, then bet any retail price that beats it).

### 6. Closing Line Value (CLV) as the measure of skill

Short-term win/loss records are noise. The book argues the honest scorecard is whether your bet prices consistently beat the devigged closing price at the sharpest market. Positive CLV over a meaningful sample implies real edge and predicts long-run profit; negative CLV means you are the sucker regardless of recent results. Grade the process, not the outcome.

### 7. Derivative markets and internal consistency

Books offer hundreds of **derivative markets** (first halves, quarters/periods, team totals, alt lines, props, live lines) generated algorithmically from a handful of primary inputs (full-game spread and total). These generators make systematic errors — wrong margin distributions, ignored key numbers, mishandled correlations, rules edge cases. Two attack modes:

- **Cross-market consistency**: derive what the derivative *should* cost from the sharp primary line (e.g., via an empirical margin distribution); bet derivatives that are mispriced relative to it.
- **Synthetic replication**: combine bets (e.g., first half + second half, or moneyline + spread) to replicate another market; when the synthetic beats the direct price, trade the discrepancy (including middles and outright arbs).

### 8. Key numbers and the value of half points

In football, margins cluster on key numbers (3 and 7 above all). A half point is not worth a constant amount: its value equals the probability mass sitting on the number it crosses. The book teaches pricing half points from push probabilities (formula below) so a bettor knows when buying/selling points or taking an off-market number is +EV — and why teasers crossing 3 and 7 (Wong-style) historically beat their pricing.

### 9. Bet timing, limits, and account economics

Bet early (into openers) when you have an information/model edge the market hasn't priced; bet late when you are piggybacking market information. Respect that limits are a signal: books offer high limits where they trust their price. Winning players must manage account longevity at retail books (bet sizing, market selection) because being limited is the tax on beating copiers. Promotions and bonuses in the new legal market are real, computable EV and should be harvested, not ignored.

## The Math

All formulas use decimal odds `d` (payout per 1 unit staked, stake included). Stakes are 1 unit unless stated.

**1. American ↔ decimal odds conversion.** For American odds `A`:
- If `A >= 100` (positive): `d = 1 + A/100`
- If `A <= -100` (negative): `d = 1 + 100/|A|`
- Inverse: if `d >= 2`: `A = 100*(d-1)`; if `d < 2`: `A = -100/(d-1)`

**2. Implied probability of a price.** `p_imp = 1/d`. Equivalently from American odds: negative `A`: `p_imp = |A| / (|A| + 100)`; positive `A`: `p_imp = 100 / (A + 100)`. (Example: −110 → 110/210 = 0.5238.)

**3. Booksum (overround).** For an n-outcome market with prices `d_1..d_n`: `B = sum_i (1/d_i)`. `B > 1` means the market holds margin; `B - 1` is the overround.

**4. Theoretical hold percentage** (book's take as a fraction of balanced two-way handle): `H = 1 - 1/B = (B - 1)/B`. Example: −110/−110 → `B = 2 * 0.52381 = 1.04762`, `H = 4.55%`. Equivalently, a no-edge bettor's expected loss per unit staked at −110 is `0.5*(100/110) - 0.5 = -4.55%`.

**5. Proportional (multiplicative) devig.** Fair probability of outcome i: `p_fair_i = (1/d_i) / B`. Fair decimal odds: `d_fair_i = 1/p_fair_i = d_i * B`. (This is the method the book uses; see Limitations for refinements.)

**6. Synthetic booksum and synthetic hold** (line shopping across k books). Let `d_i* = max over all books of d_i` (best available price on outcome i). Then `B_syn = sum_i (1/d_i*)` and `H_syn = 1 - 1/B_syn`. `B_syn < 1` ⇒ arbitrage exists.

**7. Arbitrage staking and guaranteed profit.** When `B_syn < 1`, stake fraction on outcome i: `s_i = (1/d_i*) / B_syn` (fractions sum to 1). Guaranteed return per 1 unit of total stake: `1/B_syn`; guaranteed profit margin: `1/B_syn - 1`.

**8. Expected value of a bet.** With true (fair) probability `p` and offered decimal odds `d`: `EV = p*d - 1` per unit staked. Bet qualifies when `EV > threshold` (threshold covers estimation error and costs).

**9. Breakeven win probability.** `p_be = 1/d` (American: `p_be = |A|/(|A|+100)` for negative `A`, `100/(A+100)` for positive `A`). You need `p > p_be` to profit.

**10. Closing Line Value (per bet, in EV terms).** Let `p_close` = proportionally devigged closing probability at the reference market maker for your outcome, and `d_bet` = the decimal odds you actually got. `CLV_EV = p_close * d_bet - 1`. Aggregate mean `CLV_EV > 0` over a sample ⇒ evidence of edge; use it as the model's grading metric.

**11. Half-point value at a key number** (spread markets). Let `P_k = P(final margin lands exactly on number k)` (empirical, per league/era; NFL: `P_3 ≈ 0.09–0.10`, `P_7 ≈ 0.05–0.06`). Moving your line by half a point across `k`:
- Loss becomes push (e.g., dog +2.5 → +3): `ΔEV = +P_k * 1` per unit staked (stake refunded instead of lost).
- Push becomes win (e.g., dog +3 → +3.5): `ΔEV = +P_k * (d - 1)` per unit staked.
- Full point through `k` (loss → win): `ΔEV = +P_k * d`.
Buy/sell points only when the price charged is less than `ΔEV`.

**12. Free-bet (bonus) conversion EV.** A free bet of size `S` returns winnings only: `EV = p * (d - 1) * S`. Under efficient pricing (`p ≈ 1/d`), `EV ≈ S * (d-1)/d`, which increases with `d` — convert free bets on longshots (in low-hold markets) to realize 70%+ of face value.

**13. Top-down bet trigger (the book's core loop, composed from 5, 6, 8).** For each outcome in each market: compute `p_fair` from the sharpest available book (or a devigged consensus of market makers); find `d_best` across all connected books; bet when `p_fair * d_best - 1 > threshold`.

## Strengths and Limitations

### Strengths

- **The correct mental model of the industry.** The market-maker/retail distinction, line origination, and "you trade prices, not teams" remain the accurate description of how the market works, and everything in it is testable against data.
- **Actionable without a model.** Synthetic hold, line shopping, devigging, and CLV grading are implementable by any bettor (or engine) immediately; they don't depend on proprietary handicapping.
- **Honest about where edge lives.** It explicitly denies selling a picks system, and correctly ranks accessible edges: price access first, market selection second, original modeling last.
- **Foundational vocabulary.** Later sharp-community infrastructure (odds-screen tools, devig calculators, CLV tracking, prop-consistency scanners) is essentially this book turned into software.

### Limitations and what has aged or been superseded

- **Devigging is treated only proportionally.** Subsequent practice shows multiplicative devig misprices longshots (favorite–longshot bias). Modern engines use power, logarithmic/additive, and Shin-probability methods — often a weighted blend chosen per market shape. SharpOds should implement multiple devig methods, not just formula 5.
- **No staking theory.** The book deliberately omits bankroll math; Kelly and fractional-Kelly sizing must come from elsewhere (Kelly 1956; the *Fixed Odds Sports Betting* / academic literature).
- **2019 market snapshot.** Pinnacle no longer serves the US; Circa and betting exchanges/Novig-style operators filled the market-maker role stateside; retail books now buy pricing and risk services from feeds (Kambi, OpenBet, etc.) and use automated, near-instant copying plus per-customer limiting — the stale-line windows the book describes are much shorter, and promo generosity has been cut back since the 2021–22 acquisition wars. The *structure* still holds; the parameters have moved.
- **CLV is not universal.** Beating the close is a reliable skill signal only where the close is sharp (high-limit, liquid markets). In props, small leagues, and some derivatives the closing price is itself soft, so CLV against it is a weak or even misleading grader. The sequel *Interception* (2023) and later community work address these markets; SharpOds should apply CLV grading with a liquidity/limit weight.
- **Qualitative on derivatives.** The book says derivative generators err systematically but supplies no distributions or code; an implementer must build margin/score distributions (from data or simulation) to operationalize concept 7.
- **The "market price is truth" claim is a prior, not a law.** It is the right default, but documented inefficiencies (key-number pricing, longshot bias, correlated-parlay pricing) are exactly where the book itself tells you to attack — the claim should be encoded as a strong Bayesian prior with market-dependent confidence, not as dogma.

## What SharpOds Takes From This Book

Concrete directives for the unified model:

1. **Establish a price-authority hierarchy.** Classify every ingested book as market maker (Pinnacle, Circa, exchanges) or retail (copiers). Compute `p_fair` (formula 5, plus alternative devig methods) from market-maker prices only — weighted by limits and liquidity — and treat it as the baseline truth estimate. Retail prices are *targets* to bet into, never inputs to `p_fair`.
2. **Compute hold everywhere.** For every market snapshot store per-book booksum `B` and hold `H` (formulas 3–4), and cross-book synthetic booksum `B_syn` / hold `H_syn` (formula 6). Route bets exclusively through best-price execution; flag `H_syn < 1%` as near-arb and `B_syn < 1` as arb with stakes from formula 7.
3. **Top-down EV trigger as the default strategy.** Fire a bet recommendation when `p_fair * d_best - 1 > threshold` (formula 13), with the threshold scaled up in markets where `p_fair` confidence is low (low limits, single-originator markets, wide market-maker disagreement).
4. **Grade with CLV, weighted by market sharpness.** Log `CLV_EV` (formula 10) for every recommendation against the devigged market-maker close; require component strategies to show positive limit-weighted CLV to stay enabled; down-weight CLV as a grader in prop/small markets where the close is soft.
5. **Interpret line moves by source.** A market-maker move updates `p_fair` immediately (information); a retail-only move triggers a stale-line scan across lagging copiers (opportunity) rather than a belief update.
6. **Model derivatives from primaries.** Maintain empirical margin/score distributions per league; derive fair prices for halves, quarters, team totals, and alt lines from the sharp full-game line; bet derivative prices that violate consistency, and detect synthetic-replication arbs/middles (concept 7).
7. **Price half points empirically.** Use league-specific key-number masses `P_k` (formula 11) to value alt lines, point buys, and teaser legs; never pay more than `ΔEV` for a half point and always take extra value when off-market numbers cross 3/7 in football.
8. **Treat promos as a first-class EV stream.** Value free bets and boosts with formula 12 and route conversions to high-odds, low-hold markets; account-longevity constraints (limit risk at retail books) are part of the optimization, not an afterthought.
