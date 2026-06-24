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
