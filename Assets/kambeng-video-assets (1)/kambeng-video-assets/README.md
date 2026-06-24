# Kambeng — Animated Logo Assets

A note before you dive in: you asked for **Remotion** specifically. Remotion renders through a headless Chrome browser, and this sandbox's network is locked to a short allow-list of package registries (npm, pip, GitHub) — it can't reach the servers that ship Chrome/Chromium binaries, so Remotion can't actually launch here. Instead, I built the same kind of frame-by-frame animation pipeline by hand (vector frames via the same SVG renderer used for the static logos, assembled into video with ffmpeg) — same end result, no browser dependency. If you run Remotion yourself locally or in CI with full network access, the `generate_frames.py` script in this folder is a useful reference for the easing/timing logic to port into a `<Composition>`.

## What's included

### Light / cream versions (general marketing use)
| File | Size | Use case |
|---|---|---|
| `kambeng-logo-reveal-square.mp4` | 1080×1080, 4.5s | Feed post on light backgrounds |
| `kambeng-logo-reveal-vertical.mp4` | 1080×1920, 4.5s | Stories/Reels on light backgrounds |
| `kambeng-logo-reveal-transparent.webm` | 1080×1080, alpha | Overlay on any footage |
| `kambeng-logo-reveal.gif` | 480×480 | Fallback for non-video contexts |

### Dark theme versions (matches the live kambeng.hexai.gm site exactly)
Colors sampled directly from the live site: dark navy background (`#0B0F1A`), card surfaces (`#121826`), the same bright cyan-blue accent (`#16B7F0`), and the glowing text treatment used on "The Gambia" in the hero.

| File | Spec | Use case |
|---|---|---|
| `kambeng-logo-reveal-dark-square.mp4` | 1080×1080, 4.5s | Feed post / video intro matching the live app's look |
| `kambeng-logo-reveal-dark-vertical.mp4` | 1080×1920, 5.5s | Stories/Reels intro, recreates the actual hero headline with the glowing "The Gambia" treatment |
| `kambeng-logo-reveal-dark.gif` | 480×480 | Fallback version of the dark square reveal |
| `kambeng-stats-counter.mp4` | 1080×1080, 6s | Animated count-up of live platform stats (Total Raised / Live Campaigns / Donations) — great for a "look what we've built" social post. **Numbers are hardcoded from the screenshot you shared (744.8 GMD / 6 / 8) — update the `total_raised`, `live_campaigns`, `donations` args in `build_stats_counter()` before reposting, since these will be stale by the time you publish.**

### Loader (in-app use)
| File | Spec | Use case |
|---|---|---|
| `kambeng-loader-loop.webm` | 512×512, 1.5s loop, alpha | In-app loading spinner |
| `kambeng-loader-loop.gif` | 256×256 | Fallback loader

## Animation

Icon scales in with a slight overshoot ("pop"), the gold accent dot pops in just after, then the wordmark slides up and fades in, followed by the tagline. Total reveal takes about 1.7s, then holds for the rest of the clip so it reads comfortably as a video opener.

## Using the transparent WebM

The `-transparent.webm` and loader `.webm` files use VP9 with a real alpha channel (`alpha_mode=1` in the container). They'll show correctly:
- In Chrome, Firefox, Edge — as an HTML5 `<video>` element directly in a webpage
- In editing software that supports VP9 alpha (Premiere Pro, DaVinci Resolve, After Effects via plugin)

They will **not** show transparency in QuickTime or some default OS video previewers — that's a player limitation, not a problem with the file. If you need ProRes 4444 or another alpha-friendly codec for a specific NLE, let me know and I can re-encode.

## Re-generating or tweaking

`generate_frames.py` (included) regenerates every frame sequence from scratch — it's plain Python + cairosvg, no external services. To adjust timing, edit the frame numbers in the `segment_progress(...)` calls (e.g. `segment_progress(f, 32, 58, ease_out_cubic)` means "this property animates between frame 32 and frame 58"). To re-encode after changing frames, the ffmpeg commands are in the conversation history — happy to drop them into a shell script if you want to rebuild this regularly (e.g. every time you tweak brand colors).
