#!/usr/bin/env python3
"""Render the front page for Thursday 19 November 2026.

A single-page newspaper look built with Pillow: a serif masthead, a
red date line, three lead stories across the top, then the remaining
stories flowing down three columns under red section headers, and a
closing markets strip at the foot of the page.

Run:  python3 render_19nov.py
Out:  news-2026-11-19.png  (1024 x 1024, deterministic)
"""

import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "news-2026-11-19.png")

INK = (12, 12, 12)          # near-black text
GREY = (96, 96, 96)         # deck / small print
RED = (176, 18, 18)         # date line and section headers
RULE = (30, 30, 30)         # horizontal rules
FAINT = (190, 190, 190)     # vertical column separators
PAPER = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype"
SERIF_BOLD = os.path.join(FONT_DIR, "liberation", "LiberationSerif-Bold.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "liberation", "LiberationSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "liberation", "LiberationSans-Regular.ttf")

MARGIN = 28
GUTTER = 16
COL_W = (PAGE_W - 2 * MARGIN - 2 * GUTTER) // 3   # 312
COL_X = [MARGIN + i * (COL_W + GUTTER) for i in range(3)]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_lines(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text(((PAGE_W - w) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


# ---------------------------------------------------------------- stories
# (headline, deck) pairs. 3 leads + 47 section items = 50 stories.

LEADS = [
    ("TRUMP, XI, PUTIN SHAKE HANDS",
     "Trilateral summit of three nuclear powers due today in Shenzhen."),
    ("CRIMEA BRIDGE HIT AGAIN",
     "Traffic halted after a fresh attack; second strike in days."),
    ("ISRAEL LAUNCHES GAZA GROUND RAID",
     "Rare incursion beyond the Yellow Line; families flee tents."),
]

SECTIONS = [
    ("ASIA", [
        ("ICJ TO RULE ON MYANMAR TODAY",
         "World Court judgment due at 10:00 in The Hague."),
        ("NORTH KOREA FIRES MISSILES",
         "Launches follow US\u2013South Korea\u2013Japan drills."),
        ("INDIA, JAPAN HOLD 2+2 TALKS",
         "Defence ties top the agenda, Jaishankar says."),
        ("CYCLONE AKVAN NEARS INDIA",
         "Landfall expected between Machilipatnam and Puri."),
        ("CANADA RECALIBRATES CHINA TIES",
         "Carney seeks the right deal with the US too."),
        ("ESTONIA TO SHUT RUSSIA BORDER",
         "Crossings close in December after attack bid."),
        ("PRAGUE RALLIES FOR FREE PRESS",
         "Hundreds of thousands protest media law."),
        ("CHINA BAULKS AT NUCLEAR TALKS",
         "Beijing resists trilateral arms control."),
    ]),
    ("MIDDLE EAST", [
        ("FOUR NATIONS PRESS ISRAEL ON AID",
         "Australia, Canada, Italy, UK demand Gaza access as floods hit."),
        ("EISENKOT TAPPED TO FORM GOVERNMENT",
         "President's ex-army chief over Netanyahu."),
        ("US DETAILS $12BN VENEZUELA FUNDS",
         "State Dept report on oil and mineral revenue."),
        ("HOUTHI ROCKET KILLS 53 IN YEMEN",
         "Strike hits government military camp."),
        ("SAUDI DANGER PASSED IN SOUTH",
         "Alerts lifted in three southern cities."),
        ("ISRAEL LIMITS CARE FOR 1,100 CHILDREN",
         "NGO: child amputees in Gaza denied treatment."),
    ]),
    ("EUROPE", [
        ("EU PROPOSES \u20ac45BN UKRAINE LOAN",
         "Repaid after Russia pays reparations."),
        ("RUSSIA, UKRAINE TRADE DRONE STRIKES",
         "Attacks continue despite Abu Dhabi peace talks."),
        ("FINLAND OPENS NUCLEAR WASTE SITE",
         "World's first spent-fuel repository approved."),
        ("RUSSIAN SPY HELD IN GERMANY",
         "Suspect arrested for espionage, cases rise."),
        ("ILONA W. CHARGED IN BERLIN",
         "Ukrainian-German accused of spying for Russia."),
        ("FRANCE FACES FOURTH PROTEST WEEKEND",
         "Cost-of-living marches roll on."),
        ("M\u00c9LENCHON COULD WIN, MINISTER WARNS",
         "Hard-left leader tipped for French presidency."),
        ("SPAIN GENERAL STRIKE BITES",
         "Ports and factories disrupted."),
        ("GERMANY WARNS OF HYBRID THREATS",
         "Police flag rising cyberattacks."),
        ("ZELENSKY: US BLOCKS MISSILE DEALS",
         "Kyiv says paid deliveries held up."),
    ]),
    ("AMERICAS", [
        ("JEFFRIES SET FOR SPEAKER FIRST",
         "Democrats nominate him; first Black Speaker."),
        ("SENATORS WARN OF AI CYBER THREAT",
         "Attacks outpacing US defences."),
        ("MCDONALD'S ABUSE CLAIMS AIRED",
         "BBC: girls targeted as they turned 18."),
        ("US PANEL: PUNISH CHINA OVER SHIPS",
         "Panama-flagged detentions called coercion."),
        ("STACY KEACH DIES AT 85",
         "American actor's career spanned decades."),
        ("HOUSE DEMS ORDER RECORDS KEPT",
         "Garcia tells 12 Trump allies to preserve files."),
        ("RUSSIAN HELD OVER PALANTIR SPY PLOT",
         "Arrest tied to Ukraine support."),
        ("TRUMP TO FLY HOME AFTER SUMMIT",
         "Asia trip ends after Shenzhen talks."),
        ("US ASKS MICROSOFT ON BYTEDANCE",
         "Lawmakers seek briefing on AI deal talks."),
    ]),
    ("AFRICA", [
        ("TROOPS KILL 21 ISWAP FIGHTERS",
         "Nigerian army operation in Borno."),
        ("EGYPT, SYRIA SIGN AVIATION PACT",
         "Flights to resume under new protocol."),
        ("RUTO ADMITS STATE FAULT IN PROTESTS",
         "Kenya paid Sh1.2bn to 1,476 victims."),
        ("COCAINE, PILLS SEIZED IN LIBYA",
         "Haul found in the east, officials say."),
    ]),
    ("OCEANIA", [
        ("KIWIS ABROAD MAY DECIDE NZ VOTE",
         "Saturday's election too close to call."),
        ("PETERS BAFFLED BY AUSSIE POLITICS",
         "NZ minister aghast as Taylor ousts Ley."),
    ]),
    ("BUSINESS & TECH", [
        ("VAN GOGH SELLS FOR $190.4M",
         "Record price after Nazi-history row."),
        ("VOYAGER 1 HITS LIGHT-DAY MARK",
         "Probe sets distance record, 50 years on."),
        ("GTA VI ROLLS OUT GLOBALLY",
         "Vice City opens after 13-year wait."),
        ("ISLAM TO TOP RELIGION BY 2035",
         "Pew: Muslims set to pass Christians."),
        ("REEFS FACE WIPEOUT IN 50 YEARS",
         "Nearly all coral reefs at risk, study warns."),
        ("ANTHROPIC IPO RAISES $81.3BN",
         "Biggest float in history; shares at $83."),
        ("NVIDIA FADES AFTER BEAT",
         "Shares fall 2.9% as Waller flags 50bp hike."),
        ("OIL PRICES DROP",
         "Supply gains outweigh Mideast tension."),
    ]),
]

KICKER = "Trump\u2013Xi\u2013Putin summit day  \u00b7  Crimea Bridge hit again  \u00b7  50 stories from six continents"
MARKETS = "MARKETS 19 NOV:  S&P 500 7,323.63 -0.23%  |  Nasdaq 24,429.88 +0.42%  |  Gold $3,761.84 -2.34%  |  Brent $91.70 -1.55%"
FOOTER = "50 stories from six continents \u2014 all from Thursday 19 November 2026 \u2014 Sources: BBC, NYT, Al Jazeera, BusinessWorld, NDTV, Vanguard, Kenya Today, Nine, Ainance"


def story_count():
    return len(LEADS) + sum(len(items) for _, items in SECTIONS)


def render():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    d = ImageDraw.Draw(img)

    masthead = font(SERIF_BOLD, 86)
    date_f = font(SANS_BOLD, 21)
    kicker_f = font(SANS, 15)
    lead_head = font(SANS_BOLD, 15)
    lead_deck = font(SANS, 12)
    head_f = font(SANS_BOLD, 14)
    deck_f = font(SANS, 11)
    section_f = font(SANS_BOLD, 12)
    market_f = font(SANS_BOLD, 13)
    foot_f = font(SANS, 10)

    y = 8
    # --- masthead ------------------------------------------------------
    y = draw_centered(d, y, "THE WORLD", masthead, INK)
    d.line([(MARGIN, y + 2), (PAGE_W - MARGIN, y + 2)], fill=RULE, width=3)
    y += 12
    y = draw_centered(d, y, "THURSDAY 19 NOVEMBER 2026", date_f, RED)
    y += 6
    y = draw_centered(d, y, KICKER, kicker_f, GREY)
    d.line([(MARGIN, y + 6), (PAGE_W - MARGIN, y + 6)], fill=RULE, width=2)
    y += 16

    # --- three leads ---------------------------------------------------
    lead_top = y
    lead_bottom = lead_top
    for i, (headline, deck) in enumerate(LEADS):
        x = COL_X[i]
        yy = lead_top
        for line in wrap_lines(d, headline, lead_head, COL_W):
            d.text((x, yy), line, font=lead_head, fill=INK)
            yy += 18
        for line in wrap_lines(d, deck, lead_deck, COL_W):
            d.text((x, yy), line, font=lead_deck, fill=GREY)
            yy += 15
        lead_bottom = max(lead_bottom, yy)
        if i < 2:
            vx = COL_X[i] + COL_W + GUTTER // 2
            d.line([(vx, lead_top + 2), (vx, lead_bottom - 2)], fill=FAINT, width=1)
    y = lead_bottom + 8
    d.line([(MARGIN, y), (PAGE_W - MARGIN, y)], fill=RULE, width=2)
    y += 10

    # --- body: sections flowing down the three columns ----------------
    body_top = y
    body_bottom = 952          # markets strip starts below this
    col = 0
    cy = body_top

    def header_height():
        return 12 + 4 + 7      # text + rule gap + spacing

    def item_height(headline, deck):
        h = len(wrap_lines(d, headline, head_f, COL_W)) * 17
        h += len(wrap_lines(d, deck, deck_f, COL_W)) * 14
        return h + 9           # gap after the item; keeps the columns
                               # filling down to just above the markets strip

    for name, items in SECTIONS:
        hh = header_height()
        if cy + hh > body_bottom and col < 2:
            col += 1
            cy = body_top
        elif cy + hh > body_bottom:
            raise SystemExit("BODY OVERFLOW: ran out of columns at section " + name)
        x = COL_X[col]
        d.text((x, cy), name, font=section_f, fill=RED)
        d.line([(x, cy + 16), (x + COL_W, cy + 16)], fill=RULE, width=1)
        cy += 23
        for headline, deck in items:
            ih = item_height(headline, deck)
            if cy + ih > body_bottom and col < 2:
                col += 1
                cy = body_top
                x = COL_X[col]
                # re-draw the section header at the top of the new column
                d.text((x, cy), name + " (cont.)", font=section_f, fill=RED)
                d.line([(x, cy + 16), (x + COL_W, cy + 16)], fill=RULE, width=1)
                cy += 23
            elif cy + ih > body_bottom:
                raise SystemExit("BODY OVERFLOW: ran out of columns at " + headline)
            yy = cy
            for line in wrap_lines(d, headline, head_f, COL_W):
                d.text((x, yy), line, font=head_f, fill=INK)
                yy += 17
            for line in wrap_lines(d, deck, deck_f, COL_W):
                d.text((x, yy), line, font=deck_f, fill=GREY)
                yy += 14
            cy = yy + 9    # same gap as item_height() measures

    # --- markets strip and footer --------------------------------------
    d.line([(MARGIN, 962), (PAGE_W - MARGIN, 962)], fill=RULE, width=2)
    draw_centered(d, 972, MARKETS, market_f, INK)
    draw_centered(d, 1000, FOOTER, foot_f, GREY)

    img.save(OUT, format="PNG")
    return OUT


if __name__ == "__main__":
    path = render()
    data = open(path, "rb").read()
    print("stories:", story_count())
    print("size:", os.path.getsize(path), "bytes")
    print("sha256:", hashlib.sha256(data).hexdigest())
