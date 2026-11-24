# Single 1080x1350 image post, adapted from make_carousel.py
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
CREAM = (246, 241, 233); NAVY = (31, 47, 74); GOLD = (176, 141, 87); TAUPE = (120, 110, 98)
SERIF = "/usr/share/fonts/truetype/google-fonts/ofl/crimsontext/CrimsonText-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/google-fonts/ofl/crimsontext/CrimsonText-Italic.ttf"
SANS = "/usr/share/fonts/truetype/google-fonts/ofl/dmsans/DMSans[opsz,wght].ttf"
font = lambda p, s: ImageFont.truetype(p, s)

def center(d, text, f, y, color):
    d.text(((W - d.textlength(text, font=f)) / 2, y), text, font=f, fill=color)

def wrap(d, text, f, maxw):
    lines, line = [], ""
    for w in text.split():
        t = (line + " " + w).strip()
        if d.textlength(t, font=f) <= maxw: line = t
        else: lines.append(line); line = w
    if line: lines.append(line)
    return lines

img = Image.new("RGB", (W, H), NAVY); d = ImageDraw.Draw(img)
d.rectangle([40, 40, W - 40, H - 40], outline=GOLD, width=2)
center(d, "DESIGNER SECRETS", font(SANS, 28), 130, GOLD)
fh = font(SERIF, 96)
y = 180
for ln in ["Designers do lights", "in this order"]:
    center(d, ln, fh, y, CREAM); y += 104
d.line([(W/2 - 60, y + 30), (W/2 + 60, y + 30)], fill=GOLD, width=2)
y += 75

steps = [
    ("Test on the floor first", "Check every strand before it goes on the tree."),
    ("Start at the bottom", "Begin near the outlet and work up."),
    ("Work in vertical sections", "Like slices of a pie, not a spiral."),
    ("Trunk to tip and back", "Weave each branch out and in again."),
    ("Step back and squint", "Any dark patch gets one more strand."),
]
fn, ft, fb = font(SERIF, 64), font(SERIF, 46), font(SANS, 30)
x_num, x_txt, maxw = 150, 250, 700
for i, (t, b) in enumerate(steps, 1):
    d.text((x_num, y - 8), str(i), font=fn, fill=GOLD)
    d.text((x_txt, y), t, font=ft, fill=CREAM)
    yy = y + 58
    for ln in wrap(d, b, fb, maxw):
        d.text((x_txt, yy), ln, font=fb, fill=(214, 205, 190)); yy += 40
    y = yy + 34

center(d, "Vertical sections, not spirals.", font(SERIF_I, 44), y + 6, GOLD)
f = font(SANS, 26); center(d, "J J   M O N D E", f, H - 120, GOLD)
out = sys.argv[1] if len(sys.argv) > 1 else "out.jpg"
img.save(out, "JPEG", quality=92); print("bottom of content:", y + 60)
