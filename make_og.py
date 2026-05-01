#!/usr/bin/env python3
"""Generate og.png (1200x630) for LinkedIn / OG / Twitter previews. Factory brand-safe."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1200, 630
BLACK = (0, 0, 0)
SURFACE = (22, 20, 19)
BORDER = (52, 47, 45)
WHITE = (255, 255, 255)
GRAY = (155, 142, 135)
FOOTER = (148, 135, 129)
ORANGE = (238, 96, 24)
ORANGE_2 = (255, 139, 0)
ORANGE_3 = (243, 94, 0)

SF_MONO = "/System/Library/Fonts/SFNSMono.ttf"
SF = "/System/Library/Fonts/SFNS.ttf"

img = Image.new("RGB", (W, H), BLACK)
d = ImageDraw.Draw(img)

# Subtle radial orange glow top-right (drawn as faded ellipses)
glow = Image.new("RGB", (W, H), BLACK)
gd = ImageDraw.Draw(glow)
for r, a in [(900, 18), (700, 28), (500, 40), (300, 60)]:
    gd.ellipse(
        (W - r // 2 - 100, -r // 2 - 60, W - r // 2 - 100 + r, -r // 2 - 60 + r),
        fill=(min(238, a), min(96, a // 3), min(24, a // 8)),
    )
glow = glow.filter(ImageFilter.GaussianBlur(80))
img = Image.blend(img, glow, 0.6)
d = ImageDraw.Draw(img)

# Scanlines
sl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(sl)
for y in range(0, H, 4):
    sd.rectangle((0, y, W, y), fill=(255, 255, 255, 8))
img = Image.alpha_composite(img.convert("RGBA"), sl).convert("RGB")
d = ImageDraw.Draw(img)

# Top-left brand mark: rotor + FACTORY
def rotor(cx, cy, scale=1.0):
    r = int(8 * scale)
    arm_w = int(4 * scale)
    arm_l = int(18 * scale)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=ORANGE)
    # 4 arms
    d.rectangle((cx - arm_w // 2, cy - r - arm_l, cx + arm_w // 2, cy - r), fill=WHITE)
    d.rectangle((cx - arm_w // 2, cy + r, cx + arm_w // 2, cy + r + arm_l), fill=WHITE)
    d.rectangle((cx - r - arm_l, cy - arm_w // 2, cx - r, cy + arm_w // 2), fill=WHITE)
    d.rectangle((cx + r, cy - arm_w // 2, cx + r + arm_l, cy + arm_w // 2), fill=WHITE)

rotor(80, 80, scale=1.4)
brand_font = ImageFont.truetype(SF_MONO, 22)
d.text((125, 70), "FACTORY", font=brand_font, fill=WHITE)
small_font = ImageFont.truetype(SF_MONO, 14)
d.text((125, 100), "DROID DEFENCE  /  v1.0", font=small_font, fill=FOOTER)

# Top-right tag
tag_font = ImageFont.truetype(SF_MONO, 16)
tag_text = "PLAY  →"
tw = d.textlength(tag_text, font=tag_font)
pad_x, pad_y = 18, 10
tx = W - 80 - tw - pad_x * 2
ty = 64
d.rounded_rectangle(
    (tx, ty, tx + tw + pad_x * 2, ty + 36), radius=4, fill=ORANGE
)
d.text((tx + pad_x, ty + 10), tag_text, font=tag_font, fill=BLACK)

# Title — DROID DEFENCE (DEFENCE in orange)
title_font = ImageFont.truetype(SF_MONO, 132)
title1 = "DROID"
title2 = "DEFENCE"
y0 = 200
gap = 26
w1 = d.textlength(title1, font=title_font)
w2 = d.textlength(title2, font=title_font)
total = w1 + gap + w2
x0 = (W - total) // 2
d.text((x0, y0), title1, font=title_font, fill=WHITE)
d.text((x0 + w1 + gap, y0), title2, font=title_font, fill=ORANGE)

# Underline gradient bar
bar_y = y0 + 160
bar_h = 6
bar_w = 460
bar_x = (W - bar_w) // 2
grad = Image.new("RGB", (bar_w, bar_h), BLACK)
gp = grad.load()
stops = [(0, (255, 159, 43)), (0.5, (255, 139, 0)), (1.0, (243, 94, 0))]
for x in range(bar_w):
    t = x / (bar_w - 1)
    # interpolate between stops
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]
        t1, c1 = stops[i + 1]
        if t0 <= t <= t1:
            tt = (t - t0) / (t1 - t0)
            r = int(c0[0] + (c1[0] - c0[0]) * tt)
            g = int(c0[1] + (c1[1] - c0[1]) * tt)
            b = int(c0[2] + (c1[2] - c0[2]) * tt)
            for y in range(bar_h):
                gp[x, y] = (r, g, b)
            break
img.paste(grad, (bar_x, bar_y))
d = ImageDraw.Draw(img)

# Subtitle
sub_font = ImageFont.truetype(SF, 30)
sub = "Bring autonomy to the arcade."
sw = d.textlength(sub, font=sub_font)
d.text(((W - sw) // 2, bar_y + 28), sub, font=sub_font, fill=GRAY)

# Pixel-art bug row (3 unique tiers, repeated)
def draw_pixel_grid(grid, x, y, cell, color):
    for ry, row in enumerate(grid):
        for rx, ch in enumerate(row):
            if ch == "X":
                d.rectangle(
                    (x + rx * cell, y + ry * cell, x + rx * cell + cell - 1, y + ry * cell + cell - 1),
                    fill=color,
                )

bug1 = [
    "..X.....X..",
    "X..X...X..X",
    "X..XXXXX..X",
    "XXXX...XXXX",
    "XXXXXXXXXXX",
    ".XXXXXXXXX.",
    "..X.....X..",
    ".X.......X.",
]
bug2 = [
    ".X.....X.",
    "..X...X..",
    ".XXXXXXX.",
    "XX.XXX.XX",
    "XXXXXXXXX",
    "X.XXXXX.X",
    "X.X...X.X",
    "...XXX...",
]
bug3 = [
    "....XXXXX....",
    ".XXXXXXXXXXX.",
    "XXXXXXXXXXXXX",
    "XXX.XXXXX.XXX",
    "XXXXXXXXXXXXX",
    "..XXX...XXX..",
    ".XX.XX.XX.XX.",
    "XX.........XX",
]

ship = [
    ".....X.....",
    "....XXX....",
    "....XXX....",
    ".XXXXXXXXX.",
    "XXXXXXXXXXX",
    "XXXXXXXXXXX",
    "X.X.X.X.X.X",
]

# Bottom row of bugs
cell = 5
y_bugs = H - 130
spacing = 70

bugs_seq = [bug1, bug2, bug3, bug1, bug2, bug3, bug1]
total_w = 0
widths = []
for g in bugs_seq:
    w = len(g[0]) * cell
    widths.append(w)
    total_w += w
total_w += spacing * (len(bugs_seq) - 1)
x_cur = (W - total_w) // 2
for g, w in zip(bugs_seq, widths):
    draw_pixel_grid(g, x_cur, y_bugs, cell, WHITE)
    x_cur += w + spacing

# Player ship below the bugs, in orange
sw = len(ship[0]) * cell
draw_pixel_grid(ship, (W - sw) // 2, H - 60, cell, ORANGE)

# Bottom-left URL
url_font = ImageFont.truetype(SF_MONO, 16)
d.text((80, H - 50), "michaeldavies-factory.github.io/droid-defence", font=url_font, fill=FOOTER)

# Bottom-right meta
meta_font = ImageFont.truetype(SF_MONO, 14)
meta = "BUILT WITH FACTORY"
mw = d.textlength(meta, font=meta_font)
d.text((W - 80 - mw, H - 48), meta, font=meta_font, fill=FOOTER)

# Top divider line
d.rectangle((0, 130, W, 131), fill=BORDER)
# Bottom divider line
d.rectangle((0, H - 80, W, H - 79), fill=BORDER)

img.save("/Users/michaeldavies/factory-invaders/og.png", "PNG", optimize=True)
print("wrote og.png", img.size)
