"""Render the news-image-20261119 front page: 50 stories, 1024x1024.

Deterministic, offline. Run: python3 render_19nov.py
Writes news-2026-11-19.png in this directory. All stories are from
Thursday 19 Nov 2026; see BUILD-NOTES.md for the source list.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 26
GUTTER = 14
COLS = 3
COL_W = (W - 2 * MARGIN - (COLS - 1) * GUTTER) // COLS  # 313

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
BOLDSANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SERIFB = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"

PAPER = (251, 250, 245)
INK = (17, 17, 17)
GREY = (90, 90, 90)
RULE = (40, 40, 40)
ACCENT = (150, 20, 20)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap by pixel width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_deck(draw, text, fnt, width):
    """Single-line deck, truncated with ellipsis to fit."""
    if draw.textlength(text, font=fnt) <= width:
        return text
    while text and draw.textlength(text + "...", font=fnt) > width:
        text = text[:-1].rstrip()
    return text + "..."


# (headline, deck) — headlines short caps, decks one line.
LEADS = [
    ("TRUMP, XI, PUTIN SHAKE HANDS",
     "Trilateral summit of three nuclear powers due today in Shenzhen."),
    ("CRIMEA BRIDGE HIT AGAIN",
     "Traffic halted after a fresh attack; second strike in days."),
    ("ISRAEL LAUNCHES GAZA GROUND RAID",
     "Rare incursion beyond the Yellow Line; families flee tents."),
]

# (section, [(headline, deck), ...])
SECTIONS = [
    ("ASIA", [
        ("ICJ TO RULE ON MYANMAR TODAY",
         "World Court judgment due at 10:00 in The Hague."),
        ("NORTH KOREA FIRES MISSILES",
         "Launches follow US-South Korea-Japan drills."),
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
         "President picks ex-army chief over Netanyahu."),
        ("US DETAILS $12BN VENEZUELA FUNDS",
         "State Dept report on oil and mineral revenue."),
        ("HOUTHI ROCKET KILLS 53 IN YEMEN",
         "Strike hits government military camp."),
        ("ISRAEL LIMITS CARE FOR 1,100 CHILDREN",
         "NGO: child amputees in Gaza denied treatment."),
        ("SAUDI DANGER PASSED IN SOUTH",
         "Alerts lifted in three southern cities."),
    ]),
    ("EUROPE", [
        ("RUSSIA, UKRAINE TRADE DRONE STRIKES",
         "Attacks continue despite Abu Dhabi peace talks."),
        ("FINLAND OPENS NUCLEAR WASTE SITE",
         "World's first spent-fuel repository approved."),
        ("EU PROPOSES \u20ac45BN UKRAINE LOAN",
         "Repaid after Russia pays reparations."),
        ("RUSSIAN SPY HELD IN GERMANY",
         "Suspect arrested as espionage cases rise."),
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
        ("HOUSE DEMS ORDER RECORDS KEPT",
         "Garcia tells 12 Trump allies to preserve files."),
        ("US PANEL: PUNISH CHINA OVER SHIPS",
         "Panama-flagged detentions called coercion."),
        ("SENATORS WARN OF AI CYBER THREAT",
         "Attacks outpacing US defences."),
        ("RUSSIAN HELD OVER PALANTIR SPY PLOT",
         "Arrest tied to Ukraine support."),
        ("STACY KEACH DIES AT 85",
         "American actor's career spanned decades."),
        ("MCDONALD'S ABUSE CLAIMS AIRED",
         "BBC: girls targeted as they turned 18."),
        ("US ASKS MICROSOFT ON BYTEDANCE",
         "Lawmakers seek briefing on AI deal talks."),
        ("TRUMP TO FLY HOME AFTER SUMMIT",
         "Asia trip ends after Shenzhen talks."),
    ]),
    ("AFRICA", [
        ("TROOPS KILL 21 ISWAP FIGHTERS",
         "Nigerian army operation in Borno."),
        ("RUTO ADMITS STATE FAULT IN PROTESTS",
         "Kenya paid Sh1.2bn to 1,476 victims."),
        ("EGYPT, SYRIA SIGN AVIATION PACT",
         "Flights to resume under new protocol."),
        ("COCAINE, PILLS SEIZED IN LIBYA",
         "Haul found in the east, officials say."),
    ]),
    ("OCEANIA", [
        ("PETERS BAFFLED BY AUSSIE POLITICS",
         "NZ minister aghast as Taylor ousts Ley."),
        ("KIWIS ABROAD MAY DECIDE NZ VOTE",
         "Saturday's election too close to call."),
    ]),
    ("BUSINESS & TECH", [
        ("ANTHROPIC IPO RAISES $81.3BN",
         "Biggest float in history; shares at $83."),
        ("VAN GOGH SELLS FOR $190.4M",
         "Record price after Nazi-history row."),
        ("VOYAGER 1 HITS LIGHT-DAY MARK",
         "Probe sets distance record, 50 years on."),
        ("GTA VI ROLLS OUT GLOBALLY",
         "Vice City opens after 13-year wait."),
        ("NVIDIA FADES AFTER BEAT",
         "Shares fall 2.9% as Waller flags 50bp hike."),
        ("ISLAM TO TOP RELIGION BY 2035",
         "Pew: Muslims set to pass Christians."),
        ("REEFS FACE WIPEOUT IN 50 YEARS",
         "Nearly all coral reefs at risk, study warns."),
        ("OIL PRICES DROP",
         "Supply gains outweigh Mideast tension."),
    ]),
]

MARKETS = "MARKETS 19 NOV:  S&P 500 7,323.63 -0.23%  |  Nasdaq 24,429.88 +0.42%  |  Gold $3,761.84 -2.34%  |  Brent $91.70 -1.55%"
FOOTER = "50 stories from six continents - all from Thursday 19 November 2026 - Sources: BBC, NYT, Al Jazeera, BusinessWorld, NDTV, Vanguard, Kenya Today, Nine, Ainance"


def measure_body(draw, hl_size, dk_size):
    """Total body height for given font sizes; returns (height, layout)."""
    f_hl = font(BOLDSANS, hl_size)
    f_dk = font(REG, dk_size)
    f_sec = font(BOLDSANS, 12)
    lh_hl = hl_size + 3
    lh_dk = dk_size + 3
    items = []  # (kind, section, lines, y_offset within column flow)
    total = 0
    for sec, stories in SECTIONS:
        total += 12 + 8 + 4  # section header + rules + gap
        for hl, dk in stories:
            lines = wrap(draw, hl, f_hl, COL_W)
            n = min(len(lines), 2)
            total += n * lh_hl + lh_dk + 7
    return total


def render(hl_size=14, dk_size=11):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    f_name = font(BOLD, 62)
    f_date = font(BOLDSANS, 21)
    f_sub = font(REG, 15)
    f_lead_hl = font(BOLDSANS, 16)
    f_lead_dk = font(REG, 12)
    f_hl = font(BOLDSANS, hl_size)
    f_dk = font(REG, dk_size)
    f_sec = font(BOLDSANS, 12)
    f_mkt = font(BOLDSANS, 12)
    f_ft = font(REG, 10)

    y = 22
    # Masthead
    d.text((W // 2, y), "THE WORLD", font=f_name, fill=INK, anchor="ma")
    y += 72
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=3)
    y += 8
    d.text((W // 2, y), "THURSDAY  19  NOVEMBER  2026", font=f_date,
           fill=ACCENT, anchor="ma")
    y += 30
    d.text((W // 2, y), "Trump\u2013Xi\u2013Putin summit day  \u00b7  Crimea Bridge hit again  \u00b7  50 stories from six continents",
           font=f_sub, fill=GREY, anchor="ma")
    y += 26
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=2)

    # Leads: three boxes across
    y += 10
    lead_top = y
    lead_h = 0
    boxes = []
    for hl, dk in LEADS:
        lines = wrap(d, hl, f_lead_hl, COL_W)
        dk_lines = wrap(d, dk, f_lead_dk, COL_W)
        h = len(lines) * 20 + len(dk_lines) * 16 + 6
        boxes.append((lines, dk_lines, h))
        lead_h = max(lead_h, h)
    for i, (lines, dk_lines, h) in enumerate(boxes):
        x = MARGIN + i * (COL_W + GUTTER)
        yy = lead_top
        for ln in lines:
            d.text((x, yy), ln, font=f_lead_hl, fill=INK)
            yy += 20
        for ln in dk_lines:
            d.text((x, yy), ln, font=f_lead_dk, fill=GREY)
            yy += 16
        if i < 2:
            d.line([(x + COL_W + GUTTER // 2, lead_top),
                    (x + COL_W + GUTTER // 2, lead_top + lead_h)],
                   fill=(200, 200, 190), width=1)
    y = lead_top + lead_h + 12
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=2)
    body_top = y + 10

    # Body: flow sections across 3 columns, balanced by measured height.
    lh_hl = hl_size + 3
    lh_dk = dk_size + 3
    # Build flat list of blocks: ("sec", name) or ("item", hl_lines, deck)
    blocks = []
    for sec, stories in SECTIONS:
        blocks.append(("sec", sec))
        for hl, dk in stories:
            lines = wrap(d, hl, f_hl, COL_W)[:2]
            deck = fit_deck(d, dk, f_dk, COL_W)
            blocks.append(("item", lines, deck))
    heights = []
    for b in blocks:
        if b[0] == "sec":
            heights.append(12 + 8 + 4)
        else:
            heights.append(len(b[1]) * lh_hl + lh_dk + 7)
    # Greedy column balance: assign consecutive blocks to the
    # currently shortest column, but never split a section header
    # from its first item (keep header+next item together).
    cols = [[], [], []]
    col_h = [0, 0, 0]
    i = 0
    while i < len(blocks):
        take = 1
        if blocks[i][0] == "sec" and i + 1 < len(blocks):
            take = 2  # header + first item together
        h = sum(heights[i:i + take])
        c = col_h.index(min(col_h))
        cols[c].extend(blocks[i:i + take])
        col_h[c] += h
        i += take
    body_h = max(col_h)
    footer_top = H - MARGIN - 44
    avail = footer_top - body_top - 6
    if body_h > avail:
        return None, body_h, avail

    for ci, col in enumerate(cols):
        x = MARGIN + ci * (COL_W + GUTTER)
        yy = body_top
        for b in col:
            if b[0] == "sec":
                d.text((x, yy), b[1], font=f_sec, fill=ACCENT)
                yy += 12
                d.line([(x, yy + 2), (x + COL_W, yy + 2)], fill=RULE, width=1)
                yy += 8 + 4
            else:
                for ln in b[1]:
                    d.text((x, yy), ln, font=f_hl, fill=INK)
                    yy += lh_hl
                d.text((x, yy), b[2], font=f_dk, fill=GREY)
                yy += lh_dk + 7
    # Footer
    d.line([(MARGIN, footer_top), (W - MARGIN, footer_top)], fill=RULE, width=2)
    d.text((W // 2, footer_top + 8), MARKETS, font=f_mkt, fill=INK, anchor="ma")
    d.text((W // 2, footer_top + 28), FOOTER, font=f_ft, fill=GREY, anchor="ma")
    return img, body_h, avail


if __name__ == "__main__":
    for hl, dk in [(14, 11), (13, 11), (13, 10)]:
        img, bh, av = render(hl, dk)
        if img is not None:
            print(f"fits at headline {hl} / deck {dk}: body {bh}px, avail {av}px")
            break
        print(f"overflow at headline {hl} / deck {dk}: body {bh}px > avail {av}px")
    else:
        raise SystemExit("19nov does not fit at any tried size")
    out = "news-2026-11-19.png"
    img.save(out, optimize=True)
    import hashlib
    from pathlib import Path
    data = Path(out).read_bytes()
    print(f"wrote {out}: {len(data)} bytes, sha256 {hashlib.sha256(data).hexdigest()}")
    n = sum(len(s) for _, s in SECTIONS) + len(LEADS)
    print(f"stories: {n} (leads {len(LEADS)} + sections {sum(len(s) for _, s in SECTIONS)})")
