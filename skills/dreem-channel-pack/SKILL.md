---
name: dreem-channel-pack
description: Spread one finished shot across every channel the brand sells through - PDP, marketplace 1:1, Stories/TikTok 9:16, feed 4:5, email hero, Pinterest - each recomposed at its target ratio, never cropped. Works from a shot another Dreem skill just generated, a live store image, or an upload. Use whenever the user wants an existing image "everywhere", asks for a Story or TikTok or feed version, an email hero, Pinterest pins, marketplace-ratio versions, asks to resize or reformat a shot, or picks a favorite from a generation run and wants it in all formats. For building a NEW set from a raw product photo use dreem-content-kit - this skill multiplies a shot you already like. Requires the Dreem connector.
metadata:
  version: 0.1.0
  pack: dreem-content
  skill_type: generation
---

# Dreem Channel Pack

A crop amputates a composition - a 9:16 cut of a square shot loses the shoes or the face. This skill takes ONE shot the user already likes and re-generates it at each channel's native ratio: composed FOR that ratio, full figure in frame, headroom where the platform puts UI.

## Before you start

- `../../shared/references/_shared-channel-specs.md` - the channel map IS this skill's menu. Read first.
- `../../shared/references/_shared-input-analysis.md` - Step 0 and the hard rules.
- `../../shared/references/_shared-dreem-mcp-guide.md`, `../../shared/references/_shared-credit-model.md`, `../../shared/references/_shared-output-conventions.md`.

## Step 1 - The source shot, analyzed

Exactly one hero source per run (several products means one run each; a full new build belongs to dreem-content-kit). Run Step 0 on it. The findings gate everything:

- **Content type picks the engine.** On-model source: virtual-model rows, with the source as the garment input (`productType: Main`). Flat or ghost source: Product Shot rows only, and no video rows at all until an on-model exists (HARD RULE 2 - offer the two-step via dreem-virtual-model-shots).
- **Identity, said out loud.** A source from this pack's own manifest carries a `talent_id` - reuse the SAME talent and the person stays the person; that is the true reframe. A store photo of an unknown human is different: Dreem re-casts with a virtual talent, the garment and styling carry but the face changes. Say that BEFORE the plan and get an explicit ok, not after six generations.
- **Views bound the formats.** Front-only source: no output that reveals the back, including turn/rotation video (HARD RULE 1).

## Step 2 - Pick the channels once

Default pack from `_shared-channel-specs.md`: PDP `Ratio3x4` `TwoK`, marketplace `Ratio1x1` `TwoK`, Story/Reels `Ratio9x16` `OneK`, feed `Ratio4x5` `OneK`, email hero `Ratio16x9` `TwoK`. Optional video add-ons when the source (or a sibling on-model output) allows it: PDP 5s subtle motion, Stories 10s vertical.

One question: which of these does the brand actually sell through? Drop the rest - a format for a channel they do not use is a credit spent on nothing.

## Step 3 - Plan + one gate

Plan table per `_shared-credit-model.md`: one row per channel; the engine (Product Shot vs virtual model vs video) and the resolution tier decide each row's price - compute exact credits from the table, show one total. Interactive: `confirm` LAST (RULE-A), stop, wait.

## Step 4 - Generate

Same engine inputs on every row; only ratio, resolution, and duration change. Async pattern from the MCP guide, max 3 concurrent, `show_generation_result` once per completed row.

## Step 5 - QA per ratio, deliver by channel

Fidelity QA per `_shared-output-conventions.md`, plus the pack-specific check: composition per ratio - full figure where the channel expects it, nothing vital parked under platform UI zones, the garment reading consistently across all formats. Manifest one row per channel; summary grouped by channel with upload notes (manual today, or Dreem's n8n templates for automated delivery).

## Where it sits in the pack

Chain IN from anywhere: a content-kit or launch winner ("make row 3 work everywhere"), a seasonal-restyle hero, the strongest shot of an inclusive set, or a store image the audit rated highly. Chain OUT to `dreem-image-to-video` when a still should also move.
