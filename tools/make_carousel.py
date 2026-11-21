from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1350
CREAM = (246, 241, 233)
NAVY = (31, 47, 74)
GOLD = (176, 141, 87)
TAUPE = (120, 110, 98)

SERIF = "/usr/share/fonts/truetype/google-fonts/ofl/crimsontext/CrimsonText-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/google-fonts/ofl/crimsontext/CrimsonText-Italic.ttf"
SANS = "/usr/share/fonts/truetype/google-fonts/ofl/dmsans/DMSans[opsz,wght].ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, f, maxw):
    lines, line = [], ""
    for word in text.split():
        test = (line + " " + word).strip()
        if draw.textlength(test, font=f) <= maxw:
            line = test
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines

def block(draw, text, f, y, color, maxw=840, spacing=1.35, center=True):
    for para in text.split("\n"):
        for ln in wrap(draw, para, f, maxw):
            w = draw.textlength(ln, font=f)
            x = (W - w) / 2 if center else 120
            draw.text((x, y), ln, font=f, fill=color)
            y += int(f.size * spacing)
    return y

def frame(draw, color):
    draw.rectangle([40, 40, W - 40, H - 40], outline=color, width=2)

def brand(draw, color):
    f = font(SANS, 26)
    t = "J J   M O N D E"
    draw.text(((W - draw.textlength(t, font=f)) / 2, H - 120), t, font=f, fill=color)

def rule(draw, y, color):
    draw.line([(W / 2 - 60, y), (W / 2 + 60, y)], fill=color, width=2)

slides = []

# 1 cover
img = Image.new("RGB", (W, H), NAVY); d = ImageDraw.Draw(img)
frame(d, GOLD)
d.text(((W - d.textlength("DESIGNER SECRETS", font=font(SANS, 30))) / 2, 330), "DESIGNER SECRETS", font=font(SANS, 30), fill=GOLD)
y = block(d, "The 5-Step\nDesigner Tree", font(SERIF, 120), 420, CREAM, spacing=1.1)
rule(d, y + 40, GOLD)
block(d, "How stylists make any tree look high-end", font(SERIF_I, 50), y + 90, CREAM)
d.text(((W - d.textlength("Swipe  →", font=font(SANS, 32))) / 2, H - 230), "Swipe  →", font=font(SANS, 32), fill=GOLD)
brand(d, GOLD)
slides.append(img)

steps = [
    ("Choose one palette", "Two main colors plus one metallic.\nNavy, ivory and gold. Sage, cream and champagne.\nFewer colors always read as more expensive."),
    ("Lights go first", "Plan on about 100 lights per foot of tree.\nWeave them from the trunk out to the tips so the tree glows from within, not just on the surface."),
    ("Ribbon in loose cascades", "Tuck ribbon in and out every 12 to 16 inches, working top to bottom.\nLet the tails fall naturally. Perfect loops look stiff."),
    ("Ornaments in three sizes", "Largest deep inside to fill the gaps.\nMedium mid-branch. Smallest at the tips.\nCluster them in threes."),
    ("Finish, then edit", "Add picks and the topper last.\nThen step back and remove 10%.\nEditing is the real designer secret."),
]
for i, (title, body) in enumerate(steps, start=1):
    img = Image.new("RGB", (W, H), CREAM); d = ImageDraw.Draw(img)
    frame(d, GOLD)
    num = f"0{i}"
    fn = font(SERIF, 200)
    d.text(((W - d.textlength(num, font=fn)) / 2, 200), num, font=fn, fill=GOLD)
    sl = f"STEP {i} OF 5"
    d.text(((W - d.textlength(sl, font=font(SANS, 28))) / 2, 470), sl, font=font(SANS, 28), fill=TAUPE)
    y = block(d, title, font(SERIF, 84), 540, NAVY, spacing=1.1)
    rule(d, y + 30, GOLD)
    block(d, body, font(SANS, 40), y + 80, NAVY, maxw=820, spacing=1.45)
    brand(d, TAUPE)
    slides.append(img)

# 7 CTA
img = Image.new("RGB", (W, H), NAVY); d = ImageDraw.Draw(img)
frame(d, GOLD)
y = block(d, "Save this for\ndecorating day.", font(SERIF, 110), 360, CREAM, spacing=1.1)
rule(d, y + 40, GOLD)
y = block(d, "And send it to the friend who's styling the tree this year.", font(SERIF_I, 52), y + 100, CREAM)
block(d, "Follow for more designer formulas", font(SANS, 36), y + 60, GOLD)
brand(d, GOLD)
slides.append(img)

os.makedirs("out", exist_ok=True)
for n, s in enumerate(slides, start=1):
    s.save(f"out/designer-tree-{n:02d}.jpg", "JPEG", quality=92)
print("done", len(slides))
