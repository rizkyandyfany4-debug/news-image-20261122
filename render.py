#!/usr/bin/env python3
"""Render the front page for 22 November 2026 and write entry.png.

Deterministic: fixed layout, fixed coordinates, no randomness, no clock.
Each illustration is drawn on its own layer and pasted, so nothing can
spill over a panel border. Run: python3 render.py
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024

PAPER = (247, 242, 231)
INK = (26, 26, 26)
RED = (163, 22, 33)
SKY = (246, 217, 160)

FONTS = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def f_serif_b(s):
    return font("DejaVuSerif-Bold.ttf", s)


def f_sans(s):
    return font("DejaVuSans.ttf", s)


def f_sans_b(s):
    return font("DejaVuSans-Bold.ttf", s)


def fit(draw, text, max_width, start, maker):
    """Largest font size (<= start) at which text fits max_width."""
    size = start
    while size > 10 and draw.textlength(text, font=maker(size)) > max_width:
        size -= 1
    return maker(size)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.25)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def draw_flames(d, cx, base_y, scale=1.0):
    cols = [(230, 126, 34), (241, 196, 15), (220, 80, 20)]
    for i, (w, h) in enumerate([(46, 78), (30, 58), (18, 40)]):
        w, h = int(w * scale), int(h * scale)
        x0 = cx - w // 2 + int((i - 1) * 8 * scale)
        pts = [
            (x0, base_y),
            (x0 + w * 0.25, base_y - h * 0.7),
            (x0 + w * 0.5, base_y - h),
            (x0 + w * 0.75, base_y - h * 0.6),
            (x0 + w, base_y),
        ]
        d.polygon(pts, fill=cols[i % 3])


def draw_smoke(d, cx, top_y, scale=1.0):
    for dx, dy, r in [(-14, 0, 16), (6, -14, 20), (-4, -30, 24)]:
        r = int(r * scale)
        dx, dy = int(dx * scale), int(dy * scale)
        d.ellipse([cx + dx - r, top_y + dy - r, cx + dx + r, top_y + dy + r],
                  fill=(150, 148, 142))


def gulf_layer():
    """Tanker, flames and missile streaks. Size 608x172."""
    lw, lh = 608, 172
    img = Image.new("RGB", (lw, lh), SKY)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 84, lw, lh], fill=(22, 50, 79))
    d.ellipse([lw - 72, 10, lw - 28, 54], fill=(250, 224, 130))
    for (sx, sy, ex, ey) in [(30, 18, 190, 76), (90, 6, 260, 70)]:
        d.line([sx, sy, ex, ey], fill=(255, 255, 255), width=3)
        d.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=(255, 255, 255))
    for wy in (lh - 46, lh - 24, lh - 8):
        for wx in range(8, lw - 20, 46):
            d.arc([wx, wy, wx + 34, wy + 12], 180, 360,
                  fill=(140, 180, 210), width=2)
    hx0, hx1, hy = 110, lw - 90, lh - 58
    d.polygon([(hx0, hy), (hx1, hy), (hx1 - 24, hy + 34), (hx0 + 10, hy + 34)],
              fill=(20, 20, 20))
    d.rectangle([hx0 + 20, hy - 26, hx1 - 60, hy], fill=(40, 40, 40))
    for i, c in enumerate([(196, 60, 40), (60, 120, 90), (200, 160, 60)]):
        cx = hx0 + 40 + i * 62
        d.rectangle([cx, hy - 52, cx + 54, hy - 26], fill=c)
    d.rectangle([hx1 - 58, hy - 62, hx1 - 8, hy - 26], fill=(230, 230, 225))
    d.rectangle([hx1 - 52, hy - 56, hx1 - 14, hy - 44], fill=(90, 140, 190))
    draw_flames(d, hx0 + 210, hy - 50, scale=0.55)
    draw_smoke(d, hx0 + 210, hy - 72, scale=0.55)
    return img


def cop31_layer():
    """Globe and sun. Size 328x44."""
    lw, lh = 328, 44
    img = Image.new("RGB", (lw, lh), (220, 235, 245))
    d = ImageDraw.Draw(img)
    cx, cy, r = 46, 22, 15
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 130, 190))
    d.ellipse([cx - r + 3, cy - r + 7, cx - r + 15, cy - r + 16],
              fill=(90, 170, 90))
    d.ellipse([cx + 1, cy + 1, cx + 13, cy + 12], fill=(90, 170, 90))
    d.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=1)
    d.line([cx, cy - r, cx, cy + r], fill=(255, 255, 255), width=1)
    sx, sy = lw - 34, 22
    d.ellipse([sx - 11, sy - 11, sx + 11, sy + 11], fill=(240, 180, 40))
    for ang in (0, 45, 90, 135, 180, 225, 270, 315):
        a = math.radians(ang)
        d.line([sx + 14 * math.cos(a), sy + 14 * math.sin(a),
                sx + 21 * math.cos(a), sy + 21 * math.sin(a)],
               fill=(240, 180, 40), width=2)
    d.rectangle([92, lh - 10, lw - 8, lh - 6], fill=(120, 90, 60))
    return img


def factory_layer():
    """Factory with a small flame. Size 328x44."""
    lw, lh = 328, 44
    img = Image.new("RGB", (lw, lh), (228, 226, 220))
    d = ImageDraw.Draw(img)
    bx0, bx1, by = 60, lw - 70, lh - 2
    d.rectangle([bx0, by - 22, bx1, by], fill=(110, 110, 108))
    for i in range(3):
        rx = bx0 + i * ((bx1 - bx0) // 3)
        d.polygon([(rx, by - 22), (rx + (bx1 - bx0) // 6, by - 32),
                   (rx + (bx1 - bx0) // 3, by - 22)], fill=(80, 80, 78))
    d.rectangle([bx0 + 12, by - 15, bx0 + 30, by], fill=(163, 22, 33))
    d.rectangle([bx1 - 34, by - 15, bx1 - 16, by], fill=(60, 90, 130))
    draw_flames(d, bx0 + 96, by - 30, scale=0.28)
    return img


def mexico_layer():
    """Desert, road and helicopter. Size 264x226."""
    lw, lh = 264, 226
    img = Image.new("RGB", (lw, lh), (240, 201, 138))
    d = ImageDraw.Draw(img)
    d.polygon([(0, lh - 90), (70, lh - 170), (140, lh - 90)],
              fill=(150, 100, 60))
    d.polygon([(110, lh - 90), (190, lh - 150), (lw, lh - 90)],
              fill=(120, 80, 50))
    d.rectangle([0, lh - 90, lw, lh], fill=(201, 143, 78))
    d.polygon([(30, lh), (110, lh - 90), (140, lh - 90), (80, lh)],
              fill=(90, 90, 88))
    for i in range(4):
        ry = lh - 20 - i * 22
        d.line([62 + i * 7, ry, 66 + i * 7, ry - 10],
               fill=(240, 240, 230), width=2)
    hx, hy = 170, 46
    d.ellipse([hx - 26, hy - 10, hx + 26, hy + 12], fill=(30, 30, 30))
    d.line([hx + 24, hy, hx + 62, hy - 8], fill=(30, 30, 30), width=4)
    d.line([hx - 52, hy - 16, hx + 52, hy - 16], fill=(30, 30, 30), width=3)
    d.line([hx, hy - 16, hx, hy - 30], fill=(30, 30, 30), width=2)
    d.line([hx - 30, hy + 16, hx - 30, hy + 34], fill=(30, 30, 30), width=2)
    d.line([hx + 10, hy + 16, hx + 10, hy + 34], fill=(30, 30, 30), width=2)
    return img


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.text((W // 2, 30), "THE WORLD IN ONE IMAGE", font=f_serif_b(54),
           fill=INK, anchor="ma")
    d.text((W // 2, 96), "SUNDAY, 22 NOVEMBER 2026", font=f_sans_b(25),
           fill=RED, anchor="ma")
    d.line([24, 128, 1000, 128], fill=INK, width=4)
    d.line([24, 134, 1000, 134], fill=INK, width=1)

    # ---- lead story: Gulf ----
    d.rectangle([24, 146, 640, 500], outline=INK, width=3)
    img.paste(gulf_layer(), (28, 150))
    d.text((332, 332), "MIDDLE EAST — BAHRAIN", font=f_sans_b(19),
           fill=RED, anchor="ma")
    d.text((332, 356), "GULF IN FLAMES", font=f_serif_b(50), fill=INK,
           anchor="ma")
    deck = wrap(d, "Iran strikes a civilian plant in Bahrain and hits two "
                   "tankers in the Strait of Hormuz. No casualties reported "
                   "as the Gulf war widens.", f_sans(22), 580)
    text_block(d, 42, 414, deck, f_sans(22))

    # ---- COP31 ----
    d.rectangle([664, 146, 1000, 316], outline=INK, width=3)
    img.paste(cop31_layer(), (668, 150))
    d.text((682, 198), "CLIMATE — ANTALYA", font=f_sans_b(16), fill=RED)
    d.text((682, 214), "COP31 INTO", font=f_serif_b(28), fill=INK)
    d.text((682, 242), "OVERTIME", font=f_serif_b(28), fill=INK)
    deck = wrap(d, "Overtime talks stall over fossil-fuel wording.",
                f_sans(18), 300)
    text_block(d, 682, 274, deck, f_sans(18), leading=19)

    # ---- Indonesia factory fire ----
    d.rectangle([664, 328, 1000, 500], outline=INK, width=3)
    img.paste(factory_layer(), (668, 332))
    d.text((682, 382), "INDONESIA — BANTEN", font=f_sans_b(16), fill=RED)
    f1 = fit(d, "FACTORY FIRE", 300, 28, f_serif_b)
    d.text((682, 400), "FACTORY FIRE", font=f1, fill=INK)
    f2 = fit(d, "7 DEAD, 50 MISSING", 300, 28, f_serif_b)
    d.text((682, 430), "7 DEAD, 50 MISSING", font=f2, fill=INK)
    deck = wrap(d, "Blaze at a sweets plant in Cikande, Banten.",
                f_sans(18), 300)
    text_block(d, 682, 458, deck, f_sans(18), leading=19)

    # ---- Mexico band ----
    d.rectangle([24, 514, 1000, 748], outline=INK, width=3)
    img.paste(mexico_layer(), (28, 518))
    d.text((312, 528), "MEXICO — SINALOA", font=f_sans_b(19), fill=RED)
    d.text((312, 552), "CARTEL BOSS CAPTURED,", font=f_serif_b(38), fill=INK)
    d.text((312, 594), "11 KILLED IN RAID", font=f_serif_b(38), fill=INK)
    deck = wrap(d, "Troops seize Fausto Isidro Meza Flores, known as "
                   "'El Chapo Isidro', in Guasave. Seven gunmen and four "
                   "soldiers die in the operation.", f_sans(22), 660)
    text_block(d, 312, 646, deck, f_sans(22))

    # ---- ALSO strip ----
    d.text((24, 764), "ALSO IN THE NEWS", font=f_sans_b(21), fill=INK)
    d.line([24, 792, 1000, 792], fill=INK, width=2)
    also = [
        "Russian cargo ship still burning off Finland after a drone strike",
        "S&P 500 enters correction as AI shares sell off",
        "Verstappen wins the Las Vegas Grand Prix",
        "Trump confirms the FBI crime database was breached",
        "Nepal's PM begins a two-day state visit to India",
        "India declare on 720/9 and lead New Zealand by 352",
    ]
    for i, item in enumerate(also):
        col = i % 2
        row = i // 2
        x = 24 + col * 500
        y = 806 + row * 64
        d.rectangle([x, y + 6, x + 10, y + 16], fill=RED)
        lines = wrap(d, item, f_sans(19), 452)
        text_block(d, x + 20, y, lines, f_sans(19), leading=23)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG")
    print("wrote", out)


if __name__ == "__main__":
    render()
