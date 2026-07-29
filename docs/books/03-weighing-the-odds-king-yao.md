# Weighing the Odds in Sports Betting

**King Yao, 2007** (Pi Yee Press — Stanford Wong's imprint — July 2007; 254 pages, 23 chapters; later reissued in paperback and ebook). Yao spent years as a professional options/derivatives trader before becoming a full-time gambler; he also wrote *Weighing the Odds in Hold'em Poker* (2005) and the long-running Super Bowl prop analyses on Wong's bj21.com.

---

## Why This Book Is Canon

*Weighing the Odds in Sports Betting* is the sharp community's original **relative-value playbook**. Published by the same house as Stanford Wong's *Sharp Sports Betting* (2001) and written as its natural companion, it appears on virtually every credible "best sports betting books" list and was, for over a decade, the standard answer to "how do I beat the market without a handicapping model?"

Its unique contribution is the systematic transfer of a **derivatives-trading mindset** to the sportsbook menu. Yao — a former options trader — treats the main game line (side and total at a sharp book) as the *underlying*, and everything else on the board as *derivatives priced off it*: first halves, second halves, quarters, team totals, moneylines vs. spreads, props, parlay cards, teasers, season win totals, futures. Where the underlying is efficient, the derivatives frequently are not, and Yao shows how to compute their fair prices from the underlying plus an empirical results database, and how to harvest the difference through relative-value bets, scalps, middles, hedges, and correlated parlays.

The book states its own purpose plainly: to teach the reader to evaluate sports betting "from an analytical perspective, not from a gambling perspective," and to serve as "a guideline to sports betting rather than a blueprint." It introduced (or standardized) the now-common distinction between the **handicapper**, who forms original opinions about teams, and the **relative-value player**, who profits purely from price discrepancies between related markets. Nearly all of the market-centric literature that followed — including Miller & Davidow's *The Logic of Sports Betting* (2019) — is a modernization of the frame Yao laid out here. For SharpOds, this book is the spec for the **derivative-pricing and cross-market-consistency layer** of the engine.

## Core Thesis

Every sports bet is a price, and the sharpest prices in the market are the main game lines; almost everything else a sportsbook offers is a derivative of those lines, priced with more vig, less attention, and frequent errors. A bettor therefore does not need to out-predict games to win: by anchoring fair value to the efficient main line (and an empirical database of score outcomes), computing what each derivative *should* cost, and betting only when the offered price deviates by more than the vig — while pricing every half point, hedge, middle, scalp, and parlay in explicit expected-value terms — a disciplined "relative-value player" can extract steady positive EV from the structure of the market itself.

## Key Concepts

### 1. Handicappers vs. relative-value players

Yao's foundational split. A **handicapper** wins by knowing something about the game the market doesn't. A **relative-value player** wins by knowing something about the *prices* — that two markets which must be mathematically related are quoted inconsistently. The book is overwhelmingly for the second player. This matters because relative-value edges are (a) testable against data, (b) durable across sports you know nothing about, and (c) exactly what software can automate. Everything below is a species of relative value.

### 2. The main line as the anchor; derivatives as the target

Sharp books take their biggest volume and sharpest action on full-game sides and totals, so those converge to near-efficient prices. First-half lines, quarter lines, team totals, moneylines (relative to spreads), props, parlay cards, and season win totals are generated *from* the main line — historically by an oddsmaker with a rule of thumb, today by an algorithm — and receive far less corrective action. Yao's core loop: take the main line as (approximately) true, derive the fair value of the derivative from it using historical score distributions, and bet the derivative when it is off by more than its vig. He applies this concretely to first-half betting, halftime (second-half) lines, team totals, Super Bowl props, and parlay cards.

### 3. Why lines move, line shopping, and bet timing

Lines move because of sharp action and new information (injuries, weather), and because books manage exposure. Consequences Yao draws:

- **Multiple outs are capital.** Different books hang different numbers; the best price across books is the only price that matters. Disagreement between books creates scalps and middles.
- **Bet timing is market-dependent.** Bet *early* into markets that are posted soft and corrected slowly — openers, props, derivative menus, and especially **parlay cards**, which are printed days before kickoff and go stale as the market moves. Bet *late* when you are trading with market information (e.g., waiting for the public to push a line to a better number, or for a key number to be crossed). In the 2000s NFL market the public reliably pushed favorites/overs, so value on dogs/unders tended to improve toward kickoff.
- **Reading moves.** A move at a sharp book signals information; chasing it ("steam") only works if you beat the slower books' copies — an early statement of the stale-line attack later formalized by Miller & Davidow.

### 4. The half point and push percentages

Perhaps the book's most-cited technical content. On spread bets, outcomes land on exact numbers with knowable frequency (NFL margins: 3 ≈ 9–10% of games, 7 ≈ 5–6%, 10 ≈ 4–5%; totals cluster on 41, 44, 37, 51 at ≈ 3–4% each — era-dependent and to be re-estimated from data). The value of a half point is therefore *not constant*: it equals the probability mass on the number it crosses (converted to EV), so a half point on/off 3 in the NFL is worth roughly 20–25 cents of moneyline juice while a half point through 8 is worth a few cents. Yao's push-percentage tables answer, in EV terms: when is buying a half point worth 10 cents? When is +2.5 −105 better than +3 −120? When is an off-market number worth hitting at a worse price? This is also the engine behind teaser evaluation (legs that cross both 3 and 7 — the Wong teaser from *Sharp Sports Betting* — are the only standard teasers that historically beat their price).

### 5. Removing pushes: comparing bets on different numbers

To compare a bet with push risk (e.g., −3) against one without (e.g., −2.5 or a moneyline), Yao conditions on the no-push outcomes: compute win probability among decided bets and compare that to the breakeven rate implied by the juice. This "remove the pushes" normalization is the correct general tool for comparing any two prices on different numbers, and it recurs throughout the book.

### 6. Moneylines vs. spreads (market value across bet forms)

The same opinion can be expressed as a spread bet or a moneyline bet, and the two are linked through the empirical distribution of victory margins: a given spread implies a fair moneyline and vice versa. Yao provides conversion tables built from his database and shows how to detect when one form is cheaper than the other — the simplest instance of his "market value" idea: *always express a view through the cheapest available instrument.*

### 7. Hedging as priced insurance; hedge mistakes

Hedging (betting the other side of an existing position, typically a futures ticket or accumulated parlay leg) almost always *costs* EV, because the hedge bet itself carries vig. Yao's framework: compute the EV of the unhedged ticket from a fair probability estimate, compute the EV cost of the hedge, and treat that cost as an insurance premium to be paid only when the variance reduction is worth it (ticket large relative to bankroll, or utility reasons) — or when the hedge is itself zero/positive EV, in which case it is really a scalp and should be taken to the maximum. His catalogued **hedge mistakes**: hedging trivially small positions (paying vig for insurance you don't need), hedging through heavily juiced derivative markets when a cheaper instrument exists, hedging at the worst point of a line move, and reflexively "locking up" profit without computing what the lock costs. A dedicated chapter applies this to **hedging with second-half lines** at halftime.

