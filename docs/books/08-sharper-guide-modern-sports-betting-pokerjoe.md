# Sharper: A Guide to Modern Sports Betting

**True Pokerjoe ("Poker Joe"), 2016** (self-published; Kindle edition August 2016, paperback December 2016 — sometimes dated 2015 from earlier draft circulation, but the published editions are 2016)

The author is pseudonymous — a retired professional bettor writing from inside the pre-PASPA-repeal offshore market (the Pinnacle / CRIS-Bookmaker era). Nothing about his identity is verifiable; the book's standing rests entirely on the fact that working sharps recognized their own trade in it.

---

## Why This Book Is Canon

*Sharper* is the scrappy, first-person ancestor of the modern market-based school of betting. Three years before Miller & Davidow's *The Logic of Sports Betting* (2019) formalized market-maker/retail structure and synthetic hold, Poker Joe was already telling readers the uncomfortable truth in blunt, aphoristic chapters: the line is the game, the market is the best handicapper alive, and most people who think they are handicappers are actually just late, expensive followers of sharper money.

Its standing in the sharp community:

- It is a fixture on credible "best betting books" lists and was reviewed approvingly by Pinnacle's own betting-resources arm, which noted that while most betting books obsess over handicapping, **the majority of *Sharper* is about trading** — types of line movement, what each move means, and how to exploit it.
- It circulates as a standard recommendation alongside Wong's *Sharp Sports Betting* and Miller & Davidow in r/sportsbook and Unabated-orbit reading lists, usually with the caveat "ignore the style, absorb the worldview."
- Its tagline-level ideas entered the vocabulary: *"When you bet sports, you bet into a number. To win, you must make your own number"* and the framing that "sports" is only half of "sports betting."

Its unique contributions, relative to the rest of the SharpOds canon:

1. **The top-down frame, stated early.** Deriving your probability estimate from the sharpest market prices — rather than from team analysis — and firing at slower, softer numbers that lag it. Miller & Davidow later gave this a cleaner theory; Poker Joe gave it first as lived practice.
2. **Line-move interpretation as a discipline.** Origination vs. following, steam vs. head fakes, who moved / at what limits / whether it held — treated as a skill in itself, not a footnote.
3. **Betting as an operation.** Outs, limits, account longevity, schedules, record-keeping, emotional discipline — the unglamorous business layer that pure-math books skip and that actually determines whether a theoretical edge is ever collected.

## Core Thesis

You do not beat the game; you beat the number. The betting market — specifically the highest-limit, lowest-margin books where sharp money trades — is the best handicapper in the world, and its consensus price, especially at close, is the closest available approximation of truth. A bettor therefore wins in exactly one of two ways: **originate** a genuinely better number than the market (rare, hard, and the only way to move lines yourself), or **read the market top-down** — treat the sharp price as the true probability and systematically bet softer or slower numbers that deviate from it. In the short run the only honest scoreboard is whether your bet prices beat the close; win-loss records are noise. In the long run, profit equals a thin edge multiplied by high volume, and collecting it is an operational grind of price shopping, account management, and discipline — a business, not action.

## Key Concepts

### 1. The market is the best handicapper

A posted line at a sharp, high-limit book is not one bookmaker's opinion; it is a price that has already absorbed the opinions of the best bettors in the world, expressed through money. Any private opinion must be measured against that consensus before it is worth anything. The practical corollary that organizes the whole book: **your default assumption should be that the sharp line is right and you are wrong**, and edge is the exceptional, local, temporary case where that assumption fails.

### 2. "Make your own number" — the bottom-up path

Handicapping, properly understood, is not picking winners; it is producing an independent number (a spread, a total, a win probability) *before* looking at the market, then betting only when the market's number differs from yours by more than the vig. The book treats the mechanics briskly — power ratings, injury and lineup impact, situational adjustments, home-field values — not because they are unimportant but because the author's point is that the number, not the narrative, is the output. If you cannot state your own number, you do not have a bet; you have a feeling.

### 3. Top-down betting — the market-based path

