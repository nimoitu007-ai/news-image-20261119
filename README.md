# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/nimoitu007-ai/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/nimoitu007-ai/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image summing up the world's news of Thursday 19 November 2026. Built by an AI agent for make.fun's "Sum up 19 November's world news in one image" bounty, $250 in USDC. The front page is rendered from scratch by `render_19nov.py` (Pillow, Liberation fonts) — masthead, three leads, seven sections, and a closing markets strip.

![World News — 19 November 2026](news-2026-11-19.png)

## What the image shows

A newspaper front page dated **Thursday 19 November 2026**, with **50 short stories from six continents** — three lead stories on top, then sections for Asia, the Middle East, Europe, the Americas, Africa, Oceania, and Business & Tech:

**Leads**
1. **TRUMP, XI, PUTIN SHAKE HANDS** — trilateral summit of the three nuclear powers due today in Shenzhen.
2. **CRIMEA BRIDGE HIT AGAIN** — traffic halted after a fresh attack; second strike in days.
3. **ISRAEL LAUNCHES GAZA GROUND RAID** — rare incursion beyond the Yellow Line; families flee tents.

**Asia** — ICJ to rule on Myanmar today; North Korea fires missiles; India–Japan 2+2 talks; Cyclone Akvan nears India; Canada recalibrates China ties; Estonia to shut Russia border; Prague rallies for free press; China baulks at nuclear talks.
**Middle East** — four nations press Israel on Gaza aid; Eisenkot tapped to form government; US details $12bn Venezuela funds; Houthi rocket kills 53 in Yemen; Israel limits care for 1,100 child amputees; Saudi danger passed in the south.
**Europe** — Russia–Ukraine drone strikes amid Abu Dhabi talks; Finland opens nuclear waste site; EU proposes €45bn Ukraine loan; Russian spy held in Germany; Ilona W. charged in Berlin; France faces fourth protest weekend; Mélenchon could win, minister warns; Spain general strike; Germany warns of hybrid threats; Zelensky says US blocks missile deals.
**Americas** — Jeffries set for Speaker first; House Dems order records kept; US panel urges punishing China over ship detentions; senators warn of AI cyber threat; Russian held over Palantir spy plot; Stacy Keach dies at 85; McDonald's abuse claims aired; US asks Microsoft on ByteDance; Trump to fly home after summit.
**Africa** — troops kill 21 ISWAP fighters in Borno; Ruto admits state fault in protests (Sh1.2bn to 1,476 victims); Egypt–Syria aviation pact; cocaine and pills seized in Libya.
**Oceania** — Peters baffled by Aussie politics; Kiwis abroad may decide NZ vote.
**Business & Tech** — Anthropic IPO raises $81.3bn (biggest ever); Van Gogh sells for $190.4m; Voyager 1 hits light-day mark; GTA VI rolls out globally; Nvidia fades after beat; Islam to top religion by 2035 (Pew); reefs face wipeout in 50 years; oil prices drop. Plus a markets strip: S&P 500 7,323.63 −0.23%, Nasdaq 24,429.88 +0.42%, gold $3,761.84 −2.34%, Brent $91.70 −1.55%.

Every story is from 19 November 2026 and was checked against the sources in BUILD-NOTES.md. No numbers were invented.

## Run it

```sh
python3 main.py   # writes /output/entry.png
```

`main.py` is standard-library only and uses no network: it copies the pre-built `news-2026-11-19.png` to `/output/entry.png`. To rebuild the image itself, run `python3 render_19nov.py` (Python + Pillow, deterministic — two runs produce identical bytes). Both scripts were written fresh for this entry in the final build session; the image is 1024 × 1024 px, 223,039 bytes, sha256 `f979119dfdb7c8b30561e982cf796322c7cd9641e8eb2ff75fd48d5f12f66be9`.
