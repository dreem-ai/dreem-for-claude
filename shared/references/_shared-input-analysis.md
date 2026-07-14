# Input Analysis - the mandatory Step 0

Every generation skill in this pack starts here, before any picker opens and before any plan table is drawn. The rules exist because generating from unexamined inputs produces confident garbage: invented back panels, videos animating a garment nobody is wearing, and 3:4 outputs dropped into a 1:1 store.

## Step 0 - look at every input image first

Fetch and LOOK at each input image (and, when working from a store, the product's existing live images). Record three things per image:

1. **View**: front, back, side, detail. A front-only source means the back of the garment is UNKNOWN.
2. **Content type**: flat lay, ghost mannequin, on-model. This gates what may be generated from it (see the hard rules).
3. **Aspect ratio and framing**: the shape the store actually uses today (compare across the product's existing gallery - most stores are consistent).
4. **Props and compliance flags**: hands, hangers, clips, busy backgrounds. Marketplace mains (Amazon, Google Shopping) require prop-free pure-white compositions - note explicitly that these get removed in the generated output, and pick styles that recompose the garment prop-free.

Write the findings into the plan so the user sees them: "source: 1 image, ghost mannequin, front view, 3:4."

When working from a store (not a loose upload), also read the store's market once - country + currency from `/meta.json` (see the audit skill's `storefront-reading.md`, *1c*). It sets the default talent region for casting (a Danish store -> Scandinavian talents first). Carry it into the casting step.

## HARD RULE 1 - no invented back views

Never generate a back-facing output (a back Product Shot, a back-facing pose, or turn/rotation video that reveals the back) when no back-view input exists. The model does not know what the back looks like - it will invent labels, pockets, seams, and prints that are not on the real garment.

- Choose `shotCodes` from the views the input actually supports. Front-only input -> front, three-quarter, side, and detail shots only.
- If the user explicitly asks for a back view anyway: say plainly that the back will be MADE UP because no back image exists, and only include the row after they acknowledge that. Mark the row `check-details` in the manifest before anyone even QAs it.
- The clean fix is always to ask for a back photo - one phone snap unlocks accurate back views forever.

## HARD RULE 2 - video needs an on-model first frame

Never call `generate_product_video` with a first frame that is not an on-model image. Motion sells the garment on a body; animating a flat lay or ghost mannequin produces a floating garment that reads as AI sludge.

- Input is flat/ghost and the user wants video? Generate the on-model shot first (route to `dreem-virtual-model-shots`, or do both in `dreem-content-kit`), then animate THAT output.
- In `dreem-content-kit` the video row always sources its `FirstFrame` from the kit's own generated virtual-model output - never from the raw product image, and never from a Product Shot row.
- If the kit produces no on-model asset (e.g. no suitable talent exists for the garment category), there is no video row. Say why instead of quietly animating a still.
- Turn/360/rotation motion is a back view in disguise: it requires a back-view input (or the user's explicit acknowledgment per HARD RULE 1). Otherwise pick motion that stays front-facing: push-in, fabric sway, weight shift.

## HARD RULE 3 - baby clothes are Product Shots only

Baby/infant garments (sold as "Baby ...", sized 0-24 months, or clearly infant-proportioned) NEVER get on-model generation and NEVER get video. No baby talents exist, and putting a baby garment on an older child model misrepresents the product. Product Shots are the full menu for baby items: flat lay, ghost mannequin, side, detail. Say so in the plan - "baby garment: Product Shots only" - instead of quietly skipping rows.

## HARD RULE 4 - swim, underwear, and lingerie cast adult talents only

Swimwear, underwear, lingerie, and similar intimate categories NEVER go on kids or teen talents - regardless of the size range the garment sells in, regardless of what the user asks for. Cast adults only, and confirm the chosen talent explicitly before the plan (no silent default casting for these categories). Kids swimwear exists as a product; its imagery path is Product Shots, the same menu as HARD RULE 3. Say so in the plan instead of quietly skipping rows.

## Input rights and output use - say it once, plainly

- Generate only from images the user owns or has the rights to use - their own product photos, their store's imagery, their shoots. If a source photo shows a person (a model from an old shoot, a photo found online), note before the plan that Dreem replaces the person with a virtual talent and the output does NOT license anything from the original photo - and if the user plainly has no rights to the source at all, say that generating from it is on them and recommend using their own product image instead.
- Outputs are AI-generated imagery. Some channels have disclosure or labeling policies for AI content (marketplaces, ad platforms); flag this once in the summary when outputs are bound for those channels - checking the specific policy is the user's call.

## FORMAT RULE - match the store's existing format by default

Detect the aspect ratio of the product's existing live imagery in Step 0. That ratio is the DEFAULT for every output - a mixed-ratio gallery is exactly the inconsistency `dreem-imagery-audit` flags on other people's stores.

- Default: generate in the same ratio the product page already uses.
- Then offer, once: "your current images are 3:4 - keep that for the new shots, or also generate other formats (1:1 marketplace, 9:16 Stories)?" The channel map in `_shared-channel-specs.md` is the menu; the store's existing format is the default.
- Only skip the question when the user already named the destination ("for TikTok") - then the channel spec wins.
- **No store to match** (a single loose photo, no live gallery): record the source photo's own ratio as a signal, use the channel defaults from `_shared-channel-specs.md` for any named destinations, and confirm the primary ratio once instead of assuming.
- **Right content, wrong ratio** (e.g. an on-model 1:1 still bound for 9:16 Reels): don't quietly ship the wrong shape and don't crop. Offer both paths with honest costs - animate/use as-is at the source ratio, or regenerate at the target ratio first (for video: a virtual-model reframe at 9:16, then animate that output).

## Order of precedence

1. These hard rules (never overridden silently).
2. The user's explicit, informed choice (after the warning, in the plan, on the record).
3. Channel specs and kit defaults.
