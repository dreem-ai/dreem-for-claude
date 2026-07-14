---
name: dreem-new-product-launch
description: Launch-day imagery for new products - a single product or a whole drop, planned backwards from the live date. Product photos in, a prioritized launch set out - PDP on-model shots, marketplace stills, social formats, video - with ONE cost preview and ONE approval for the entire drop. Use whenever the user is launching something new with a date attached - "goes live Thursday", "new drop next week", "the collection launches Friday", "just added new products and they need imagery before launch" - or when dreem-imagery-audit finds brand-new products with empty galleries. For a full set on one product with no deadline, use dreem-content-kit. Requires the Dreem connector.
metadata:
  version: 0.1.1
  pack: dreem-content
  skill_type: orchestration
---

# Dreem New Product Launch

The starting point is a date, not a gap. Something goes live Thursday and the imagery has to exist by then. This skill plans a drop backwards from the live date, keeps one coherent look across every product in it, and gates the whole thing behind a single approval.

## Before you start

- `../../shared/references/_shared-input-analysis.md` - Step 0 and the hard rules. The launch plan is built on them.
- `../../shared/references/_shared-dreem-mcp-guide.md` - flows, RULE-A/RULE-B, batch mode.
- `../../shared/references/_shared-channel-specs.md`, `../../shared/references/_shared-credit-model.md`, `../../shared/references/_shared-output-conventions.md`.
- The per-product kit shape follows dreem-content-kit; this skill sequences and batches it for a launch.

## Step 1 - Capture the drop

Four facts before any picker opens:

1. **The products** - one or many. Images per product: front, plus back when it exists. Ask for backs once - they unlock back poses and turn video per HARD RULE 1.
2. **The live date** - it decides how much fits before launch and what ships as a follow-up wave.
3. **The channels** - PDP is a given; marketplace, social, email only if they sell there.
4. **Store context** - if the store is live, read the existing gallery format so the new products land in the store's ratio (FORMAT RULE). No gallery to match: fashion default (`Ratio3x4` `TwoK`), confirmed once.

Run Step 0 from `_shared-input-analysis.md` on every input image. Baby/infant products: Product Shot rows only (HARD RULE 3) - say it in the plan.

## Step 2 - Plan backwards from the date

Three tiers, in launch order:

| Tier | Assets | Why first |
|---|---|---|
| 1 - live at launch | PDP on-model set (2-3 shots) + marketplace Product Shot | The PDP cannot be empty on day one |
| 2 - announcement | Story/Reels `Ratio9x16` + feed `Ratio4x5` | The launch post and the paid push |
| 3 - momentum | Product video (5s) from a Tier 1 on-model output | HARD RULE 2 - video only from the drop's own on-model outputs, never the raw photos |

Deadline tight or the drop large? Offer the cut: Tier 1 for every product now, Tiers 2-3 as a second wave after launch. Half a launch set on time beats a full set late.

## Step 3 - One look for the whole drop

A drop reads as a collection when casting and styling hold across products. One picker session for everything (batch mode from the MCP guide):

- **One talent** (or a deliberate small cast) via `browse_models`. A launch is time-pressured by definition, so default straight to suggesting a named talent rather than asking the suggest-vs-pick question from `_shared-dreem-mcp-guide.md` first - say plainly that you defaulted and that swapping is one word away. Still confirm the suggestion before pricing, per the normal casting flow - the shortcut is skipping the extra meta-question, never skipping the user's say on WHO got cast.
- **One styling answer** (the styling step from dreem-virtual-model-shots), applied across the drop.
- **One shot-style set** via `browse_product_shot_styles` - pose gender checked against the talent, back poses only where back inputs exist.

## Step 4 - ONE cost preview, ONE approval

One plan table for the whole drop: product x asset x tier, exact credits per `_shared-credit-model.md`, per-tier subtotals, one total. A 3-product drop at full kit is real money - show the number plainly and offer the Tier 1 cut again if it lands high. Interactive: `confirm` LAST (RULE-A), stop, wait. Nothing generates before the approval; nothing gets re-asked after it.

## Step 5 - Generate in launch order

Hero product first, then the rest. Per product, the content-kit stage barriers hold: all Product Shots complete and pass fidelity QA, then on-model rows, then video rows (sourced from the drop's own completed on-model outputs). Max 3 concurrent. If a row fails, report it per product and keep the drop moving - one retry must not hold nine finished assets.

Tight deadline: hand over each product's Tier 1 as it completes so the store team can start uploading.

## Step 6 - Launch handover

One manifest for the drop; summary organized as a launch checklist per channel - what to upload where (PDP gallery order, marketplace slot, posts to schedule). Delivery is manual upload today, or Dreem's n8n templates for automated pushes.

Then the chain, one line each:
- Extra announcement formats (email hero, Pinterest) from the best completed shot -> `dreem-channel-pack`.
- Once the launch settles, extend the hero product across bodies, ages, or genders -> `dreem-extend-talents-set`.
