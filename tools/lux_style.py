"""JJ Monde holiday luxury style (approved by Janet, Nov 2026).

Hunter green / oxblood tartan, ivory, brushed gold foil, Crimson Text + DM Sans,
double foil frame with diamond corners, JJ crest, "J J   M O N D E" footer plaque.
All slides are 1080x1350 RGB JPEGs.

Building blocks:
  cover_slide(kicker, title, subtitle)              hunter tartan, crest, foil frame
  step_slide(i, n, title, body)                     odd = hunter tartan, even = ivory
  cta_slide(title, line, foot)                      oxblood tartan, crest
  single_post(kicker, title, items, closer)         one-image post on hunter tartan
  save(slides, folder, slug)                        writes <slug>-01.jpg ...
Run this file directly to render the Designer Tree sample into ./out-lux/.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os

W, H = 1080, 1350
HUNTER = (20, 46, 36); HUNTER_D = (12, 32, 25)
OXBLOOD = (88, 20, 30); OXBLOOD_D = (62, 12, 20)
IVORY = (246, 241, 233); INK = (24, 40, 33); GOLD = (176, 141, 87)
SOFT_IVORY = (214, 206, 190)

_D = "/usr/share/fonts/truetype/google-fonts/ofl/crimsontext/"
SERIF = _D + "CrimsonText-Regular.ttf"
SERIF_I = _D + "CrimsonText-Italic.ttf"
SANS = "/usr/share/fonts/truetype/google-fonts/ofl/dmsans/DMSans[opsz,wght].ttf"
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]


def F(path, size):
    return ImageFont.truetype(path, size)


def _foil(size):
    stops = [(0, (140, 104, 52)), (0.35, (226, 196, 136)), (0.5, (244, 222, 168)),
             (0.65, (200, 162, 98)), (1, (150, 112, 58))]
    w, h = size
    # build a 1-D ramp then stretch: t = 0.7*x/w + 0.3*y/h
    ramp = Image.new("RGB", (1024, 1))
    for i in range(1024):
        t = i / 1023
        for k in range(len(stops) - 1):
            a, ca = stops[k]; b, cb = stops[k + 1]
            if a <= t <= b:
                u = (t - a) / (b - a)
                ramp.putpixel((i, 0), tuple(int(ca[j] + (cb[j] - ca[j]) * u) for j in range(3)))
                break
    g = Image.new("RGB", size)
    px = g.load(); rp = ramp.load()
    for y in range(h):
        for x in range(w):
            px[x, y] = rp[int((0.7 * x / w + 0.3 * y / h) * 1023), 0]
    return g.filter(ImageFilter.GaussianBlur(1))


FOIL_LIGHT = _foil((W, H))  # on dark backgrounds
FOIL_DARK = ImageEnhance.Contrast(ImageEnhance.Brightness(FOIL_LIGHT).enhance(0.72)).enhance(1.25)  # on ivory
_CUR = [FOIL_LIGHT]


def _paste_foil(img, mask):
    img.paste(_CUR[0], (0, 0), mask)


def foil_shape(img, fn):
    m = Image.new("L", (W, H), 0); fn(ImageDraw.Draw(m)); _paste_foil(img, m)


def _tw(d, t, f, tr):
    return sum(d.textlength(c, font=f) for c in t) + tr * (len(t) - 1)


def text(img, t, f, y, col=None, tr=0, foiled=False):
    """Centered text; col=None with foiled=True draws gold foil. tr = letter tracking px."""
    d = ImageDraw.Draw(img); x = (W - _tw(d, t, f, tr)) / 2
    if foiled:
        m = Image.new("L", (W, H), 0); md = ImageDraw.Draw(m)
        for c in t:
            md.text((x, y), c, font=f, fill=255); x += md.textlength(c, font=f) + tr
        _paste_foil(img, m)
    else:
        for c in t:
            d.text((x, y), c, font=f, fill=col); x += d.textlength(c, font=f) + tr


def wrap(d, t, f, mw):
    lines, line = [], ""
    for w in t.split():
        x = (line + " " + w).strip()
        if d.textlength(x, font=f) <= mw: line = x
        else: lines.append(line); line = w
    if line: lines.append(line)
    return lines


def block(img, t, f, y, col, mw=820, sp=1.35, foiled=False):
    """Centered wrapped paragraphs ("\\n" = new paragraph). Returns next y."""
    d = ImageDraw.Draw(img)
    for p in t.split("\n"):
        for ln in wrap(d, p, f, mw):
            text(img, ln, f, y, col, 0, foiled); y += int(f.size * sp)
    return y


def frame(img):
    def f(md):
        md.rectangle([36, 36, W - 36, H - 36], outline=255, width=3)
        md.rectangle([50, 50, W - 50, H - 50], outline=255, width=1)
        for cx, cy in ((50, 50), (W - 50, 50), (50, H - 50), (W - 50, H - 50)):
            md.polygon([(cx, cy - 9), (cx + 9, cy), (cx, cy + 9), (cx - 9, cy)], fill=255)
    foil_shape(img, f)


def rule(img, y, w=90):
    def f(md):
        md.line([(W / 2 - w - 18, y), (W / 2 - 18, y)], fill=255, width=2)
        md.line([(W / 2 + 18, y), (W / 2 + w + 18, y)], fill=255, width=2)
        md.polygon([(W / 2, y - 8), (W / 2 + 8, y), (W / 2, y + 8), (W / 2 - 8, y)], fill=255)
    foil_shape(img, f)


def crest(img, cy):
    def f(md):
        md.ellipse([W / 2 - 58, cy - 58, W / 2 + 58, cy + 58], outline=255, width=2)
        md.ellipse([W / 2 - 50, cy - 50, W / 2 + 50, cy + 50], outline=255, width=1)
    foil_shape(img, f)
    text(img, "JJ", F(SERIF_I, 58), cy - 38, None, 2, True)


def brand(img, plate=None):
    """Footer. plate = background colour of a small foil-edged plaque (dark slides)."""
    if plate:
        box = [W / 2 - 190, H - 140, W / 2 + 190, H - 70]
        ImageDraw.Draw(img).rectangle(box, fill=plate)
        foil_shape(img, lambda md: md.rectangle(box, outline=255, width=1))
    text(img, "J J   M O N D E", F(SANS, 24), H - 112, None, 4, True)


def tartan(img, dark, accent1, accent2, alpha=60):
    o = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(o)
    for k in range(-1, W // 180 + 2):
        x = k * 180
        d.rectangle([x, 0, x + 70, H], fill=dark + (alpha,))
        d.rectangle([x + 100, 0, x + 103, H], fill=accent1 + (alpha + 30,))
        d.rectangle([x + 140, 0, x + 141, H], fill=accent2 + (alpha + 40,))
    for k in range(-1, H // 180 + 2):
        y = k * 180
        d.rectangle([0, y, W, y + 70], fill=dark + (alpha,))
        d.rectangle([0, y + 100, W, y + 103], fill=accent1 + (alpha + 30,))
        d.rectangle([0, y + 140, W, y + 141], fill=accent2 + (alpha + 40,))
    img.paste(o, (0, 0), o)


def vignette(img):
    v = Image.new("L", (W, H), 0); ImageDraw.Draw(v).ellipse([-200, -150, W + 200, H + 150], fill=255)
    v = v.filter(ImageFilter.GaussianBlur(160))
    return Image.composite(img, Image.blend(img, Image.new("RGB", (W, H)), 0.45), v)


def _bg(kind):
    if kind == "hunter":
        img = Image.new("RGB", (W, H), HUNTER); tartan(img, HUNTER_D, OXBLOOD, GOLD, 70); return vignette(img)
    if kind == "hunter_soft":
        img = Image.new("RGB", (W, H), HUNTER); tartan(img, HUNTER_D, OXBLOOD, GOLD, 38); return vignette(img)
    if kind == "oxblood":
        img = Image.new("RGB", (W, H), OXBLOOD); tartan(img, OXBLOOD_D, HUNTER, GOLD, 60); return vignette(img)
    img = Image.new("RGB", (W, H), IVORY)  # ivory with tartan bands top and bottom
    tb = Image.new("RGB", (W, 22), HUNTER); t2 = Image.new("RGB", (W, H), HUNTER)
    tartan(t2, HUNTER_D, OXBLOOD, GOLD, 90); tb = t2.crop((0, 0, W, 22))
    img.paste(tb, (0, 0)); img.paste(tb, (0, H - 22))
    return img


def _panel(img, color, box=(120, 250, W - 120, 1060)):
    p = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(p).rectangle(box, fill=color + (235,))
    img.paste(p, (0, 0), p)


def cover_slide(kicker, title, subtitle, swipe=True):
    _CUR[0] = FOIL_LIGHT
    img = _bg("hunter"); _panel(img, HUNTER_D); frame(img); crest(img, 340)
    text(img, kicker.upper(), F(SANS, 26), 450, IVORY, 8)
    y = block(img, title, F(SERIF, 118), 510, IVORY, sp=1.04)
    rule(img, y + 40)
    block(img, subtitle, F(SERIF_I, 46), y + 80, SOFT_IVORY)
    if swipe: text(img, "SWIPE  →", F(SANS, 24), 975, None, 6, True)
    brand(img, plate=HUNTER_D)
    return img


def step_slide(i, n, title, body):
    dark = i % 2 == 1
    _CUR[0] = FOIL_LIGHT if dark else FOIL_DARK
    img = _bg("hunter_soft" if dark else "ivory")
    head, txt, lab = (IVORY, SOFT_IVORY, (222, 190, 140)) if dark else (INK, (50, 62, 56), OXBLOOD)
    frame(img)
    text(img, ROMAN[i - 1], F(SERIF, 190), 180, None, 0, True)
    text(img, f"STEP {ROMAN[i - 1]} OF {ROMAN[n - 1]}", F(SANS, 24), 450, lab, 7)
    y = block(img, title, F(SERIF, 84), 505, head, sp=1.08)
    rule(img, y + 32, 70)
    block(img, body, F(SANS, 38), y + 82, txt, mw=780, sp=1.5)
    brand(img, plate=HUNTER_D if dark else None)
    _CUR[0] = FOIL_LIGHT
    return img


def cta_slide(title, line, foot):
    _CUR[0] = FOIL_LIGHT
    img = _bg("oxblood"); _panel(img, OXBLOOD_D); frame(img); crest(img, 340)
    y = block(img, title, F(SERIF, 108), 450, IVORY, sp=1.05)
    rule(img, y + 40)
    y = block(img, line, F(SERIF_I, 48), y + 85, (226, 212, 196), mw=760)
    text(img, foot.upper(), F(SANS, 24), y + 40, None, 5, True)
    brand(img, plate=(52, 10, 18))
    return img


def single_post(kicker, title, items, closer):
    """One-image post: items = [(heading, one line), ...] up to 5, numbered I, II, ..."""
    _CUR[0] = FOIL_LIGHT
    img = _bg("hunter"); _panel(img, HUNTER_D, (100, 110, W - 100, 1180)); frame(img)
    text(img, kicker.upper(), F(SANS, 24), 150, IVORY, 8)
    y = block(img, title, F(SERIF, 88), 195, IVORY, sp=1.05)
    rule(img, y + 28); y += 70
    d = ImageDraw.Draw(img)
    for i, (h, b) in enumerate(items, 1):
        m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).text((160, y - 4), ROMAN[i - 1], font=F(SERIF, 52), fill=255)
        _paste_foil(img, m)
        d.text((270, y), h, font=F(SERIF, 46), fill=IVORY)
        yy = y + 58
        for ln in wrap(d, b, F(SANS, 30), 680):
            d.text((270, yy), ln, font=F(SANS, 30), fill=SOFT_IVORY); yy += 40
        y = yy + 30
    block(img, closer, F(SERIF_I, 44), y + 6, None, foiled=True)
    brand(img, plate=HUNTER_D)
    return img, y + 60  # second value: bottom of content (must stay < 1180)


def save(slides, folder, slug):
    os.makedirs(folder, exist_ok=True)
    paths = []
    for n, s in enumerate(slides, 1):
        p = os.path.join(folder, f"{slug}-{n:02d}.jpg"); s.save(p, "JPEG", quality=93); paths.append(p)
    return paths


if __name__ == "__main__":
    steps = [
        ("Choose one palette", "Two main colors plus one metallic.\nNavy, ivory and gold. Sage, cream and champagne.\nFewer colors always read as more expensive."),
        ("Lights go first", "Plan on about 100 lights per foot of tree.\nWeave them from the trunk out to the tips so the tree glows from within, not just on the surface."),
        ("Ribbon in loose cascades", "Tuck ribbon in and out every 12 to 16 inches, working top to bottom.\nLet the tails fall naturally. Perfect loops look stiff."),
        ("Ornaments in three sizes", "Largest deep inside to fill the gaps.\nMedium mid-branch. Smallest at the tips.\nCluster them in threes."),
        ("Finish, then edit", "Add picks and the topper last.\nThen step back and remove 10%.\nEditing is the real designer secret."),
    ]
    slides = [cover_slide("The Holiday Edit", "The Five-Step\nDesigner Tree", "How stylists make any tree look high-end")]
    slides += [step_slide(i, len(steps), t, b) for i, (t, b) in enumerate(steps, 1)]
    slides.append(cta_slide("Save this for\ndecorating day.", "And send it to the friend who's styling the tree this year.", "Follow for more designer formulas"))
    print(save(slides, "out-lux", "designer-tree-lux"))
