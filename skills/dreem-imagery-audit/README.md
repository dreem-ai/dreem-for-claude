# dreem-imagery-audit

Ask Claude to audit your product imagery. You get a scored gap report and a fix plan.

## What it finds

- Products with a single lonely image on the PDP
- Apparel with no on-model shot
- Sets with no back view or too few angles
- Which Dreem skill fixes each gap, and roughly what it costs vs a studio shoot

## What it needs

Any ONE of: your store URL, a Shopify product export CSV, or pasted product images. No store login. No Dreem credits - this skill is read-only.

## Try it

> "Audit the product imagery on ourstore.com - what's missing?"

> "Here's our product export. Which products need better images before Black Friday?"

## Output

`audit.csv` (one row per product, HIGH/MEDIUM/LOW) + `summary.md` (headline, top examples, prioritized fix plan).
