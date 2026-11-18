#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news front page (entry.png, 1024x1024).

Editorial-illustration style: a newspaper front page with a lead story, four
more stories and an ALSO strip. Every scene is drawn from scratch with PIL
primitives (gradients, silhouettes, flat shapes) -- no photos, no network,
no clock, no randomness except a fixed-seed speckle, so the output bytes are
fully deterministic: run it twice and the sha256 is identical.

Stories (all reported 18 November 2026, cross-checked across Reuters / AP /
AFP wires and national briefings):
  LEAD  APEC opens in Shenzhen; first U.S.-China-Russia trilateral set
        for Thursday.
  2     Quad leaders unveil a new plan in Manila.
  3     Iran claims a drone strike on a U.S. radar site in Bahrain;
        Kuwait reports drone interceptions.
  4     Israel's president taps ex-army chief Eisenkot to form the next
        government, bypassing Netanyahu.
  5     General strike paralyses Spain's ports and factories.
  ALSO  North Korea fires a missile into the Sea of Japan; a Russian
        military plane crashes in Siberia, killing 19; Cyclone Akvan
        bears down on India's Andhra coast.
"""

import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (22, 22, 22)
GREY = (110, 106, 96)
RED = (176, 32, 32)
NAVY = (20, 33, 61)
RULE = (30, 30, 30)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def vgrad(img, box, top, bottom):
    """Vertical gradient inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(img)
    h = max(1, y1 - y0)
    for y in range(y0, y1):
        d.line([(x0, y), (x1, y)], fill=lerp(top, bottom, (y - y0) / h))


def speckle(img, box, n, seed, color, alpha=60):
    """Deterministic grain: n dots of `color` inside box."""
    rng = random.Random(seed)
    x0, y0, x1, y1 = box
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for _ in range(n):
        x = rng.randint(x0, x1)
        y = rng.randint(y0, y1)
        r = rng.randint(1, 2)
        d.ellipse([x - r, y - r, x + r, y + r], fill=color + (alpha,))
    img.alpha_composite(layer)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, fnt, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- scenes
# Each scene draws on its own RGB image of (w, h) and returns it.

def scene_skyline(w, h):
    im = Image.new("RGB", (w, h), (46, 32, 72))
    d = ImageDraw.Draw(im)
    vgrad(im, (0, 0, w, int(h * 0.66)), (58, 40, 92), (238, 138, 66))
    # crescent moon
    d.ellipse([int(w * 0.78), int(h * 0.08), int(w * 0.88), int(h * 0.24)],
              fill=(250, 236, 190))
    d.ellipse([int(w * 0.80), int(h * 0.06), int(w * 0.90), int(h * 0.22)],
              fill=(58, 40, 92))
    # modern skyline: towers, one tapered, one twisted (offset slabs)
    base = int(h * 0.86)
    towers = [(0, 46, 120), (44, 34, 190), (76, 40, 150), (114, 30, 210),
              (142, 44, 170), (184, 36, 230), (218, 30, 140), (246, 40, 180)]
    for x0, bw, bh in towers:
        d.rectangle([x0, base - bh, x0 + bw, base], fill=(28, 24, 44))
        for wy in range(base - bh + 10, base - 8, 16):
            for wx in range(x0 + 6, x0 + bw - 6, 12):
                if (wx + wy) % 3:
                    d.rectangle([wx, wy, wx + 5, wy + 6], fill=(250, 204, 110))
    # tapered flagship tower
    d.polygon([(300, base), (312, base - 260), (336, base - 260), (348, base)],
              fill=(20, 18, 36))
    for wy in range(base - 240, base - 10, 18):
        d.rectangle([306 + (base - wy) // 40, wy, 342 - (base - wy) // 40, wy + 6],
                    fill=(250, 204, 110))
    # water + reflections
    d.rectangle([0, base, w, h], fill=(24, 34, 64))
    for i in range(5):
        yy = base + 8 + i * 12
        d.line([(20, yy), (w - 20, yy)], fill=(90, 120, 160), width=2)
    return im


def scene_quad(w, h):
    im = Image.new("RGB", (w, h), (214, 228, 238))
    d = ImageDraw.Draw(im)
    vgrad(im, (0, 0, w, h), (198, 220, 235), (240, 236, 222))
    d.ellipse([int(w * 0.76), int(h * 0.10), int(w * 0.88), int(h * 0.28)],
              fill=(248, 220, 140))
    base = int(h * 0.98)
    for x0, bw, bh in [(0, 24, 44), (22, 30, 62), (50, 24, 48), (72, 34, 70),
                       (104, 26, 52), (128, 32, 66), (158, 24, 46), (180, 28, 58)]:
        d.rectangle([x0, base - bh, x0 + bw, base], fill=(58, 70, 88))
        for wy in range(base - bh + 7, base - 5, 11):
            for wx in range(x0 + 4, x0 + bw - 3, 9):
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(250, 214, 120))
    # four flag poles, two-stripe flags
    for i, (c1, c2) in enumerate([((200, 40, 40), (255, 255, 255)),
                                  ((30, 90, 160), (255, 255, 255)),
                                  ((30, 120, 60), (255, 215, 0)),
                                  ((220, 120, 30), (30, 60, 140))]):
        px = 18 + i * 46
        d.rectangle([px, int(h * 0.16), px + 3, base], fill=(40, 40, 44))
        d.rectangle([px + 3, int(h * 0.16), px + 31, int(h * 0.16) + 11], fill=c1)
        d.rectangle([px + 3, int(h * 0.16) + 11, px + 31, int(h * 0.16) + 22], fill=c2)
    return im