### 8. Scalping and middling

- A **scalp** is riskless: two books quote prices on opposite sides whose implied probabilities sum to less than 1; bet both, guarantee profit. Yao treats scalps as the purest fruit of having many outs, and notes their real-world frictions (limits, timing risk of one leg moving, account wear).
- A **middle** buys both sides at *different numbers* (e.g., +7 and −6.5, or Over 44 / Under 45.5), losing a small known amount (the juice) when the result misses the window and winning both bets when it lands inside. Middling is +EV precisely when the probability of landing in the window exceeds the breakeven percentage implied by the juice (~4.8% at −110 both sides for a pure 1-point middle) — which is why middles across NFL key numbers 3 and 7 can be systematically profitable while most other middles are lottery tickets. The push-percentage tables from concept 4 are exactly the input needed.

### 9. Parlays, parlay cards, and correlation

- **Fair parlays**: a parlay of independent legs at true multiplied odds is just a re-vigged compound bet — the house edge compounds with each leg, and fixed payout charts (13/5 on two teams, 6/1 on three) are worse still. Parlays of *+EV* legs, however, compound the edge along with the variance, so parlays are not inherently sucker bets — pricing decides.
- **Correlated parlays** are the book's signature attack: when legs are positively correlated (same-game side and total in the right game shapes, first half + full game, a team's win and its season total), the true joint probability exceeds the product of the marginals, while the payout assumes independence. If the correlation lift beats the vig, the parlay is +EV. Books ban the strongest correlations; Yao teaches finding the ones that slip through — especially on **parlay cards** (ties-win/ties-lose rules, half-point cards, stale numbers vs. the live market), which combine correlation leaks with stale-line value.

