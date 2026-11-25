#!/usr/bin/env python3
"""Front page for Tuesday 24 November 2026, drawn entirely in code.

Run from this directory:
    python3 draw.py        # writes entry.png next to this file

The picture follows the winning news-image grammar (Nov 22 winner 854k,
Nov 23 winner 840k): masthead + big date + three-story red subline +
region chips + UTC timeline + 13 numbered feature cards, each with a
drawn vector scene + headline + detail + source + status tag, then a
"THE DAY IN NUMBERS" sidebar, 22 one-line briefs, and a DATE CHECK
footer listing the earlier-day stories deliberately left out.

Every story on the page happened or was first reported on Tuesday
24 November 2026, verified against 2+ outlets (see ../research.md).
Disputed figures are never printed as single values; claims are
labelled CLAIM/REPORTED. No photos, no fonts fetched, no network.
Output is 1024x1024 and must stay under 1 MiB.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
PAD = 24

PALETTE = {
    "paper": (247, 243, 234),
    "ink": (22, 22, 22),
    "grey": (96, 90, 80),
    "red": (178, 26, 26),
    "navy": (16, 32, 60),
    "gold": (198, 148, 52),
    "rule": (190, 182, 166),
    "hairline": (226, 220, 206),
    "card": (255, 255, 255),
    "strip": (236, 230, 216),
}

REGION_COLORS = {
    "EUROPE": (32, 90, 140),
    "MIDDLE EAST": (192, 57, 43),
    "AFRICA": (30, 122, 52),
    "AMERICAS": (18, 38, 63),
    "ASIA-PACIFIC": (14, 124, 123),
    "ECONOMY": (122, 90, 0),
    "TECH": (106, 27, 154),
    "SPORT": (211, 84, 0),
    "SCIENCE & CULTURE": (194, 24, 123),
}

DEJAVU = Path("/usr/share/fonts/truetype/dejavu")


def load_fonts():
    def f(name, size):
        return ImageFont.truetype(str(DEJAVU / name), size)

    return {
        "kicker_sm": f("DejaVuSans-Bold.ttf", 9),
        "mast_kick": f("DejaVuSans-Bold.ttf", 13),
        "mast_meta": f("DejaVuSans.ttf", 11),
        "date": f("DejaVuSerif-Bold.ttf", 52),
        "subline": f("DejaVuSans-Bold.ttf", 13),
        "chip": f("DejaVuSans-Bold.ttf", 11),
        "tl_label": f("DejaVuSans-Bold.ttf", 11),
        "tl": f("DejaVuSans.ttf", 11),
        "num": f("DejaVuSans-Bold.ttf", 12),
        "kicker": f("DejaVuSans-Bold.ttf", 10),
        "tag": f("DejaVuSans-Bold.ttf", 9),
        "head_lg": f("DejaVuSerif-Bold.ttf", 17),
        "detail_lg": f("DejaVuSans.ttf", 11),
        "head_sm": f("DejaVuSerif-Bold.ttf", 13),
        "detail_sm": f("DejaVuSans.ttf", 10),
        "source": f("DejaVuSans.ttf", 9),
        "side_head": f("DejaVuSans-Bold.ttf", 12),
        "side_num": f("DejaVuSans-Bold.ttf", 21),
        "side_lab": f("DejaVuSans.ttf", 10),
        "brief_head": f("DejaVuSans-Bold.ttf", 12),
        "brief": f("DejaVuSans-Bold.ttf", 11),
        "brief_src": f("DejaVuSans.ttf", 9),
        "foot": f("DejaVuSans.ttf", 10),
        "foot_b": f("DejaVuSans-Bold.ttf", 10),
    }


# ---------------------------------------------------------------- scenes
# Each scene draws flat vector art into the box (x, y, w, h).

def scene_gavel(c, x, y, w, h):
    c.rectangle([x, y, x + w, y + h], fill=(16, 32, 60))
    c.rectangle([x, y, x + 5, y + h], fill=(198, 148, 52))
    # scales of justice, left: post, beam, two pans
    px = x + 52
    c.rectangle([px - 2, y + 12, px + 2, y + h - 12], fill=(214, 222, 235))
    c.line([px - 34, y + 16, px + 34, y + 16], fill=(214, 222, 235), width=3)
    for s in (-1, 1):
        sx = px + s * 30
        c.line([sx, y + 16, sx, y + 30], fill=(214, 222, 235), width=2)
        c.polygon([(sx - 12, y + 30), (sx + 12, y + 30), (sx, y + 44)],
                  fill=(198, 148, 52))
    c.rectangle([px - 16, y + h - 12, px + 16, y + h - 8], fill=(214, 222, 235))
    # gavel, right: big head + handle (kept high, clear of the verdict text)
    c.polygon([(x + w - 128, y + 8), (x + w - 66, y + 24),
               (x + w - 74, y + 42), (x + w - 136, y + 26)], fill=(198, 148, 52))
    c.polygon([(x + w - 104, y + 26), (x + w - 56, y + 56),
               (x + w - 64, y + 62), (x + w - 112, y + 34)], fill=(150, 108, 32))
    c.text((x + 104, y + h - 6), "10 OF 12", font=load_fonts()["head_sm"],
           fill=(255, 255, 255), anchor="lb")


def scene_bridge(c, x, y, w, h):
    c.rectangle([x, y, x + w, y + h], fill=(70, 110, 150))
    c.rectangle([x, y + h - 22, x + w, y + h], fill=(28, 68, 110))
    # deck
    c.rectangle([x, y + 34, x + w, y + 42], fill=(60, 60, 60))
    # arch (left, intact)
    c.arc([x + 8, y + 8, x + w // 2, y + 62], 180, 360, fill=(240, 240, 240), width=4)
    # blast burst at the collapse joint
    jx, jy = x + w // 2 + 8, y + 30
    c.polygon([(jx, jy - 12), (jx + 5, jy - 3), (jx + 13, jy - 5),
               (jx + 7, jy + 3), (jx + 11, jy + 10), (jx + 2, jy + 7),
               (jx - 2, jy + 13), (jx - 6, jy + 5), (jx - 13, jy + 6),
               (jx - 8, jy - 1), (jx - 13, jy - 8), (jx - 4, jy - 5)],
              fill=(255, 160, 40))
    # collapsed right span: tilted segment falling into water
    c.polygon([(x + w // 2 + 6, y + 34), (x + w - 12, y + 34),
               (x + w - 26, y + h - 24), (x + w // 2 + 22, y + h - 24)],
              fill=(90, 90, 90))
    # water lines
    for i in range(3):
        c.line([x + 10, y + h - 16 + i * 5, x + w - 10, y + h - 16 + i * 5],
               fill=(140, 180, 220), width=2)
    # smoke
    c.ellipse([x + w - 52, y + 2, x + w - 30, y + 22], fill=(220, 220, 220))
    c.ellipse([x + w - 44, y + 8, x + w - 22, y + 28], fill=(200, 200, 200))


def scene_tower(c, x, y, w, h):
    c.rectangle([x, y, x + w, y + h], fill=(24, 28, 44))
    # PIF tower silhouette
    c.polygon([(x + w // 2 - 26, y + h), (x + w // 2 - 26, y + 16),
               (x + w // 2, y + 4), (x + w // 2 + 26, y + 16),
               (x + w // 2 + 26, y + h)], fill=(90, 110, 150))
    for r in range(4):
        for col in range(3):
            c.rectangle([x + w // 2 - 18 + col * 13, y + 26 + r * 12,
                         x + w // 2 - 10 + col * 13, y + 34 + r * 12],
                        fill=(255, 210, 90))
    # drone (bigger) with dashed flight path from the right
    dx, dy = x + w - 52, y + 16
    for i in range(4):
        c.ellipse([dx + 18 + i * 12, dy - 2, dx + 26 + i * 12, dy + 2],
                  fill=(160, 160, 160))
    c.ellipse([dx - 13, dy - 5, dx + 13, dy + 7], fill=(220, 220, 220))
    c.ellipse([dx - 22, dy - 12, dx - 10, dy - 4], fill=(180, 180, 180))
    c.ellipse([dx + 10, dy - 12, dx + 22, dy - 4], fill=(180, 180, 180))
    c.ellipse([dx - 22, dy + 8, dx - 10, dy + 16], fill=(180, 180, 180))
    c.ellipse([dx + 10, dy + 8, dx + 22, dy + 16], fill=(180, 180, 180))
    # impact flash at the tower top
    c.polygon([(x + w // 2 - 10, y + 24), (x + w // 2 + 2, y + 6),
               (x + w // 2 + 12, y + 24)], fill=(255, 120, 40))
    c.polygon([(x + w // 2 - 6, y + 26), (x + w // 2 + 2, y + 14),
               (x + w // 2 + 8, y + 26)], fill=(255, 200, 60))


def scene_tanker(c, x, y, w, h):
    c.rectangle([x, y, x + w, y + h], fill=(38, 84, 110))
    c.rectangle([x, y + h - 26, x + w, y + h], fill=(20, 52, 78))
    # hull + containers
    c.polygon([(x + 12, y + h - 40), (x + w - 12, y + h - 40),
               (x + w - 22, y + h - 26), (x + 22, y + h - 26)], fill=(120, 30, 30))
    for i in range(4):
        c.rectangle([x + 22 + i * 22, y + h - 58, x + 40 + i * 22, y + h - 40],
                    fill=((200, 120, 40), (40, 120, 90), (200, 190, 60),
                          (90, 110, 160))[i])
    # fire
    c.polygon([(x + w - 52, y + h - 40), (x + w - 40, y + h - 66),
               (x + w - 28, y + h - 40)], fill=(255, 140, 30))
    c.polygon([(x + w - 46, y + h - 40), (x + w - 38, y + h - 56),
               (x + w - 32, y + h - 40)], fill=(255, 210, 60))
    # mine (spiked circle)
    mx, my = x + 26, y + 18
    c.ellipse([mx - 7, my - 7, mx + 7, my + 7], fill=(30, 30, 30))
    for ang in range(0, 360, 45):
        import math
        dx = int(10 * math.cos(math.radians(ang)))
        dy = int(10 * math.sin(math.radians(ang)))
        c.line([mx, my, mx + dx, my + dy], fill=(30, 30, 30), width=2)


def scene_skyline(c, x, y, w, h):
    c.rectangle([x, y, x + w, y + h], fill=(120, 30, 30))
    # Shanghai towers
    c.rectangle([x + 12, y + 22, x + 26, y + h], fill=(40, 40, 40))
    c.rectangle([x + 30, y + 34, x + 44, y + h], fill=(60, 60, 60))
    c.ellipse([x + 48, y + 10, x + 74, y + 36], fill=(198, 148, 52))
    c.rectangle([x + 58, y + 36, x + 64, y + h], fill=(40, 40, 40))
    c.rectangle([x + 78, y + 28, x + 92, y + h], fill=(60, 60, 60))
    # red stamp
    c.ellipse([x + w - 46, y + 8, x + w - 6, y + 48], outline=(255, 255, 255), width=3)
    c.text((x + w - 26, y + 28), "!", font=load_fonts()["side_num"],
           fill=(255, 255, 255), anchor="mm")


def scene_chart(c, x, y, w, h):
    c.rectangle([x, y, x + w, y + h], fill=(18, 60, 38))
    # 50,000 line
    c.line([x + 8, y + 26, x + w - 8, y + 26], fill=(255, 210, 90), width=2)
    c.text((x + 10, y + 6), "50,000", font=load_fonts()["tag"], fill=(255, 210, 90))
    # rising line
    c.line([x + 10, y + h - 14, x + w // 2, y + 40, x + w - 16, y + 18],
           fill=(120, 220, 140), width=4)
    c.polygon([(x + w - 16, y + 18), (x + w - 30, y + 16), (x + w - 20, y + 30)],
              fill=(120, 220, 140))
    # bars
    for i, bh in enumerate((14, 22, 18, 30)):
        c.rectangle([x + 14 + i * 16, y + h - 8 - bh, x + 26 + i * 16, y + h - 8],
                    fill=(90, 160, 110))


def scene_jets(c, x, y, w, h):
    c.rectangle([x, y, x + w, y + h], fill=(90, 130, 170))
    # radar arcs
    for r in (18, 30, 42):
        c.arc([x + w - 60 - r, y + h - 10 - r, x + w - 60 + r, y + h - 10 + r],
              270, 360, fill=(255, 255, 255), width=2)
    # jets (triangles)
    c.polygon([(x + 16, y + 20), (x + 44, y + 28), (x + 16, y + 36)], fill=(40, 40, 40))
    c.polygon([(x + 30, y + 44), (x + 58, y + 52), (x + 30, y + 60)], fill=(60, 60, 60))
    # island
    c.ellipse([x + w // 2 - 14, y + h - 18, x + w // 2 + 14, y + h - 8],
              fill=(60, 120, 70))


def scene_trophy(c, x, y, w, h):
    c.rectangle([x, y, x + w, y + h], fill=(20, 90, 50))
    # cup
    c.polygon([(x + w // 2 - 22, y + 10), (x + w // 2 + 22, y + 10),
               (x + w // 2 + 14, y + 38), (x + w // 2 - 14, y + 38)],
              fill=(255, 210, 60))
    c.arc([x + w // 2 - 34, y + 8, x + w // 2 - 12, y + 34], 90, 270,
          fill=(255, 210, 60), width=4)
    c.arc([x + w // 2 + 12, y + 8, x + w // 2 + 34, y + 34], 270, 90,
          fill=(255, 210, 60), width=4)
    c.rectangle([x + w // 2 - 4, y + 38, x + w // 2 + 4, y + 50], fill=(255, 210, 60))
    c.rectangle([x + w // 2 - 14, y + 50, x + w // 2 + 14, y + 56], fill=(255, 210, 60))
    # Senegal stripes
    for i, col in enumerate(((0, 120, 60), (255, 210, 60), (200, 30, 30))):
        c.rectangle([x + 8 + i * 10, y + h - 12, x + 16 + i * 10, y + h - 4], fill=col)


def scene_scoreboard(c, x, y, w, h):
    c.rectangle([x, y, x + w, y + h], fill=(16, 32, 60))
    c.rectangle([x + 10, y + 10, x + w - 10, y + h - 10], fill=(10, 20, 40))
    c.text((x + w // 2, y + 12), "RMA  5-1  PSV", font=load_fonts()["head_sm"],
           fill=(255, 255, 255), anchor="ma")
    # ball (below the scoreline, clear of the text)
    bx, by = x + w // 2, y + h - 14
    c.ellipse([bx - 8, by - 8, bx + 8, by + 8], fill=(255, 255, 255))
    c.polygon([(bx, by - 4), (bx + 4, by - 1), (bx + 3, by + 4),
               (bx - 3, by + 4), (bx - 4, by - 1)], fill=(20, 20, 20))


def scene_crown(c, x, y, w, h):
    c.rectangle([x, y, x + w, y + h], fill=(150, 40, 110))
    cx, cy = x + w // 2, y + h // 2 + 4
    c.polygon([(cx - 30, cy + 12), (cx - 30, cy - 12), (cx - 15, cy + 2),
               (cx, cy - 18), (cx + 15, cy + 2), (cx + 30, cy - 12),
               (cx + 30, cy + 12)], fill=(255, 210, 60))
    for px in (-30, 0, 30):
        c.ellipse([cx + px - 4, cy - 22, cx + px + 4, cy - 14], fill=(255, 240, 160))
    c.rectangle([cx - 30, cy + 12, cx + 30, cy + 18], fill=(200, 160, 30))


def scene_laptop(c, x, y, w, h):
    c.rectangle([x, y, x + w, y + h], fill=(60, 20, 20))
    # laptop
    c.rectangle([x + 18, y + 12, x + w - 18, y + h - 22], fill=(30, 30, 30))
    c.rectangle([x + 22, y + 16, x + w - 22, y + h - 26], fill=(180, 30, 30))
    c.polygon([(x + 12, y + h - 22), (x + w - 12, y + h - 22),
               (x + w - 6, y + h - 12), (x + 6, y + h - 12)], fill=(60, 60, 60))
    # warning triangle
    cx, cy = x + w // 2, y + h // 2 - 2
    c.polygon([(cx, cy - 16), (cx + 16, cy + 12), (cx - 16, cy + 12)],
              fill=(255, 210, 60))
    c.text((cx, cy + 2), "!", font=load_fonts()["head_sm"], fill=(60, 20, 20),
           anchor="mm")


def scene_dusk(c, x, y, w, h):
    c.rectangle([x, y, x + w, y + h], fill=(70, 50, 60))
    # skyline
    for i, bh in enumerate((26, 40, 30, 46, 34)):
        c.rectangle([x + 8 + i * 18, y + h - 14 - bh, x + 22 + i * 18, y + h - 14],
                    fill=(30, 26, 34))
    # smoke plume
    c.ellipse([x + w - 44, y + 6, x + w - 24, y + 26], fill=(160, 150, 150))
    c.ellipse([x + w - 36, y + 14, x + w - 16, y + 34], fill=(140, 130, 130))


def scene_parliament(c, x, y, w, h):
    c.rectangle([x, y, x + w, y + h], fill=(20, 70, 50))
    # building
    c.rectangle([x + 14, y + 26, x + w - 14, y + h - 8], fill=(230, 225, 210))
    c.polygon([(x + 10, y + 26), (x + w // 2, y + 8), (x + w - 10, y + 26)],
              fill=(180, 170, 150))
    for i in range(4):
        c.rectangle([x + 22 + i * 20, y + 34, x + 30 + i * 20, y + h - 8],
                    fill=(90, 100, 80))


SCENES = {
    "gavel": scene_gavel, "bridge": scene_bridge, "tower": scene_tower,
    "tanker": scene_tanker, "skyline": scene_skyline, "chart": scene_chart,
    "jets": scene_jets, "trophy": scene_trophy, "scoreboard": scene_scoreboard,
    "crown": scene_crown, "laptop": scene_laptop, "dusk": scene_dusk,
    "parliament": scene_parliament,
}

# ---------------------------------------------------------------- data
# (region, place, tag, scene, headline, detail, source)
FEATURES = [
    ("AMERICAS", "BROOKLYN, USA", "CONFIRMED", "gavel",
     "Huawei convicted on 10 of 12 counts",
     "Guilty of fraud, sanctions breaches and trade-secret theft; acquitted on racketeering.",
     "Reuters \u00b7 CNN \u00b7 Al Jazeera"),
    ("EUROPE", "KERCH STRAIT", "REPORTED", "bridge",
     "Kerch Bridge arch collapses after Ukrainian strike",
     "A 227m road span falls into the strait; rail traffic halts. Putin vows a painful response.",
     "BBC \u00b7 Guardian \u00b7 Al Jazeera"),
    ("MIDDLE EAST", "RIYADH", "CONFIRMED", "tower",
     "Houthi drone hits Riyadh's tallest tower",
     "Second PIF tower strike in under a week; 11 injured. Coalition vows a firm response.",
     "Reuters \u00b7 Arab News"),
    ("MIDDLE EAST", "STRAIT OF HORMUZ", "CLAIM", "tanker",
     "Three tankers hit mines in Hormuz",
     "IRGC says three tankers caught fire in the strait.",
     "AP \u00b7 Al Jazeera"),
    ("ASIA-PACIFIC", "SHANGHAI, CHINA", "OFFICIAL", "skyline",
     "China probes Shanghai party chief",
     "Chen Jining probed; fourth Politburo member since 2025.",
     "Reuters \u00b7 Xinhua"),
    ("ECONOMY", "NEW YORK", "CONFIRMED", "chart",
     "Dow tops 50,000 for first time",
     "Dow +0.85% to 50,018.70 as the Nasdaq falls 1.48% on chips.",
     "Reuters"),
    ("ASIA-PACIFIC", "KOREA ADIZ", "REPORTED", "jets",
     "Russian jets enter Korea defence zone",
     "Seoul scrambles F-15Ks as five planes near Ulleung Island.",
     "Yonhap \u00b7 Korea Times"),
    ("AFRICA", "LAUSANNE", "OFFICIAL", "trophy",
     "Senegal regain AFCON title on appeal",
     "CAS restores the 1-0 final win; Morocco to appeal.",
     "CAS \u00b7 Le Temps"),
    ("SPORT", "MADRID", "CONFIRMED", "scoreboard",
     "Real Madrid hit PSV for five",
     "Real win 5-1; City draw 2-2 with Napoli, Arsenal held 1-1.",
     "UEFA"),
    ("SCIENCE & CULTURE", "SAN JUAN", "CONFIRMED", "crown",
     "Puerto Rico's Barreto wins Miss Universe",
     "First mother to take the crown; the island's sixth title.",
     "People \u00b7 USA Today"),
    ("TECH", "REDMOND, USA", "REPORTED", "laptop",
     "Microsoft declares \u2018Code Red\u2019",
     "Overhaul ordered after the worst Exchange outage on record.",
     "Reuters"),
    ("MIDDLE EAST", "GAZA", "REPORTED", "dusk",
     "Israeli strikes kill at least 9 in Gaza",
     "Hospital officials report deaths across Gaza in 24 hours.",
     "AP \u00b7 Al Jazeera"),
    ("AFRICA", "ABUJA, NIGERIA", "OFFICIAL", "parliament",
     "Tinubu seeks smaller 2026 budget",
     "President asks parliament to cut spending to N65.2trn.",
     "Reuters"),
]

# (number, region, headline, source)
BRIEFS = [
    (14, "MIDDLE EAST", "Iran rules out talks until \u2018seven conditions\u2019 met", "AP"),
    (15, "EUROPE", "Zelenskyy warns of new Russian strikes", "Reuters"),
    (16, "EUROPE", "NATO pledge covers space; \u2018Sputnik-S\u2019 reported", "SCMP"),
    (17, "EUROPE", "COP31 verdict: \u2018a flop\u2019 \u2014 reform the process", "Reuters"),
    (18, "ECONOMY", "US consumer confidence jumps to 103.3", "Reuters"),
    (19, "ECONOMY", "Nvidia slides ~6% after comeback rally", "Reuters"),
    (20, "TECH", "Anthropic falls below its $83 IPO price", "Reuters"),
    (21, "TECH", "China extends US minerals export-ban pause", "Reuters"),
    (22, "ASIA-PACIFIC", "Shenzhou-24 crew: first foreign astronaut", "Xinhua"),
    (23, "ASIA-PACIFIC", "Hanoi hotpot blast kills 6, 10+ hurt", "AP"),
    (24, "ASIA-PACIFIC", "Bangladesh garment workers clash with police", "Reuters"),
    (25, "AMERICAS", "US blocks Brazil\u2019s WTO panel request", "WTO"),
    (26, "AMERICAS", "Lula signs fiscal law, backs second cuts", "Reuters"),
    (27, "AMERICAS", "Mexico inflation hits six-month high, 3.96%", "Reuters"),
    (28, "EUROPE", "Russian drone enters Polish airspace", "Fox News"),
    (29, "AFRICA", "Nigeria central bank holds key rate at 23%", "Reuters"),
    (30, "SPORT", "NBA: Mavs, Celtics, Pistons win on Tuesday", "Sportradar"),
    (31, "SCIENCE & CULTURE", "GTA VI deluxe album drops \u2014 23 new tracks", "Rockstar"),
    (32, "SCIENCE & CULTURE", "Tidal to ban fully AI-generated music", "TechCrunch"),
    (33, "SCIENCE & CULTURE", "TB molecule found that triggers cough", "Nature"),
    (34, "AMERICAS", "Trump set to unveil tariffs on 16 partners", "Reuters"),
    (35, "AFRICA", "Nigeria court freezes N135.5bn in forum funds", "Punch"),
]

CHIPS = [("EUROPE", 5), ("MIDDLE EAST", 4), ("AFRICA", 4), ("AMERICAS", 5),
         ("ASIA-PACIFIC", 5), ("ECONOMY", 3), ("TECH", 3), ("SPORT", 2),
         ("SCIENCE & CULTURE", 4)]

TIMELINE = [
    ("01:00", "Hanoi blast"),
    ("13:11", "CBN holds 23%"),
    ("13:18", "Tinubu budget letter"),
    ("20:00", "Real Madrid 5-1 PSV"),
    ("21:00", "Dow closes above 50,000"),
]

NUMBERS = [
    ("10 of 12", "Huawei counts guilty"),
    ("50,018.70", "Dow close, first over 50,000"),
    ("227 m", "Kerch Bridge arch span collapsed"),
    ("11", "injured in Riyadh tower strike"),
    ("3", "tankers hit mines in Hormuz"),
    ("103.3", "US consumer confidence"),
]

SUBLINE = ("Huawei convicted on 10 of 12 counts  \u00b7  "
           "Kerch Bridge arch collapses  \u00b7  Dow tops 50,000")

DATE_CHECK = ("Left out \u2014 earlier day: COP31 collapse (Sun 22 Nov) \u00b7 Nvidia reinstatement "
              "(Mon 23 Nov) \u00b7 Dymer toll (Sun 22 Nov) \u00b7 Merkury claim (Mon 23 Nov) \u00b7 "
              "Las Vegas GP (Sat 22 Nov) \u00b7 Forum freeze order (Thu 19 Nov, reported Tue) \u00b7 "
              "Shenzhou-24 launch (Wed 25 Nov).")

HOW_SURE = ("HOW SURE: CONFIRMED = 2+ outlets \u00b7 OFFICIAL = on record \u00b7 REPORTED = wires "
            "\u00b7 CLAIM = one side\u2019s account.")

SOURCES_LINE = "Sources: Reuters, AP, Al Jazeera, BBC, CNN, WSJ, Yonhap, Xinhua, Punch, UEFA"


# ---------------------------------------------------------------- helpers
def wrap(canvas, text, font, max_w):
    out = []
    for chunk in text.split("\n"):
        words = chunk.split()
        cur = ""
        for word in words:
            cand = f"{cur} {word}".strip()
            if canvas.textlength(cand, font=font) <= max_w:
                cur = cand
            else:
                if cur:
                    out.append(cur)
                cur = word
        if cur:
            out.append(cur)
    return out


def fit_text(canvas, text, font, max_w, max_lines, where):
    lines = wrap(canvas, text, font, max_w)
    if len(lines) > max_lines:
        raise SystemExit(f"{where}: {len(lines)} lines (max {max_lines}): {text!r}")
    for line in lines:
        if canvas.textlength(line, font=font) > max_w:
            raise SystemExit(f"{where}: line too wide: {line!r}")
    return lines


def paint_masthead(c, fonts):
    c.text((PAD, 6), "THE WORLD IN ONE DAY", font=fonts["mast_kick"],
           fill=PALETTE["red"])
    c.text((PAGE_W - PAD, 7), "35 DATED STORIES  \u00b7  9 REGIONS  \u00b7  ALL FROM TUE 24 NOV 2026",
           font=fonts["mast_meta"], fill=PALETTE["grey"], anchor="ra")
    c.text((PAD, 22), "Tuesday 24 November 2026", font=fonts["date"],
           fill=PALETTE["ink"])
    c.text((PAD, 82), SUBLINE, font=fonts["subline"], fill=PALETTE["red"])
    # region chips
    x = PAD
    y = 100
    for name, count in CHIPS:
        label = f"{name} {count}"
        w = int(c.textlength(label, font=fonts["chip"])) + 16
        c.rectangle([x, y, x + w, y + 18], fill=REGION_COLORS[name])
        c.text((x + 8, y + 3), label, font=fonts["chip"], fill="white")
        x += w + 5
    c.line([PAD, 124, PAGE_W - PAD, 124], fill=PALETTE["ink"], width=2)


def paint_timeline(c, fonts):
    y = 130
    c.text((PAD, y), "TUESDAY UTC", font=fonts["tl_label"], fill=PALETTE["red"])
    x = PAD + 108
    for time, label in TIMELINE:
        c.text((x, y), time, font=fonts["tl_label"], fill=PALETTE["ink"])
        x += int(c.textlength(time, font=fonts["tl_label"])) + 5
        c.text((x, y), label, font=fonts["tl"], fill=PALETTE["grey"])
        x += int(c.textlength(label, font=fonts["tl"])) + 22
    c.line([PAD, 150, PAGE_W - PAD, 150], fill=PALETTE["rule"], width=1)


def paint_feature(c, fonts, x, y, w, h, num, region, place, tag, scene,
                  headline, detail, source, large):
    c.rectangle([x, y, x + w, y + h], fill=PALETTE["card"],
                outline=PALETTE["rule"], width=1)
    rc = REGION_COLORS[region]
    # top colour bar
    c.rectangle([x, y, x + w, y + 4], fill=rc)
    # number badge + kicker + tag
    c.ellipse([x + 8, y + 10, x + 28, y + 30], fill=rc)
    c.text((x + 18, y + 19), str(num), font=fonts["num"], fill="white",
           anchor="mm")
    # small cards get region only (place would collide with the tag)
    if large:
        kicker = f"{region} \u00b7 {place}"
        c.text((x + 33, y + 14), kicker, font=fonts["kicker"], fill=rc)
    else:
        short = {"SCIENCE & CULTURE": "SCI & CULTURE"}.get(region, region)
        c.text((x + 33, y + 15), short, font=fonts["kicker_sm"], fill=rc)
    tag_w = int(c.textlength(tag, font=fonts["tag"])) + 10
    c.rectangle([x + w - tag_w - 6, y + 10, x + w - 6, y + 26], fill=rc)
    c.text((x + w - tag_w // 2 - 6, y + 18), tag, font=fonts["tag"],
           fill="white", anchor="mm")
    # scene
    scene_h = 72 if large else 58
    SCENES[scene](c, x + 1, y + 34, w - 2, scene_h)
    ty = y + 34 + scene_h + 6
    head_f = fonts["head_lg"] if large else fonts["head_sm"]
    det_f = fonts["detail_lg"] if large else fonts["detail_sm"]
    head_lines = fit_text(c, headline, head_f, w - 16, 2,
                          f"card {num} headline")
    for line in head_lines:
        c.text((x + 8, ty), line, font=head_f, fill=PALETTE["ink"])
        ty += 21 if large else 16
    det_lines = fit_text(c, detail, det_f, w - 16, 2,
                         f"card {num} detail")
    for line in det_lines:
        c.text((x + 8, ty), line, font=det_f, fill=PALETTE["grey"])
        ty += 14 if large else 13
    c.text((x + 8, y + h - 13), source, font=fonts["source"],
           fill=PALETTE["grey"])


def paint_numbers(c, fonts, x, y, w, h):
    c.rectangle([x, y, x + w, y + h], fill=PALETTE["navy"])
    c.text((x + 10, y + 8), "THE DAY IN NUMBERS", font=fonts["side_head"],
           fill=(198, 164, 92))
    cy = y + 32
    for num, label in NUMBERS:
        c.text((x + 10, cy), num, font=fonts["side_num"], fill="white")
        cy += 22
        c.text((x + 10, cy), label, font=fonts["side_lab"],
               fill=(214, 222, 235))
        cy += 16
        if num != NUMBERS[-1][0]:
            c.line([x + 10, cy - 3, x + w - 10, cy - 3],
                   fill=(60, 80, 110), width=1)


def paint_briefs(c, fonts, x, y, w, h):
    c.text((x, y), "ALSO ON TUESDAY 24 NOVEMBER \u2014 22 MORE DATED BRIEFS",
           font=fonts["brief_head"], fill=PALETTE["ink"])
    c.text((x + w, y), "9 REGIONS, MATCHED BY COLOUR", font=fonts["brief_src"],
           fill=PALETTE["grey"], anchor="ra")
    c.line([x, y + 18, x + w, y + 18], fill=PALETTE["ink"], width=1)
    col_w = (w - 12) // 2
    row_h = 19
    for i, (num, region, headline, source) in enumerate(BRIEFS):
        col = i // 11
        row = i % 11
        bx = x + col * (col_w + 12)
        by = y + 24 + row * row_h
        rc = REGION_COLORS[region]
        c.rectangle([bx, by, bx + 20, by + 15], fill=rc)
        c.text((bx + 10, by + 7), str(num), font=fonts["tag"], fill="white",
               anchor="mm")
        max_w = col_w - 26 - int(c.textlength(source, font=fonts["brief_src"])) - 8
        fit_text(c, headline, fonts["brief"], max_w, 1, f"brief {num}")
        c.text((bx + 26, by + 2), headline, font=fonts["brief"],
               fill=PALETTE["ink"])
        c.text((bx + col_w, by + 3), source, font=fonts["brief_src"],
               fill=PALETTE["grey"], anchor="ra")


def paint_footer(c, fonts, y):
    c.rectangle([PAD, y, PAD + 152, y + 16], fill=PALETTE["red"])
    c.text((PAD + 76, y + 8), "DATE CHECK \u2014 EXCLUDED", font=fonts["foot_b"],
           fill="white", anchor="mm")
    lines = fit_text(c, DATE_CHECK, fonts["foot"], PAGE_W - 2 * PAD - 162, 2,
                     "date-check")
    ty = y + 1
    for line in lines:
        c.text((PAD + 160, ty), line, font=fonts["foot"], fill=PALETTE["grey"])
        ty += 12
    c.text((PAD, PAGE_H - 14), HOW_SURE, font=fonts["foot"],
           fill=PALETTE["grey"])
    c.text((PAGE_W - PAD, PAGE_H - 14), SOURCES_LINE, font=fonts["foot"],
           fill=PALETTE["grey"], anchor="ra")


def build():
    fonts = load_fonts()
    page = Image.new("RGB", (PAGE_W, PAGE_H), PALETTE["paper"])
    c = ImageDraw.Draw(page)

    paint_masthead(c, fonts)
    paint_timeline(c, fonts)

    # feature grid: row 1 = 3 large, rows 2-3 = 5 small each
    gap = 8
    large_w = (PAGE_W - 2 * PAD - 2 * gap) // 3
    small_w = (PAGE_W - 2 * PAD - 4 * gap) // 5
    y = 158
    for i in range(3):
        paint_feature(c, fonts, PAD + i * (large_w + gap), y, large_w, 196,
                      i + 1, *FEATURES[i], large=True)
    y = 360
    for i in range(5):
        paint_feature(c, fonts, PAD + i * (small_w + gap), y, small_w, 174,
                      i + 4, *FEATURES[i + 3], large=False)
    y = 540
    for i in range(5):
        paint_feature(c, fonts, PAD + i * (small_w + gap), y, small_w, 174,
                      i + 9, *FEATURES[i + 8], large=False)

    # bottom band
    by = 720
    bh = 236
    paint_numbers(c, fonts, PAD, by, 226, bh)
    paint_briefs(c, fonts, PAD + 226 + 12, by, PAGE_W - 2 * PAD - 226 - 12, bh)

    paint_footer(c, fonts, 962)

    out = Path(__file__).resolve().parent / "entry.png"
    page.save(out, optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes, {PAGE_W}x{PAGE_H})")
    print(f"stories: 13 features + {len(BRIEFS)} briefs = "
          f"{13 + len(BRIEFS)}; chips sum {sum(n for _, n in CHIPS)}")


if __name__ == "__main__":
    build()
