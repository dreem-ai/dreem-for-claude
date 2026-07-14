# Credit Model + Cost Preview

Generation spends the user's Dreem credits. Credits are real money. The contract of this pack: **no `generate_*` call ever fires before the user has seen a cost preview and explicitly approved it.** This is what makes the pack safe to hand to a stranger.

## What generations cost (official Dreem pricing, confirmed 2026-07-07)

Per-generation credit costs, by feature and resolution tier:

| Feature | Unit | 1K | 2K | 4K |
|---|---|---|---|---|
| Virtual Model | 1 asset (per pose) | 9 | 11 | 14 |
| Product Shots | 1 asset (per view) | 6 | 8 | 10 |
| Image Refining | 1 asset | 4 | 8 | 10 |
| Image to Video | per second of video | 2 | - | - |

- Video is priced per second: a 5s clip = 10 credits, a 10s clip = 20 credits (1080p output).
- Every Product Shot view and every Virtual Model pose is its own asset - a 3-pose set at 2K is 3 x 11 = 33 credits.
- Failed or wrong-output generations still consume credits - another reason the cost preview and QA matter.
- Money framing: per-credit price falls with plan size, roughly $0.05-0.12 per credit. Free plan: 100 credits/mo at 1K. So a 2K Virtual Model shot is roughly $0.55-1.30.

Compute the EXACT total for every plan from this table. If a feature is missing from the table, say so and use directional language for that row only.

## The cost preview (required before every generation)

Show this table with a credits column and an exact total, then stop for approval:

```markdown
## Generation plan - approve to run

| # | Product | Type | Style | Ratio | Resolution | Credits |
|---|---------|------|-------|-------|------------|---------|
| 1 | Essential Black Tee | Virtual model | Studio Soft Light | 3:4 | 2K | 11 |
| 2 | Essential Black Tee | Virtual model | Studio Soft Light | 9:16 | 1K | 9 |
| 3 | Essential Black Tee | Video (5s) | Slow Turn | - | - | 10 |

**Total: 30 credits** (3 generations). These spend credits from your Dreem balance - check the balance in Dreem Studio if unsure.
Reply "go" to generate, or tell me what to change.
```

In interactive mode the Dreem confirm button plays the approve role; in batch mode this table plus an explicit user "go" is the gate. Either way: no approval, no generation.

## The comparison that sells the math

When the user asks "is this worth it", frame against traditional production, honestly:

- A traditional on-model shoot runs hundreds of dollars per finished image once you count studio, model, photographer, and retouch. Common all-in benchmarks are $150-1,500 per image depending on market and production level.
- The same on-model image from Dreem costs a few credits - single-digit dollars at most plan tiers.
- So a 50-product refresh that would be a five-figure shoot becomes a two-to-three-figure credit spend, same week, no logistics.

Use ranges, not fake precision. If the user wants exact numbers, have them check their plan's credit price and the in-app estimate.

## Partial failure accounting

If a batch partially fails, report exactly what was attempted, what completed, and what failed (with error messages). Failed generations may still consume attempts on the user's side - tell them to check their balance and re-run only the failed rows (the manifest marks them).
