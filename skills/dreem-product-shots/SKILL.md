---
name: dreem-product-shots
description: Generate clean, ecommerce-ready Product Shots from any product photo using Dreem - flat lay, invisible mannequin, side and detail views, any aspect ratio from square to 9:16, up to 4K. Use whenever the user wants product images or product stills, white-background versions for Amazon or Google Shopping, marketplace-compliant images, extra angles from one photo, wants to turn a phone photo into store-ready stills, or needs to batch-produce imagery for multiple SKUs. Also use when the user says "packshot" - and call the output Product Shots. Requires the Dreem connector; every generation is cost-previewed and approved before it runs.
metadata:
  version: 0.2.0
  pack: dreem-content
  skill_type: generation
---

# Dreem Product Shots

One product photo in, clean store-ready stills out. The user's phone photo becomes a marketplace-compliant image set.

Naming rule: the output is called **Product Shots** in every sentence the user reads. Never "Packshots".

## Before you start

- `../../shared/references/_shared-input-analysis.md` - Step 0 and the hard rules (back views, format matching). Read FIRST.
- `../../shared/references/_shared-dreem-mcp-guide.md` - tool flows, RULE-A/RULE-B, image sourcing, exact enums.
- `../../shared/references/_shared-channel-specs.md` - ratio/resolution/format per destination.
- `../../shared/references/_shared-credit-model.md` - the cost preview that gates every generation.
- `../../shared/references/_shared-output-conventions.md` - manifest.csv, summary.md, QA pass.

## Step 1 - Get the product image(s) and LOOK at them

Per the sourcing rules in the MCP guide: local file -> `upload_image` -> `fileId`; public HTTPS URL (Shopify CDN etc.) -> pass directly as `url`. Take front and back when the user has both (`viewType: Front` / `Back`) - back inputs make back-facing outputs accurate.

Then run Step 0 from `_shared-input-analysis.md`: record each input's view (front/back), content type, and the ratio the product's live gallery uses. This decides which shot styles are even allowed: **front-only input means NO back-facing `shotCodes`** (HARD RULE 1) - the back would be invented. If the user insists, warn plainly and get an explicit acknowledgment before including the row.

A decent phone photo works. Blurry, cropped, or heavily filtered inputs degrade output - say so before generating, not after.

## Step 2 - Pin the destination and the format

Default the output ratio to what the product's gallery already uses (FORMAT RULE in `_shared-input-analysis.md`), and offer once: same format, or additional channel formats? When the user names a destination, take ratio/resolution/format straight from `_shared-channel-specs.md` (e.g. Amazon main -> `Ratio1x1` `TwoK` jpeg; PDP fashion -> `Ratio3x4` `TwoK`). Generating at the target ratio beats cropping - the scene is composed for the frame.

## Step 3 - Pick styles

- **Interactive (1-3 products):** call `browse_product_shot_styles` with a semantic query built from the user's words ("flat lay front", "invisible mannequin", "side view", "detail"). The catalog covers presentation views - flat lay, invisible mannequin, side, detail - not styled scenes or environments. The user picks in the visual picker.
- **Batch (4+):** pick styles ONCE for the whole batch, confirm they apply to all products.

Use each chosen style's `code` (not `id`) in `shotCodes`. For marketplace compliance pick clean, light, prop-free backgrounds. Filter every pick against the Step 1 input analysis - no back-facing style without a back input.

## Step 4 - Cost preview, then the gate

Build the generation plan table per `_shared-credit-model.md`: one row per generation (product x style x ratio). Interactive mode: open `confirm` LAST after the pickers (RULE-A), then STOP and wait. Batch mode: show the plan table and wait for an explicit "go".

No approval, no generation. No exceptions.

## Step 5 - Generate

`generate_product_shot` per plan row: `images`, `shotCodes`, `outputFormat`, `outputAspectRatio`, `resolution`. Follow the async pattern from the MCP guide (`wait_for_content` until a real output URL exists; max 3 concurrent; `show_generation_result` exactly once per completed request).

## Step 6 - QA and hand over

Run the QA pass from `_shared-output-conventions.md` - for Product Shots the failure modes are logo softness, pattern drift, and color shift against the input. Fill `qa_flag` per row honestly. Write `manifest.csv` + `summary.md`. Point flagged shots at Dreem Studio's edit mode (prompt edit + brush) - a 10-second fix beats a re-generation.

Delivery today is manual (download and upload to the store) or via Dreem's n8n templates - say which in the summary.