### 10. Season win totals and futures

Season win totals are derivatives of ~16 (then) individual game lines; futures are derivatives of the whole schedule. Yao shows how to project a team's win distribution, compare it to the posted total and price, exploit disagreements *between books' win totals*, relate win totals to divisional/championship futures, and hedge or scalp futures positions late in the season using game moneylines. Futures carry enormous overround (booksums of 120–160%), so a futures bet must beat not just your projection but the worst vig on the board — often the same exposure is available far cheaper as a sequence of game bets.

### 11. Props and Super Bowl props

Prop menus — hundreds of markets posted quickly by a small crew, at high vig but with soft prices and low limits — are the derivative attack at maximum intensity. Many props are directly derivable from the main lines (team totals from spread+total; margin and first-score props from margin distributions; player props from season rates), and the sheer menu breadth guarantees mistakes and cross-book discrepancies. Yao's Super Bowl prop chapter is the classic worked example: derive fair values, shop every book, bet the outliers, and accept the low limits as the price of the highest per-dollar edges in sports.

### 12. Money management

Deliberately brief and conservative: know the EV and variance of what you bet, size bets as a small fraction of a dedicated bankroll, scale with edge, and never let hedging/staking decisions be driven by fear of variance you could afford. The formal Kelly apparatus is mentioned but not developed — Yao's stance is that bet *selection* (price) dominates bet *sizing* for the relative-value player, and oversizing is the classic way winners go broke.

## The Math

Notation: decimal odds `d` (total return per 1 staked); American odds `A` (negative `A`: risk `|A|` to win 100; positive `A`: risk 100 to win `A`); `p` = true probability. Conversions: `d = 1 + 100/|A|` for negative `A`, `d = 1 + A/100` for positive `A`; implied probability `p_imp = 1/d`.

**1. Expected value with pushes.** For a spread/total bet with win, push, loss probabilities `p_w`, `p_0`, `p_l` (`p_w + p_0 + p_l = 1`) at decimal odds `d`, per unit staked:
`EV = p_w*(d - 1) - p_l`
(pushes return the stake and contribute 0). This is the master formula; everything below specializes it.

**2. Breakeven win rate and push removal.** Breakeven no-push win probability at odds `d`: `p_be = 1/d` (at −110, `p_be = 110/210 = 0.5238`). To compare bets on different numbers, remove pushes: `p' = p_w / (p_w + p_l)`; the bet is +EV iff `p' > p_be`.

**3. Half-point value across number k.** Let `P_k = P(result lands exactly on k)` (from empirical push-percentage tables, per league/market/era). Moving your number by half a point across `k`, per unit staked:
- loss becomes push (e.g., +2.5 → +3): `ΔEV = P_k * 1`
- push becomes win (e.g., +3 → +3.5): `ΔEV = P_k * (d - 1)`
- full point, loss becomes win (e.g., +2.5 → +3.5): `ΔEV = P_k * d`
Buy/sell the half point iff `ΔEV` exceeds the EV cost of the price change (compute both sides with formula 1). Example: NFL `P_3 ≈ 0.095` makes +2.5 → +3 worth ≈ 9.5% of stake ≈ 20–25 cents of moneyline, while a 10-cent price move from −110 to −120 costs ≈ 4% of stake — so paying 10 cents to cross 3 is clearly +EV and paying 10 cents to cross 8 (`P_8 ≈ 0.02`) is clearly −EV.

**4. Scalp (two-sided arbitrage) condition and staking.** Best available prices `d_A`, `d_B` on the two sides: scalp exists iff `1/d_A + 1/d_B < 1`. Let `B = 1/d_A + 1/d_B`. Stake fraction on each side `s_i = (1/d_i)/B`; guaranteed profit per unit of total stake = `1/B - 1`.

