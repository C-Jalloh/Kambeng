# Kambeng — Animated Logo Assets

A note before you dive in: you asked for **Remotion** specifically. Remotion renders through a headless Chrome browser, and this sandbox's network is locked to a short allow-list of package registries (npm, pip, GitHub) — it can't reach the servers that ship Chrome/Chromium binaries, so Remotion can't actually launch here. Instead, I built the same kind of frame-by-frame animation pipeline by hand (vector frames via the same SVG renderer used for the static logos, assembled into video with ffmpeg) — same end result, no browser dependency. If you run Remotion yourself locally or in CI with full network access, the `generate_frames.py` script in this folder is a useful reference for the easing/timing logic to port into a `<Composition>`.

## What's included

| File | Size | Use case |
|---|---|---|
| `kambeng-logo-reveal-square.mp4` | 1080×1080, 4.5s | Instagram/Facebook feed post, general intro clip |
| `kambeng-logo-reveal-vertical.mp4` | 1080×1920, 4.5s | Instagram/TikTok Stories & Reels intro |
| `kambeng-logo-reveal-transparent.webm` | 1080×1080, 4.5s, **alpha channel** | Overlay on top of existing video/website hero footage |
| `kambeng-loader-loop.webm` | 512×512, 1.5s loop, **alpha channel** | In-app loading spinner / splash screen |
| `kambeng-logo-reveal.gif` | 480×480, 4.5s | Email signatures, README files, anywhere video isn't supported |
| `kambeng-loader-loop.gif` | 256×256, 1.5s loop | Same as above, for the loader |

## Animation

Icon scales in with a slight overshoot ("pop"), the gold accent dot pops in just after, then the wordmark slides up and fades in, followed by the tagline. Total reveal takes about 1.7s, then holds for the rest of the clip so it reads comfortably as a video opener.

## Using the transparent WebM

The `-transparent.webm` and loader `.webm` files use VP9 with a real alpha channel (`alpha_mode=1` in the container). They'll show correctly:
- In Chrome, Firefox, Edge — as an HTML5 `<video>` element directly in a webpage
- In editing software that supports VP9 alpha (Premiere Pro, DaVinci Resolve, After Effects via plugin)

They will **not** show transparency in QuickTime or some default OS video previewers — that's a player limitation, not a problem with the file. If you need ProRes 4444 or another alpha-friendly codec for a specific NLE, let me know and I can re-encode.

## Re-generating or tweaking

`generate_frames.py` (included) regenerates every frame sequence from scratch — it's plain Python + cairosvg, no external services. To adjust timing, edit the frame numbers in the `segment_progress(...)` calls (e.g. `segment_progress(f, 32, 58, ease_out_cubic)` means "this property animates between frame 32 and frame 58"). To re-encode after changing frames, the ffmpeg commands are in the conversation history — happy to drop them into a shell script if you want to rebuild this regularly (e.g. every time you tweak brand colors).
