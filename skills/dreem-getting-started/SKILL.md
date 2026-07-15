---
name: dreem-getting-started
description: First-run guide for the Dreem Content Studio plugin. Use when the user has just installed the plugin, asks what it can do, how to get started, how to connect Dreem, whether they need an account, what things cost, or opens with a vague greeting right after install ("hi", "what is this", "help"). Also use when any Dreem skill is wanted but the Dreem connection is missing. Never generates anything and never spends credits - it orients, connects, and hands off to the right skill.
metadata:
  version: 0.3.3
  pack: dreem-content
  skill_type: onboarding
---

# Dreem Getting Started

The first five minutes decide whether this plugin becomes a habit or shelf-ware. This skill runs the welcome: connect Dreem, show what is possible, and route the user into their first win - which is almost always the free audit.

## Step 1 - Connect Dreem (do this first)

Everything except the free audit needs a live Dreem connection. Get it done before anything else.

**1a. Check first - do not ask, look.** Scan the session for Dreem tools by their base name (`generate_product_shot`, `browse_models`, etc. - prefixes vary by host, see `../../shared/references/_shared-dreem-mcp-guide.md`). Never open this skill by asking "are you connected?" - check silently first, every time, even on a returning user. If the tools are present, the user is already connected: say one line - "Connected - your Dreem account is live" - and skip straight to Step 2. Only run the guide below when the tools are missing.

**1b. Not connected - walk them through it.** One sentence of what it is, then the steps for their host. The connector uses OAuth into their Dreem account - **no API keys, nothing to paste.**

If a **Connect to Dreem** prompt appears (Claude Desktop / Cowork with the plugin installed), approve it and log in with your Dreem account in the browser window - done. If no prompt shows, or Dreem is not in the connector list, add it by hand. The **Add custom connector** dialog is the same in Claude Desktop and claude.ai:

1. Open **Settings → Connectors** (in Claude Desktop, Connectors sits under the **Customize** section of Settings).
2. Top right, click **Add ▾ → Add custom connector**. The dialog is marked BETA.
3. **Name** (first field): type `Dreem`.
4. **URL** (second field): paste `https://mcp.dreem.ai/mcp`.
5. Leave **Advanced settings** alone - **OAuth Client ID and OAuth Client Secret stay empty.** Dreem's OAuth handles login for you; there are no keys to enter. (If they ask: the trust notice is Anthropic's standard line for any custom connector, safe to proceed.)
6. Click **Add**. Dreem now appears in the connector list.
7. Click **Connect** on the Dreem row, then log in with your Dreem account in the browser window that opens.

- **Claude Code (CLI):** skip the dialog - one command does it: `claude mcp add --transport http dreem https://mcp.dreem.ai/mcp`, then run `/mcp` to trigger the Dreem login and approve the OAuth prompt. (`/mcp` alone also works if the connector is already registered.)

**1c. Need an account?** A **free Dreem account works** - 100 credits/month at [dreem.ai](https://dreem.ai). Create it, then run the connect step above.

**1d. Verify it took.** After they connect, confirm the tools are now live before promising anything - re-check for the Dreem tools, then "You're connected - ready when you are." If they are still missing, go to troubleshooting.

**1e. Troubleshooting.**
- *No "Connect to Dreem" prompt appeared* → add the server by hand with the endpoint `https://mcp.dreem.ai/mcp` (claude.ai / Desktop: Settings → Connectors → Add custom connector; CLI: `claude mcp add --transport http dreem https://mcp.dreem.ai/mcp`). If that still does nothing, the plugin may not be installed/enabled - reinstall the Dreem Content pack.
- *Approved but tools still missing* → the OAuth window may have been closed early or blocked. Retry the connect; allow the popup.
- *Was connected, now failing* → the session likely lost auth or the token expired. Reconnect via the same host path.
- *Wrong or empty account* → make sure you logged into the Dreem account that holds your credits (free tier = 100/month).

**1f. Not ready to connect? Start free anyway.** The audit needs none of the above. Offer it now: "While you sort the connection, give me your store URL and I'll audit your product imagery for free - no account, no credits, just a gap report." A user who sees their own gaps connects on their own.

## Step 2 - Show what is possible, with prompts they can steal

Present the menu as things to SAY, not features to read:

| Try saying | What happens | Credits |
|---|---|---|
| "Audit my store: mystore.com" | Scored gap report - missing on-model, single-image PDPs, no video. You pick the category to scan | Free |
| "Make product shots of this photo for Amazon" | Marketplace-ready stills - flat lay, mannequin, side, detail views | ~6-10 per image |
| "Put this dress on a model in her 40s" | Your garment on one of 400+ virtual talents - it asks how to style her and suggests the look | ~9-14 per shot |
| "Style this vest with a black jacket and white sneakers" | Complete-the-look on-model imagery - pair it with your own products or any piece you show it | ~9-14 per shot |
| "Make a 5-second video of this on-model shot" | Product video for PDP or social | 2 per second |
| "Full content kit for this product" | Shots + on-model + video, one plan, one approval | Priced per kit |
| "3 new products go live Thursday - get them launch-ready" | A launch set per product, planned backwards from the date - one approval for the whole drop | Priced per drop |
| "Make this shot work everywhere" | One finished shot recomposed for PDP, marketplace, Stories, feed, email - never cropped | ~6-11 per format |
| "Restyle the catalog for fall" | Existing on-model imagery rethemed for the season - same garments, new mood | ~9-14 per shot |
| "Show this dress on every body type" | Your current on-model look extended across sizes, ages, or genders - styling carried over | ~9-14 per shot |

Close with the two promises that make it safe to play:
- **Nothing ever generates without a cost preview and your explicit approval.**
- **The audit is always free** - it reads your public store, spends nothing.

## Step 3 - Route the first move

Recommend the audit as the natural entry ("most people start by pointing me at their store"), but follow whatever the user grabs. Hand off to the matching skill and get out of the way - this skill's job ends the moment a real task starts.

## What NOT to do

- No generation, no pickers, no cost previews here - that belongs to the task skills.
- Do not re-run the full welcome for a user who clearly knows the pack; answer the specific question and move on.
- Do not oversell: quality claims stay honest (strong on-model results, Product Shots improving - Dreem Studio has edit tools for fixes).
