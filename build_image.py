#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news front page as one 1024x1024 PNG.

A dense single-page newspaper: 40 stories first reported on Friday
20 November 2026 -- three illustrated features, nine medium panels, a
pinned schematic world map, a UTC day strip, four stat boxes, a
date-check box and 28 one-line briefs. Every headline was checked
against named reporting (BBC, Reuters, AP, CNBC, IMD, NASA and the
day's news digests) before it was set. Drawn entirely with PIL
primitives -- flat shapes only, no photographs, no real people.
"""

from PIL import Image, ImageDraw, ImageFont

W = 1024
M = 16
CW = W - 2 * M
PAPER = (246, 242, 233)
CARD = (255, 255, 255)
INK = (23, 25, 31)
MUTE = (95, 99, 108)
FAINT = (204, 199, 187)
RED = (176, 30, 36)

LB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
LR = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
LS = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"

REG = {
    "ASIA": (13, 118, 112),
    "MIDDLE EAST": (214, 106, 28),
    "EUROPE": (33, 80, 164),
    "AMERICAS": (44, 136, 66),
    "AFRICA": (120, 70, 158),
    "OCEANIA": (196, 54, 90),
    "SPACE": (38, 48, 108),
}


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, x, y, text, fnt, fill, max_w, max_lines, lh):
    lines = wrap(d, text, fnt, max_w)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while last and d.textlength(last + "…", font=fnt) > max_w:
            last = last[:-1]
        lines[-1] = last.rstrip() + "…"
    for i, ln in enumerate(lines):
        d.text((x, y + i * lh), ln, font=fnt, fill=fill)
    return y + len(lines) * lh


def badge(d, cx, cy, num, colour, r=10, fsize=11):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=colour)
    t = str(num)
    f = F(LB, fsize)
    bb = d.textbbox((0, 0), t, font=f)
    d.text((cx - (bb[2] - bb[0]) / 2 - bb[0], cy - (bb[3] - bb[1]) / 2 - bb[1]),
           t, font=f, fill=(255, 255, 255))


def panel_head(d, x, y, num, region, field, src, colour, width):
    badge(d, x + 10, y + 8, num, colour)
    d.text((x + 26, y + 1), f"{region} · {field}", font=F(LB, 10), fill=colour)
    sf = F(LB, 8)
    sw = d.textlength(src, font=sf)
    d.text((x + width - sw - 2, y + 2), src, font=sf, fill=MUTE)


# ------------------------------------------------------------ feature art
# Each painter fills the art box (x0, y0, x1, y1) with a flat scene.

def paint_court(d, x0, y0, x1, y1):
    """Courthouse portico and a balance scale: the ICJ genocide ruling."""
    d.rectangle([x0, y0, x1, y1], fill=(216, 226, 238))
    base = y1 - 6
    d.polygon([(x0 + 14, y0 + 22), ((x0 + x1) // 2, y0 + 4), (x1 - 14, y0 + 22)],
              fill=(58, 66, 84))
    d.rectangle([x0 + 14, y0 + 22, x1 - 14, y0 + 27], fill=(58, 66, 84))
    colw = 7
    span = x1 - x0 - 56
    for i in range(5):
        cx = x0 + 28 + i * (span // 4)
        d.rectangle([cx, y0 + 30, cx + colw, base - 10], fill=(240, 242, 245))
    d.rectangle([x0 + 14, base - 10, x1 - 14, base], fill=(58, 66, 84))
    # balance scale on the right
    sx = x1 - 52
    d.line([sx, y0 + 34, sx, base - 14], fill=(120, 84, 20), width=3)
    d.line([sx - 24, y0 + 40, sx + 24, y0 + 40], fill=(120, 84, 20), width=3)
    for px in (sx - 24, sx + 24):
        d.line([px, y0 + 40, px - 8, y0 + 58], fill=(120, 84, 20), width=2)
        d.line([px, y0 + 40, px + 8, y0 + 58], fill=(120, 84, 20), width=2)
        d.arc([px - 11, y0 + 52, px + 11, y0 + 70], 0, 180, fill=(120, 84, 20), width=2)


def paint_summit(d, x0, y0, x1, y1):
    """Shenzhen towers under three flags: China, Russia, United States."""
    d.rectangle([x0, y0, x1, y1], fill=(198, 224, 244))
    d.ellipse([x0 + 16, y0 + 8, x0 + 48, y0 + 40], fill=(247, 192, 62))
    base = y1 - 4
    heights = [26, 44, 34, 56, 38, 48, 30, 42, 36]
    bw = (x1 - x0 - 20) // len(heights)
    for i, h in enumerate(heights):
        bx = x0 + 10 + i * bw
        d.rectangle([bx, base - h, bx + bw - 4, base], fill=(50, 64, 86))
    poles = [x0 + 56, (x0 + x1) // 2 - 16, x1 - 88]
    fw, fh = 34, 21
    for px in poles:
        d.line([px, base - 58, px, base - 4], fill=(28, 28, 28), width=3)
    fx, fy = poles[0], base - 58
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 41, 46))
    d.polygon([(fx + 7, fy + 3), (fx + 9, fy + 8), (fx + 14, fy + 8),
               (fx + 10, fy + 11), (fx + 11, fy + 16), (fx + 7, fy + 13),
               (fx + 3, fy + 16), (fx + 4, fy + 11), (fx + 1, fy + 8),
               (fx + 6, fy + 8)], fill=(255, 222, 60))
    fx, fy = poles[1], base - 58
    d.rectangle([fx, fy, fx + fw, fy + fh // 3], fill=(245, 245, 245))
    d.rectangle([fx, fy + fh // 3, fx + fw, fy + 2 * fh // 3], fill=(36, 84, 168))
    d.rectangle([fx, fy + 2 * fh // 3, fx + fw, fy + fh], fill=(214, 40, 48))
    fx, fy = poles[2], base - 58
    for i in range(4):
        col = (178, 34, 52) if i % 2 == 0 else (245, 245, 245)
        d.rectangle([fx, fy + i * (fh // 4), fx + fw, fy + (i + 1) * (fh // 4)], fill=col)
    d.rectangle([fx, fy, fx + 15, fy + fh // 2], fill=(38, 54, 120))


def paint_market(d, x0, y0, x1, y1):
    """A launch bell and a falling chart: record IPO, fifth day of losses."""
    d.rectangle([x0, y0, x1, y1], fill=(26, 32, 48))
    for gx in range(x0 + 14, x1 - 8, 26):
        d.line([gx, y0 + 6, gx, y1 - 16], fill=(44, 54, 74), width=1)
    for gy in range(y0 + 12, y1 - 10, 18):
        d.line([x0 + 8, gy, x1 - 8, gy], fill=(44, 54, 74), width=1)
    pts = [(x0 + 16, y0 + 18), (x0 + 62, y0 + 30), (x0 + 104, y0 + 24),
           (x0 + 148, y0 + 46), (x0 + 190, y0 + 58), (x0 + 232, y0 + 52),
           (x0 + 274, y1 - 22)]
    d.line(pts, fill=(240, 84, 76), width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(240, 84, 76))
    lx, ly = pts[-1]
    d.polygon([(lx, ly), (lx - 12, ly - 3), (lx - 4, ly - 12)], fill=(240, 84, 76))
    # exchange bell, top right
    bx, by = x1 - 44, y0 + 10
    d.arc([bx, by, bx + 30, by + 26], 180, 360, fill=(247, 192, 62), width=3)
    d.line([bx - 3, by + 14, bx + 33, by + 14], fill=(247, 192, 62), width=3)
    d.ellipse([bx + 11, by + 16, bx + 19, by + 23], fill=(247, 192, 62))
    d.text((x0 + 14, y1 - 20), "ANT +17% · S&P −2%", font=F(LB, 11),
           fill=(240, 200, 90))


# ------------------------------------------------------------ story data
FEATURES = [
    dict(n=1, region="ASIA", field="JUSTICE", src="BBC · UN NEWS",
         head="World Court: Myanmar committed genocide against Rohingya",
         dek="The 9–6 ruling is the first finding of genocide against a state; "
             "1.3 million Rohingya remain displaced",
         art=paint_court),
    dict(n=2, region="ASIA", field="SUMMIT", src="REUTERS · CNN",
         head="Trump, Xi & Putin sign Shenzhen peace declaration",
         dek="81-minute first trilateral pledges nuclear-risk cuts and UN reform; "
             "no word on Ukraine or Iran",
         art=paint_summit),
    dict(n=3, region="AMERICAS", field="MARKETS", src="CNBC · BBC",
         head="Anthropic's record IPO can't stop the AI sell-off",
         dek="Debut closes +17% near $97 after raising $81.3bn — yet US stocks "
             "fall a fifth straight day",
         art=paint_market),
]

PANELS = [
    dict(n=4, region="EUROPE", field="WAR", src="REUTERS · AP",
         head="Kyiv struck again overnight; Kerch Bridge hit a third time",
         dek="Missiles and drones kill in the capital as Ukraine halts rail "
             "traffic over the strait"),
    dict(n=5, region="MIDDLE EAST", field="WAR", src="SKY NEWS · MEE",
         head="Houthi missile damages Riyadh's wealth-fund tower",
         dek="Strike hits the PIF tower in the financial district; Saudis "
             "intercept more missiles and drones"),
    dict(n=6, region="MIDDLE EAST", field="WAR", src="JAPAN TIMES · CBS",
         head="Hormuz tanker attacks step up as Iran war enters month nine",
         dek="A tanker burns after striking a mine; the Pentagon puts the "
             "war's cost so far at $48.3bn"),
    dict(n=7, region="EUROPE", field="CLIMATE", src="JAPAN TIMES · CBC",
         head="COP31 final day: draft deal drops fossil-fuel phase-out",
         dek="Pacific states demand phase-out language as the Antalya text "
             "also drops net-zero dates"),
    dict(n=8, region="ASIA", field="STORM", src="IMD · REUTERS",
         head="Cyclone Akvan crosses the Odisha coast at Gopalpur",
         dek="Winds of 70–80 km/h, gusts to 90; no major damage reported — "
             "India's third cyclone in a month"),
    dict(n=9, region="AMERICAS", field="TECH", src="BBC · CNBC",
         head="California probes Nvidia as chip sales to China face scrutiny",
         dek="Subpoena follows CEO Huang's resignation; 879,000 AI-chip "
             "licences to China revealed"),
    dict(n=10, region="EUROPE", field="DIPLOMACY", src="BBC · FRANCE 24",
         head="Ukraine's allies in Berlin: Europe 'ready to talk' to Russia",
         dek="US floats a NATO-style guarantee for Kyiv; Macron wants the "
             "membership question reopened"),
    dict(n=11, region="AFRICA", field="HEALTH", src="ALLAFRICA",
         head="Kenya discharges its last Ebola patient",
         dek="The ward empties 37 days after the first case — preparedness, "
             "not luck, say commentators"),
    dict(n=12, region="SPACE", field="SCIENCE", src="NASA · FRANCE 24",
         head="Voyager 1 reaches one light-day from Earth",
         dek="26 billion km out after 49 years, as BepiColombo slips into "
             "orbit around Mercury"),
]

BRIEFS = [
    (13, "AMERICAS", "Gold falls 4.2% as a stronger dollar and 5% yields dull its shine"),
    (14, "AMERICAS", "IMF: world public debt nears 100% of GDP, highest since WWII"),
    (15, "ASIA", "Japan core inflation hits year's high; BoJ still on track to hike"),
    (16, "AMERICAS", "Brazil sells $1bn of reserves as the real slides 18% in a month"),
    (17, "AMERICAS", "US Senate passes energy permitting overhaul, 62–33"),
    (18, "AMERICAS", "White House fires cyber chief Cairncross after a week of outages"),
    (19, "AMERICAS", "Justice Dept drops Alaska suit; Peltola's Senate win stands"),
    (20, "EUROPE", "UK & EU set to agree youth mobility scheme in Brussels"),
    (21, "EUROPE", "Youth strike in 25+ countries over living costs & militarisation"),
    (22, "MIDDLE EAST", "Israeli troops cross Gaza's Yellow Line; camps flood as winter bites"),
    (23, "ASIA", "IAEA: North Korea is expanding uranium enrichment at Yongbyon"),
    (24, "AFRICA", "Drone strike kills 10 at a gold mine in Sudan's South Kordofan"),
    (25, "AMERICAS", "Haiti forces retake Martissant corridor; 34 gang suspects killed"),
    (26, "AMERICAS", "Bukele registers to run for a third term in El Salvador"),
    (27, "AMERICAS", "US & Venezuela sign military cooperation deal in Caracas"),
    (28, "MIDDLE EAST", "Iraq gives Kataib Hezbollah until Friday to quit Jurf al-Nasr"),
    (29, "AFRICA", "Drone & artillery strikes reported on Ethiopia–Eritrea border"),
    (30, "AFRICA", "Migrant boat sinks off Senegal; dozens missing en route to Canaries"),
    (31, "OCEANIA", "Fiji & Tonga declare disasters as El Niño drought deepens"),
    (32, "AMERICAS", "El Niño storm threatens Los Angeles with floods & mudslides"),
    (33, "EUROPE", "Denmark ratifies Greenland security deal with the United States"),
    (34, "ASIA", "Mongolia's president resigns; parliament speaker steps in"),
    (35, "AMERICAS", "GTA VI tops $2.3bn — set to be the biggest entertainment launch ever"),
    (36, "EUROPE", "Italy fines Meta €805m over Android photo access"),
    (37, "AFRICA", "Marathon champion Jepchirchir banned three years for doping"),
    (38, "AMERICAS", "Trump grants late baseball star Pete Rose a posthumous pardon"),
    (39, "ASIA", "Philippines & Chile sign their first free-trade deal at APEC"),
    (40, "AFRICA", "US consortium wins Kenya's $60bn Mrima Hill minerals deal"),
]

TIMELINE = [
    ("OVERNIGHT", "Kyiv hit again; fire in the Obolonskyi district"),
    ("02:00 UTC", "Akvan crosses the Odisha coast near Gopalpur"),
    ("TOKYO", "Nikkei ends −4.8%; SoftBank drops 16%"),
    ("ANTALYA", "COP31's final day: phase-out dropped"),
    ("25+ COUNTRIES", "Youth strike over costs & militarisation"),
    ("NEW YORK", "AI doubts deepen; gold −4.2%, Brent $90.05"),
]

STATS = [
    ("9–6", "ICJ vote finding Myanmar responsible for genocide"),
    ("$81.3bn", "raised in Anthropic's IPO — a record offering"),
    ("−4.8%", "the Nikkei's Friday fall as the AI trade slid"),
    ("26bn km", "Voyager 1's distance — one light-day out"),
]

DATE_CHECK = ("Held out as older news: the US ground stop was Fri 13 Nov — "
              "Friday brought the router probe, not a new halt. Still ahead: "
              "Sat — Akvan's rains reach Bihar & Jharkhand; COP31's slimmed "
              "text faces its closing plenary.")


# ------------------------------------------------------------ world map
# Schematic continents as rough lon/lat polygons, equirectangular.

CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 70), (-85, 66),
     (-80, 73), (-78, 62), (-85, 55), (-92, 57), (-95, 49), (-89, 48),
     (-84, 46), (-76, 44), (-70, 42), (-74, 39), (-76, 35), (-81, 31),
     (-80, 26), (-84, 30), (-90, 29), (-97, 26), (-97, 22), (-94, 18),
     (-90, 15), (-83, 9), (-79, 9), (-86, 13), (-92, 15), (-105, 20),
     (-110, 24), (-114, 29), (-117, 33), (-122, 37), (-124, 46), (-130, 55),
     (-150, 60), (-162, 61)],
    # Greenland
    [(-45, 60), (-30, 68), (-22, 70), (-25, 76), (-45, 80), (-58, 76),
     (-55, 70), (-52, 64)],
    # South America
    [(-79, 9), (-72, 12), (-64, 10), (-55, 6), (-50, 0), (-44, -3),
     (-35, -8), (-39, -13), (-40, -20), (-46, -24), (-52, -32), (-58, -35),
     (-62, -39), (-65, -41), (-65, -45), (-67, -50), (-69, -54), (-71, -54),
     (-73, -46), (-73, -37), (-71, -30), (-70, -20), (-75, -15), (-79, -8),
     (-81, -4), (-80, 1), (-77, 4)],
    # Europe
    [(-9, 43), (-2, 44), (0, 46), (-5, 48), (-1, 50), (2, 51), (5, 53),
     (8, 55), (8, 57), (12, 56), (18, 56), (21, 60), (19, 55), (24, 59),
     (28, 60), (30, 62), (28, 66), (32, 70), (45, 68), (60, 69), (75, 68),
     (90, 66), (100, 70), (90, 62), (75, 60), (60, 58), (50, 55), (40, 52),
     (38, 47), (30, 46), (28, 41), (23, 40), (23, 36), (19, 40), (15, 38),
     (16, 40), (12, 44), (8, 44), (3, 43), (3, 42), (-2, 37), (-6, 36),
     (-9, 37), (-9, 43)],
    # Africa
    [(-6, 35), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28), (38, 22),
     (40, 15), (43, 12), (48, 11), (51, 12), (48, 5), (42, -2), (40, -10),
     (39, -18), (36, -22), (33, -26), (28, -33), (20, -35), (17, -32),
     (15, -27), (13, -18), (12, -12), (13, -6), (9, -1), (9, 4), (4, 6),
     (-3, 5), (-8, 5), (-13, 8), (-17, 12), (-17, 15), (-16, 20),
     (-15, 25), (-10, 30), (-6, 35)],
    # Asia (mainland east of Europe block)
    [(90, 66), (105, 68), (120, 70), (140, 72), (160, 70), (178, 66),
     (178, 62), (162, 60), (156, 52), (142, 50), (140, 45), (135, 40),
     (129, 33), (122, 31), (120, 25), (110, 20), (108, 15), (106, 9),
     (103, 5), (100, 8), (98, 14), (95, 16), (92, 20), (89, 22), (86, 20),
     (80, 15), (77, 8), (73, 18), (70, 22), (66, 25), (61, 25), (57, 27),
     (52, 28), (50, 29), (54, 26), (58, 23), (59, 22), (55, 17), (52, 15),
     (45, 12), (43, 12), (40, 15), (38, 22), (35, 28), (36, 36), (30, 36),
     (27, 37), (30, 41), (38, 47), (40, 52), (50, 55), (60, 58), (75, 60),
     (90, 62)],
    # Indonesia / New Guinea
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -9),
     (125, -9), (130, -4), (136, -2), (142, -3), (147, -6), (150, -9),
     (146, -9), (140, -8), (134, -4), (128, -3), (120, -2), (112, -2),
     (104, 2), (98, 4)],
    # Australia
    [(113, -22), (114, -28), (115, -34), (118, -35), (124, -33), (130, -32),
     (135, -35), (138, -36), (140, -38), (145, -38), (150, -37), (153, -30),
     (153, -25), (151, -20), (149, -15), (146, -11), (142, -11), (142, -17),
     (140, -18), (136, -15), (135, -12), (132, -11), (130, -13), (126, -14),
     (122, -17), (118, -20), (113, -22)],
    # Japan
    [(130, 31), (133, 34), (137, 35), (140, 36), (141, 40), (142, 44),
     (144, 44), (143, 42), (141, 39), (139, 35), (135, 34), (131, 32)],
    # UK
    [(-5, 50), (-3, 53), (-5, 55), (-3, 57), (-1, 57), (0, 54), (1, 51)],
    # New Zealand
    [(167, -46), (170, -44), (173, -42), (174, -40), (176, -38), (178, -37),
     (176, -39), (174, -41), (171, -44), (168, -46)],
]

PINS = [  # story number -> (lon, lat)
    (1, (96, 21)), (2, (114, 22)), (4, (30, 50)), (5, (46, 24)),
    (6, (56, 26)), (7, (30, 36)), (8, (85, 20)), (10, (13, 52)),
    (11, (35, -2)),
]


def paint_map(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(233, 238, 240))
    w, h = x1 - x0, y1 - y0

    def px(lon, lat):
        return (x0 + (lon + 170) / 360 * w, y0 + (80 - lat) / 135 * h)

    for poly in CONTINENTS:
        d.polygon([px(lon, lat) for lon, lat in poly], fill=(206, 199, 178))
    for num, (lon, lat) in PINS:
        cx, cy = px(lon, lat)
        reg = next(s["region"] for s in FEATURES + PANELS if s["n"] == num)
        badge(d, cx, cy, num, REG[reg], r=8, fsize=9)
    # Voyager marker, top-right corner (interstellar, off the map)
    sx, sy = x1 - 56, y0 + 12
    d.polygon([(sx, sy - 6), (sx + 2, sy - 2), (sx + 6, sy), (sx + 2, sy + 2),
               (sx, sy + 6), (sx - 2, sy + 2), (sx - 6, sy), (sx - 2, sy - 2)],
              fill=REG["SPACE"])
    d.text((sx + 9, sy - 5), "12", font=F(LB, 9), fill=REG["SPACE"])


# ------------------------------------------------------------ page build

def main():
    img = Image.new("RGB", (W, W), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.rectangle([M, 10, M + 62, 84], fill=RED)
    d.text((M + 31, 16), "NOV", font=F(LB, 13), fill=(255, 255, 255), anchor="ma")
    d.text((M + 31, 32), "20", font=F(LB, 30), fill=(255, 255, 255), anchor="ma")
    d.text((M + 31, 66), "FRI", font=F(LB, 11), fill=(255, 255, 255), anchor="ma")
    d.text((M + 76, 12), "THE DAY IN WORLD NEWS", font=F(LB, 10), fill=MUTE)
    d.text((W - M, 12), "EVERY STORY FIRST REPORTED ON THE DAY · ANY TIME ZONE",
           font=F(LB, 10), fill=MUTE, anchor="ra")
    d.text((M + 76, 26), "Friday 20 November 2026", font=F(LS, 43), fill=INK)
    d.text((M + 77, 71), "40 STORIES · 7 REGIONS · ONE FRONT PAGE",
           font=F(LB, 12), fill=RED)
    d.text((W - M, 71), "SUMMED UP IN A SINGLE IMAGE", font=F(LB, 10),
           fill=MUTE, anchor="ra")

    # ---- region strip (counts computed from the story data)
    counts = {}
    for s in FEATURES + PANELS:
        counts[s["region"]] = counts.get(s["region"], 0) + 1
    for _, reg, _ in BRIEFS:
        counts[reg] = counts.get(reg, 0) + 1
    order = ["EUROPE", "ASIA", "MIDDLE EAST", "AMERICAS", "AFRICA", "OCEANIA", "SPACE"]
    y = 92
    seg = CW // len(order)
    for i, reg in enumerate(order):
        x = M + i * seg
        wseg = seg if i < len(order) - 1 else CW - i * seg
        d.rectangle([x, y, x + wseg - 2, y + 22], fill=REG[reg])
        d.text((x + wseg / 2 - 1, y + 5), f"{reg} · {counts[reg]}",
               font=F(LB, 10), fill=(255, 255, 255), anchor="ma")

    # ---- timeline strip
    y = 122
    d.rectangle([M, y, M + CW, y + 46], fill=CARD, outline=FAINT)
    d.text((M + 8, y + 6), "THE DAY", font=F(LB, 10), fill=INK)
    d.text((M + 8, y + 20), "IN UTC", font=F(LB, 10), fill=INK)
    colw = (CW - 74) // 6
    for i, (when, what) in enumerate(TIMELINE):
        x = M + 74 + i * colw
        d.text((x, y + 5), when, font=F(LB, 11), fill=RED)
        draw_wrapped(d, x, y + 20, what, F(LR, 8), MUTE, colw - 8, 2, 10)

    # ---- feature cards
    y = 176
    fw = (CW - 16) // 3
    fh = 158
    for i, s in enumerate(FEATURES):
        x = M + i * (fw + 8)
        colour = REG[s["region"]]
        d.rectangle([x, y, x + fw, y + fh], fill=CARD, outline=FAINT)
        d.rectangle([x, y, x + fw, y + 3], fill=colour)
        s["art"](d, x + 6, y + 9, x + fw - 6, y + 79)
        panel_head(d, x + 6, y + 84, s["n"], s["region"], s["field"],
                   s["src"], colour, fw - 12)
        draw_wrapped(d, x + 8, y + 100, s["head"], F(LS, 15), INK, fw - 16, 2, 16)
        draw_wrapped(d, x + 8, y + 134, s["dek"], F(LR, 9), MUTE, fw - 16, 2, 11)

    # ---- medium panels, three rows of three
    y = 342
    pw = (CW - 16) // 3
    ph = 88
    for r in range(3):
        for c in range(3):
            s = PANELS[r * 3 + c]
            x = M + c * (pw + 8)
            yy = y + r * (ph + 6)
            colour = REG[s["region"]]
            d.rectangle([x, yy, x + pw, yy + ph], fill=CARD, outline=FAINT)
            d.rectangle([x, yy, x + 3, yy + ph], fill=colour)
            panel_head(d, x + 8, yy + 6, s["n"], s["region"], s["field"],
                       s["src"], colour, pw - 16)
            draw_wrapped(d, x + 10, yy + 26, s["head"], F(LB, 13), INK,
                         pw - 20, 2, 15)
            draw_wrapped(d, x + 10, yy + 58, s["dek"], F(LR, 9), MUTE,
                         pw - 20, 2, 11)

    # ---- map + stats + date check
    y = 342 + 3 * (ph + 6) + 2
    mapw = 548
    d.rectangle([M, y, M + mapw, y + 148], fill=CARD, outline=FAINT)
    d.text((M + 8, y + 5), "WHERE IT HAPPENED", font=F(LB, 10), fill=INK)
    d.text((M + mapw - 8, y + 5), "PINS MATCH THE STORY NUMBERS",
           font=F(LB, 8), fill=MUTE, anchor="ra")
    paint_map(d, M + 6, y + 22, M + mapw - 6, y + 142)
    sx = M + mapw + 8
    sw = (CW - mapw - 8 - 6) // 2
    for i, (big, small) in enumerate(STATS):
        x = sx + (i % 2) * (sw + 6)
        yy = y + (i // 2) * 52
        d.rectangle([x, yy, x + sw, yy + 48], fill=INK)
        d.text((x + sw / 2, yy + 4), big, font=F(LB, 19),
               fill=(255, 255, 255), anchor="ma")
        draw_wrapped(d, x + 6, yy + 28, small, F(LR, 8), (210, 212, 218),
                     sw - 12, 2, 10)
    yy = y + 108
    d.rectangle([sx, yy, M + CW, y + 156], fill=(250, 244, 222), outline=FAINT)
    d.text((sx + 8, yy + 4), "DATE CHECK", font=F(LB, 9), fill=RED)
    draw_wrapped(d, sx + 8, yy + 17, DATE_CHECK, F(LR, 8), INK,
                 CW - mapw - 24, 3, 10)

    # ---- briefs
    y = y + 164
    d.line([M, y, M + CW, y + 0], fill=INK, width=2)
    d.text((M, y + 5), "ALSO ON FRIDAY 20 NOVEMBER", font=F(LB, 11), fill=INK)
    d.text((M + CW, y + 5), "BRIEFS 13–40 · ONE LINE EACH", font=F(LB, 8),
           fill=MUTE, anchor="ra")
    y += 24
    colw = (CW - 24) // 2
    for j, (num, reg, text) in enumerate(BRIEFS):
        col = 0 if j < 14 else 1
        row = j if j < 14 else j - 14
        x = M + col * (colw + 24)
        yy = y + row * 13
        colour = REG[reg]
        nf = F(LB, 10)
        d.text((x, yy), str(num), font=nf, fill=colour)
        nw = d.textlength(str(num) + " ", font=nf)
        draw_wrapped(d, x + nw + 2, yy, text, F(LR, 10), INK, colw - nw - 4,
                     1, 12)

    img.save("/home/hatch/workspace/makefun/news20-entry/entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
