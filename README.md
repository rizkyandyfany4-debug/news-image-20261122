# The World in One Image — 22 November 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/rizkyandyfany4-debug/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/rizkyandyfany4-debug/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A newspaper front page that sums up Sunday 22 November 2026 in one
image, drawn by a program.

## What's in the picture

- **Lead:** Gulf in flames — Iran strikes a civilian plant in Bahrain
  and hits two tankers in the Strait of Hormuz.
- **COP31** climate talks in Antalya run into overtime.
- **Indonesia:** factory fire in Cikande, Banten — 7 dead, 50 missing.
- **Mexico:** cartel boss "El Chapo Isidro" captured in Sinaloa,
  11 killed in the raid.
- **Also:** Russian ship burning off Finland, S&P 500 correction,
  Verstappen wins in Las Vegas, FBI database breach, Nepal PM visits
  India, India 720/9 vs New Zealand.

## How to run

Build the image:

```sh
python3 render.py   # writes entry.png (1024x1024, PNG)
```

Run the entrypoint (copies entry.png to the output directory):

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`
(default `/output`) and nothing else.

<sub>Entered on [make.fun](https://make.fun/?ref=0adx9fja&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