**5. Middle breakeven percentage.** Both sides bet at American −`J` (risk `J/100` to win 1 each). If the result lands in the middle window with probability `P_mid`: net `+2` on a middle, net `(100 - J)/100` otherwise. Breakeven:
`P_be = (J - 100) / (J + 100)`
At −110/−110: `P_be = 10/210 = 4.76%`. Bet the middle iff `P_mid > P_be` (with `P_mid` from the empirical landing distribution of the gap numbers; note that a result landing exactly on one bet's number pushes that side and wins the other, netting +1 — include this term when the window contains a whole number).

**6. Hedge EV and full-hedge stake.** Hold a ticket paying `W` if the position wins, with true win probability `p`. Unhedged `EV = p*W`. Hedge `h` on the opposite side at decimal `d_h` (true probability of that side `q = 1 - p`):
`EV_hedged = p*W - h*(1 - q*d_h)`
so the **EV cost of the hedge** is `h*(1 - q*d_h)` — positive whenever the hedge price is worse than fair (`d_h < 1/q`), zero at fair, negative (a scalp) when `q*d_h > 1`. The stake that equalizes both outcomes (full hedge / lock): `h* = W/d_h`, locking `W*(d_h - 1)/d_h`. Rule: pay the EV cost only as deliberate insurance sized to bankroll utility; if the cost is ≤ 0, max the bet.

**7. Parlay pricing and correlation.** Independent legs with true probabilities `p_1..p_n` and a parlay paying decimal `d_par`:
`EV = (∏ p_i) * d_par - 1`
"True odds" parlays set `d_par = ∏ d_i` (compounding each leg's vig); fixed charts (2-team 13/5 → coin-flip EV = 0.25*3.6 − 1 = −10%) are worse. For two correlated legs:
`EV = P(A) * P(B|A) * d_par - 1`
Bet iff `P(A ∩ B) > 1/d_par`, i.e., when the correlation lift `P(B|A)/P(B)` exceeds the total vig embedded in `d_par`.

**8. Team totals from spread and total.** Game total `T`, favorite spread `S` (points laid): fair expected points — favorite `(T + S)/2`, underdog `(T - S)/2`. Use as the anchor for team-total and derived prop pricing (with a distribution around the mean for O/U probabilities).

**9. Derivative-line consistency (first half / halves / quarters).** Fair 1H line = `r * (game line)`, with `r` estimated per league from the historical joint distribution of period scores (empirically NFL 1H totals ≈ 45–48% of game totals because of end-of-game scoring dynamics; 1H spreads slightly above half the game spread). Second-half line at halftime must be consistent with the pre-game line and the 1H score. Bet the derivative when `|posted − fair|` exceeds the derivative's vig plus an error buffer; the ratios/distributions are estimated, never assumed.

**10. Spread ↔ moneyline equivalence.** Given the empirical margin distribution `f(m | S)` for games with spread `S`, fair moneyline probability `p_ML = P(margin > 0 | S)` (excluding ties per market rules). Maintain the mapping as a table per league; bet whichever form (spread or ML) offers the bigger EV for the same opinion (formula 1).

**11. Season win totals.** From per-game win probabilities `p_1..p_n` (derived from market lines or a rating system): mean `μ = Σ p_i`, variance `σ² = Σ p_i*(1 - p_i)`; `P(over x.5) ≈ 1 - Φ((x + 0.5 - μ)/σ)` by normal approximation (Yao works from projections and historical distributions; the normal/Poisson-binomial implementation is the modern operationalization — exact Poisson-binomial is cheap and preferred). Compare against every book's number and price; also check consistency between win totals, division odds, and futures.

**12. Futures overround and replication.** Futures booksum `B = Σ 1/d_i` over all entrants (commonly 1.2–1.6). Fair probability by normalization `p_i = (1/d_i)/B` is only a weak prior at that vig level; before betting any future, price the **replicating sequence of game bets** (rolling moneylines) and take the cheaper route.

## Strengths and Limitations

### Strengths

- **The right abstraction.** Underlying-vs-derivative is the correct model of a sportsbook menu, and it turns most of the board into computable relative-value problems. This is the single most automatable betting book of its era.
- **Empirical, not anecdotal.** Push percentages, margin distributions, ML/spread conversions, and 1H relationships all come from a results database, and Yao is explicit that the tables are estimates to be refreshed — a data pipeline, described in 2007.
- **Complete EV accounting of position management.** The hedging/middling/scalping treatment — pricing insurance instead of moralizing about it — is still the cleanest in the literature, and the "hedge mistakes" catalogue remains accurate about how winners leak EV.
- **Honest scope.** "A guideline rather than a blueprint": Yao tells the reader the tables will age and the method is what transfers. That honesty is why it aged as well as it has.

### Limitations and what has aged or been superseded

- **The numbers are stale.** Yao's NFL tables predate the 2015 extra-point move (33-yard PATs and the two-point uptick shifted margin masses on 3, 7, and 8), rule-driven scoring inflation, and three-point-era NBA scoring. Every table must be re-estimated per era; only the *method* is durable. His parlay-card and Vegas-retail specifics describe a pre-2018, pre-mobile market.
- **Market-structure vocabulary predates the modern school.** Yao uses sharp lines as anchors but does not formalize market-maker vs. retail hierarchies, devigging methods, or CLV as a grading metric — *The Logic of Sports Betting* (2019) supplies that layer. SharpOds should anchor Yao's derivative pricing to the devigged market-maker probabilities defined in the Miller/Davidow spec, not to raw quoted lines.
- **Devig is implicit and simple.** Where Yao removes vig he does so proportionally; favorite–longshot bias in high-overround markets (his own futures and props targets!) calls for power/Shin methods. Apply modern devig before using any anchor.
- **Staking theory is thin.** Kelly and fractional-Kelly sizing, simultaneous-bet Kelly, and correlation-aware portfolio sizing must come from elsewhere (Kelly 1956; the academic literature).
- **The softest targets have hardened.** Same-game correlations are now priced (SGP engines), derivative menus are generated by feed vendors with fewer gross errors, and stale windows are shorter. The edges Yao describes persist mainly in props, low-liquidity derivatives, parlay-card rules quirks, and cross-book inconsistency — smaller and faster, but structurally identical.
- **Pre-legalization landscape.** The Vegas/offshore world of 2007 (walk-in parlay cards, slow copying) differs from the post-2018 US market in parameters, though not in structure.

## What SharpOds Takes From This Book

Concrete directives for the unified model:

1. **Build the derivative-pricing layer exactly as Yao specifies.** For every game, compute fair values for 1H/2H/quarter lines, team totals, ML↔spread equivalents, and derivable props *from the devigged sharp main line* plus per-league empirical score distributions (formulas 8–10). Emit a bet signal when `posted EV − fair` clears the derivative's vig plus an error buffer scaled to the estimate's sample size.
2. **Maintain living push-percentage tables.** Estimate `P_k` per league, market type, and era window (post-2015 NFL split); price every half point, alt line, teaser leg, and off-market number with formula 3; never pay more for a half point than `ΔEV` converts to in cents, and auto-flag books selling half points below fair.
3. **Run a standing scalp/middle scanner across all connected books.** Trigger scalps on `Σ 1/d_i < 1` (formula 4) with stake allocation `s_i = (1/d_i)/B`; trigger middles when the empirical landing mass of the gap window exceeds `(J-100)/(J+100)` (formula 5) plus a buffer — prioritize windows containing 3 and 7 in football.
4. **Price every hedge before recommending it.** Compute hedge EV cost `h*(1 − q*d_h)` (formula 6) using devigged `q`; recommend hedges only when cost ≤ 0 (scalp — then maximize) or when a bankroll-utility rule justifies the premium; route hedges through the cheapest consistent instrument (Yao's hedge-mistakes list becomes validation checks).
5. **Scan for under-priced correlation.** Model joint distributions of same-game side/total and 1H/full-game outcomes; bet any parlay where modeled `P(A∩B) > 1/d_par` (formula 7); apply the same joint model to parlay-card rules (ties-win, stale card numbers vs. live market).
6. **Schedule bets by market maturity.** Attack derivative menus, props, and early-posted numbers at open (soft, slowly corrected); bet main lines late with the market's information; treat any card/menu printed before a main-line move as a stale-line scan trigger.
7. **Price season wins and futures by replication.** Compute win-total distributions via Poisson-binomial over market-implied game probabilities (formula 11); compare every book's total/price pair; refuse futures whose EV is beaten by the replicating game-bet sequence after the futures booksum (formula 12) is accounted for.
8. **Normalize all cross-number comparisons by removing pushes** (formula 2) so the EV engine compares −3 −105 vs −2.5 −115 vs ML on one scale — this is the low-level utility every other directive calls.
