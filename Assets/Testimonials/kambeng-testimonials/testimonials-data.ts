// testimonials-data.ts
//
// ⚠️ PLACEHOLDER CONTENT — these are illustrative, not real user quotes.
// Replace every entry with an actual donor/campaigner quote before this
// goes live. Shipping fabricated testimonials as genuine user feedback
// is a trust risk the moment anyone asks "who is this?" — swap these out
// as soon as you have 3-6 real ones, even if the design stays the same.
//
// Suggested way to collect real ones fast: after a campaign closes or
// hits a milestone, send a one-question WhatsApp/SMS follow-up to the
// campaigner and to 2-3 of their larger donors: "What made you trust
// this campaign / what almost stopped you from giving?" Real answers to
// that question tend to be better testimonial material than "how was
// your experience" because they surface the actual objection you need
// to overcome on the landing page.

export type Testimonial = {
  id: string;
  quote: string;
  name: string;
  role: "donor" | "campaigner";
  location: string;
  rating: number; // 1-5
};

export const placeholderTestimonials: Testimonial[] = [
  {
    id: "t1",
    quote:
      "I sent money through Wave in under a minute, and I could actually see photos of the borehole being built. That's the part that got me — most fundraisers, you never know what happened with your money.",
    name: "Aisha N.",
    role: "donor",
    location: "Serrekunda",
    rating: 5,
  },
  {
    id: "t2",
    quote:
      "My brother is in the UK and wanted to support a campaign here but didn't have Wave. He used his card and it just worked. Donating felt as easy as it should be.",
    name: "Lamin J.",
    role: "donor",
    location: "Bakau",
    rating: 5,
  },
  {
    id: "t3",
    quote:
      "What convinced me to donate was seeing the campaigner was KYC verified. In a small country like ours, that reassurance matters more than people think.",
    name: "Fatoumatta C.",
    role: "donor",
    location: "Banjul",
    rating: 5,
  },
  {
    id: "t4",
    quote:
      "We raised more for the school's library in three weeks on Kambeng than we did in three months asking around. Posting receipts each week kept donors coming back.",
    name: "Modou S.",
    role: "campaigner",
    location: "Brikama",
    rating: 5,
  },
  {
    id: "t5",
    quote:
      "I was nervous putting my ID up for verification, but it's what made donors trust the campaign. We hit our goal for the borehole faster than I expected.",
    name: "Sarjo B.",
    role: "campaigner",
    location: "Farafenni",
    rating: 4,
  },
  {
    id: "t6",
    quote:
      "Being able to show exactly what we spent — cement, labor, transport — meant nobody asked 'where did the money go?' It was all right there.",
    name: "Ndey F.",
    role: "campaigner",
    location: "Gunjur",
    rating: 5,
  },
];
