# Dreem Claude Skills

Skills that turn Claude + the [Dreem MCP](https://dreem.ai) into a working content studio for ecommerce fashion brands. One product image in, full content out - audited, planned, cost-previewed, and generated.

## The pack (10 skills)

| Skill | What it does | Spends credits? |
|---|---|---|
| `dreem-getting-started` | First-run welcome: connect Dreem, see what the pack does, get routed to a first task. | No |
| `dreem-imagery-audit` | Scan a store or catalog for imagery gaps: single-image PDPs, missing on-model shots, missing video. Scored report. | No - read-only |
| `dreem-product-shots` | Clean Product Shots from any product photo. Marketplace-compliant, any aspect ratio, up to 4K. | Yes, after approval |
| `dreem-virtual-model-shots` | Put any garment on any of 400+ virtual talents. Flat/mannequin to on-model. | Yes, after approval |
| `dreem-image-to-video` | Turn a still into a 5-10s product video for PDP, TikTok, Reels. | Yes, after approval |
| `dreem-content-kit` | The everything pack: Product Shots + on-model + video for a product, one approval. | Yes, after approval |
| `dreem-new-product-launch` | Launch imagery planned backwards from the live date - one product or a whole drop, one approval. | Yes, after approval |
| `dreem-channel-pack` | One finished shot recomposed for every channel: PDP, marketplace, Stories, feed, email, Pinterest. | Yes, after approval |
| `dreem-seasonal-restyle` | Retheme existing on-model imagery for a season or campaign - same garments, new look, one batch. | Yes, after approval |
| `dreem-extend-talents-set` | Extend the current on-model shot across body types and sizes, ages, or genders - same styling, different people. | Yes, after approval |

The four starting-point skills chain: the audit routes gaps to the right fix, a launch or restyle hands its winner to `dreem-channel-pack`, and any approved on-model look extends through `dreem-extend-talents-set`.

Safety contract across the pack: **no generation before you see a plan and a cost preview and approve it.** The audit skill never generates at all.

## Prerequisites

1. A Dreem account (free plan works: [dreem.ai](https://dreem.ai))
2. A connection to the Dreem MCP (`https://mcp.dreem.ai/mcp`). The plugin registers it automatically - on first use you approve the "Connect to Dreem" prompt and log into your Dreem account (OAuth, no API key). On claude.ai without the plugin: Settings -> Connectors -> Dreem.

## Install

The pack ships as a **plugin only** - skills link to shared reference files at the plugin root, so individual skill folders are not self-contained and are not distributed separately.

**claude.ai / Claude Desktop:** install the plugin zip (download it from this repo's Releases, or build it yourself with `python3 scripts/package.py`) via Cowork -> Customize -> Browse plugins -> Add from file.

**Claude Code:** `/plugin marketplace add dreem-ai/dreem-for-claude`, then install `dreem-content`. Or clone the repo and add it as a local plugin.

## First run (what a new user experiences)

1. **Install** the plugin (Releases zip, or the marketplace listing).
2. **Connect** - the plugin registers the Dreem MCP (`https://mcp.dreem.ai/mcp`); the client shows a "Connect to Dreem" prompt. Approve, log into your Dreem account (free tier works). No API keys.
3. **Say anything** - "get started", "what can this do", or just drop a store URL. The `dreem-getting-started` skill runs the welcome: connection check, copy-paste example prompts with credit costs, and the recommended first move - the free store audit, which needs no account at all.

Two standing promises: nothing generates without a cost preview + explicit approval, and the audit never spends credits.

## Build the distributables

```bash
python3 scripts/package.py
```

Outputs to `dist/`: `dreem-content-plugin.zip` (manifest + all skills + shared references + MCP wiring via `.claude-plugin/plugin.json`).

The `_shared-*.md` files live once in `shared/references/`; every skill links to them via `../../shared/references/`. The package script validates those links and ships `shared/` inside the plugin zip - no copies, no sync step.

## Repo layout

```
.claude-plugin/plugin.json     plugin manifest (registers skills + Dreem MCP)
skills/<skill-name>/           SKILL.md + README.md (+ references/ for skill-specific files)
shared/references/             _shared-*.md - single copy, linked from every skill
scripts/package.py             builds dist/
```

## Roadmap

- Tier 2: store write-back (push approved assets to Shopify PDPs) once the Dreem MCP exposes store tools. Until then the manifest + Dreem's n8n templates cover delivery.
- Next skills: slow-mover-refresh, replace-model (dedicated flow - the mechanic ships inside dreem-virtual-model-shots today), content-roadmap.
- Video demo + landing page.
