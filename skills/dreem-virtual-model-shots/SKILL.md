---
name: dreem-virtual-model-shots
description: Put any garment on any of Dreem's 400+ virtual talents - flat lay or mannequin photo in, on-model imagery out, cast across body types, ages, sizes, and ethnicities. Use whenever the user wants on-model or model shots, wants to show a product on a person, wants the model STYLED a certain way (pair it with a black jacket and white shoes, style it for winter, complete the look), wants to swap or replace the model on an existing photo, or has products that were never shot on a person. Also the fix for every "no on-model" finding from dreem-imagery-audit. For extending an EXISTING approved on-model look across body types, sizes, ages, or genders, use dreem-extend-talents-set - this skill creates the first look. Requires the Dreem connector; every generation is cost-previewed and approved first.
metadata:
  version: 0.3.0
  pack: dreem-content
  skill_type: generation
---

# Dreem Virtual Model Shots

Dress a virtual talent in the user's actual garment. A flat lay becomes a person wearing the product; one garment becomes a size-inclusive set.

## Before you start

- `../../shared/references/_shared-input-analysis.md` - Step 0 and the hard rules (back views, format matching). Read FIRST.
- `../../shared/references/_shared-dreem-mcp-guide.md` - flows, RULE-A/RULE-B, sourcing, enums.
- `../../shared/references/_shared-channel-specs.md`, `../../shared/references/_shared-credit-model.md`, `../../shared/references/_shared-output-conventions.md`.

## Step 1 - Garment inputs, analyzed

1-10 images per generation. The garment being sold: `productType: Main` (front, plus `viewType: Back` when the user has a back shot - it makes back-facing poses accurate). Supporting pieces to complete the look: `productType: Outfit`.

Run Step 0 from `_shared-input-analysis.md` on every input: view, content type, and the ratio the product's gallery uses. **Front-only input means NO back-facing poses** (HARD RULE 1) - the garment's back would be invented. Offer the one-phone-snap fix; include a back pose only after an explicit user acknowledgment.

**Baby/infant garments: refuse** (HARD RULE 3) - no baby talents exist, and an older child model misrepresents the fit. Route to `dreem-product-shots` instead.

**Swimwear, underwear, and lingerie: adult talents only** (HARD RULE 4) - never cast kids/teen talents for these categories, no matter what size range the garment sells in, and confirm the casting explicitly before the plan.

**The garment source can be an existing on-model photo.** Dreem keeps the garment and swaps the person. This is how you replace a model catalog-wide without a reshoot, restyle imagery you cannot license anymore, or re-cast a look - feed the current on-model image as the outfit, pick a new talent.

**Ask how the model should be styled - always, before the plan.** Unless the user already gave styling direction, one question with examples:

> How should the model be styled around the \[garment\]? For example:
>
> - pair it with specific pieces - "a black jacket and white sneakers"
> - style it for a season - "winter look: coat, beanie, boots"
> - keep it minimal - simple neutrals, the \[garment\] is the hero

The mechanics behind each answer:

- **Specific pieces**: each piece needs an image - pass it as `images[]` with `productType: Outfit` (photo upload, URL, or best of all a product from the user's OWN store catalog; the CDN URLs from an audit work directly). The model then wears THEIR products - complete-the-look imagery that cross-sells.
- **Season/mood without piece photos**: be honest - outfit control comes from Outfit images. Offer to pull matching pieces from their store ("you have a beanie and boots in your catalog - want those on the model?") or let Dreem improvise simple neutrals.
- **Minimal / no answer**: no Outfit images; Dreem dresses the talent in plain neutrals so the main garment stays the hero.

## Step 2 - Cast the talent

**Ask how they want to cast - unless the brief already describes the model.** One question before any browsing:

> Want me to suggest a model based on your product page, or would you rather pick one? You can select from examples in the picker, or describe the look ("woman in her 40s, mid-size, warm approachable") and Dreem will find it.

- **Suggest**: build the `browse_models` query from what the product page and store actually say - garment category, price positioning, who appears in the existing imagery, and the store's market region (a DK store casts Scandinavian talent first). No store context to read from? Anchor with one question first: "who's your typical customer - rough age range and vibe?"
- **Pick from examples**: open `browse_models` with a broad query for the garment; the visual picker is the selection surface.
- **Describe it**: run their description as the `browse_models` semantic query ("man 60+, silver hair, editorial").

Whichever path, close per **Casting and pose: suggest, explain, confirm** in `_shared-dreem-mcp-guide.md`: name the best-fit talent with a one-line reason, ask the user to confirm it, and offer 2-3 named alternatives if they decline. The picker is the override path; if picker state and the user's words disagree, the words win.

- **Diversity/size/age sets:** lock ONE garment and iterate `talentId` across the chosen talents (e.g. 5 talents across the size range, or 20s/30s/40s/60s). One picker session, N casting choices, one batch. When the starting point is the product's EXISTING on-model shot and the brief is "same look, different people" (bodies, ages, or genders), hand off to dreem-extend-talents-set - it carries the source styling, shot style, and format automatically.
- Talent gender must match the pose set you pick in Step 3 - poses are gendered, and a mismatch fails or looks wrong.

## Step 3 - Pick shots (pose + camera)

`browse_product_shot_styles` for the shot styles: pose, camera, framing, mood. Check each shot's `pose.gender` against the chosen talent. Apply the same suggest -&gt; explain -&gt; confirm pattern to the pose (`_shared-dreem-mcp-guide.md`): propose the best-fit pose(s) with a one-line reason, ask before locking, and offer named alternatives if the user declines. PDP sets read best with 2-3 shots: one straight-on full body, one three-quarter, one detail-adjacent. Filter picks against the Step 1 input analysis - back-facing poses only with a back input (or explicit acknowledgment).

## Step 4 - Ratios and tiers

Default to the ratio the product's gallery already uses (FORMAT RULE), and ask once whether to add other formats. When a channel is named, `_shared-channel-specs.md` wins: PDP `Ratio3x4` `TwoK` is the fashion standard. Add `Ratio9x16` `OneK` only if the user wants social from the same session.

## Step 5 - Cost preview, then the gate

Plan table per `_shared-credit-model.md`: rows = talent x shot x ratio. Diversity sets multiply fast - a 5-talent x 3-shot set is 15 generations; show that number before it surprises anyone. Interactive: `confirm` LAST (RULE-A), stop, wait. Batch: plan table + explicit "go".

## Step 6 - Generate

`generate_virtual_model` with `talentId`, `shotCodes` (the `code` values), `images`, `outputFormat`, `outputAspectRatio`, `resolution`. Async pattern from the MCP guide; max 3 concurrent; `show_generation_result` once per completed request.

## Step 7 - QA hard, then hand over

This is where garment fidelity matters most. Per output check: logo position and sharpness, stitching, pattern direction (stripes and checks drift), garment shape and length, color against the input, and that it is the user's actual garment rather than a lookalike. Fill `qa_flag` honestly per `_shared-output-conventions.md`; route fixes to Dreem Studio's brush edit. Write `manifest.csv` + `summary.md` with per-talent results.
