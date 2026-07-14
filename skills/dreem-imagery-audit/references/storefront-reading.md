# Reading a Storefront Without Credentials

Three ways to get a catalog, no admin access required. Be a polite guest: these are public endpoints - fetch what the scope needs, never hammer.

> **Shopify only.** These endpoints work because the store runs Shopify. If `/products.json` returns an HTML page instead of JSON, the store is NOT Shopify - do not reverse-engineer its private platform API, scrape rendered pages, or guess REST/GraphQL routes. Return to SKILL.md Step 1's *Not a Shopify store* path (redirect the user to an image upload, or a CSV export).

## 1. Shopify `/products.json` (fastest)

Every Shopify store exposes its published catalog at:

```
https://{store-domain}/products.json?limit=250&page=1
```

- Paginate by incrementing `page` until the `products` array comes back empty.
- Useful fields per product: `handle`, `title`, `product_type`, `tags`, `images[]` (each with `src`, `position`), `variants[]` (each with `available` - the per-variant stock flag; a product is in stock when ANY variant has `available: true`).
- Some stores disable this endpoint. A 404/401/empty response means fall back to option 2 or 3 - do not retry repeatedly.
- **Do not guess the catalog size by bisecting page numbers** - fetch `meta.json` instead (see 1c) for the exact count in one call.
- **Ordering is not chronological.** This endpoint's default order is close to product-ID order, not `created_at` - a page near the start can mix a brand-new item next to a year-old one, and later pages are not reliably "older." If the scope needs true newest-N, there is no shortcut: paginate the full catalog and sort by `created_at` client-side (see SKILL.md Step 0's newest-arrivals cost note).

`Image src` URLs are Shopify CDN (`cdn.shopify.com`), public HTTPS, jpg/png/webp - they can be passed straight into Dreem `generate_*` calls later as `images[].url`.

## 1b. Discovering the store's structure (for the scoping menu)

Two no-auth ways to build the category list the user picks from:

- **Collections:** `https://{store-domain}/collections.json?limit=250` returns the store's collections (handle, title). Products per collection: `https://{store-domain}/collections/{handle}/products.json?limit=250` (paginate the same way). Best when the store curates collections.
- **Product types and tags:** already in the `/products.json` payload - group by `product_type` (fall back to `tags` if types are empty) and count. Always available, one pass over data you already fetched.

Present whichever is cleaner as a short menu with counts ("Kids (214), Running (167), ..."). If both are messy, offer newest-N and full-catalog only.

## 1c. Detecting the store's market (for regional talent casting)

The store tells you its country and currency without a login - read it, because it drives which talents fit (a Danish store wants Scandinavian faces first).

- **`https://{store}/meta.json`** - returns `country` (ISO, e.g. `DK`), `currency` (e.g. `EUR`), and the shop `name` (often carries the region, e.g. "Nordic Outfitters EU"). Fastest, most authoritative. It also returns `published_products_count` and `published_collections_count` - read these FIRST, before any pagination, so you know the catalog size and can decide the Step 0 scoping question with one fetch instead of paging through `/products.json` to find where it ends.
- **Currency fallback:** `https://{store}/cart.json` exposes `currency` if meta.json is blocked.
- **Language fallback:** the `product_type`/`tags` language in `/products.json` (Danish: "Jakker", "Skjorter", "Bukser") and the domain TLD (`.dk`, `.se`, `.no`) both signal the market.

Record the detected market (country + region) and pass it to any downstream casting step. Map country to talent region: DK/SE/NO/FI/IS -> Scandinavian; then widen from there. The bias sets the FIRST suggestion, never a hard filter.

## 2. Shopify Storefront MCP

Every Shopify store also hosts a public MCP endpoint:

```
https://{store}.myshopify.com/api/mcp
```

If the user has added it as a connector, use its catalog tools (`search_shop_catalog`, product lookup) instead of raw HTTP. Same data, structured access.

## 3. Product export CSV

Shopify Admin -> Products -> Export -> CSV. Format gotchas:

- One row per image: group by `Handle`. The first row per handle carries `Title`, `Body (HTML)`, `Type`, `Tags`, `Status`.
- Rows with a blank `Image Src` are variant rows - skip for imagery purposes.
- `Image Position` orders the gallery; position 1 is the PDP hero.

Other platforms (BigCommerce, WooCommerce) export similar shapes - identify the handle/title/image-URL columns and proceed the same way.

## Vision classification tips

- Inspect the FULL gallery per product - every image, in position order. Fetch small renders (append `?width=512` to Shopify CDN URLs, or `&width=512` when the URL already has query params) to keep it fast; classification does not need full resolution.
- Dedupe by raw `src` (before you add the width param) across the whole scope before classifying - reused hero shots across variants or bundle products should only be vision-classified once. See SKILL.md Step 2.
- On-model counts wherever the person is - studio or a real environment.
- Ghost-mannequin (3D garment shape, no person) is NOT on-model. It is the classic "needs a model" candidate.
- If an image will not load or is ambiguous, mark `unknown`. An honest unknown beats a confident guess - the user will read this report next to their own store.
- Judge the hero (position 1) hardest: a flat-lay hero on apparel is a conversion leak even when on-model shots exist deeper in the gallery. Note it.
