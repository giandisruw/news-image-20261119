#!/usr/bin/env python3
"""Draw the one-page newspaper front page for 19 November 2026.

Renders entry.png (1024x1024) from the story list below, using Pillow
and the Liberation fonts. No network, no randomness, no clock: running
this script twice produces byte-identical output.

Usage:
    python3 build_image.py            # writes entry.png next to this file
    python3 build_image.py out.png    # writes to the given path
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 38

PAPER = (248, 244, 235)      # warm newsprint
INK = (26, 26, 24)           # near-black text
SOFT = (74, 70, 64)          # grey captions
RED = (172, 32, 32)          # kicker / accent red
NAVY = (16, 36, 64)          # ticker strip
PANEL = (226, 234, 242)      # cyclone panel background
RULE = (150, 142, 128)       # hairline rules

FONT_DIR = "/usr/share/fonts/truetype/liberation"
SERIF = os.path.join(FONT_DIR, "LiberationSerif-Regular.ttf")
SERIF_BOLD = os.path.join(FONT_DIR, "LiberationSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "LiberationSans-Regular.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "LiberationSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines = []
    for chunk in text.split("\n"):
        words = chunk.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = current + " " + word
            if draw.textlength(trial, font=fnt) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hrule(draw, y, weight=2, colour=RULE, x0=None, x1=None):
    x0 = MARGIN if x0 is None else x0
    x1 = W - MARGIN if x1 is None else x1
    draw.line([(x0, y), (x1, y)], fill=colour, width=weight)
    return y + weight


def centre(draw, y, text, fnt, fill):
    width = draw.textlength(text, font=fnt)
    draw.text(((W - width) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


LEAD = {
    "kicker": "LEAD  \u00b7  THE GULF",
    "headline": "Iran widens Gulf attacks to Kuwait and Bahrain",
    "body": (
        "Tehran targets the Ali Al Salem air base \u2014 its first strike on "
        "Kuwait since September \u2014 and hits Bahrain again. Gulf states "
        "say the drones and missiles were intercepted; the United States "
        "hit a launch site on Qeshm Island on Tuesday."
    ),
}

GRID = [
    {
        "kicker": "SUMMIT  \u00b7  SHENZHEN",
        "headline": "Trump, Xi and Putin meet today in Shenzhen",
        "body": (
            "First-ever trilateral of the three leaders, on the APEC "
            "sidelines. Nuclear arms and AI on the agenda."
        ),
    },
    {
        "kicker": "WASHINGTON",
        "headline": "Democrats pick Jeffries for speaker, 251\u201311",
        "body": (
            "In line to become the first Black speaker. The full House "
            "votes on 3 January."
        ),
    },
    {
        "kicker": "CULTURE  \u00b7  GAMES",
        "headline": "GTA VI rolls out around the world",
        "body": (
            "Thirteen years after GTA V, Rockstar\u2019s game unlocks at "
            "midnight local time, New Zealand first. Critics score it 99; "
            "preorders near $1.5bn."
        ),
    },
    {
        "kicker": "GAZA",
        "headline": "Israeli tanks cross the Yellow Line",
        "body": (
            "First advance past the Gaza ceasefire line since October "
            "2025. Hamas calls it a violation."
        ),
    },
]

CYCLONE = {
    "kicker": "WEATHER  \u00b7  BAY OF BENGAL",
    "headline": "Cyclone Akvan nears India\u2019s east coast",
    "body": (
        "Severe storm; red alerts for 19\u201320 Nov. Landfall forecast noon "
        "Fri 20 Nov, between Machilipatnam and Puri, winds 90\u2013100 km/h."
    ),
}

TICKER = (
    "ALSO TODAY  \u00b7  Anthropic prices a record $81.3bn IPO, shares trade "
    "today as ANT  \u00b7  EU proposes a \u20ac45bn loan for Ukraine  \u00b7  "
    "US loses measles-elimination status  \u00b7  NASA: Voyager 1 one "
    "light-day from Earth"
)


def draw_masthead(draw):
    y = 26
    f_small = font(SANS_BOLD, 19)
    y = centre(draw, y, "THURSDAY, 19 NOVEMBER 2026", f_small, SOFT)
    y += 2
    f_mast = font(SERIF_BOLD, 96)
    y = centre(draw, y, "THE WORLD", f_mast, INK)
    y += 4
    hrule(draw, y, weight=3, colour=INK)
    y += 3
    hrule(draw, y, weight=1, colour=INK)
    return y + 14


def draw_lead(draw):
    y = 196
    f_kick = font(SANS_BOLD, 20)
    draw.text((MARGIN, y), LEAD["kicker"], font=f_kick, fill=RED)
    y += 30
    f_head = font(SERIF_BOLD, 44)
    head_lines = wrap(draw, LEAD["headline"], f_head, W - 2 * MARGIN)
    y = draw_lines(draw, head_lines, MARGIN, y, f_head, INK, 52)
    y += 6
    f_body = font(SANS, 22)
    body_lines = wrap(draw, LEAD["body"], f_body, W - 2 * MARGIN)
    y = draw_lines(draw, body_lines, MARGIN, y, f_body, INK, 30)
    return y + 10


def draw_grid(draw, top):
    col_w = (W - 2 * MARGIN - 28) // 2
    row_h = 178
    f_kick = font(SANS_BOLD, 17)
    f_head = font(SERIF_BOLD, 29)
    f_body = font(SANS, 19)
    for index, story in enumerate(GRID):
        col = index % 2
        row = index // 2
        x = MARGIN + col * (col_w + 28)
        y = top + row * row_h
        if col == 1:
            draw.line([(x - 14, y + 4), (x - 14, y + row_h - 16)],
                      fill=RULE, width=1)
        draw.text((x, y), story["kicker"], font=f_kick, fill=RED)
        y += 26
        head_lines = wrap(draw, story["headline"], f_head, col_w)
        y = draw_lines(draw, head_lines, x, y, f_head, INK, 35)
        y += 4
        body_lines = wrap(draw, story["body"], f_body, col_w)
        draw_lines(draw, body_lines, x, y, f_body, INK, 26)
    return top + 2 * row_h


def draw_cyclone(draw, top):
    panel_top = top + 4
    panel_bottom = panel_top + 134
    draw.rounded_rectangle(
        [MARGIN, panel_top, W - MARGIN, panel_bottom],
        radius=10, fill=PANEL, outline=RULE, width=1)
    # Small spiral motif on the right of the panel.
    cx, cy = W - MARGIN - 52, (panel_top + panel_bottom) // 2
    for radius in (34, 26, 18, 10):
        draw.arc([cx - radius, cy - radius, cx + radius, cy + radius],
                 start=20, end=300, fill=NAVY, width=3)
    x = MARGIN + 18
    y = panel_top + 14
    f_kick = font(SANS_BOLD, 17)
    draw.text((x, y), CYCLONE["kicker"], font=f_kick, fill=NAVY)
    y += 26
    f_head = font(SERIF_BOLD, 28)
    draw.text((x, y), CYCLONE["headline"], font=f_head, fill=INK)
    y += 36
    f_body = font(SANS, 19)
    body_lines = wrap(draw, CYCLONE["body"], f_body,
                      W - 2 * MARGIN - 130)
    draw_lines(draw, body_lines, x, y, f_body, INK, 25)
    return panel_bottom + 12


def draw_ticker(draw, top):
    strip_top = top
    strip_bottom = strip_top + 66
    draw.rectangle([MARGIN, strip_top, W - MARGIN, strip_bottom],
                   fill=NAVY)
    f_tick = font(SANS_BOLD, 17)
    lines = wrap(draw, TICKER, f_tick, W - 2 * MARGIN - 28)
    y = strip_top + 8
    for line in lines[:2]:
        draw.text((MARGIN + 14, y), line, font=f_tick, fill=(255, 255, 255))
        y += 24
    return strip_bottom


def draw_footer(draw, y):
    f_foot = font(SANS, 15)
    centre(draw, y, "THE WORLD \u00b7 19 NOVEMBER 2026 \u00b7 "
           "Stories reported 18\u201319 Nov 2026", f_foot, SOFT)


def build(path):
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    y = draw_lead(draw)
    hrule(draw, y, weight=1)
    y = draw_grid(draw, y + 16)
    hrule(draw, y + 4, weight=1)
    y = draw_cyclone(draw, y + 12)
    draw_ticker(draw, y + 2)
    draw_footer(draw, H - 26)
    img.save(path, format="PNG")
    return path


def main(argv):
    out = argv[1] if len(argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    build(out)
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv)
