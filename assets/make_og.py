#!/usr/bin/env python3
"""Generate the Tire Trader social share (Open Graph) image — 1200x630.
On-brand: charcoal #171a1f + acid-yellow #e5ff00, Helvetica wordmark, a designed
geometric tire-ring mark (no AI imagery). Deterministic, no network."""
from PIL import Image, ImageDraw, ImageFont
import math, os

W, H = 1200, 630
BRAND = (23, 26, 31)     # #171a1f
ACCENT = (229, 255, 0)   # #e5ff00
WHITE = (255, 255, 255)
MUTE = (159, 176, 204)   # #9fb0cc-ish cool grey
PANEL = (30, 34, 40)

HN = "/System/Library/Fonts/HelveticaNeue.ttc"
ARB = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
ART = "/System/Library/Fonts/Supplemental/Arial.ttf"

def font(path, size, idx=None):
    try:
        return ImageFont.truetype(path, size, index=idx) if idx is not None else ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

img = Image.new("RGB", (W, H), BRAND)
d = ImageDraw.Draw(img)

# subtle top-left brand gradient wash (kept low-contrast, not a glossy AI wash)
for y in range(H):
    t = y / H
    r = int(BRAND[0] + (18 - BRAND[0]) * 0)  # keep flat-ish; tiny vertical lift
    shade = int(6 * (1 - t))
    d.line([(0, y), (W, y)], fill=(BRAND[0] + shade, BRAND[1] + shade, BRAND[2] + shade))

# --- designed tire-ring mark, right side, asymmetric ---
cx, cy = 960, 300
outer, inner = 175, 96
d.ellipse([cx-outer, cy-outer, cx+outer, cy+outer], fill=(15, 17, 20))
# tread ticks around the outer band
ticks = 40
for i in range(ticks):
    a = (i / ticks) * 2 * math.pi
    r1, r2 = outer-6, outer-30
    x1, y1 = cx + r1*math.cos(a), cy + r1*math.sin(a)
    x2, y2 = cx + r2*math.cos(a), cy + r2*math.sin(a)
    d.line([(x1, y1), (x2, y2)], fill=ACCENT if i % 5 == 0 else (70, 76, 84), width=6)
# inner hub ring + accent stroke
d.ellipse([cx-inner, cy-inner, cx+inner, cy+inner], outline=ACCENT, width=8)
d.ellipse([cx-inner+22, cy-inner+22, cx+inner-22, cy+inner-22], outline=(70, 76, 84), width=4)
# TT monogram in hub
mono = font(ARB, 78)
mt = "TT"
bb = d.textbbox((0, 0), mt, font=mono)
d.text((cx-(bb[2]-bb[0])/2, cy-(bb[3]-bb[1])/2 - bb[1]), mt, font=mono, fill=WHITE)

# --- left text block ---
x = 84
# small eyebrow
eb = font(ARB, 26)
d.text((x, 150), "SOUTH FLORIDA", font=eb, fill=ACCENT)
# wordmark
wm = font(ARB, 96)
d.text((x, 190), "Tire Trader", font=wm, fill=WHITE)
# accent underline
d.rectangle([x, 300, x+150, 308], fill=ACCENT)
# tagline
tg = font(HN, 40)
d.text((x, 340), "Buy & sell tires locally —", font=tg, fill=WHITE)
d.text((x, 392), "no middleman markup.", font=tg, fill=WHITE)
# url
url = font(ARB, 30)
d.text((x, 470), "shoptiretrader.com", font=url, fill=MUTE)

out = os.path.join(os.path.dirname(__file__), "og-image.png")
img.save(out, "PNG")
print("wrote", out, img.size)
