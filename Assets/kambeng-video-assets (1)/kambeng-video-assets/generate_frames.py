import cairosvg
import math
import os

TEAL_GRAD_1 = "#16B7F0"
TEAL_GRAD_2 = "#0B82BD"
GOLD = "#F2A93B"
CREAM = "#FBF7F0"
INK = "#0B82BD"
SAGE = "#4F7186"
LIGHT_SAGE = "#9FDBF5"

# Dark theme palette, sampled directly from the live kambeng.hexai.gm site
DARK_BG = "#0B0F1A"
DARK_BG_2 = "#10162400"  # unused placeholder
CARD_BG = "#121826"
ACCENT_BLUE = "#16B7F0"
ACCENT_BLUE_LIGHT = "#3DD0FF"
WHITE = "#F5F7FA"
MUTED_SLATE = "#8C9AB3"
SUCCESS_GREEN = "#1DBC86"

def ease_out_cubic(t):
    return 1 - pow(1 - t, 3)

def ease_out_back(t, overshoot=1.7):
    c1 = overshoot
    c3 = c1 + 1
    return 1 + c3 * pow(t - 1, 3) + c1 * pow(t - 1, 2)

def clamp01(x):
    return max(0.0, min(1.0, x))

def segment_progress(frame, start, end, easing=ease_out_cubic):
    if frame <= start:
        return 0.0
    if frame >= end:
        return 1.0
    t = (frame - start) / (end - start)
    return easing(clamp01(t))

def icon_svg(cx, cy, size, scale, opacity, dot_scale, dot_opacity, bg_fill="grad", k_color=CREAM):
    """Returns SVG <g> markup for the icon mark, centered at (cx, cy) with given box `size`."""
    half = size / 2.0
    s = scale
    # local coordinate system for the 240x240 source art, scaled to `size`
    factor = (size / 240.0) * s
    ox = cx - half * s
    oy = cy - half * s

    if bg_fill == "grad":
        bg = f'fill="url(#bggrad)"'
    elif bg_fill == "cream":
        bg = f'fill="{CREAM}"'
    else:
        bg = 'fill="none"'

    stroke_w = 24 * factor
    rx = 54 * factor

    def pt(x, y):
        return f"{ox + x*factor:.2f},{oy + y*factor:.2f}"

    g = f'<g opacity="{opacity:.3f}">'
    if bg_fill != "none":
        g += f'<rect x="{ox:.2f}" y="{oy:.2f}" width="{240*factor:.2f}" height="{240*factor:.2f}" rx="{rx:.2f}" {bg}/>'
    g += f'''<g stroke="{k_color}" stroke-width="{stroke_w:.2f}" stroke-linecap="round" stroke-linejoin="round" fill="none">
        <path d="M{pt(84,64)} L{pt(84,176)}"/>
        <path d="M{pt(84,122)} L{pt(162,64)}"/>
        <path d="M{pt(84,122)} L{pt(162,176)}"/>
    </g>'''
    # gold accent dot, independently scaled/faded
    dot_cx = ox + 192 * factor
    dot_cy = oy + 124 * factor
    dot_r = 14 * factor * dot_scale
    g += f'<circle cx="{dot_cx:.2f}" cy="{dot_cy:.2f}" r="{dot_r:.2f}" fill="{GOLD}" opacity="{dot_opacity:.3f}"/>'
    g += '</g>'
    return g

def defs_block():
    return f'''<defs>
        <linearGradient id="bggrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="{TEAL_GRAD_1}"/>
            <stop offset="100%" stop-color="{TEAL_GRAD_2}"/>
        </linearGradient>
    </defs>'''

def render_frame(svg_str, width, height, out_path):
    cairosvg.svg2png(bytestring=svg_str.encode("utf-8"), write_to=out_path,
                      output_width=width, output_height=height)

