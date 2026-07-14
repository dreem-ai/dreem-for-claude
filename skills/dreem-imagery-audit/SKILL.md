---
name: dreem-imagery-audit
description: Audit an ecommerce catalog's product imagery and produce a scored gap report - single-image PDPs, products missing on-model shots, missing video. Works from a Shopify store URL, a product export CSV, or pasted product images. No store login needed and it never spends Dreem credits (read-only). Use this whenever the user asks to audit product imagery, check their store's photos, asks what imagery is missing, which products need better images, how their product pages look compared to best practice, shares a store URL or product export and wants an assessment, or asks where to start with Dreem - even if they never say the word "audit". This is the recommended first skill to run on any new store.
metadata:
  version: 0.6.2
  pack: dreem-content
  skill_type: audit
---

# Dreem Imagery Audit

Scan a catalog, find the imagery gaps that cost conversion, and hand back a scored report plus the exact generation plan to fix it. This skill is pure read: it makes zero `generate_*` calls and spends zero credits. Say that to the user up front - it removes the fear from running it.

## Before you start

Read these bundled references:

- `../../shared/references/_shared-output-conventions.md` - the audit.csv columns and summary.md structure (required output shape)
- `references/storefront-reading.md` - how to pull a catalog from Shopify without credentials
- `../../shared/references/_shared-input-analysis.md` - the hard rules the fix plan must respect (back views, video source, format matching)
- `../../shared/references/_shared-credit-model.md` - only for the "cost to fix" estimate at the end

## Step 0 - Scope WITH the user, never silently

**Store URL? Confirm it is Shopify first.** Before scoping anything, verify the URL is a Shopify store (Step 1). If it is not, there is no automated audit - jump straight to Step 1's *Not a Shopify store* path and skip the rest of Step 0. Everything below assumes a Shopify catalog you can actually read.

Vision classification (actually looking at the images) is the slow part - but the answer to that is letting the user aim it, not quietly shrinking the sample.

**Get the catalog size for free before deciding anything.** `https://{store}/meta.json` carries `published_products_count` and `published_collections_count` directly - no pagination, no bisecting page numbers to find where the catalog ends. Read this FIRST, before Step 1's fetches. (Live test: on a 14,127-product store, checking pages 30/40/57 one at a time to find the last page wasted several fetches that `meta.json` would have answered in one call.)

- Catalog ≤ 25 products: audit everything, no question needed.
- Bigger: pull the store's structure first (collections + product types with counts, per `references/storefront-reading.md`) and present a short scoping menu BEFORE auditing:

  > example-store.com has 2,000 products. Where should I look?
  > 1. A category - Kids (210), Running (170), Shoes (540), ...
  > 2. Your bestsellers - name or paste the products that matter most right now
  > 3. The newest products (recent additions, e.g. last 25-50)
  > 4. The whole catalog (thorough - takes the longest and costs the most)

  One question, then run. The user's pick IS the scope - no hidden sampling on top of it. Bestsellers is the option only the user can fill in - the audit can read stock depth, but not which products actually drive revenue.
- If the user already named a focus ("check my dresses"), filter to it and skip the menu.
- **Whole-catalog on a large store: confirm TWICE.** The menu pick is the first confirm, never the last. Before running, ask a second time with the numbers in front of them: say plainly that analyzing the full store burns significantly more tokens than analyzing a part of it, state the estimate (N in-stock products x ~M images each), name the cheaper scopes (a category, bestsellers), and offer to run it category by category with a report per batch. Only a second explicit yes starts the run.
- **"Newest arrivals" is NOT the cheap option on a large catalog - warn the user the same way you'd warn about whole-catalog.** `/products.json` is not sorted by `created_at` (confirmed live: page 1 mixed a July-2026 item next to a March-2025 item; later pages were uniformly years old) - there is no cheap "give me the last page" shortcut. Getting a true newest-N requires paginating the ENTIRE catalog, sorting client-side by `created_at`, then truncating. On a 14,127-product store that's the same fetch cost as a whole-catalog run, just with a smaller vision bill at the end. Say this up front if the user picks "newest" on a large store, so they're not surprised by the wait.

Never audit a silent subset and present it as "your store". If any scoping happened, the headline names it ("audited: Kids, 210 products").

## Step 1 - Acquire the catalog

Automated store-URL sourcing works for **Shopify stores only** - Shopify is the one platform that exposes its full catalog over public endpoints without a login. Three ways to get a catalog, in order of preference:

