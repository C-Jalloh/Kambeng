// TestimonialsSection.tsx
// Drop into your components folder. Pulls from testimonials-data.ts —
// replace that file's contents with real quotes when you have them;
// this component doesn't need to change.

import "./kambeng-testimonials.css";
import { placeholderTestimonials, type Testimonial } from "./testimonials-data";

const AVATAR_COLORS = ["#16B7F0", "#0B82BD"];

function initials(name: string) {
  return name
    .split(" ")
    .map((p) => p[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();
}

function Stars({ rating }: { rating: number }) {
  return (
    <div className="kb-testimonial-card__stars" aria-label={`${rating} out of 5 stars`}>
      {"★".repeat(rating)}
      {"☆".repeat(5 - rating)}
    </div>
  );
}

function TestimonialCard({ t, index }: { t: Testimonial; index: number }) {
  return (
    <div className="kb-testimonial-card">
      <Stars rating={t.rating} />
      <p className="kb-testimonial-card__quote">&ldquo;{t.quote}&rdquo;</p>
      <div className="kb-testimonial-card__footer">
        <div
          className="kb-testimonial-card__avatar"
          style={{ background: AVATAR_COLORS[index % AVATAR_COLORS.length] }}
        >
          {initials(t.name)}
        </div>
        <div>
          <div className="kb-testimonial-card__name">{t.name}</div>
          <div className="kb-testimonial-card__meta">
            {t.role === "donor" ? "Donor" : "Campaign organizer"} · {t.location}
          </div>
        </div>
        <span className="kb-testimonial-card__badge">
          {t.role === "donor" ? "Verified donor" : "KYC verified"}
        </span>
      </div>
    </div>
  );
}

export function TestimonialsSection({
  testimonials = placeholderTestimonials,
}: {
  testimonials?: Testimonial[];
}) {
  return (
    <section className="kb-testimonials">
      <div className="kb-testimonials__header">
        <div className="kb-testimonials__eyebrow">What people are saying</div>
        <h2 className="kb-testimonials__title">Real causes. Real Gambians.</h2>
      </div>
      <div className="kb-testimonials__grid">
        {testimonials.map((t, i) => (
          <TestimonialCard key={t.id} t={t} index={i} />
        ))}
      </div>
    </section>
  );
}