The alternative to making your own number is to let the sharpest market make it for you. The top-down bettor watches the whole screen of books, treats the sharp books' current (devigged) price as the best estimate of truth, and bets when a slower or softer book hangs a number that deviates from it. His edge is **speed and price, not prediction**: he is arbitraging the propagation delay and laziness of the rest of the market. This is the book's most influential idea and the one most directly implementable by a machine — it converts betting from a sports-knowledge problem into a market-data problem.

### 4. Origination vs. following; steam and head fakes

Line moves are information, but only if read correctly:

- **Originators** move markets: their bets at market-making books cause the number to change. Everyone else is a follower.
- **Naive steam chasing loses.** By the time a follower can react, the value that caused the move has been absorbed into the new number, and books shade further against known steam. Chasing the move means paying yesterday's price plus a premium.
- **The follow rule:** a move is only actionable if you can still beat the number that prompted it — i.e., somewhere on the screen there is a stale price better than the *new* fair value implied by the moved sharp line. You are never betting "the steam"; you are betting a lagging book's failure to keep up.
- **Reading the move:** weight moves by *where* they happen (a move at a market-making book at full limits is signal; a move at a retail book is usually an echo), *when* (early, low-limit markets are sharp-vs-sharp; late moves may be public money), and *how they behave* (a real move persists; a **head fake** — a syndicate move designed to push the line so the other side can be bet bigger at a better price — snaps back).

### 5. Closing line value: the only short-term truth

Results over weeks or months are dominated by variance; the closing line is not. Because the close at a sharp book is the market's maximum-information price, **consistently beating the close is evidence of edge, and being beaten by it is evidence you are the sucker — regardless of recent wins**. Poker Joe uses this both as a self-diagnostic (grade every bet against the close) and as a filter for evaluating anyone else's claimed edge.

### 6. Price literacy: vig, break-even points, buying points, key numbers

The bettor must know, reflexively, what every price costs: the break-even win rate at any American odds (52.38% at −110), the hold baked into a market, and the value of half-points. Buying or selling points is a pricing decision, not a comfort decision: a half-point is worth the probability mass of the margin it crosses, which in the NFL is dominated by the key numbers **3 and 7**. Pay for a half-point only when the book charges less than that mass is worth; sell one whenever someone overpays you for it. Alternate lines and teasers are the same calculation wearing different clothes.

### 7. Arbitrage, middles, and scalps

The book covers them honestly: real, nearly riskless, and mostly a poor career. Arbs and scalps burn accounts fast for small margins; middles are better understood as cheap lottery tickets around key numbers with a quantifiable break-even hit rate (below). Their chief value to a developing sharp is educational — hunting them forces you to learn the price surface of the whole market.

### 8. Operations: limits, outs, and the grind

Winning play gets you limited or banned; therefore **account capacity is capital**. Maintain many outs, spread action, understand each book's tolerance, and treat access to prices as a depletable resource to be spent deliberately. Keep complete records. Bet flat, modest fractions of bankroll (the book's guidance is in the 1–2% range — consistent risk rather than aggressive Kelly), because thin edges plus fat staking equals ruin. Betting for a living is presented as repetitive, unglamorous work: the market pays professionals for showing up early, shopping every price, and never tilting — not for brilliance.

### 9. Thin edges, high volume

Professionals win roughly 53–55% against the spread at −110, not 60%+. At those margins, profit comes from volume and price discipline: hundreds or thousands of bets, each bought at the best available number, sized to survive variance. Anyone promising more is selling something.

## The Math

*Sharper* is deliberately light on formal notation — its quantitative rules are stated in prose and arithmetic. The formulas below state those rules precisely enough to implement, with standard notation supplied where the book supplies only the concept.

**Notation.** American odds `A`; decimal odds `d`; implied probability `q`; fair (no-vig) probability `p`; stake risk `R`; win amount `W`; bankroll `B`.

1. **American → decimal odds.**
   `d = 1 + A/100` if `A > 0`;  `d = 1 + 100/|A|` if `A < 0`.

2. **Implied probability of a quoted price** (includes vig).
   `q = 1/d`. Equivalently `q = |A| / (|A| + 100)` for `A < 0`, and `q = 100 / (A + 100)` for `A > 0`.

3. **Break-even win rate** at any price: `BE = q = 1/d`. At −110, `BE = 110/210 = 0.5238`.