def scene_drones(w, h):
    im = Image.new("RGB", (w, h), (14, 22, 44))
    d = ImageDraw.Draw(im)
    vgrad(im, (0, 0, w, h), (12, 20, 42), (30, 48, 84))
    rng = random.Random(7)
    for _ in range(40):
        x, y = rng.randint(0, w), rng.randint(0, int(h * 0.5))
        d.ellipse([x, y, x + 2, y + 2], fill=(220, 224, 240))
    # searchlight beams
    d.polygon([(20, h), (70, h), (150, 0)], fill=(90, 110, 150))
    d.polygon([(w - 30, h), (w - 80, h), (w - 170, 0)], fill=(80, 100, 140))
    # radar dome + sweeping arm
    bx, by = int(w * 0.50), int(h * 0.92)
    d.pieslice([bx - 52, by - 52, bx + 52, by + 52], 180, 360, fill=(120, 130, 145))
    d.rectangle([bx - 58, by - 6, bx + 58, by + 4], fill=(90, 98, 112))
    d.line([(bx, by - 46), (bx + 44, by - 78)], fill=(250, 220, 120), width=3)
    d.ellipse([bx + 40, by - 82, bx + 48, by - 74], fill=(250, 220, 120))
    # quadcopter silhouettes
    def drone(cx, cy, s):
        d.rectangle([cx - s, cy - s // 3, cx + s, cy + s // 3], fill=(10, 12, 16))
        for dx in (-s - 6, s + 6):
            d.line([(cx + dx - 8, cy - s), (cx + dx + 8, cy - s)],
                   fill=(200, 200, 210), width=2)
            d.line([(cx + dx, cy - s), (cx + dx, cy - s // 3)],
                   fill=(10, 12, 16), width=2)
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(250, 80, 60))
    drone(int(w * 0.24), int(h * 0.30), 12)
    drone(int(w * 0.68), int(h * 0.18), 10)
    drone(int(w * 0.82), int(h * 0.44), 8)
    return im


def scene_parliament(w, h):
    im = Image.new("RGB", (w, h), (226, 232, 238))
    d = ImageDraw.Draw(im)
    vgrad(im, (0, 0, w, h), (206, 220, 234), (238, 236, 228))
    d.ellipse([int(w * 0.78), int(h * 0.08), int(w * 0.90), int(h * 0.26)],
              fill=(250, 224, 150))
    base = int(h * 0.94)
    # steps
    for i in range(3):
        d.rectangle([int(w * 0.10) - i * 8, base - 8 - i * 9,
                     int(w * 0.90) + i * 8, base - i * 9], fill=(150, 148, 140))
    # columns + pediment
    top = int(h * 0.30)
    d.polygon([(int(w * 0.12), top + 26), (int(w * 0.50), top),
               (int(w * 0.88), top + 26)], fill=(196, 192, 182))
    d.rectangle([int(w * 0.12), top + 26, int(w * 0.88), top + 38],
                fill=(176, 172, 162))
    for i in range(5):
        cx = int(w * 0.20) + i * int(w * 0.15)
        d.rectangle([cx - 7, top + 38, cx + 7, base - 26], fill=(228, 224, 214))
        d.rectangle([cx - 11, top + 38, cx + 11, top + 46], fill=(210, 206, 196))
        d.rectangle([cx - 11, base - 34, cx + 11, base - 26], fill=(210, 206, 196))
    # flag on top
    d.rectangle([int(w * 0.50) - 1, int(h * 0.10), int(w * 0.50) + 1, top],
                fill=(60, 60, 64))
    d.rectangle([int(w * 0.50) + 1, int(h * 0.10), int(w * 0.50) + 34,
                 int(h * 0.10) + 12], fill=(30, 90, 160))
    d.rectangle([int(w * 0.50) + 1, int(h * 0.10) + 12, int(w * 0.50) + 34,
                 int(h * 0.10) + 24], fill=(255, 255, 255))
    return im


def scene_factory(w, h):
    im = Image.new("RGB", (w, h), (232, 222, 208))
    d = ImageDraw.Draw(im)
    vgrad(im, (0, 0, w, int(h * 0.60)), (214, 224, 232), (238, 228, 210))
    d.ellipse([int(w * 0.76), int(h * 0.08), int(w * 0.90), int(h * 0.28)],
              fill=(250, 224, 150))
    base = int(h * 0.96)
    # factory block + sawtooth roof + chimneys
    d.rectangle([0, int(h * 0.58), int(w * 0.72), base], fill=(96, 96, 100))
    for i in range(3):
        x0 = i * int(w * 0.24)
        d.polygon([(x0, int(h * 0.58)), (x0 + int(w * 0.12), int(h * 0.44)),
                   (x0 + int(w * 0.24), int(h * 0.58))], fill=(76, 76, 80))
    for cx in (int(w * 0.78), int(w * 0.88)):
        d.rectangle([cx - 7, int(h * 0.34), cx + 7, base], fill=(70, 70, 74))
        d.rectangle([cx - 10, int(h * 0.34), cx + 10, int(h * 0.34) + 8],
                    fill=(60, 60, 64))
    for i, (sx, sy, sr) in enumerate([(0, -16, 10), (8, -34, 13), (-4, -52, 15)]):
        d.ellipse([int(w * 0.78) + sx - sr, int(h * 0.34) + sy - sr,
                   int(w * 0.78) + sx + sr, int(h * 0.34) + sy + sr],
                  fill=(150, 150, 154))
    # crowd: heads + shoulders, two raised arms, two placards
    for i in range(9):
        cx = 14 + i * 20
        d.ellipse([cx - 6, int(h * 0.74), cx + 6, int(h * 0.74) + 12],
                  fill=(40, 40, 46))
        d.pieslice([cx - 11, int(h * 0.74) + 10, cx + 11, int(h * 0.74) + 34],
                   180, 360, fill=(52, 52, 58))
    d.line([(34, int(h * 0.74)), (26, int(h * 0.56))], fill=(40, 40, 46), width=4)
    d.line([(150, int(h * 0.74)), (158, int(h * 0.56))], fill=(40, 40, 46), width=4)
    for px, py in [(54, int(h * 0.60)), (118, int(h * 0.58))]:
        d.rectangle([px, py, px + 26, py + 16], fill=(245, 243, 236),
                    outline=(176, 32, 32), width=2)
        d.line([(px + 13, py + 16), (px + 13, py + 30)], fill=(60, 60, 64), width=3)
    return im


# ---------------------------------------------------------------- layout

LEAD = {
    "kicker": "ASIA  ·  APEC",
    "headline": "APEC opens in Shenzhen as a big-power summit looms",
    "summary": ("Trump, Xi and Putin are due to meet on Thursday in the "
                "first U.S.–China–Russia trilateral."),
    "scene": scene_skyline,
}

SECONDARIES = [
    {
        "kicker": "ASIA  ·  QUAD",
        "headline": "Quad leaders unveil new plan in Manila",
        "summary": ("U.S., India, Japan and Australia pledge closer maritime "
                    "and tech ties."),
        "scene": scene_quad,
    },
    {
        "kicker": "GULF",
        "headline": "Iran claims drone strike on U.S. radar in Bahrain",
        "summary": ("Kuwait reports drone interceptions as Gulf tensions "
                    "spike."),
        "scene": scene_drones,
    },
    {
        "kicker": "ISRAEL",
        "headline": "Herzog taps Eisenkot to form Israel's next government",
        "summary": ("Ex-army chief gets the nod over Netanyahu; ally Kahana "
                    "becomes speaker."),
        "scene": scene_parliament,
    },
    {
        "kicker": "EUROPE  ·  SPAIN",
        "headline": "General strike paralyses Spain's ports and factories",
        "summary": ("Police clash with protesters as unions walk out."),
        "scene": scene_factory,
    },
]

ALSO = ("ALSO:  North Korea fires a missile into the Sea of Japan  ·  "
        "Russian plane crash kills 19 in Siberia  ·  Cyclone Akvan nears "
        "India's Andhra coast")



def build():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    mx = 36  # side margin

    # masthead
    d.text((mx, 22), "THE WORLD", font=SERIF_B(62), fill=INK)
    d.text((W - mx, 30), "WEDNESDAY, 18 NOVEMBER 2026", font=SANS_B(23),
           fill=INK, anchor="ra")
    d.text((W - mx, 62), "FIVE STORIES  ·  ONE DAY", font=SANS(15),
           fill=GREY, anchor="ra")
    d.rectangle([mx, 100, W - mx, 104], fill=RED)

    # ---- lead story
    ly = 122
    lead_img = LEAD["scene"](524, 330)
    im.paste(lead_img, (mx, ly))
    d.rectangle([mx, ly, mx + 524, ly + 330], outline=RULE, width=2)
    tx = mx + 548
    tw = W - mx - tx
    d.text((tx, ly + 2), LEAD["kicker"], font=SANS_B(21), fill=RED)
    y = text_block(d, tx, ly + 34,
                   wrap(d, LEAD["headline"], SERIF_B(44), tw),
                   SERIF_B(44), INK, 52)
    text_block(d, tx, y + 10,
               wrap(d, LEAD["summary"], SANS(22), tw), SANS(22),
               (58, 58, 58), 30)

    # ---- secondary grid (2 x 2)
    gy = 470
    d.rectangle([mx, gy - 6, W - mx, gy - 2], fill=RULE)
    cell_w = (W - 2 * mx - 28) // 2
    cell_h = 200
    for i, st in enumerate(SECONDARIES):
        cx = mx + (i % 2) * (cell_w + 28)
        cy = gy + 12 + (i // 2) * (cell_h + 12)
        img = st["scene"](196, 148)
        im.paste(img, (cx, cy))
        d.rectangle([cx, cy, cx + 196, cy + 148], outline=RULE, width=2)
        tx2 = cx + 212
        tw2 = cx + cell_w - tx2
        d.text((tx2, cy), st["kicker"], font=SANS_B(17), fill=RED)
        y2 = text_block(d, tx2, cy + 26,
                        wrap(d, st["headline"], SERIF_B(25), tw2),
                        SERIF_B(25), INK, 29)
        text_block(d, tx2, y2 + 6,
                   wrap(d, st["summary"], SANS(17), tw2), SANS(17),
                   (58, 58, 58), 21)

    # ---- ALSO strip + footer
    ay = 912
    d.rectangle([mx, ay - 8, W - mx, ay - 4], fill=RULE)
    fsize = 18
    while d.textlength(ALSO, font=SANS(fsize)) > W - 2 * mx and fsize > 12:
        fsize -= 1
    d.text((mx, ay + 6), ALSO, font=SANS(fsize), fill=(74, 74, 74))
    d.text((mx, H - 26),
           "All events reported Wednesday 18 November 2026  ·  Sources: "
           "Reuters, AP, AFP.",
           font=SANS(14), fill=GREY)
    d.text((W - mx, H - 26), "THE WORLD IN ONE DAY", font=SANS_B(14),
           fill=GREY, anchor="ra")
    return im


def main():
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    img = build()
    if out:
        os.makedirs(out, exist_ok=True)
        img.save(os.path.join(out, "entry.png"), optimize=True)
    else:
        img.save(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "entry.png"), optimize=True)


if __name__ == "__main__":
    main()
