"""Draw the news-image-20261119 front page with PIL and save entry.png.

Newspaper front page for Thursday 19 November 2026: lead story is Iran
widening its Gulf attacks to Kuwait and Bahrain, then the first-ever
Trump-Xi-Putin trilateral in Shenzhen, Jeffries' speaker nomination,
the GTA VI global rollout, Israeli tanks crossing Gaza's Yellow Line,
Cyclone Akvan, plus an "Also today" ticker.
Run:  python3 build_image.py   -> writes entry.png next to this file.
Deterministic: no network, no randomness, no timestamps in the image.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (247, 242, 231)
INK = (17, 17, 17)
RED = (163, 22, 33)
BLUE = (29, 78, 137)
GREEN = (30, 107, 52)
GREY = (90, 84, 74)
LINE = (17, 17, 17)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


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


def para(draw, x, y, text, fnt, width, fill=INK, leading=None):
    """Draw wrapped paragraph; returns y after the last line."""
    lh = leading or int(fnt.size * 1.22)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def kicker(draw, x, y, text, color=RED):
    draw.text((x, y), text, font=font(SANS_B, 19), fill=color)
    return y + 27


def headline(draw, x, y, text, size, width, fill=INK):
    fnt = font(SERIF_B, size)
    lh = int(size * 1.08)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def hrule(draw, y, x0=34, x1=990, width=2):
    draw.line([(x0, y), (x1, y)], fill=LINE, width=width)


def draw_missile(draw, x, y, w, h):
    """Missile streaking down at an angle, with a blast below."""
    draw.line([(x + 20, y + 8), (x + w - 60, y + h - 46)], fill=INK, width=7)
    draw.polygon([(x + w - 60, y + h - 46), (x + w - 26, y + h - 58),
                  (x + w - 34, y + h - 18)], fill=RED)
    draw.line([(x + 34, y + 22), (x + 66, y + 44)], fill=GREY, width=3)
    draw.line([(x + 52, y + 8), (x + 84, y + 30)], fill=GREY, width=3)
    for cx, cy, r in ((x + w - 44, y + h - 16, 12),
                      (x + w - 70, y + h - 8, 9),
                      (x + w - 18, y + h - 6, 8)):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(200, 60, 40))


def draw_summit_flags(draw, x, y, w, h):
    """Three summit flags: US, China, Russia (simplified)."""
    step = w // 3
    # US: red-white stripes
    fx = x + 6
    draw.line([(fx, y + 12), (fx, y + h - 22)], fill=INK, width=4)
    for i in range(5):
        c = RED if i % 2 == 0 else BG
        draw.rectangle([fx, y + 12 + i * 5, fx + step - 8, y + 17 + i * 5],
                       fill=c)
    # China: red flag, small stars as dots
    fx = x + step + 6
    draw.line([(fx, y + 12), (fx, y + h - 22)], fill=INK, width=4)
    draw.polygon([(fx, y + 12), (fx + step - 8, y + 22),
                  (fx, y + 34)], fill=RED)
    draw.ellipse([fx + 4, y + 16, fx + 10, y + 22], fill=(255, 220, 60))
    # Russia: white-blue-red bands
    fx = x + 2 * step + 6
    draw.line([(fx, y + 12), (fx, y + h - 22)], fill=INK, width=4)
    for i, c in enumerate((BG, BLUE, RED)):
        draw.rectangle([fx, y + 12 + i * 7, fx + step - 8, y + 19 + i * 7],
                       fill=c, outline=INK)


def draw_gavel(draw, x, y, w, h):
    """A judge's gavel: head and handle."""
    draw.line([(x + 22, y + h - 26), (x + w - 30, y + 22)], fill=(150, 110, 60),
              width=9)
    draw.rectangle([x + w - 52, y + 8, x + w - 8, y + 40], fill=INK)
    draw.rectangle([x + w - 62, y + 16, x + w - 52, y + 32], fill=INK)
    draw.rectangle([x + 8, y + h - 34, x + 64, y + h - 22], fill=INK)


def draw_controller(draw, x, y, w, h):
    """Game controller: rounded body, pad and buttons."""
    draw.rounded_rectangle([x + 8, y + 30, x + w - 8, y + h - 14],
                           radius=22, fill=INK)
    draw.ellipse([x + 22, y + 46, x + 46, y + 70], fill=BG)
    for bx, by, c in ((x + w - 44, y + 46, RED), (x + w - 62, y + 60, (255, 220, 60)),
                      (x + w - 28, y + 62, BLUE), (x + w - 46, y + 76, GREEN)):
        draw.ellipse([bx, by, bx + 12, by + 12], fill=c)
    draw.line([(x + 30, y + 84), (x + 42, y + 84)], fill=BG, width=4)
    draw.line([(x + 36, y + 78), (x + 36, y + 90)], fill=BG, width=4)


def draw_tank(draw, x, y, w, h):
    """Tank with barrel pointing right and tread wheels."""
    draw.rectangle([x + 10, y + 40, x + w - 30, y + h - 34], fill=INK)
    draw.rectangle([x + 34, y + 20, x + w - 58, y + 44], fill=INK)
    draw.line([(x + w - 58, y + 30), (x + w - 6, y + 26)], fill=INK, width=7)
    for i in range(5):
        cx = x + 22 + i * ((w - 44) // 4)
        cy = y + h - 22
        draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=BG)


