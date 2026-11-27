#!/usr/bin/env python3
"""Draw entry.png: a one-page newspaper summing up 26 November 2026.

Deterministic: no network, no randomness, no timestamps. Pillow renders
the same bytes on every run. Run: python3 generate_entry.py
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
INK = (26, 26, 26)
PAPER = (247, 241, 227)
GREY = (110, 105, 95)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit `width`."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def card(draw, x, y, w, h, fill, border, tag, tag_color, headline, body,
         head_size=30, body_size=20):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=fill, outline=border, width=2)
    px = x + 18
    draw.text((px, y + 14), tag, font=font(SANS_B, 18), fill=tag_color)
    draw.text((px, y + 42), headline, font=font(SERIF, head_size), fill=INK)
    lines = wrap(draw, body, font(SANS, body_size), w - 36)
    lines = lines[:3]  # never spill past the card's bottom edge
    text_block(draw, px, y + 42 + head_size + 12, lines,
               font(SANS, body_size), INK, body_size + 7)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 34  # margin
    cw = W - 2 * mx  # content width

    # Top red rule.
    d.rectangle([mx, 22, mx + cw, 28], fill=(178, 34, 34))

    # Masthead.
    mast = "THE WORLD IN ONE PAGE"
    mf = font(SERIF, 58)
    d.text(((W - d.textlength(mast, font=mf)) / 2, 38), mast,
           font=mf, fill=INK)

    # Dateline bar.
    d.line([mx, 112, mx + cw, 112], fill=INK, width=3)
    d.line([mx, 142, mx + cw, 142], fill=INK, width=1)
    date = "THURSDAY, 26 NOVEMBER 2026  \u2022  SIX STORIES THAT DEFINED THE DAY"
    df = font(SANS_B, 20)
    d.text(((W - d.textlength(date, font=df)) / 2, 116), date,
           font=df, fill=INK)

    # --- Lead story: tariffs. ---
    lx, ly, lw, lh = mx, 158, cw, 232
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=10,
                        fill=(232, 238, 244), outline=(31, 58, 95), width=2)
    # Bar chart icon on the left: four tariff bars, 15 / 20 / 25 / 35 %.
    ix, iy = lx + 26, ly + 96
    rates = [(15, "EU"), (20, "CN"), (25, "IN"), (35, "VN")]
    for i, (rate, lab) in enumerate(rates):
        bx = ix + i * 52
        bh = int(rate * 3.2)
        d.rectangle([bx, iy + 112 - bh, bx + 34, iy + 112],
                    fill=(31, 58, 95))
        d.text((bx + 1, iy + 118), lab, font=font(SANS_B, 15), fill=INK)
        d.text((bx - 2, iy + 96 - bh), f"{rate}%", font=font(SANS_B, 15),
               fill=(178, 34, 34))
    d.text((ix - 4, iy - 26), "NEW TARIFFS, %", font=font(SANS_B, 15),
           fill=INK)
    # Lead text on the right.
    tx = lx + 250
    d.text((tx, ly + 14), "1  \u2022  TRADE \u2014 TARIFFS ON 14 NATIONS",
           font=font(SANS_B, 18), fill=(31, 58, 95))
    d.text((tx, ly + 42), "Tariffs hit 14 nations",
           font=font(SERIF, 52), fill=INK)
    body = ("Washington unveils proposed tariffs on 14 economies over excess "
            "industrial capacity. China faces 20%, India 25%, Vietnam 35%; "
            "the EU, Japan, South Korea, Switzerland and Taiwan 15%.")
    lines = wrap(d, body, font(SANS, 21), lw - 250 - 22)
    text_block(d, tx, ly + 108, lines, font(SANS, 21), INK, 27)
    # Badge.
    badge = "CHINA 20%  \u2022  INDIA 25%  \u2022  VIETNAM 35%"
    bf = font(SANS_B, 19)
    bw = d.textlength(badge, font=bf) + 28
    by = ly + lh - 38
    d.rounded_rectangle([tx, by, tx + bw, by + 32], radius=16,
                        fill=(31, 58, 95))
    d.text((tx + 14, by + 5), badge, font=bf, fill=(255, 255, 255))

    # --- Middle grid, 2 x 2. ---
    gy, gh, gap = 406, 164, 16
    gw = (cw - gap) // 2
    card(d, mx, gy, gw, gh, (245, 233, 216), (150, 110, 60),
         "2  \u2022  KUWAIT \u2014 IRANIAN DRONE ATTACK", (150, 80, 20),
         "Two killed in Kuwait",
         "Iranian drones hit an air-defence station in Kuwait, killing two "
         "Italian Rheinmetall technicians. Two others are hurt.")
    card(d, mx + gw + gap, gy, gw, gh, (226, 235, 245), (50, 90, 150),
         "3  \u2022  UKRAINE \u2014 MISSILES HIT KYIV", (40, 80, 140),
         "Kyiv mall struck",
         "Russian missiles hit a Kyiv mall, wounding seven, after 113 "
         "drones fly overnight. Grain ships hit near Odesa.")
    card(d, mx, gy + gh + gap, gw, gh, (251, 233, 220), (180, 100, 40),
         "4  \u2022  EGYPT \u2014 TANKER FIRE", (170, 90, 30),
         "31 die in Cairo fire",
         "A fuel tanker overturns and explodes on Cairo's Ring Road, "
         "killing 31 and injuring 21. Twenty-seven vehicles are charred.")
    card(d, mx + gw + gap, gy + gh + gap, gw, gh, (237, 231, 243),
         (110, 70, 140),
         "5  \u2022  MARKETS \u2014 AI SELL-OFF", (100, 60, 130),
         "Nvidia on watch",
         "S&P puts Nvidia's rating on downgrade watch over board and "
         "management worries. Shares fall 3.9% to $149.30.")

    # --- Bottom strip: the parade. ---
    sx, sy, sw, sh = mx, 758, cw, 148
    d.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=10,
                        fill=(223, 240, 228), outline=(30, 120, 90), width=2)
    d.text((sx + 18, sy + 14), "6  \u2022  AMERICA \u2014 PARADE POSTPONED",
           font=font(SANS_B, 18), fill=(20, 110, 80))
    d.text((sx + 18, sy + 42), "Macy's parade delayed by storm",
           font=font(SERIF, 34), fill=INK)
    body6 = ("New York's 100th Thanksgiving Day Parade is put off to Saturday "
             "28 November by a nor'easter \u2014 the first weather delay in "
             "its century-long history.")
    lines6 = wrap(d, body6, font(SANS, 20), sw - 36)
    text_block(d, sx + 18, sy + 88, lines6, font(SANS, 20), INK, 27)

    # Footer.
    foot = "Sources: Reuters  \u2022  26 November 2026"
    ff = font(SANS, 17)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 924), foot,
           font=ff, fill=GREY)

    img.save("entry.png", format="PNG", optimize=False)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
