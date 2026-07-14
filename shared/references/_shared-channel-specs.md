# Channel Specs

Which aspect ratio, resolution, and format to generate per destination. Use these defaults when the user names a channel; ask only when the destination is genuinely unclear.

## The map

| Destination | Aspect ratio (enum) | Resolution | Format | Notes |
|---|---|---|---|---|
| PDP main image (fashion) | `Ratio3x4` or `Ratio4x5` | `TwoK` | jpeg | Portrait converts best for apparel |
| PDP gallery / detail | `Ratio3x4` | `TwoK` | jpeg | Keep the set consistent |
| Amazon / marketplace main | `Ratio1x1` | `TwoK` | jpeg | Clean light background, product fills most of frame |
| Google Shopping | `Ratio1x1` | `OneK`+ | jpeg | Clean background, no overlay text |
| Instagram feed | `Ratio1x1` or `Ratio4x5` | `OneK` | jpeg | 4:5 takes more screen |
| Stories / Reels / TikTok | `Ratio9x16` | `OneK` | jpeg | Full-bleed vertical |
| Pinterest | `Ratio2x3` | `OneK` | jpeg | Tall pins win |
| Email hero | `Ratio16x9` or `Ratio21x9` | `TwoK` | jpeg | Displays ~600px wide; ship 2x for retina |
| Website hero / banner | `Ratio16x9` or `Ratio21x9` | `FourK` | jpeg | Brand-grade tier |
| Print / campaign | `Ratio3x2` or brief-specific | `FourK` | png | 4K is the print tier |
| Video: PDP / site | `5s`, source still in `Ratio3x4` or `Ratio16x9` | - | - | Subtle motion reads premium |
| Video: TikTok / Reels / Stories | `10s`, source still in `Ratio9x16` | - | - | Vertical source, more movement |

## Resolution rule of thumb

- `OneK` - social feeds, tests, anything viewed small.
- `TwoK` - PDP and marketplace. The default.
- `FourK` - print, heroes, campaign. Costs more credits; only when the destination earns it.

## Channel pack defaults

When the user asks for "all formats" for one product, the standard kit is:

1. PDP: `Ratio3x4` `TwoK`
2. Marketplace: `Ratio1x1` `TwoK`
3. Story/Reels: `Ratio9x16` `OneK`
4. Feed: `Ratio4x5` `OneK`
5. Email hero: `Ratio16x9` `TwoK`

Five images per product. Confirm the list before generating; drop what the user does not sell through.

## Why generate instead of crop

A 9:16 crop of a 1:1 image amputates the scene. Generating at the target ratio composes the shot FOR that ratio - full figure in frame, headroom where the platform puts UI. That is the whole point of asking Dreem for the ratio instead of cropping after.
