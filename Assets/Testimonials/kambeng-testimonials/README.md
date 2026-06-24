# Kambeng Testimonials Section

## ⚠️ Before you publish this

Every quote in `testimonials-data.ts` is a placeholder I wrote to match your platform's actual features (Wave/card payments, KYC verification, proof-of-expenditure) — none of these are real people or real quotes. They're there so the design reads naturally and you can show stakeholders what the finished section will feel like.

**Replace them with real quotes before this goes live.** Publishing fabricated testimonials attributed to named people is a credibility risk the moment anyone — a journalist, a competitor, a skeptical donor — asks who these people are. It also opens you up to a real ethical/legal problem if invented quotes get treated as fraud or misrepresentation in donor communications.

### Fast way to get real ones
After a campaign closes or hits a milestone, send a one-question WhatsApp/SMS follow-up:
- To the campaigner: *"What made donors trust your campaign?"*
- To 2-3 of their bigger donors: *"What almost stopped you from giving, and what changed your mind?"*

Answers to "what almost stopped you" tend to make better landing-page copy than generic praise, because they surface the actual objection your other visitors are silently having.

## What's included

| File | Purpose |
|---|---|
| `testimonials-data.ts` | The content — array of quote/name/role/location/rating. **Edit this file only** when you get real quotes; the component doesn't need to change. |
| `TestimonialsSection.tsx` | The React component that renders the grid |
| `kambeng-testimonials.css` | Styling, matches your live site's dark theme exactly |
| `demo.html` | Open directly in a browser to preview, no build step |

## Using it in your Next.js app

1. Copy all four files into your project (e.g. `components/testimonials/`).
2. Import the section wherever you want it on the page:

```tsx
import { TestimonialsSection } from "@/components/testimonials/TestimonialsSection";

// uses the placeholder data automatically
<TestimonialsSection />

// or pass real data once you have it
<TestimonialsSection testimonials={myRealTestimonials} />
```

3. Once you have real quotes, just edit the array in `testimonials-data.ts` — add, remove, or reorder entries freely. The grid re-flows automatically (3 per row on desktop, fewer on smaller screens).

## Design notes

- Avatar circles use initials instead of photos, alternating between your two brand blues — easy to swap for real profile photos later if you start collecting them (just add a `photoUrl` field to the data type and conditionally render an `<img>` instead of the initials div).
- The badge ("Verified donor" / "KYC verified") reinforces your trust positioning right inside the testimonial, not just on cards elsewhere on the page.
- Star ratings are included since you already have a donor review feature — if you wire this up to real reviews later, the rating can come straight from your reviews data instead of being hardcoded per testimonial.
