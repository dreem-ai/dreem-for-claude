---
name: dreem-content-kit
description: The everything pack - one product image in, a full set out. Product Shots for marketplace, on-model shots for the PDP and social, and a short product video, planned as one kit with ONE cost preview and ONE approval. Use whenever the user wants the full set, a content kit, everything for one product, imagery plus video in one go, asks to get a product ready for their store and social at once, or after dreem-imagery-audit finds multiple gaps on the same product. For a launch with a live date or a multi-product drop use dreem-new-product-launch; to spread one FINISHED shot across channel formats use dreem-channel-pack. Requires the Dreem connector.
metadata:
  version: 0.2.2
  pack: dreem-content
  skill_type: orchestration
---

# Dreem Content Kit

The button people press on launch day. This skill composes the other three generation flows into one planned, one-approval kit per product.

## Before you start

- `../../shared/references/_shared-input-analysis.md` - Step 0 and the hard rules (back views, video source, format matching). Read FIRST; the kit plan is built on it.
- `../../shared/references/_shared-dreem-mcp-guide.md` - all three flows live here.
- `../../shared/references/_shared-channel-specs.md` - the kit defaults come from this file.
- `../../shared/references/_shared-credit-model.md`, `../../shared/references/_shared-output-conventions.md`.

## Step 1 - Analyze inputs, then pin channels

Get the product image(s) per the sourcing rules (front + back if available), then run Step 0 from `_shared-input-analysis.md`: LOOK at every input, record view (front/back), content type (flat/ghost/on-model), and the aspect ratio the product's live gallery already uses.

The analysis shapes the kit before any picker opens:

- No back-view input -> no back-facing rows and no turn/rotation video (HARD RULE 1). Offer the one-phone-snap fix; only include a back row after the user explicitly acknowledges the back will be made up.
- The store's existing aspect ratio is the DEFAULT ratio for the kit's PDP rows (FORMAT RULE). Ask once whether to also add other channel formats; the table below is the menu, not the default.

Then establish which channels the user actually sells through - the kit only includes formats they can use.

## Step 2 - Plan the kit

Default kit per product (trim to the user's channels AND to what the input analysis allows):

| # | Asset | Flow | Ratio / tier |
|---|---|---|---|
| 1 | Marketplace Product Shot | product shot | `Ratio1x1` `TwoK` |
| 2 | PDP on-model | virtual model | match store ratio, `TwoK` |
| 3 | Second PDP on-model (alt pose) | virtual model | match store ratio, `TwoK` |
| 4 | Story/Reels on-model | virtual model | `Ratio9x16` `OneK` |
| 5 | Feed shot | product shot or virtual model | `Ratio4x5` `OneK` |
| 6 | Product video (5s) | video | from a completed on-model row |

The video row exists ONLY when the kit contains at least one virtual-model row (HARD RULE 2). A kit with no on-model asset (e.g. no suitable talent for the garment category) has no video row - say why in the plan instead of quietly animating a still.

No store context (single loose photo): "match store ratio" has nothing to match - use the fashion PDP channel default (`Ratio3x4` `TwoK`) for PDP rows and confirm the ratio once in the plan.

Baby/infant garments (HARD RULE 3): the kit is Product Shot rows only - no virtual-model rows, no video row. State it in the plan.

## Step 3 - Pickers once

One casting + style session for the whole kit: `browse_models` (talent), `browse_product_shot_styles` (views + poses; check pose gender vs talent), `browse_video_styles` (motion). Ask the styling question ONCE for all on-model rows (per the styling step in dreem-virtual-model-shots: specific pieces as `productType: Outfit` images, season look, or minimal neutrals) - the answer applies across the kit. For talent and pose, apply **Casting and pose: suggest, explain, confirm** from `_shared-dreem-mcp-guide.md`: name the best-fit pick with a one-line reason, ask the user to confirm each, and offer 2-3 named alternatives if they decline - the galleries are the override path. A plain "confirm"/"go" on your named suggestions counts, as long as the picks, their reasons, and the alternatives offer are already on screen. If picker state and the user's words disagree, the words win. (Motion/video prompt is a suggestion too - flag an obvious mismatch, e.g. a waist-down motion on an upper-body garment.) The choices apply across the whole kit.

## Step 4 - ONE cost preview, ONE gate

Show the whole kit as a single plan table per `_shared-credit-model.md` (a 6-asset kit is 6 generations - say it plainly, video costs more than stills). Interactive: `confirm` LAST (RULE-A), stop, wait for the user. This is the only approval in the flow - make it count, then do not ask again per asset.

## Step 5 - Generate in strict sequence, with barriers

The three stages run in order, and each stage WAITS for the previous one to fully complete before starting:

1. **Product Shots first - all of them.** Wait until every Product Shot row completes and passes the garment-fidelity check (logo, pattern, color). If fidelity drifts here, pause and tell the user before spending on model and video rows.
2. **Virtual model rows next - only after stage 1 is done.** Wait until every on-model row completes and passes QA.
3. **Video last - only after stage 2 is done**, sourcing its `FirstFrame` from the kit's own completed virtual-model output (completed output URLs are public HTTPS - chaining is the point). Never from the raw product image and never from a Product Shot row (HARD RULE 2). Prefer the 9:16 on-model output for social video; pick front-facing motion unless a back-view input exists.

Within a stage the async pattern from the MCP guide applies (max 3 concurrent); across stages there is a hard barrier. `show_generation_result` once per completed request.

## Step 6 - One manifest, honest QA

Single `manifest.csv` covering every row, full QA pass per `_shared-output-conventions.md` (fidelity on stills, warping/artifacts on video), `summary.md` organized by channel with delivery notes (manual upload today, or Dreem's n8n templates for automated delivery). If any row failed, list exactly which and offer to re-run just those.