# ---------------------------------------------------------------------------
# ASSET 1: Square reveal, 1080x1080, cream background, for feed posts
# ---------------------------------------------------------------------------
def build_square_reveal(out_dir, total_frames=105):
    W = H = 1080
    icon_cx, icon_cy, icon_size = 540, 430, 280
    for f in range(total_frames):
        icon_p = segment_progress(f, 0, 22, ease_out_back)
        icon_op = segment_progress(f, 0, 10, ease_out_cubic)
        dot_p = segment_progress(f, 16, 34, ease_out_back)
        dot_op = segment_progress(f, 16, 26, ease_out_cubic)
        word_p = segment_progress(f, 32, 58, ease_out_cubic)
        word_op = segment_progress(f, 32, 52, ease_out_cubic)
        tag_op = segment_progress(f, 56, 76, ease_out_cubic)

        word_y_offset = (1 - word_p) * 40
        svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
            {defs_block()}
            <rect width="{W}" height="{H}" fill="{CREAM}"/>
            {icon_svg(icon_cx, icon_cy, icon_size, max(icon_p,0.001), icon_op, max(dot_p,0.001), dot_op)}
            <text x="{W/2}" y="{650 + word_y_offset:.1f}" font-family="Poppins" font-weight="600" font-size="100" fill="{INK}" text-anchor="middle" opacity="{word_op:.3f}">kambeng</text>
            <text x="{W/2}" y="{700:.1f}" font-family="Poppins" font-weight="500" font-size="28" letter-spacing="2" fill="{SAGE}" text-anchor="middle" opacity="{tag_op:.3f}">FUND WHAT MATTERS</text>
        </svg>'''
        render_frame(svg, W, H, os.path.join(out_dir, f"f{f:04d}.png"))
    return total_frames

# ---------------------------------------------------------------------------
# ASSET 2: Vertical reveal, 1080x1920, teal background, for Stories/Reels intro
# ---------------------------------------------------------------------------
def build_vertical_reveal(out_dir, total_frames=105):
    W, H = 1080, 1920
    icon_cx, icon_cy, icon_size = 540, 820, 300
    for f in range(total_frames):
        icon_p = segment_progress(f, 0, 22, ease_out_back)
        icon_op = segment_progress(f, 0, 10, ease_out_cubic)
        dot_p = segment_progress(f, 16, 34, ease_out_back)
        dot_op = segment_progress(f, 16, 26, ease_out_cubic)
        word_p = segment_progress(f, 32, 58, ease_out_cubic)
        word_op = segment_progress(f, 32, 52, ease_out_cubic)
        tag_op = segment_progress(f, 56, 76, ease_out_cubic)

        word_y_offset = (1 - word_p) * 40
        svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
            {defs_block()}
            <rect width="{W}" height="{H}" fill="{TEAL_GRAD_2}"/>
            <circle cx="120" cy="1750" r="260" fill="{CREAM}" opacity="0.04"/>
            <circle cx="960" cy="200" r="200" fill="{GOLD}" opacity="0.05"/>
            {icon_svg(icon_cx, icon_cy, icon_size, max(icon_p,0.001), icon_op, max(dot_p,0.001), dot_op, bg_fill="cream", k_color=TEAL_GRAD_2)}
            <text x="{W/2}" y="{1060 + word_y_offset:.1f}" font-family="Poppins" font-weight="600" font-size="100" fill="{CREAM}" text-anchor="middle" opacity="{word_op:.3f}">kambeng</text>
            <text x="{W/2}" y="{1110:.1f}" font-family="Poppins" font-weight="500" font-size="28" letter-spacing="2" fill="{LIGHT_SAGE}" text-anchor="middle" opacity="{tag_op:.3f}">FUND WHAT MATTERS</text>
        </svg>'''
        render_frame(svg, W, H, os.path.join(out_dir, f"f{f:04d}.png"))
    return total_frames

