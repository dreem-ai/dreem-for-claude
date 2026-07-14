---
name: dreem-extend-talents-set
description: Extend a product's current on-model shot across an inclusivity axis - body types and sizes, ages, or genders - same garment, same styling, same shot family and format, different people. Shoppers see the piece on someone like them before buying. Use whenever the user wants size-inclusive or body-diverse imagery ("show it on every size", "on a plus-size model", "different body types"), an age-diverse set ("same look, 20s through 60s", "show it on older models too", "made for every age"), a gender set ("show it on men and women", "unisex", "each gender", "his and hers"), or "models that look like our customers". Works from the current PDP on-model image, an upload, or a shot another pack skill generated. If the product has no on-model image yet, dreem-virtual-model-shots creates the first look - this skill multiplies it across people. Requires the Dreem connector.
metadata:
  version: 0.3.0
  pack: dreem-content
  skill_type: generation
---

# Dreem Inclusive Set

High return rates in fashion are mostly a "didn't look like this on ME" problem. This skill takes the on-model look a brand already approved - the current PDP shot - and rebuilds it on different people along one axis: body type and size, age, or gender. Everything else holds: same garment, same styling, same shot family, same ratio. Only the person changes. Published together, the set answers the shopper's real question before they gamble on an order.

## Before you start

- `../../shared/references/_shared-input-analysis.md` - Step 0 and the hard rules.
- `../../shared/references/_shared-dreem-mcp-guide.md` - flows, RULE-A/RULE-B, sourcing.
- `../../shared/references/_shared-channel-specs.md`, `../../shared/references/_shared-credit-model.md`, `../../shared/references/_shared-output-conventions.md`.
- The mechanism is dreem-virtual-model-shots' garment-source trick, specialized: source on-model image in, new people out.

## Step 1 - The source look

One product, one current on-model image: the live PDP shot (CDN URL), an upload, or a completed row from another pack skill's manifest. Run Step 0 on it and record the three things every output must match:

1. **View** - a front-only source means every output is front-facing (HARD RULE 1).
2. **Ratio** - the set sits next to the source on the PDP, so it ships in the source's ratio (FORMAT RULE).
3. **The visible styling** - what the model wears around the garment (jacket, sneakers, jewelry). That styling is what carries.

The source image is the garment input (`productType: Main`): Dreem keeps the garment and swaps the person. Two honest notes before planning: the output models are Dreem virtual talents, not the person in the source photo; and baby/infant garments get no on-model set at all (HARD RULE 3 - route to dreem-product-shots).

## Step 2 - Carry the styling

The brief is "only the person changes", so the styling cannot be left to chance. Styling pieces visible in the source do not automatically survive the person swap - pin them as `productType: Outfit` images:

- Best case: the pieces are the brand's own products - pull their CDN URLs from the store. The set then cross-sells the look.
- Or the user shares photos of the pieces.
- Neither: say plainly that Dreem will approximate the source styling from the image and may simplify it - and get an ok before generating N variations of an approximation.

## Step 3 - Pick the axis, cast the range

ONE axis per set. Combining axes is allowed only when the user asks for it, with the multiplication shown honestly first (4 bodies x 3 ages is 12 talents before shots multiply it further).

- **Body/size** - the default when the brief says sizes or bodies. Dreem casts by **Body Build**, not garment size - the builds are Very Slim, Slim, Lean, Average, Athletic, Plus (verify against `dreem://attributes/*` in case the list grew). Default lineup: 4 talents across Slim / Average / Athletic / Plus, matched to the source model's gender, age band, and vibe; add Very Slim and Lean when the user wants the full range. When the user speaks in sizes, translate to the closest build and NAME the translation in the plan:

  | User says | Cast as |
  |---|---|
  | XS, extra small | Very Slim |
  | S, small, petite | Slim |
  | slender, toned, lean | Lean |
  | M, medium, mid-size | Average |
  | athletic, sporty, muscular | Athletic |
  | L, XL | Average or Athletic (the fuller end - no dedicated build exists; say which you picked) |
  | plus, plus-size, curvy, 1X and up | Plus |

  Garment sizes are brand-relative, so the mapping is a judgment call, not a size chart - the plan states the chosen builds and the picker exists to correct them.
- **Age** - "same look, every generation". Lineup: 4 talents across 20s / 30s-40s / 50s / 60s+, matched to the source model's gender, body type, and vibe. Cast the ages the garment's target wearer actually spans - kids/teen talents only for garments cut for them.
- **Gender** - "show it on men and women". Lineup: one talent per gender, matched to the source model's age band and vibe. Two axis-specific rules: poses are gendered in Dreem, so each talent gets the gender-matched variant of the SAME pose family (Step 4); and the garment renders as it is cut - true unisex pieces (hoodies, tees, outerwear) are the sweet spot, while a strongly gendered cut (a fitted dress) on another gender's talent is a deliberate styling statement, not an error. Confirm intent once for strongly gendered garments instead of silently generating.

`browse_models` per segment, using Dreem's own terms in the query ("Plus build, woman, 30s, warm approachable"). Suggest a NAMED default lineup and ask for a confirm or swaps BEFORE pricing - per **Casting and pose: suggest, explain, confirm** in `_shared-dreem-mcp-guide.md`, the cost preview waits until the lineup is confirmed or actively chosen (once for the whole set, never per talent):

> Default lineup (body axis): 4 talents - Slim, Average, Athletic, Plus (Dreem's Body Build terms). Want the full range? Very Slim and Lean join too. Swap any talent in the picker or by name, or say "go" to keep these.

The user's words override picker state. Check pose gender against every talent in the lineup.

## Step 4 - Same shot, same frame

`browse_product_shot_styles` with a query built from the Step 0 read of the source ("straight-on full body, soft studio, neutral backdrop") - the goal is the source's pose family and mood, not a new creative direction. Lock ONE shotCode set (1-2 codes) for the whole lineup. On the gender axis, pose codes differ per gender: pick the matching pair from the same pose family - same framing, same mood, gender-appropriate code - so the set still reads as one shoot. Ratio and resolution: the source's (typically `TwoK` for PDP).

## Step 5 - The multiplication, priced

Plan table per `_shared-credit-model.md`: rows = talent x shot. This skill multiplies fast and the preview must show it: 4 talents x 2 shots at 2K is 8 virtual-model generations = 88 credits. Exact math, one total, `confirm` LAST (RULE-A), stop, wait.

## Step 6 - Generate + set QA

Max 3 concurrent, `show_generation_result` once per row. QA per `_shared-output-conventions.md` with the set-specific check on top: the garment must read as the SAME garment on every person. Fit differences are the point; garment differences - color drift, pattern changes, a hemline that moves - are failures. Styling consistency across the lineup matters as much as garment fidelity (on the gender axis, check the styling pieces held for every talent); flag any output whose styling drifted.

Manifest one row per talent x shot. The summary recommends publishing the set together on the PDP (a lone plus-size or 60s shot in a sea of sample-size twenty-something imagery misses the point) and names the chain:
- Strongest shot of the set across channels -> `dreem-channel-pack`.
- Motion on one -> `dreem-image-to-video`.
- The whole look, rethemed for next season -> `dreem-seasonal-restyle`.
