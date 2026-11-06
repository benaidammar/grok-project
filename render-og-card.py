"""Instrument plate for public/og.jpg — exact type, exact palette. Staged PNG only."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
PAPER = (0xF3, 0xEF, 0xE6)
INK = (0x1A, 0x24, 0x20)
BRASS = (0x8D, 0x5A, 0x16)
CARD = (0xFB, 0xF8, 0xF2)

SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

out = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(out)

# Deep-ink spine, the product's sidebar, with a brass filament.
d.rectangle([0, 0, 16, H], fill=INK)
d.rectangle([16, 0, 19, H], fill=BRASS)

plate = (84, 50, 1116, 580)
d.rectangle(plate, fill=CARD)
d.rectangle(plate, outline=BRASS, width=2)


def corner(x, y, sx, sy, length=16):
    d.line([(x, y), (x + sx * length, y)], fill=INK, width=2)
    d.line([(x, y), (x, y + sy * length)], fill=INK, width=2)


# Registration ticks on the paper, clear of the frame edges.
corner(62, 32, 1, 1)
corner(1138, 32, -1, 1)
corner(62, 598, 1, -1)
corner(1138, 598, -1, -1)

CX = 608  # optical center of the paper field (spine occupies the left 19px)


def tracked(text, font, y, fill, tracking, center=CX):
    widths = [font.getlength(ch) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = center - total / 2
    for ch, w in zip(text, widths):
        d.text((x, y), ch, font=font, fill=fill, anchor="lt")
        x += w + tracking
    return total


def reticle(cx, cy):
    # Meridian: ink axis, brass ring. Same mark as the favicon.
    d.line([(cx, cy - 36), (cx, cy + 36)], fill=INK, width=3)
    d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], outline=BRASS, width=3)
    d.line([(cx - 30, cy), (cx - 20, cy)], fill=BRASS, width=3)
    d.line([(cx + 20, cy), (cx + 30, cy)], fill=BRASS, width=3)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=BRASS)


reticle(CX, 132)

title_font = ImageFont.truetype(SANS_BOLD, 104)
title_w = tracked("MERIDIAN", title_font, 176, INK, 22)
print("title_width", round(title_w, 1))

# Brass double rule under the wordmark — instrument scale, not a decoration bar.
rule_w = 196
d.line([(CX - rule_w / 2, 292), (CX + rule_w / 2, 292)], fill=BRASS, width=2)
d.line([(CX - rule_w / 2 + 28, 298), (CX + rule_w / 2 - 28, 298)], fill=BRASS, width=1)

v_font = ImageFont.truetype(SANS_BOLD, 28)
tracked("V19", v_font, 314, BRASS, 10)

tag_font = ImageFont.truetype(SANS, 18)
tracked("PRODUCTION TWIN", tag_font, 358, BRASS, 5)


def well(cx, base_y):
    """Geometric well symbol: stem off the flowline, ring for the wellhead."""
    d.line([(cx, base_y), (cx, base_y - 26)], fill=BRASS, width=2)
    r = 7
    top = base_y - 26 - r
    d.ellipse([cx - r, top - r, cx + r, top + r], outline=BRASS, width=2)


# Production network along the lower plate — facility, flowline, four wells.
flow_y = 516
left, right = CX - 250, CX + 250
d.line([(left, flow_y), (right, flow_y)], fill=BRASS, width=2)

# Facility pad
fw, fh = 22, 18
d.rectangle(
    [left - fw / 2, flow_y - fh / 2, left + fw / 2, flow_y + fh / 2],
    fill=CARD,
    outline=BRASS,
    width=2,
)

for i, t in enumerate((0.28, 0.5, 0.72, 1.0)):
    well(left + (right - left) * t, flow_y)

cap_font = ImageFont.truetype(SANS, 13)
tracked("FIELD  ·  WELLS  ·  FLOW", cap_font, 534, INK, 3)

out.save("/workspace/.grok/og-raw.png", "PNG")
print("saved", out.size)