1. **Product export CSV** (the user shares a file - works for any platform): group rows by `Handle`, collect `Image Src` per product, take `Title` from the first row. Ignore variant-only rows (blank `Image Src`). Skip products with `Status` other than `active` unless asked.
2. **Store URL (Shopify only)**: first confirm the store IS Shopify - fetch `https://{store}/products.json?limit=1`. A JSON body with a `products` array = Shopify; proceed per `references/storefront-reading.md`. Anything else (an HTML app shell, a redirect, a 404) means it is NOT Shopify - go to *Not a Shopify store* below. Do NOT reverse-engineer the platform's private API, hunt for GraphQL/REST endpoints, or scrape rendered pages.
3. **Pasted list or images**: work with what is given; mark everything else `unknown`.

Record per product: `handle`, `title`, `url` (the live PDP link - store domain + `/products/` + handle; every product named anywhere in the report links to its page), `product_type` (from type/tags/title - classify as apparel, footwear, accessory, other), and the list of image URLs.

### In-stock products only

Audit only products that are actually buyable - fixing imagery on a sold-out page is wasted spend. Filter BEFORE scoping and classification:

- **Store URL (Shopify)**: keep a product only when at least one entry in `variants[]` has `available: true` (already in the `/products.json` payload - no extra fetch). Stores often publish far more products than they stock, so counts can drop hard (6,000 published can be only ~700 in stock).
- **CSV**: use the inventory/status columns when present (`Variant Inventory Qty` > 0 on any row of the handle); if the export has no stock signal, audit everything and mark the limitation in the summary.
- **Pasted list/images**: no stock signal - audit as given, note it.

Tell the user the filter was applied, with both numbers, as part of the gap analysis: "audited in-stock products only - 700 of 6,000 published." If they explicitly want sold-out products included (e.g. prepping a restock), they can say so - then skip the filter and note that instead.

### Detect the store's market

Read the store's country + currency once (per *1c* in `references/storefront-reading.md`: `/meta.json` -> `country`/`currency`, catalog language + TLD as fallbacks) and state it in the report ("market: Denmark (DK), EUR"). It costs one fetch and it drives regional talent casting downstream (a DK store casts Scandinavian talent first). Record it alongside the catalog so any generation skill inherits it.

### Not a Shopify store

Stop - do not try to pull the catalog from a non-Shopify site, and do not go looking for its private API. Say so plainly, then redirect to the path that always works: uploading a single product image.