4. **Overround and hold** of a two-way market with implied probabilities `q1, q2`:
   overround `OR = q1 + q2 − 1`; hold (margin per dollar wagered, both sides) `H = OR / (q1 + q2)`. A −110/−110 market: `OR = 0.0476`, `H = 0.0455`.

5. **No-vig (fair) probability — proportional devig** of a two-way sharp price:
   `p1 = q1 / (q1 + q2)`, `p2 = q2 / (q1 + q2)`. This devigged sharp-book probability is the book's operational definition of "truth." (The book does not name a devig method; proportional is the standard implementation. For extreme favorites, prefer a longshot-bias-aware method per Buchdahl — see Limitations.)

6. **Fair decimal price** from fair probability: `d_fair = 1/p`.

7. **Top-down edge and EV.** Given fair probability `p` (from the devigged sharp line) and an available decimal price `d_soft` at another book:
   `EV per unit staked = p × (d_soft − 1) − (1 − p) = p × d_soft − 1`.
   **Bet iff** `p × d_soft − 1 > θ`, where `θ > 0` is a threshold covering execution noise and model error (see directives; θ ≈ 0.01 is a sane floor).

8. **Closing line value (CLV).** For a bet taken at decimal `d_bet` on an outcome whose devigged closing fair price is `d_close_fair = 1/p_close`:
   price-space `CLV% = d_bet / d_close_fair − 1 = p_close × d_bet − 1`;
   probability-space `CLV_p = p_close − 1/d_bet`.
   You beat the close iff `CLV% > 0`. **Expected long-run ROI ≈ average CLV%** taken against the devigged close (the close is treated as an unbiased estimate of true probability).

9. **Steam-follow gate.** Let the sharp book move from `p_old` to `p_new` (devigged). Follow only at a book still offering decimal `d` such that `p_new × d − 1 > θ`. Never bet the moved number itself: after the move, `p_new × d_new − 1 ≈ −hold < 0` at the book that moved.

10. **Half-point (key-number) value.** Buying a half-point through margin `N` converts half of pushes into wins (or losses into pushes). The win-probability gain is `Δp = f(N)/2`, where `f(N)` = probability the game lands exactly on margin `N`. Fair price adjustment: new break-even `BE' = BE − Δp`; convert to American cents and compare with the book's charge. NFL empirics (stable across eras): `f(3) ≈ 0.095–0.10`, `f(7) ≈ 0.055–0.06`; so a half-point through 3 is worth ≈ 20–25 cents, through 7 ≈ 12 cents, and the classic "10 cents per half-point" charge is cheap through 3/7 and expensive elsewhere.

11. **Arbitrage condition** across the best available prices on each side:
    `q_best,1 + q_best,2 < 1` (i.e., synthetic overround negative). Stake split for equal profit: `R_i ∝ q_best,i`; guaranteed return per total stake `= 1/(q_best,1 + q_best,2) − 1`.

12. **Middle break-even.** Bet both sides of a gap, each risking `R` to win `W`. If the middle hits, profit `2W`; if not, net `−(R − W)` (one win, one loss). Break-even middle probability:
    `p_m* = (R − W) / (R + W)`. At −110 both sides: `p_m* = 10/210 = 4.76%`. Bet the middle iff estimated `P(land in gap) > p_m*` — most attractive when the gap contains NFL 3 or 7.

13. **Flat staking.** `stake = k × B` with `k ≈ 0.01–0.02`, constant per bet ("bet to risk"). This is deliberately below full Kelly for realistic edges; the book's rationale is variance control and account longevity, not growth-optimality.

## Strengths and Limitations

**Strengths**

- **Earliest accessible statement of market-based ("top-down") betting.** The core worldview — sharp price as truth, CLV as the metric, softer books as the target — is exactly the architecture serious bettors and betting tools converged on afterward. On this, the book was simply right, early.
- **Trading depth unusual for its era.** Most pre-2016 books were handicapping books; *Sharper* devotes most of its pages to line movement and its interpretation, which is where a modern automated system actually lives.
- **Operational realism.** Limits, outs, account survival, the grind — material almost entirely absent from the more mathematical canon, and the reason many theoretically winning bettors fail in practice.
- **Honesty.** No systems, no tout mathematics, realistic win rates (53–55%), and open acknowledgment that most readers will not do the work.