def draw_cyclone(draw, x, y, w, h):
    """Cyclone spiral, scaled to fit its box."""
    cx, cy = x + w // 2, y + h // 2
    s = min(w, h) / 112.0
    for r, a0, a1 in ((46, 0, 300), (34, 40, 340), (22, 80, 380), (10, 120, 420)):
        r = max(3, int(r * s))
        draw.arc([cx - r, cy - r, cx + r, cy + r], a0, a1, fill=BLUE, width=5)
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)


def story(draw, x, y, kicker_text, color, head, deck, icon=None, icon_xy=None,
          text_w=340, head_size=31, deck_size=20):
    """One story block: kicker, headline, deck, optional icon at right."""
    y = kicker(draw, x, y, kicker_text, color)
    y = headline(draw, x, y, head, head_size, text_w)
    y += 4
    y = para(draw, x, y, deck, font(SERIF, deck_size), text_w)
    if icon is not None and icon_xy is not None:
        icon(draw, icon_xy[0], icon_xy[1], 120, 100)
    return y


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    MX = 34

    # ---- Masthead ----
    title = "THE WORLD"
    tf = font(SERIF_B, 96)
    d.text(((W - d.textlength(title, font=tf)) / 2, 22), title, font=tf, fill=INK)
    df = font(SANS_B, 25)
    date = "THURSDAY  \u2022  19 NOVEMBER 2026  \u2022  ONE DAY, ONE PAGE"
    d.text(((W - d.textlength(date, font=df)) / 2, 128), date, font=df, fill=RED)
    hrule(d, 162, width=3)
    hrule(d, 168, width=1)

    # ---- LEAD: Iran widens Gulf attacks ----
    y = 184
    y = kicker(d, MX, y, "WAR  \u2022  THE GULF", RED)
    y = headline(d, MX, y, "Iran widens Gulf attacks to Kuwait and Bahrain",
                 44, 650)
    y += 6
    y = para(d, MX, y,
             "Tehran targets the Ali Al Salem air base \u2014 its first "
             "strike on Kuwait since September \u2014 and hits Bahrain "
             "again. Gulf states say the drones and missiles were "
             "intercepted; the US hit a launch site on Qeshm Island.",
             font(SERIF, 22), 650)
    draw_missile(d, 712, 196, 268, 140)
    d.text((712, 366), "Ali Al Salem air base, Kuwait",
           font=font(SANS, 17), fill=GREY)

    hrule(d, 404)

    # ---- Row 2 ----
    y2 = 418
    story(d, MX, y2, "ASIA  \u2022  DIPLOMACY", BLUE,
          "Trump, Xi and Putin meet today in Shenzhen",
          "First-ever trilateral of the three leaders, on the APEC "
          "sidelines. Nuclear arms, AI on the agenda.",
          icon=draw_summit_flags, icon_xy=(380, 422), deck_size=19)
    story(d, 524, y2, "USA  \u2022  POLITICS", RED,
          "Democrats pick Jeffries for speaker, 251\u201311",
          "In line to become the first Black speaker. The full House "
          "votes on 3 January.",
          icon=draw_gavel, icon_xy=(870, 422), deck_size=19)
    hrule(d, 596)

    # ---- Row 3 ----
    y3 = 610
    story(d, MX, y3, "CULTURE  \u2022  GAMING", GREEN,
          "GTA VI rolls out around the world",
          "Thirteen years after GTA V, it unlocks at midnight, New "
          "Zealand first. Critics score it 99; preorders near $1.5bn.",
          icon=draw_controller, icon_xy=(380, 614), deck_size=19)
    story(d, 524, y3, "MIDDLE EAST  \u2022  GAZA", RED,
          "Israeli tanks cross the Yellow Line",
          "First advance past the ceasefire line since October 2025. "
          "Hamas calls it a violation.",
          icon=draw_tank, icon_xy=(870, 614), deck_size=19)
    hrule(d, 788)

    # ---- Bottom row ----
    y4 = 802
    # Weather (icon left, text indented), left half
    kicker(d, MX, y4, "WEATHER  \u2022  INDIA", BLUE)
    draw_cyclone(d, MX, y4 + 52, 56, 56)
    headline(d, MX + 64, y4 + 30, "Cyclone Akvan nears India's east coast",
             23, 380)
    para(d, MX + 64, y4 + 92,
         "Severe storm; red alerts for 19\u201320 Nov. Landfall forecast "
         "noon Fri 20 Nov, Machilipatnam\u2013Puri, winds 90\u2013100 km/h.",
         font(SERIF, 19), 380)
    # Also today, right half
    d.text((524, y4), "ALSO TODAY", font=font(SANS_B, 19), fill=INK)
    d.line([(524, y4 + 27), (980, y4 + 27)], fill=LINE, width=2)
    ticker = [
        "Anthropic prices a record $81.3bn IPO; shares trade today as ANT.",
        "EU proposes a \u20ac45bn loan for Ukraine, repaid from Russian assets.",
        "US loses measles-elimination status after 26 years.",
        "NASA to confirm Voyager 1 is one light-day from Earth.",
    ]
    ty = y4 + 36
    for item in ticker:
        end = para(d, 538, ty, item, font(SERIF, 18), 442, leading=22)
        d.text((524, ty), "\u2022", font=font(SERIF_B, 18), fill=RED)
        ty = end + 5

    # ---- Footer ----
    hrule(d, 984, width=1)
    ff = font(SANS, 15)
    foot = ("The day's news as reported overnight and on Thursday 19 November 2026  "
            "\u2022  Sources: Reuters, AP, BBC, NPR, CNN, IMD")
    d.text(((W - d.textlength(foot, font=ff)) / 2, 992), foot, font=ff, fill=GREY)

    img.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
