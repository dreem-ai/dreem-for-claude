# Dreem MCP Guide

How every skill in this pack talks to Dreem. Read this before making any Dreem tool call.

## Tool surface (Dreem MCP v3)

| Tool | What it does |
|---|---|
| `browse_models` | Semantic search over 400+ virtual talents. Opens a visual picker for the user. |
| `browse_product_shot_styles` | Semantic search over shot styles (backgrounds, poses, moods). Visual picker. |
| `browse_video_styles` | Semantic search over curated video motion prompts. Visual picker. |
| `get_models` | Talent details by ID list (max 20). Use when you already have IDs. |
| `get_product_shot_styles` | Shot details by ID list (max 20). |
| `get_video_style` | Video prompt details by ID. |
| `upload_image` | The ONLY way to use a local file. Returns a `tempFileId`. |
| `confirm` | Renders a Confirm button. Open it LAST, after all pickers. |
| `generate_product_shot` | Product still. requestId in ~1s, done in ~60s. |
| `generate_virtual_model` | Talent wearing the outfit. ~60s. |
| `generate_product_video` | Image-to-video clip. ~120s for 10s. |
| `wait_for_content` | Server-side long-poll (~50s chunks) on a requestId. |
| `check_generation_status` | Single status poll. Prefer `wait_for_content`. |
| `show_generation_result` | Renders the finished asset inline. Call exactly once per completed request. |

Deprecated aliases still work if a host exposes them: `search_talents`=browse_models, `search_shots`=browse_product_shot_styles, `search_video_prompts`=browse_video_styles, `list_talents_by_ids`=get_models, `list_shots_by_ids`=get_product_shot_styles, `get_video_prompt`=get_video_style, `generate_packshot`=generate_product_shot, `generate_image_to_video`=generate_product_video, `wait_for_generation`=wait_for_content, `get_generation_status`=check_generation_status.

**Host prefixes vary.** On claude.ai the tools may appear as `Dreem:generate_product_shot`, in other hosts as `mcp__dreem__generate_product_shot`. Match tools by their base name, never by a hardcoded prefix.

**First-run connection check (before any planning).** At the start of every generation flow, verify Dreem tools are reachable by base name. If none are available, stop and walk the user through connecting BEFORE opening pickers or drawing a plan. The connect steps, by host:

- **Claude Desktop / Cowork (plugin installed):** the plugin auto-registers the Dreem MCP (`https://mcp.dreem.ai/mcp`); the user approves the **Connect to Dreem** prompt and logs into their Dreem account (OAuth - no API key to paste).
- **claude.ai:** Settings → Connectors → Dreem → Connect.
- **Claude Code (CLI):** `/mcp` to trigger login, then approve OAuth.

If a host does not auto-register Dreem, add it by hand with the endpoint `https://mcp.dreem.ai/mcp` (claude.ai / Desktop: Settings → Connectors → Add custom connector; CLI: `claude mcp add --transport http dreem https://mcp.dreem.ai/mcp`), then approve the OAuth login.

A free Dreem account works (100 credits/month at dreem.ai). After connecting, re-check the tools are live before promising output. The full connect + troubleshooting walkthrough lives in the `dreem-getting-started` skill (Step 1) - hand off there if the user gets stuck. The audit skill is the exception - it runs without any connection and is the right suggestion for a user who is not ready to connect yet.

Valid enum values are also exposed as resources at `dreem://attributes/*` (aspect ratios, resolutions, genders, ...). Field descriptions on each tool list the allowed strings.

## The two interaction modes

**Interactive mode (1-3 products).** Use the visual pickers. The user taps their choices, sees what they are getting.

Flow order matters (RULE-A):
1. Open ALL required pickers/uploader for the flow first.
2. Open `confirm` LAST. It supplements the pickers, never replaces them.
3. STOP. Wait for the user's confirm message. Do not call any `generate_*` before it.
4. On confirm, re-read the accumulated context and validate completeness yourself. The Confirm button cannot read picker state. If something is missing, say exactly what.

**Batch mode (4+ products, or a CSV).** Pickers per product would be painful. Instead:
1. Open the pickers ONCE to lock styles/talent for the whole batch ("these styles will apply to all 12 products").
2. Build a batch plan table (see `_shared-output-conventions.md`) and a single cost preview (see `_shared-credit-model.md`).
3. ONE confirm for the whole batch. Then generate sequentially, polling each request.
4. Never fire more than 3 concurrent generations. Collect results into the manifest as they complete.

## Casting and pose: suggest, explain, confirm

For talent (`browse_models`) and pose (`browse_product_shot_styles`), never silently pre-select and move on - the user gets a say before any credits are planned.

