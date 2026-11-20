# makefun-news-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Panmeii/makefun-news-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Panmeii/makefun-news-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

**The World on 20 November 2026** — a single 1024×1024 front-page image that sums up the world news of Friday 20 November 2026 in **40 verified stories**: three illustrated features (the World Court's 9–6 ruling that Myanmar committed genocide against the Rohingya; Trump, Xi and Putin signing the Shenzhen peace declaration after their first trilateral summit; Anthropic's record $81.3bn IPO closing +17% yet failing to stop a fifth straight day of stock falls), nine medium panels (the overnight strike on Kyiv and third Kerch Bridge hit, the Houthi missile strike on Riyadh's wealth-fund tower, escalating Hormuz tanker attacks, COP31's final-day draft dropping the fossil-fuel phase-out, Cyclone Akvan's Odisha landfall, California's probe into Nvidia, Ukraine's allies meeting in Berlin, Kenya discharging its last Ebola patient, and Voyager 1 reaching one light-day from Earth), a pinned world map, a UTC timeline of the day, four stat boxes, a date-check box, and 28 one-line briefs spanning seven regions. The picture (`entry.png`) is drawn entirely with a Python PIL script (`build_image.py`) — flat-design scenes with short labels, no photographs. The Node program (`main.ts`) copies the image to the output folder and then audits the copy chunk by chunk (PNG signature, a full chunk-stream walk with CRC-32 verification of every chunk, IHDR dimensions, IEND ending, contest size limits) before reporting success.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=8nt1dqan&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