# ---------------------------------------------------------------------------
# ASSET 3: Transparent reveal (alpha channel), for overlay on video/web hero
# ---------------------------------------------------------------------------
def build_transparent_reveal(out_dir, total_frames=105):
    W = H = 1080
    icon_cx, icon_cy, icon_size = 540, 430, 280
    for f in range(total_frames):
        icon_p = segment_progress(f, 0, 22, ease_out_back)
        icon_op = segment_progress(f, 0, 10, ease_out_cubic)
        dot_p = segment_progress(f, 16, 34, ease_out_back)
        dot_op = segment_progress(f, 16, 26, ease_out_cubic)
        word_p = segment_progress(f, 32, 58, ease_out_cubic)
        word_op = segment_progress(f, 32, 52, ease_out_cubic)
        tag_op = segment_progress(f, 56, 76, ease_out_cubic)

        word_y_offset = (1 - word_p) * 40
        svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
            {defs_block()}
            {icon_svg(icon_cx, icon_cy, icon_size, max(icon_p,0.001), icon_op, max(dot_p,0.001), dot_op)}
            <text x="{W/2}" y="{650 + word_y_offset:.1f}" font-family="Poppins" font-weight="600" font-size="100" fill="{INK}" text-anchor="middle" opacity="{word_op:.3f}">kambeng</text>
            <text x="{W/2}" y="{700:.1f}" font-family="Poppins" font-weight="500" font-size="28" letter-spacing="2" fill="{SAGE}" text-anchor="middle" opacity="{tag_op:.3f}">FUND WHAT MATTERS</text>
        </svg>'''
        render_frame(svg, W, H, os.path.join(out_dir, f"f{f:04d}.png"))
    return total_frames

# ---------------------------------------------------------------------------
# ASSET 4: Looping icon pulse loader, transparent, 512x512, seamless loop
# ---------------------------------------------------------------------------
def build_loader_loop(out_dir, total_frames=45):
    W = H = 512
    icon_cx, icon_cy, icon_size = 256, 256, 280
    for f in range(total_frames):
        t = f / total_frames  # 0..<1, loops seamlessly since we never hit t=1
        pulse = 1.0 + 0.06 * math.sin(2 * math.pi * t)
        dot_glow = 0.75 + 0.25 * math.sin(2 * math.pi * t + math.pi/2)
        svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
            {defs_block()}
            {icon_svg(icon_cx, icon_cy, icon_size, pulse, 1.0, 1.0, dot_glow)}
        </svg>'''
        render_frame(svg, W, H, os.path.join(out_dir, f"f{f:04d}.png"))
    return total_frames

def glow_blob(cx, cy, r, color, opacity=0.5):
    """Radial-gradient glow blob (cairosvg doesn't support feGaussianBlur, so we fake glow with gradients)."""
    gid = f"glow{int(cx)}{int(cy)}{int(r)}"
    return f'''<defs><radialGradient id="{gid}" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="{color}" stop-opacity="{opacity}"/>
        <stop offset="55%" stop-color="{color}" stop-opacity="{opacity*0.35:.3f}"/>
        <stop offset="100%" stop-color="{color}" stop-opacity="0"/>
    </radialGradient></defs>
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{gid})"/>'''

