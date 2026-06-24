# Kambeng Loading Spinners

Five lightweight, CSS-only loading states in your brand colors (`#16B7F0` / `#0B82BD` blue, `#F2A93B` gold accent). No video, no images, no JS dependencies — just CSS animations, so they're instant and infinitely scalable.

## Preview
Open `demo.html` directly in any browser (double-click it, no server or build step needed) to see all five live.

## What's included

| Component | File | Best for |
|---|---|---|
| `RingSpinner` | rotating gradient ring | Buttons, inline loading next to text |
| `DotsSpinner` | 3 bouncing dots | Chat-style "typing"/processing states |
| `MarkSpinner` | your K mark, pulsing with a soft glow | Full-page loading, splash states — most "on-brand" option |
| `BarLoader` | indeterminate sliding bar | Top-of-page route transitions (like the bar you see on Vercel/GitHub while a page loads) |
| `SkeletonLine` / `SkeletonCampaignCard` | shimmer placeholders | Campaign lists/cards while data is fetching — mirrors your actual card layout so nothing jumps when real content arrives |

## Using it in your Next.js app (kambeng.hexai.gm)

1. Copy `kambeng-spinners.css` into your project (e.g. `app/kambeng-spinners.css`), or paste its contents into your existing `globals.css`.
2. Copy `KambengSpinners.tsx` into your components folder.
3. If you put the CSS file somewhere other than next to the TSX file, update the `import "./kambeng-spinners.css"` path at the top of `KambengSpinners.tsx` (or remove that line entirely if you pasted the CSS into `globals.css`, since it'll already be loaded globally).
4. Import and use:

```tsx
import { RingSpinner, DotsSpinner, MarkSpinner, BarLoader, SkeletonCampaignCard } from "@/components/KambengSpinners";

// Inside a button while a donation is submitting:
<button disabled={isSubmitting}>
  {isSubmitting ? <RingSpinner size={18} /> : "Donate now"}
</button>

// At the top of the page during a route transition:
{isLoading && <BarLoader />}

// While campaign data is fetching:
{isLoading ? <SkeletonCampaignCard /> : <CampaignCard data={campaign} />}
```

## Customizing

- **Size**: `RingSpinner` takes a `size` (and `thickness`) prop. For the others, wrap in a container and use CSS `transform: scale()`, or adjust the fixed widths directly in the CSS (`.kb-dots > span`, `.kb-mark`).
- **Color**: every color is a literal hex value in `kambeng-spinners.css` (not a CSS variable) so it's easy to find-and-replace if the brand blue changes again — search for `#16B7F0` and `#0B82BD`.
- **Reduced motion**: included a `prefers-reduced-motion` rule that slows (rather than fully stops) the animations for users who've set that OS preference — full removal felt wrong for a "thing is actively loading" indicator, since people with that preference still need to know something is happening, just without the fast motion.

## Why CSS instead of the video loader from before

The earlier `kambeng-loader-loop.webm`/`.gif` is still useful for places that can't run CSS (e.g. an app-store preview video, or embedding in a non-web context). But for the actual website/app, CSS spinners load instantly, never buffer, scale to any size without pixelation, and are a fraction of the file size — better fit for production use inside kambeng.hexai.gm itself.
