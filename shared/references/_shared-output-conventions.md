# Output Conventions

Every skill in this pack produces output in the same shape, so a user can run any skill and know where things land.

## File locations

Default output directory (when a writeable filesystem exists):

```
./outputs/{skill-name}/{YYYY-MM-DD-HHMM}/
  manifest.csv       # generation skills: one row per generation
  audit.csv          # audit skill: one row per product
  summary.md         # every skill
```

Timestamp to the minute so re-runs never clobber earlier runs. In restricted environments (no filesystem), inline the CSV as a fenced code block and the summary as the response body, and say so.

Generated assets themselves stay in Dreem - the manifest carries their URLs, and everything is also in the user's Dreem Studio session history.

**Never hand-paste a Dreem asset URL into a markdown link.** These are AWS SigV4-signed URLs, 1,500+ characters, packed with percent-encoded characters (`%2F`, `%2B`, `%3D`) that must survive byte-for-byte - SigV4 verification is exact-match, not fuzzy. Wrapping one in `[text](url)` puts it through the chat client's markdown/link rendering, which can silently normalize percent-encoding for readability (e.g. decode `%2F` back to `/`) - that alone invalidates the signature and the link 404s/403s for the user even though the asset is completely fine. This is not theoretical: it happened on a live test, reproduced independently when hand-retyping the same URL in a shell command.

- Rely on `show_generation_result` to render the asset - that is the tested delivery path (Result Viewer / image grid, an MCP App, not markdown).
- If the host does not render MCP Apps, give the user the raw URL as **plain unformatted text**, not inside `[...]()` - and say plainly that it must be copied whole, not clicked from a shortened or reformatted version.
- If a link is reported dead, re-fetch it directly (`show_generation_result` again for a fresh presign) before assuming the generation failed - the asset usually still exists; the delivery format broke it.
- **Tell the user how to actually save the file once the link opens**, especially for video: the URL opens straight into a player, not a file download - there is no visible "Save" button on the page itself. Say explicitly: open the link, click the **three-dot menu in the bottom-left of the player**, then **Download**. Without this, a user who successfully opens a working link can still fail to get the file onto their machine and mistake that for the link being broken.

## manifest.csv (generation skills)

| Column | Example | Notes |
|---|---|---|
| `product_handle` | `essential-black-tee` | Or a short name if no store handle exists |
| `product_title` | `Essential Black Tee` | |
| `generation_type` | `virtual_model` | `product_shot`, `virtual_model`, `video` |
| `style_codes` | `SHOT-2041` | shotCodes used, `;`-separated |
| `talent_id` | `9f8e...` | Virtual model rows only |
| `aspect_ratio` | `3:4` | Human-readable, not the enum |
| `resolution` | `2K` | |
| `request_id` | `c0a8...` | The Dreem requestId, for tracing |
| `status` | `completed` | `completed`, `failed`, `skipped` |
| `output_url` | `https://...` | Empty when failed |
| `qa_flag` | `ok` | `ok`, `check-logo`, `check-pattern`, `check-fit`, `failed` |
| `notes` | `logo slightly soft, consider brush edit` | |

## audit.csv (audit skill)

| Column | Example | Notes |
|---|---|---|
| `handle` | `essential-black-tee` | Stable product identifier |
| `title` | `Essential Black Tee` | |
| `url` | `https://{store}/products/essential-black-tee` | Live PDP link (store domain + `/products/` + handle). Empty only when there is no store URL (CSV-only or pasted audits) |
| `score` | `HIGH` | `HIGH` / `MEDIUM` / `LOW` / `OK` (no gap found - opportunity tags may still apply) - never invent a fifth tier |
| `reason` | `Single image on PDP, no on-model shot` | One human-readable sentence |
| `recommended_action` | `generate_on_model` | `generate_on_model`, `generate_product_shots`, `generate_video`, `add_angles`, `review` |
| `image_count` | `1` | |
| `has_on_model` | `no` | `yes` / `no` / `unknown` |
| `has_video` | `no` | Store-URL audits: real yes/no via the product's public `.js` media endpoint. CSV-only audits: `unknown` |
| `pack_opportunities` | `video;product_shots` | `;`-separated tags from `video`, `on_model`, `product_shots` - see the audit skill's opportunity-tagging rules. Empty if none apply |
| `notes` | `flat lay only, front view` | |

## summary.md - required structure

```markdown
# {Skill name} - {Date}

## Headline
One sentence with the top number. "9 of 13 products have a single lonely image on the PDP." Audit reports also state the in-stock filter here when applied ("audited in-stock products only - 700 of 6,000 published").

## What was found / generated
Severity distribution (audit) or completed/failed counts (generation).

## Top examples
A table concrete enough that the user can sanity-check the logic in 30 seconds. Link every product name to its live PDP (the `url` column) - the user must be able to click straight from the finding to the page.

## Next step
Audit: which pack skills fix which gaps, in priority order, with an approximate generation count.
Generation: where the assets are, what to QA, how to push them live (today: download + upload to the store, or use the Dreem n8n templates for automated delivery).
```

## QA pass (generation skills, mandatory)

Dreem is honest that quality is improving, not perfect. After each batch:

1. Look at every output (fetch the image and inspect it when the environment allows).
2. Check garment fidelity: logo placement and sharpness, pattern direction (stripes!), stitching, color match to the input, correct garment (not a lookalike).
3. **Zoom into any known small-detail region - logos, tags, buttons, embroidery - at native or upscaled resolution. Do not judge these from a full-frame view.** A live test caught this the hard way: a full-body 720p video frame passed QA at a glance (garment shape, color, fit all looked right), but a 4x crop on the pocket tag showed the brand wordmark had come out as an illegible white smear - a defect invisible at full-frame scale because the tag occupies a handful of pixels. If the source has a tag, logo, or button in a specific spot, crop that spot out of the output and inspect it on its own before marking `qa_flag: ok`. This applies to both stills and video frames - video especially, since encoding adds its own softening on top of generation.
4. Mark `qa_flag` per row. Anything suspect: explain in `notes` and remind the user about Dreem Studio's edit mode (prompt edit + brush tool) - fixing beats regenerating.
5. Never present a batch as "done" without the QA column filled.