# ---------------------------------------------------------------------------
# ASSET 5: Dark-theme square reveal, 1080x1080 — matches the live site's
# dark navy background + glowing cyan accent treatment
# ---------------------------------------------------------------------------
def build_dark_square_reveal(out_dir, total_frames=105):
    W = H = 1080
    icon_cx, icon_cy, icon_size = 540, 430, 280
    for f in range(total_frames):
        icon_p = segment_progress(f, 0, 22, ease_out_back)
        icon_op = segment_progress(f, 0, 10, ease_out_cubic)
        dot_p = segment_progress(f, 16, 34, ease_out_back)
        dot_op = segment_progress(f, 16, 26, ease_out_cubic)
        word_p = segment_progress(f, 32, 58, ease_out_cubic)
        word_op = segment_progress(f, 32, 52, ease_out_cubic)
        tag_op = segment_progress(f, 56, 76, ease_out_cubic)
        glow_op = segment_progress(f, 0, 40, ease_out_cubic) * 0.6

        word_y_offset = (1 - word_p) * 40
        svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
            {defs_block()}
            <rect width="{W}" height="{H}" fill="{DARK_BG}"/>
            {glow_blob(icon_cx, icon_cy, 420, ACCENT_BLUE, glow_op)}
            <circle cx="{W-80}" cy="{H-80}" r="220" fill="{ACCENT_BLUE}" opacity="0.035"/>
            {icon_svg(icon_cx, icon_cy, icon_size, max(icon_p,0.001), icon_op, max(dot_p,0.001), dot_op)}
            <text x="{W/2}" y="{650 + word_y_offset:.1f}" font-family="Poppins" font-weight="600" font-size="100" fill="{WHITE}" text-anchor="middle" opacity="{word_op:.3f}">kambeng</text>
            <text x="{W/2}" y="{700:.1f}" font-family="Poppins" font-weight="500" font-size="28" letter-spacing="2" fill="{MUTED_SLATE}" text-anchor="middle" opacity="{tag_op:.3f}">FUND WHAT MATTERS</text>
        </svg>'''
        render_frame(svg, W, H, os.path.join(out_dir, f"f{f:04d}.png"))
    return total_frames

# ---------------------------------------------------------------------------
# ASSET 6: Dark-theme vertical reveal, 1080x1920 — Stories/Reels, includes
# the "Fund What Matters in The Gambia" glow treatment from the live hero
# ---------------------------------------------------------------------------
def build_dark_vertical_reveal(out_dir, total_frames=135):
    W, H = 1080, 1920
    icon_cx, icon_cy, icon_size = 540, 620, 260
    for f in range(total_frames):
        icon_p = segment_progress(f, 0, 22, ease_out_back)
        icon_op = segment_progress(f, 0, 10, ease_out_cubic)
        dot_p = segment_progress(f, 16, 34, ease_out_back)
        dot_op = segment_progress(f, 16, 26, ease_out_cubic)
        word_p = segment_progress(f, 32, 58, ease_out_cubic)
        word_op = segment_progress(f, 32, 52, ease_out_cubic)

        line1_op = segment_progress(f, 50, 70, ease_out_cubic)
        line2_op = segment_progress(f, 62, 82, ease_out_cubic)
        line3_op = segment_progress(f, 74, 96, ease_out_cubic)
        glow_op = segment_progress(f, 74, 110, ease_out_cubic) * 0.55
        cta_op = segment_progress(f, 100, 120, ease_out_cubic)

        word_y_offset = (1 - word_p) * 40
        svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
            {defs_block()}
            <rect width="{W}" height="{H}" fill="{DARK_BG}"/>
            {glow_blob(icon_cx, icon_cy, 380, ACCENT_BLUE, 0.4)}
            {glow_blob(540, 1230, 320, ACCENT_BLUE, glow_op)}
            {icon_svg(icon_cx, icon_cy, icon_size, max(icon_p,0.001), icon_op, max(dot_p,0.001), dot_op)}
            <text x="{W/2}" y="{800 + word_y_offset:.1f}" font-family="Poppins" font-weight="600" font-size="92" fill="{WHITE}" text-anchor="middle" opacity="{word_op:.3f}">kambeng</text>

            <text x="{W/2}" y="1110" font-family="Poppins" font-weight="700" font-size="74" fill="{WHITE}" text-anchor="middle" opacity="{line1_op:.3f}">Fund What</text>
            <text x="{W/2}" y="1195" font-family="Poppins" font-weight="700" font-size="74" fill="{WHITE}" text-anchor="middle" opacity="{line2_op:.3f}">Matters in</text>
            <text x="{W/2}" y="1290" font-family="Poppins" font-weight="700" font-size="80" fill="{ACCENT_BLUE_LIGHT}" text-anchor="middle" opacity="{line3_op:.3f}">The Gambia</text>

            <text x="{W/2}" y="1420" font-family="Poppins" font-weight="500" font-size="30" letter-spacing="1" fill="{MUTED_SLATE}" text-anchor="middle" opacity="{cta_op:.3f}">Wave · APS Mobile Money · Card</text>
        </svg>'''
        render_frame(svg, W, H, os.path.join(out_dir, f"f{f:04d}.png"))
    return total_frames