**Talent gets one upfront question when the brief doesn't already describe the model:** should Dreem suggest one based on their product page/store, or do they want to pick - either by selecting from the picker's examples, or by describing the look ("woman in her 40s, warm approachable") for Dreem to find. Skip the question when the user already described or named the model - their words ARE the answer. Then, for EACH of the two:

1. **Pick** the best-fit option from the browse results. For TALENT, bias the first pick to the store's market region when it is known - a Danish/DK store (country/currency/language from the store read) casts Scandinavian talents first (`browse_models` query e.g. "Scandinavian Danish man, fair skin"). This sets the default only; alternatives still span wider, and the user can always broaden it.
2. **Explain** it - name it with a one-line reason tied to the product and brief ("Wilder Hayes - adult man, athletic, outdoor look; fits the outdoor jacket's use case").
3. **Ask** the user to confirm: "Use this one, or pick another?" The visual picker stays open as the override path.
4. **If they decline** (or want options), suggest 2-3 named alternatives from the same results, each with a one-line differentiator ("Rafferty Cole - lighter wavy hair, more editorial; Tunde Adisa - deeper skin, same athletic build"), and let them choose in chat or the gallery.

Hold the cost preview until talent AND pose are each confirmed or actively chosen. A plain "go"/Confirm on your named suggestion counts as confirmation - but only if the suggestion, its reason, and the alternatives offer are already on screen first. Batch/diversity sets: do this once for the locked cast and pose set (list them), never per product.

## Image sourcing rules

- **User's local file** (chat upload, file on disk): call `upload_image` first, pass the returned `tempFileId` as `images[].fileId`. There is no other way to use a local file.
- **Public HTTPS URL** (Shopify CDN, any public image): pass directly as `images[].url`. No upload needed. This is what makes store-driven batches cheap.
- Exactly one of `fileId` or `url` per image entry, never both.
- Allowed extensions: `.webp`, `.png`, `.avif`, `.jpg`, `.jpeg` (video frames: `.jpg`, `.jpeg`, `.png`, `.webp`). Shopify CDN URLs with query params keep their extension in the path, which is fine.
- `viewType`: `Front` or `Back`. When the user has both, send both - back shots make back-facing outputs accurate.
- Virtual model only: `productType` per image - `Main` (the garment being sold) or `Outfit` (supporting garments for the look).

## Generation parameters (exact enums)

| Param | Values |
|---|---|
| `outputAspectRatio` | `Ratio1x1`, `Ratio4x3`, `Ratio3x2`, `Ratio2x3`, `Ratio5x4`, `Ratio4x5`, `Ratio3x4`, `Ratio9x16`, `Ratio16x9`, `Ratio21x9` |
| `resolution` | `OneK` (~1024px), `TwoK` (~2048px), `FourK` (~4096px) |
| `outputFormat` | `png`, `jpeg` |
| `duration` (video) | `5s`, `10s` |
| `shotCodes` | The `code` values from browse results. NOT the `id`. At least one required. |
| `talentId` | GUID from browse_models. Must be tenant-owned or SYSTEM. |
| `prompt` / `promptId` (video) | Exactly one of the two. `promptId` reuses a curated style; `prompt` is freeform creative direction. |

Channel-to-ratio mapping lives in `_shared-channel-specs.md`.

## Async pattern

Every `generate_*` returns a `requestId` in about a second. The generation itself takes ~60s (images) to ~120s (video).

1. Call `wait_for_content` with the requestId. It long-polls up to ~50s server-side.
2. If it returns `in_progress`, call it again with the SAME requestId. Cap the loop: after ~10 minutes of `in_progress` on one request (~12 polls), stop, report the stall with the requestId, and offer to keep waiting or check back later - never poll forever.
3. Done ONLY when `status='completed'` AND `outputs[]` has at least one entry with a non-empty URL. A `completed` with empty or URL-less outputs is NOT done - poll again.
4. `failed`/`cancelled` expose `errorCode` + `message`. Report them honestly, per product, and continue the rest of a batch.
5. RULE-B: once a request completes with a usable URL, call `show_generation_result(requestId)` exactly once. Never end a flow with result URLs only in text.

## Quality expectations (be honest)

Virtual model output is strong. Product Shots are improving, not perfect - logos, fine patterns, and stitching can drift. Never promise perfection. After generation, run the QA pass in `_shared-output-conventions.md` and tell the user Dreem Studio has built-in iterative editing (prompt edit + brush tool) to fix a shot without regenerating from scratch.

## Naming rule

The pillar is called **Product Shots** in every user-facing sentence. Never "Packshots", even though one legacy tool alias contains the word.