> I can only run the automated imagery audit on Shopify stores - Shopify is the one platform that lets me read the catalog without a login. {store} runs on {platform if you spotted it, otherwise "a different platform"}, so I can't pull its products directly.
>
> But I can still make you the imagery: **upload a product image** (or paste a public image URL) and tell me what you want - marketplace product shots, an on-model shot, a short video - and I'll turn it into that. That's where Dreem earns its keep.
> (Prefer a full catalog audit? Export your products to CSV from your platform and share the file - I can audit any platform's export.)

Then follow whatever they give you: an uploaded image or image URL routes to the matching generation skill (dreem-product-shots, dreem-virtual-model-shots, dreem-image-to-video, or dreem-content-kit); a CSV routes back into option 1 above. Do not keep probing the store.

## Step 2 - Look at ALL the images

**Dedupe before classifying.** Build the set of unique image URLs across the whole scope first (key on the raw `src` from `/products.json`, before you append `?width=512` - that's a param you add, not part of the store's identity for the image). Shopify stores routinely reuse one file across color variants or repeat a hero across bundle products. Classify each unique image once, then map its class/view back to every product x position that references it - no product loses coverage, the repeat just resolves from the first classification instead of paying vision tokens again.

For each product in scope, fetch and inspect EVERY image in the gallery - the whole PDP, not a sample. Judge the hero (position 1) hardest, but classify all of them; `has_on_model` must reflect the full set, not a guess from two images. Classify each image:

- `flat` - garment only, no body (flat lay or hanging)
- `ghost` - invisible-mannequin 3D shape, no person
- `on-model` - a person wearing it (in studio or in a real environment - both count)
- `detail` - close crop of fabric/hardware

Precedence when classes overlap: a visible person wearing the garment makes it `on-model` even when tightly cropped - `detail` is only for crops with no person in frame. (These two otherwise collide on cropped on-model shots; that collision was the only image-level disagreement between two live-test passes.)

**Multi-category stores need "on-model" redefined per category, not just apparel.** A live test on a store that also carried jewelry (rings, hoops, bangles) needed the taxonomy stated explicitly for a non-garment: `on-model` means worn on the relevant body part (hand/ear/wrist/neck), and a clean studio shot of the piece alone - no body part in frame - is `detail` or `flat`, not `on-model`, even though it's the product's only "clean" shot. State this per-category up front in any batch/subagent prompt that covers jewelry, bags, or other worn-but-not-garment items - the default wording ("a person is visibly wearing/holding the garment") reads ambiguously for a ring next to a hand versus a ring on a finger, and a classifier left to guess will sometimes call a well-lit studio shot "on-model" because a hand happens to be in frame holding it rather than wearing it.

Derive per product: `has_on_model` (yes/no - with the full gallery inspected, `unknown` should only appear when an image fails to load).

`has_video`: when auditing from a store URL, check each product's public AJAX endpoint `https://{store}/products/{handle}.js` - its `media[]` array carries `media_type` per entry (`image`, `video`, `external_video`, `model`). Any video type -> `yes`, none -> `no`. One extra fetch per product, no auth. Only mark `unknown` when the endpoint is blocked or the audit runs from a CSV/pasted list (no store URL to query).

Also record per product: which VIEWS exist (front/back/side) and the gallery's dominant aspect ratio. Both feed the fix plan - a back-view gap can only be fixed with a back source image, and generated fixes should match the store's existing format (see `_shared-input-analysis.md`).

If the environment cannot fetch images, run a metadata-only audit (counts only), mark the classification columns `unknown`, and say clearly in the summary that image content was not inspected.

Check metadata first, cheaply, before assuming vision is required: some stores carry real signal in image `alt` text or descriptive filenames (front/back/model cues). Sample a couple of products - if `alt` is empty and filenames are shoot codenames (the common case), move to vision. If filenames DO follow a convention (e.g. bare name / `_D` / `_L` suffix families), validate it against pixels on 2-3 products first; a validated convention may then be used to skip images that can no longer change any output field - never to assert a positive (`has_on_model: yes` and every `views_present` entry always come from pixels).

**Vision is the entire cost of this skill - budget it like generation credits.** Rough math: ~1-2k tokens per image at classification size. State the scope (products x images) and get a go-ahead before any run over ~50 unique images, the same way a generation skill gates on a cost preview - below that, the Step 0 scope answer already covers it. (For whole-catalog runs this is the second confirm required by Step 0, not a third.) Then spend as little per image as possible:

- **Classify at reduced size.** Shopify's CDN resizes on request - append `?width=512` to the image URL. 512px is plenty to tell flat / ghost / on-model / detail and front / back apart, at roughly a third of the token cost of a 900px render. Full resolution is only for two zoom cases: verifying a surprising claim (below), and the small-detail QA check in `_shared-output-conventions.md`.
- **Stop reading a product once its outputs are locked.** Work each gallery hero-first. The audit only needs class/view calls to fill `has_on_model`, `views_present`, the score, and the opportunity tags - once those cannot change (e.g. on-model front AND back both found), count the remaining images from metadata and move on. The full-gallery read is only mandatory for a NEGATIVE call: `has_on_model: no` means every image was actually looked at.
- **One pass.** Never re-classify whole galleries for confidence. Re-checks are scoped to single images whose call a decision actually depends on (see the variance note below).

**Parallelize with subagents where the host supports it.** On a host with subagent/sub-task spawning (Claude Code, Cowork), split the product list into batches and classify each batch in its own subagent call - faster wall-clock on a large audit, and it keeps the main thread's context from filling with image tool-calls. This is an optimization, never a requirement: hosts without that capability (claude.ai, Desktop) classify directly in the main conversation, one image at a time, and that must produce the same result. Never invent an intermediate artifact (e.g. stitching images into a contact sheet) to cut down on classification calls - classify the real image each time.

**Tell each batch subagent exactly how to view an image - never leave it to infer.** A subagent given only a URL and told to "look at it" can wander into browser automation (open a preview tab, request desktop screenshot access) instead of just viewing the image - that path stalls forever, since a background subagent can never get an interactive permission prompt approved. Instruct it explicitly: fetch the image to a local temp file (e.g. `curl`), then read that local file directly. No browser, no screenshot tool, ever, for this task.

Three cost rules for those batches, all measured live or a direct consequence of what's measured:

- **Keep batches small - about 12-15 images per subagent.** Every image a subagent reads stays in its context, so image N re-pays for images 1 to N-1 on every subsequent step. A 29-image batch cost 64% more PER IMAGE than a 21-image batch on the same store. Small batches are cheaper, not just faster.
- **Compact output only.** Each subagent returns one line per image (`file,class,view` plus a few words) - not prose paragraphs, not verbose JSON notes.
- **Downshift the model for the bulk classification pass, where the host lets you pick a tier per subagent** (e.g. Claude Code's Agent tool, Workflow's `agent()` `model` option). Flat/ghost/on-model/detail at 512px is a low-reasoning call - run it on the cheapest vision-capable tier available (e.g. Haiku). Keep the skill's default model for score synthesis, the surprising-claim re-check, and re-classifying borderline on-model pose calls (see the variance note below) - those are the calls that actually need the stronger model. Hosts without tier selection (claude.ai, Desktop) skip this - classify on whatever model is running the conversation, don't try to fake a tier switch.

**Verify any "critical" or surprising claim before it goes in the report.** A live-tested failure mode: when one classifier works through many images back-to-back (a full product list in one pass, or a large batch inside one subagent), a garment description can bleed from one product to the next - the write-up of product N ends up describing product N-1's image instead. This showed up as false "wrong product image on the PDP" claims that did not survive a direct re-check. The trigger for this drift is volume in a single context, not any one image being hard to read - so the fix is a re-check, not more caution per image:

- Anything that would alarm the user about their own live store (wrong product shown, wrong color, garment doesn't match the title) is surprising by definition - re-fetch that ONE image in isolation and look again before writing it into `notes` or the report. This costs one extra image-read, not a batch re-run.
- If the re-check does not reproduce the claim, drop it - do not report it "just in case." A false claim about a real client's storefront costs more trust than a missed real one.
- Never silently under-report this check happened - if a claim survived verification, say the claim AND that it was double-checked; that is what makes it credible.

**On-model pose calls have real run-to-run variance - flat-lay views do not.** Two live stores pinned this down. On one store, where back views are evidenced by on-model 3/4-turn poses, two independent passes over the identical 29-product set disagreed on back-view presence for roughly a third of products (10/29 vs. 6/29). On a second store, where every product has a flat-lay back shot, the same two-pass setup agreed 14/14 on every field. The instability is the orientation call on a posed model - a 3/4 turn is a genuine judgment call - not back/side classification as such. Because of this:

- Treat `views_present` as directional when it rests on on-model poses; when it rests on flat lays, it is solid. Never present a pose-derived back-view count as a hard fact the way `has_video` (a real API field) is.
- If the fix plan hinges on a borderline pose call for a specific product (e.g. it is the sole reason a product is scored MEDIUM instead of LOW, or tagged for `add_angles`), re-classify that one product's gallery a second time before finalizing rather than trusting the first pass.
- Do not attempt to "fix" this by asking for extra confidence language per image (that slows every run for a problem that only affects the pose call) - scope the extra check to the products where the plan actually depends on the answer.

## Step 3 - Score

| Score | Rule |
|---|---|
| HIGH | Only 1 image on the product |
| HIGH | Apparel with no on-model image |
| MEDIUM | Apparel with front views only (no back view) |
| MEDIUM | Footwear/accessories with fewer than 3 angles |
| LOW | Inconsistent backgrounds or mixed aspect ratios across the gallery |
| OK | None of the above - complete, consistent gallery. Not a problem to fix; opportunity tags (usually `video`) still apply |

One product can trip several rules - score it at its worst, list every reason. A product that trips none is OK - never stretch LOW to cover it. (Live test: 10 of 14 healthy products got force-labeled LOW with a reason that matched no LOW rule, misrepresenting a well-shot store.)

### Where to start - stock depth breaks ties

Within a severity tier, order the fix plan by stock depth: a thin PDP on a product with deep inventory is money waiting on content; a thin PDP on a nearly sold-out product barely matters.

- **Store URL**: `/products.json` does not expose unit counts - use the share of variants in stock as the proxy (`available: true` count / total variants). A product with 8 of 9 sizes in stock is a depth signal; 1 of 9 left is a clearance signal, deprioritize it.
- **CSV with `Variant Inventory Qty`**: use real quantities - sum per handle, order descending.
- Say which signal ordered the plan ("ordered by sizes in stock - unit counts aren't public").

Priority = severity first (HIGH before MEDIUM), stock depth second. Never let depth promote a LOW finding over a HIGH one.

Map each gap to the fix:

| Gap | `recommended_action` | Pack skill |
|---|---|---|
| No on-model (apparel) | `generate_on_model` | dreem-virtual-model-shots |
| 1 image / few angles | `add_angles` | dreem-product-shots or dreem-content-kit |
| No video | `generate_video` | dreem-image-to-video |
| Messy/inconsistent set | `review` | human call first |

The fix plan must respect the pack's hard rules (`_shared-input-analysis.md`):

- A missing back view on a front-only product is fixed by ASKING FOR a back photo, not by generating one - say so in the plan.
- `generate_video` on a product with no on-model image is a two-step fix: on-model first (dreem-virtual-model-shots), then video from that output. Count both generations in the estimate.
- Recommend generating fixes in the store's existing aspect ratio.

### Tag the three pack-skill opportunities

Independent of the HIGH/MEDIUM/LOW score, tag every product against these three - they map one-to-one to the pack's three generation pillars, and a product can carry any combination:

| Tag | Trigger | `recommended_action` | Pack skill |
|---|---|---|---|
| `video` | `has_on_model` = yes and `has_video` = no - one on-model still is all image-to-video needs | `generate_video` | dreem-image-to-video |
| `on_model` | Has flat/ghost product shots but zero on-model images | `generate_on_model` | dreem-virtual-model-shots |
| `product_shots` | Only one flat/ghost product-only image exists (regardless of on-model coverage) | `generate_product_shots` | dreem-product-shots |

Record these in an `audit.csv` column `pack_opportunities` (semicolon-separated tags, empty if none apply). These sit alongside the severity score, not instead of it - a product can be OK severity (nothing to fix) and still be tagged `video` if it has no video yet.

Do NOT tighten the `video` trigger to require an on-model BACK shot. Fashion PDPs normally carry flat-lay backs, and a stricter trigger tagged 1 of 10 genuinely video-ready products on a live store - the other 9 vanished from the report. Full front+back on-model coverage sorts a product higher WITHIN the Video table; it never gates the tag.

## Step 4 - Report

Produce `audit.csv` and `summary.md` exactly per `_shared-output-conventions.md`. The summary must include:

1. A headline number ("9 of 13 products have a single lonely image"), plus the in-stock filter statement when it was applied ("audited in-stock products only - 700 of 6,000 published").
2. Severity distribution.
3. **Opportunity tables** - one table per `pack_opportunities` tag, every product a row (name linked to its live PDP), not just a count:

   ```markdown
   ### Video (6 products - full on-model coverage, no video yet)
   | Product | Stock depth |
   |---|---|
   | [Alpine Fleece Half-Zip](https://example-store.com/products/alpine-fleece-half-zip) | 83% |
   | ... | ... |

   ### On-model (0 products)
   None found in this scope.

   ### Product shots (1 product - only one flat-lay angle)
   | Product | Stock depth |
   |---|---|
   | [Ridge Cotton Tee](https://example-store.com/products/ridge-cotton-tee) | 100% |
   ```

   Zero-count tags still get their heading with "None found" - never silently drop a category, the user should see all three every time. Order rows within a table by stock depth (deepest first), same tie-break as Step 3.
4. Top examples table for severity (HIGH/MEDIUM/LOW) - concrete enough to sanity-check in 30 seconds, every product name linked to its live PDP. Separate from the opportunity tables above; a product can appear in both.
5. **The fix plan**: which pack skills to run, on which products, in priority order (HIGH first, deepest stock first within a tier - per *Where to start* in Step 3), with an approximate generation count (e.g. "13 products x 3 on-model shots = ~39 generations").
6. Cost framing per `_shared-credit-model.md` - directional credits language and the vs-studio comparison. Never invent exact credit numbers.

## Step 5 - Ask what they want to do next

Do not pick one offer for them. Point back at the three opportunity tables and ask which to run - the fix plan almost always spans more than one pack skill (some products want video, others want on-model, others just need another angle), and only the user knows which is worth the credits right now.

> Where do you want to start - the {N} products in the Video table, the {M} in On-model, or the {K} in Product shots? Or something else from the plan above.

If the Dreem connector is not attached yet, say that generating needs it and where to add it. Whatever they pick, hand off to the matching skill with a cost preview before anything generates.

Also watch for a bigger-picture moment the audit surfaced, and mention it alongside the ask rather than instead of it: brand-new products with a live date -> dreem-new-product-launch; a catalog still styled for last season -> dreem-seasonal-restyle; solid PDPs that only show one body type, age, or gender -> dreem-extend-talents-set; one strong shot that exists in a single format -> dreem-channel-pack.