# ---------------------------------------------------------------------------
# ASSET 7: Platform stats counter, 1080x1080 — animated count-up matching
# the live dashboard's "Platform Stats" numbers
# ---------------------------------------------------------------------------
def build_stats_counter(out_dir, total_frames=150, total_raised=744.8, live_campaigns=6, donations=8):
    W = H = 1080
    count_start, count_end = 15, 85

    for f in range(total_frames):
        p = segment_progress(f, count_start, count_end, ease_out_cubic)
        raised_val = total_raised * p
        camp_val = int(round(live_campaigns * p))
        don_val = int(round(donations * p))

        logo_op = segment_progress(f, 0, 14, ease_out_cubic)
        label_op = segment_progress(f, 10, 26, ease_out_cubic)
        cards_op = segment_progress(f, 14, 30, ease_out_cubic)
        cta_op = segment_progress(f, 92, 112, ease_out_cubic)
        glow_op = 0.45

        card_y = 560
        card_w, gap = 300, 36
        total_w = card_w * 3 + gap * 2
        start_x = (W - total_w) / 2

        def stat_card(idx, value_str, label):
            x = start_x + idx * (card_w + gap)
            return f'''<g opacity="{cards_op:.3f}">
                <rect x="{x}" y="{card_y}" width="{card_w}" height="220" rx="20" fill="{CARD_BG}" stroke="#1E2636" stroke-width="2"/>
                <text x="{x+card_w/2}" y="{card_y+110}" font-family="Poppins" font-weight="700" font-size="54" fill="{ACCENT_BLUE_LIGHT}" text-anchor="middle">{value_str}</text>
                <text x="{x+card_w/2}" y="{card_y+160}" font-family="Poppins" font-weight="500" font-size="22" letter-spacing="1" fill="{MUTED_SLATE}" text-anchor="middle">{label}</text>
            </g>'''

        svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
            {defs_block()}
            <rect width="{W}" height="{H}" fill="{DARK_BG}"/>
            {glow_blob(W/2, H/2, 500, ACCENT_BLUE, glow_op)}

            <g opacity="{logo_op:.3f}">
                {icon_svg(W/2-150, 165, 90, 1.0, 1.0, 1.0, 1.0)}
                <text x="{W/2-85}" y="195" font-family="Poppins" font-weight="600" font-size="48" fill="{WHITE}">kambeng</text>
            </g>

            <text x="{W/2}" y="380" font-family="Poppins" font-weight="600" font-size="40" fill="{WHITE}" text-anchor="middle" opacity="{label_op:.3f}">Real Impact, In Real Time</text>

            {stat_card(0, f"{raised_val:,.1f}", "GMD TOTAL RAISED")}
            {stat_card(1, f"{camp_val}", "LIVE CAMPAIGNS")}
            {stat_card(2, f"{don_val}", "DONATIONS")}

            <text x="{W/2}" y="{H-110}" font-family="Poppins" font-weight="500" font-size="30" letter-spacing="1" fill="{MUTED_SLATE}" text-anchor="middle" opacity="{cta_op:.3f}">kambeng.hexai.gm</text>
        </svg>'''
        render_frame(svg, W, H, os.path.join(out_dir, f"f{f:04d}.png"))
    return total_frames

if __name__ == "__main__":
    base = "/home/claude/kambeng-video"
    n1 = build_square_reveal(f"{base}/frames_square")
    print("square frames:", n1)
    n2 = build_vertical_reveal(f"{base}/frames_vertical")
    print("vertical frames:", n2)
    n3 = build_transparent_reveal(f"{base}/frames_transparent")
    print("transparent frames:", n3)
    n4 = build_loader_loop(f"{base}/frames_loader")
    print("loader frames:", n4)
