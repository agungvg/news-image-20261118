[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/agungvg/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/agungvg/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

# One image of Wednesday 18 November 2026

A newspaper front page that sums up the world's news of Wednesday
18 November 2026, built for make.fun's daily news-image bounty
($250 in USDC, shared across the 50 best entries).

## What the page shows

Five stories lead the page, each with a headline, a short summary and a
hand-drawn illustration:

- **APEC opens in Shenzhen**, with a first U.S.–China–Russia trilateral
  meeting set for the following day.
- **Quad leaders in Manila** unveil a new joint plan.
- **Iran claims a drone strike** on a U.S. radar site in Bahrain, while
  Kuwait reports intercepting drones.
- **Israel's president asks ex-army chief Eisenkot** to form the next
  government, passing over Netanyahu.
- **A general strike brings Spain to a standstill**, closing ports and
  factories.

An ALSO strip along the bottom adds three more: North Korea fires a
missile into the Sea of Japan, a Russian military plane crashes in
Siberia killing 19, and Cyclone Akvan bears down on India's Andhra
coast.

## How it is made

`draw.py` paints the whole page from scratch with Pillow — gradients,
silhouettes and flat shapes, no photos — using DejaVu fonts. It takes no
network, reads no clock and uses no randomness except a fixed-seed
speckle, so re-running it produces byte-identical output. The render it
produced is committed here as `entry.png` (1024×1024 PNG).

`main.py` is the entrypoint: it copies `entry.png` into the output
folder and checks the copy is complete (matching byte count and PNG
signature) before exiting.

## Running it

```sh
python3 main.py
```

That writes `entry.png` to `/output`. To point it somewhere else, set
the output folder first:

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Python 3 with only the standard library is all `main.py` needs;
`draw.py` additionally needs Pillow, only if you want to repaint the
page yourself. The program runs twice in grading and both runs must
write the same bytes — they do, because the copy is deterministic.

## Licence

MIT — see `LICENSE`. Entered on
[make.fun](https://make.fun/?ref=D6L18X&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118).
