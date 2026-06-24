// KambengSpinners.tsx
// Drop this file into your components folder (e.g. components/KambengSpinners.tsx)
// and import "./kambeng-spinners.css" once in your root layout, or paste the
// CSS into your existing globals.css.
//
// Usage:
//   import { RingSpinner, DotsSpinner, MarkSpinner, BarLoader, SkeletonLine, SkeletonCampaignCard } from "@/components/KambengSpinners";
//   <RingSpinner size={32} />
//   <BarLoader />            // good for top-of-page route-transition loading
//   <SkeletonCampaignCard /> // good for campaign list while data is fetching

import "./kambeng-spinners.css";

export function RingSpinner({ size = 40, thickness = 4 }: { size?: number; thickness?: number }) {
  return (
    <div
      className="kb-ring"
      style={{ "--kb-size": `${size}px`, "--kb-thickness": `${thickness}px` } as React.CSSProperties}
      role="status"
      aria-label="Loading"
    />
  );
}

export function DotsSpinner() {
  return (
    <div className="kb-dots" role="status" aria-label="Loading">
      <span />
      <span />
      <span />
    </div>
  );
}

export function MarkSpinner() {
  return (
    <div className="kb-mark" role="status" aria-label="Loading">
      <svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
        <g stroke="#FBF7F0" strokeWidth="26" strokeLinecap="round" strokeLinejoin="round" fill="none">
          <path d="M84,64 L84,176" />
          <path d="M84,122 L162,64" />
          <path d="M84,122 L162,176" />
        </g>
      </svg>
    </div>
  );
}

export function BarLoader({ trackColor }: { trackColor?: string }) {
  return (
    <div
      className="kb-bar-track"
      style={trackColor ? ({ "--kb-track-color": trackColor } as React.CSSProperties) : undefined}
      role="status"
      aria-label="Loading"
    >
      <div className="kb-bar-fill" />
    </div>
  );
}

export function SkeletonLine({ width = "100%" }: { width?: string | number }) {
  return <div className="kb-skeleton" style={{ width }} />;
}

// Mirrors the actual campaign card layout from the live site
// (image area, title, progress bar, two buttons) so the loading state
// doesn't jump/reflow once real content arrives.
export function SkeletonCampaignCard() {
  return (
    <div
      style={{
        background: "#121826",
        border: "1px solid #1E2636",
        borderRadius: 16,
        padding: 16,
        display: "flex",
        flexDirection: "column",
        gap: 12,
      }}
      role="status"
      aria-label="Loading campaign"
    >
      <div className="kb-skeleton" style={{ width: "100%", height: 160, borderRadius: 10 }} />
      <SkeletonLine width="70%" />
      <SkeletonLine width="40%" />
      <div className="kb-skeleton" style={{ width: "100%", height: 6, borderRadius: 3 }} />
      <div style={{ display: "flex", gap: 8, marginTop: 4 }}>
        <div className="kb-skeleton" style={{ flex: 1, height: 36, borderRadius: 8 }} />
        <div className="kb-skeleton" style={{ flex: 1, height: 36, borderRadius: 8 }} />
      </div>
    </div>
  );
}
