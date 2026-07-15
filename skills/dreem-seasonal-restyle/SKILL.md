---
name: dreem-seasonal-restyle
description: Retheme existing on-model imagery for a season or campaign - same garments, same store format, new styling, setting, and mood. Fall, winter, holiday, spring, Black Friday, a named campaign theme ("Summer Escape"), or a market-specific flip like a winter set for the Nordics. Works from the products' current on-model images - live store shots or earlier pack outputs. Use whenever the user wants the catalog restyled for a season, says the store "still looks like summer", asks for holiday or campaign looks, wants imagery refreshed for the new season, or needs a seasonal batch for a specific market. Products with no on-model image yet route through dreem-virtual-model-shots first. Requires the Dreem connector.
metadata:
  version: 0.1.0
  pack: dreem-content
  skill_type: generation
---

# Dreem Seasonal Restyle

This skill rethemes existing on-model imagery in one batch: the garments stay exactly the user's garments, the store's format stays the store's format, and one locked seasonal look carries across every product - so the result reads as a campaign, not a pile of unrelated renders.

## Before you start

- `../../shared/references/_shared-input-analysis.md` - Step 0 and the hard rules.
- `../../shared/references/_shared-dreem-mcp-guide.md` - batch mode is the default here.
- `../../shared/references/_shared-channel-specs.md`, `../../shared/references/_shared-credit-model.md`, `../../shared/references/_shared-output-conventions.md`.
- The styling mechanics come from dreem-virtual-model-shots: Outfit images control the look.

## Step 1 - Collect the set

Which products flip? A store URL or collection, manifest rows from an earlier run, or uploads. Pull each product's CURRENT on-model image and run Step 0 on it: view, ratio, what styling is visible.

- No on-model image on a product: park it, name it, route it to dreem-virtual-model-shots. A restyle needs a look to restyle.
- Baby/infant items: seasonal Product Shot treatments only (new backdrop and mood, no model, no video) per HARD RULE 3.
- 4+ products is batch mode: pickers once, one plan, one gate.

## Step 2 - Lock ONE seasonal look

Coherence is the whole point. One picker session for the entire batch:

- **The theme brief** in one line ("cozy Nordic winter", "golden autumn city", "holiday gifting") - agree it with the user first.
- **Shot styles**: `browse_product_shot_styles` with the theme as the semantic query; suggest a named default set (1-2 codes) used across every product.
- **Casting**: restyling this pack's own outputs - reuse each row's `talent_id`; the same faces across seasons read as a real brand roster. Restyling store photos of unknown people - Dreem re-casts with a virtual talent; the garment carries, the person changes. Say it before the plan, one explicit ok. Either way: one talent or the existing per-product talents, never a fresh face per product.
- **Seasonal styling pieces**: the styling step from dreem-virtual-model-shots, answered once for the batch. Best case the pieces come from the user's OWN catalog (beanie, boots, coat as `productType: Outfit` via CDN URLs) - seasonal imagery that cross-sells. No piece photos: honest fallback, Dreem improvises the seasonal look.

## Step 3 - Keep the garment and the format exact

Per product: the current on-model image is the garment source (`productType: Main`) - Dreem keeps the garment and rebuilds the scene around it. Seasonal pieces ride as Outfit images. Output ratio = the store's existing ratio (FORMAT RULE); a seasonal refresh that breaks the gallery grid is a downgrade. Front-only sources: front-facing poses only (HARD RULE 1).

## Step 4 - Batch plan + ONE gate

One table: product x shot, exact credits per `_shared-credit-model.md`, one total. A 12-product flip at 2 shots each is 24 virtual-model generations - show that number plainly before it surprises anyone. `confirm` LAST (RULE-A), stop, wait. Batch mode: the table plus an explicit "go".

## Step 5 - Generate + campaign QA

Max 3 concurrent, results shown once each. QA per `_shared-output-conventions.md` plus the restyle-specific check: the SET has to cohere - same seasonal palette and mood across products, garments unchanged. A restyle that alters the product is a failure even when it looks good.

## Step 6 - Ship the season

Manifest + summary. The restyled set replaces PDP imagery (manual upload today, or Dreem's n8n templates for automated delivery). Then the chain:

- Campaign formats for the season's announcement (email hero, Stories) from the strongest restyled shot -&gt; `dreem-channel-pack`.
- Motion on the campaign hero -&gt; `dreem-image-to-video`.
- New products joining the seasonal drop -&gt; `dreem-new-product-launch`.
