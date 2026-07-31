# SharpOds — operating instructions

This repo is a live sports betting model (see README.md, docs/synthesis.md,
docs/books/). It runs a daily review-improve-ship cycle operated through chat.

## THE GO PROTOCOL

When the user says **"GO"** (alone or with a date/sport hint), execute the full
cycle at maximum capacity, exactly like the 2026-08-01 complete run:

1. **Verify the date first.** Infer today's real date from search results, not
   assumption — the clock has drifted before. "Tomorrow" = the next calendar
   day from the *verified* date.
2. **Grade** (parallel agent): settle the previous card in
   `data/track_record.json` via `sharpods.ledger` — finals, closing lines
   (devig with power method), order fill checks, ticket P&L + CLV (raw and
   no-vig), refusal validation. CLV vs the close — not P&L — is the verdict.
3. **Scout at full coverage** (3-5 parallel agents by domain): MLB (ML + run
   lines + totals), soccer (three-way 1X2 + goal totals; MLS/Liga MX/Copa do
   Brasil/whatever is in season), UFC/boxing full cards, WNBA/NBA, CFL/NFL,
   tennis — every sport with real Saturday/target-day markets. One agent
   fetches team data (records, RS/RA) for the in-house log5/Pythagorean layer.
4. **Compile the slate** (`data/slates/YYYY-MM-DD-full.json`): single-book
   boards anchor; prediction markets (Polymarket, Robinhood) are shop-only
   (sharpness 0.45 — ledger-evidenced demotion); multi-book best-price
   aggregates are EXCLUDED (they understate hold and fabricate value);
   in-house model probs ensembled 50/50 in logit space with dated third-party
   models, then `--market-weight 0.85`.
5. **Run** `python -m sharpods <slate> --bankroll 10000 --market-weight 0.85`,
   plus `python -m pytest tests/` — both must be clean before shipping.
6. **Ship**: rewrite the slip (artifact 5edc38a1-94f5-4edb-aa83-13527003c966,
   favicon 🎟️, same scratchpad path `betslip.html` to keep the URL) with the
   best bet as the headline; regenerate the tracker (`sharpods-tracker`,
   artifact a867633c-7d86-4ce1-841b-7aa779960c2f, favicon 📊) — the tracker
   shows ONE card per day: the ledger decision flagged `headline: true`.
7. **Record**: pre-register fair lines and decisions in the ledger; commit and
   push every changed file to the designated branch.

## NO-MISTAKES CHECKLIST (each item has burned us once)

- **Date discipline**: reject any price not explicitly dated to the target
  day. Same-series prior-day lines are the #1 trap (Friday Mariners -187,
  July-29 NYY line, an April Fool's Pirates recap).
- **Venue/home verification**: confirm home team by venue/ticketing, not
  article phrasing (Liberty AT Phoenix reversal; TEX@SEA mis-pairing).
- **Sport gating**: key-number machinery (Wong teasers, NFL margin middles)
  is football-only (`engine.FOOTBALL_SPORTS`).
- **Conflict refusal**: degraded anchor + negative cross-source hold =
  unpriceable, never an arb (Cubs 3.7pt miss; Polymarket 5-6pt misses ×3).
- **Decimal conversions exact**; European odds everywhere user-facing.
- **UFC convention**: fighter listed second (p2) enters as `home`.
- **Never fabricate a missing price**; partial boards stay unpriced, and a
  thin honest card beats a padded one.
- **Parameter changes only on ledger evidence**, citing the graded miss
  (Walters anti-tinkering rule). Every change lands in
  `lessons_applied` in the track record.
- **Verify the headline bet's math by hand** (devig → EV → Kelly) before it
  goes on the slip, and re-check slip captions against the actual run.

## Standing facts

- User bets ONLY the slip's best bet (tracker = one card/day, headline only).
- User's real record lives in `data/track_record.json` (`live_tickets`,
  `decisions`); bankroll history started $30,000 → Cubs win → $59,700.
- Stake guidance on slips: $10,000 reference roll, ¼ Kelly, 2% cap; the
  degraded-mode EV bar is 2.5% (1% with a market-maker anchor).
- Network policy blocks all odds feeds/sites (403) — prices come from
  WebSearch snippets of date-stamped pages; note provenance on every slip.
- Commit messages end with the standard co-author/session trailer; push to
  the designated `claude/...` branch; never create a PR unless asked.