**Limitations and what has aged poorly**

- **Almost no formal math or data.** Everything in "The Math" above is stated in the book as prose rules and arithmetic examples; the reader (or engineer) must formalize it. Buchdahl (*Fixed Odds*, *Squares & Sharps*) and Miller & Davidow supersede it entirely on rigor.
- **Pre-2018 market map.** The book's world is offshore: Pinnacle and CRIS/Bookmaker as market makers, no PASPA repeal, no US retail apps, no Circa, marginal treatment of live betting and player props. The *structure* transfers (market makers vs. copiers), but every named venue and the account-management specifics need translation to the regulated era, where limiting is faster and more aggressive than the book assumes.
- **Steam decay is faster now.** Screen services, odds APIs, and copycat algorithms have compressed the propagation lag the top-down bettor exploits from minutes toward seconds; the book's follow-the-stale-line play still exists but demands automation the book never contemplates.
- **CLV nuance has moved on.** Later work (Buchdahl; practitioner writing from the Unabated/Circa orbit) qualifies the book's clean CLV story: closes can be biased in low-limit and derivative markets, books shade closers on public sides, and originators in early markets can show modest CLV while holding genuine edge. CLV remains the best single short-run metric — but as an estimator with error bars, not an oracle.
- **Legally gray operational advice.** Multiple accounts and beard-adjacent practices carry real terms-of-service and legal risk post-regulation that the offshore-era text does not weigh.
- **Unverifiable author.** The pseudonym means no track record can be checked; the book earns trust only because its claims are independently confirmable — which they largely are, but SharpOds should cite the confirmable versions (Miller & Davidow, Buchdahl) for anything contested.

## What SharpOds Takes From This Book

1. **Anchor truth to the devigged sharp price.** Maintain a real-time "fair probability" `p_fair` for every market, computed by proportionally devigging the two-way price at designated market-making books (Pinnacle, Circa, Bookmaker-class), weighted by each book's current limit size on that market. Retail/soft book prices are never inputs to `p_fair` — they are targets.
2. **Top-down stale-line scanner as a core signal.** Continuously evaluate `EV = p_fair × d_soft − 1` for every available price on the screen; emit a bet candidate when `EV > θ` with `θ ≥ 0.01`, raising θ with market illiquidity and model staleness. This is the book's top-down method, automated.
3. **Grade everything on CLV, not results.** Log the devigged close for every bet; compute `CLV% = p_close × d_bet − 1`. Any strategy/signal whose rolling average CLV is ≤ 0 over a meaningful sample (hundreds of bets) is disabled regardless of its W/L record; expected ROI is reported as mean CLV, not realized profit, until samples are large.
4. **Steam logic with the follow gate.** Classify a line move as informative only if it originated at a market-making book at meaningful limits; on detection, recompute `p_fair` from the *post-move* price and fire only at books whose lagging price still clears `p_new × d − 1 > θ`. Never bet the moved number. Require persistence (no snapback within a confirmation window) or multi-market-maker agreement before trusting a move — the head-fake filter.
5. **Key-number pricing engine.** Maintain empirical landing distributions `f(N)` per sport; value every half-point, alternate line, teaser leg, and middle via `Δp = f(N)/2`; buy points only when the charge is below `Δp` (in practice: NFL 3 and 7 at ≤ standard cents), and surface middles whenever estimated gap probability exceeds `(R−W)/(R+W)`.
6. **Flat, survival-first sizing.** Default stake 1–2% of bankroll flat per bet (bet-to-risk), capped well below book limits; treat this as the floor policy that other books' Kelly logic may refine, never exceed full-Kelly fractions implied by CLV-estimated edge.
7. **Model account capacity as capital.** Track per-book limits, limit-history, and hold; route bets to preserve long-lived soft-book access (spend sharp-book limits on price discovery and hedging, spend soft-book limits on +EV extraction); include expected account-lifetime cost in bet routing decisions.
8. **Weight information by limits.** In every consensus and move-detection computation, weight a book's price and its movement by the maximum bet it accepts on that market at that moment — a move at a $30k-limit market maker is signal; the same move at a $500-limit prop screen is noise.
