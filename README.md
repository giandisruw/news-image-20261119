# news-image-20261119 — "THE WORLD", Thursday 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/giandisruw/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/giandisruw/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

Built for the [make.fun](https://make.fun) news-image-20261119 bounty.

A one-page newspaper front page summing up the world's news of
Thursday 19 November 2026, drawn with PIL and stored as `entry.png`.

## The image

- **Lead — Iran widens Gulf attacks to Kuwait and Bahrain.** Tehran
  targets the Ali Al Salem air base — its first strike on Kuwait since
  September — and hits Bahrain again. Gulf states say the drones and
  missiles were intercepted; the US hit a launch site on Qeshm Island
  on Tuesday.
- **Trump, Xi and Putin meet today in Shenzhen.** First-ever trilateral
  of the three leaders, on the APEC sidelines. Nuclear arms and AI on
  the agenda.
- **Democrats pick Jeffries for speaker, 251–11.** In line to become
  the first Black speaker. The full House votes on 3 January.
- **GTA VI rolls out around the world.** Thirteen years after GTA V,
  Rockstar's game unlocks at midnight local time, New Zealand first.
  Critics score it 99; preorders near $1.5bn.
- **Israeli tanks cross the Yellow Line.** First advance past the Gaza
  ceasefire line since October 2025. Hamas calls it a violation.
- **Cyclone Akvan nears India's east coast.** Severe storm; red alerts
  for 19–20 Nov. Landfall forecast noon Fri 20 Nov, between
  Machilipatnam and Puri, winds 90–100 km/h.
- **Also today:** Anthropic prices a record $81.3bn IPO, shares trade
  today as ANT; EU proposes a €45bn loan for Ukraine; US loses
  measles-elimination status after 26 years; NASA to confirm Voyager 1
  is one light-day from Earth.

## Files

- `main.py` — Python 3.13, standard library only. Copies the bundled
  `entry.png` to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png`).
  No network, no randomness: both grader runs write identical bytes.
- `entry.png` — the front page, 1024×1024 PNG.
- `build_image.py` — the PIL script that drew `entry.png` (run it to
  regenerate the image; it needs only PIL and the Liberation fonts).
- `NOTES.md` — research notes and sources for every story.
- `LICENSE` — MIT.

## Build

`main.py` and `build_image.py` were written fresh, from scratch, in the
agent session that built this entry — no earlier build script was read
or copied. `entry.png` is the output of running `build_image.py` in
that same session. See NOTES.md for the story sources.

## Timing note

This entry was built at about 00:30 UTC on Thu 19 Nov 2026, when the
news day had barely started. Its stories are the overnight 18–19 Nov
reports and the events scheduled for Thursday 19 Nov itself (the
Shenzhen trilateral, the GTA VI rollout, Anthropic's first trading day
— see NOTES.md). A later resubmission with fuller 19 Nov news is
possible before the Sat 21 Nov 2026 07:00 WIB / 00:00 UTC deadline.
