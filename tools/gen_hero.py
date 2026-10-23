#!/usr/bin/env python3
"""Generate the profile hero banner (assets/profile-hero.svg).

A dark-navy, cyan/violet/teal hero with a generative-model motif, an animated
gradient rail, a shine sweep on the name, and a stats band along the bottom.
Pure vector + SMIL so it animates when served as an <img> source on GitHub.
"""
from pathlib import Path
from xml.sax.saxutils import escape

W, H = 1440, 430
MX, MY = 1128, 168          # monogram medallion centre
FONT = "Inter, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'SF Mono', Menlo, Consolas, monospace"

# name: 13 chars at 68px bold with -1.6 tracking -> ~593px wide
NAME_W = 593

# bottom band: who I am, not what I shipped — keep this project-agnostic
STATS = [
    ("AI / ML", "RESEARCH & DEVELOPMENT"),
    ("TYPESCRIPT", "PRODUCT ENGINEERING"),
    ("PYTHON", "MODELS & PIPELINES"),
    ("WORLDWIDE", "OPEN TO COLLABORATE"),
]

NODES = [
    (928, 96), (1012, 58), (1092, 108), (1186, 66), (1272, 118), (1352, 76),
    (960, 168), (1052, 208), (1140, 160), (1226, 214), (1312, 168), (1382, 220),
    (908, 252), (1000, 288), (1096, 246), (1188, 292), (1280, 250), (1362, 292),
]

EDGES = [
    (0, 1), (1, 2), (2, 3), (3, 4), (4, 5),
    (0, 6), (1, 7), (2, 8), (3, 9), (4, 10), (5, 11),
    (6, 7), (7, 8), (8, 9), (9, 10), (10, 11),
    (6, 12), (7, 13), (8, 14), (9, 15), (10, 16), (11, 17),
    (12, 13), (13, 14), (14, 15), (15, 16), (16, 17),
]

TRACES = [
    [0, 1, 7, 8, 9, 15, 16],
    [2, 3, 9, 10, 11],
    [12, 13, 7, 6],
]


def node_points(idx):
    return " ".join(f"{NODES[i][0]},{NODES[i][1]}" for i in idx)


def build() -> str:
    edges = "\n".join(
        f'    <line x1="{NODES[a][0]}" y1="{NODES[a][1]}" x2="{NODES[b][0]}" y2="{NODES[b][1]}"/>'
        for a, b in EDGES
    )
    dots = "\n".join(
        f'    <circle cx="{x}" cy="{y}" r="{3.6 if i % 3 else 4.6}"/>'
        for i, (x, y) in enumerate(NODES)
    )
    traces = "\n".join(
        f'''    <polyline points="{node_points(t)}" stroke-dasharray="110 900">
      <animate attributeName="stroke-dashoffset" values="1010;-160" dur="{4.6 + i * 1.3}s" begin="{i * 0.9}s" repeatCount="indefinite"/>
    </polyline>'''
        for i, t in enumerate(TRACES)
    )
    stats = []
    for i, (value, label) in enumerate(STATS):
        cx = 90 + i * 360
        stats.append(
            f'''    <text x="{cx}" y="390" text-anchor="middle" font-size="23" font-weight="800" letter-spacing="-.2" fill="#f1f6ff">{escape(value)}</text>
    <text x="{cx}" y="411" text-anchor="middle" font-size="9.5" font-weight="700" letter-spacing="2" fill="#8aa2c4">{escape(label)}</text>'''
        )
        if i:
            stats.append(
                f'    <line x1="{cx - 180}" y1="368" x2="{cx - 180}" y2="414" stroke="#7f9dc4" stroke-opacity=".18"/>'
            )
    stats_block = "\n".join(stats)

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="heroTitle heroDesc">
  <title id="heroTitle">Rishi Raj DEV — AI / ML Researcher and Full-Stack Engineer</title>
  <desc id="heroDesc">Dark navy hero banner with cyan, violet and teal gradients, an animated neural network motif, the name Rishi Raj DEV, an RD monogram medallion with orbiting rings, role tags, technology tags and an identity band.</desc>

  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#070b18"/>
      <stop offset="46%" stop-color="#131634"/>
      <stop offset="100%" stop-color="#04222f"/>
    </linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#22d3ee"/>
      <stop offset="48%" stop-color="#a855f7"/>
      <stop offset="100%" stop-color="#2dd4bf"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="-360 0;360 0;-360 0" dur="11s" repeatCount="indefinite"/>
    </linearGradient>
    <linearGradient id="accentSoft" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#22d3ee" stop-opacity=".05"/>
      <stop offset="50%" stop-color="#a855f7" stop-opacity=".5"/>
      <stop offset="100%" stop-color="#2dd4bf" stop-opacity=".05"/>
    </linearGradient>
    <linearGradient id="nameFill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#cfdef7"/>
    </linearGradient>
    <linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="50%" stop-color="#ffffff" stop-opacity=".92"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0" dur="5.5s" repeatCount="indefinite"/>
    </linearGradient>
    <linearGradient id="fadeRight" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#0b1020" stop-opacity="0"/>
      <stop offset="72%" stop-color="#0b1020" stop-opacity=".72"/>
      <stop offset="100%" stop-color="#0b1020" stop-opacity=".94"/>
    </linearGradient>
    <radialGradient id="glowViolet" cx="78%" cy="26%" r="62%">
      <stop offset="0%" stop-color="#7c3aed" stop-opacity=".38"/>
      <stop offset="100%" stop-color="#7c3aed" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="medGlow" cx="50%" cy="32%" r="68%">
      <stop offset="0%" stop-color="#a855f7" stop-opacity=".3"/>
      <stop offset="62%" stop-color="#22d3ee" stop-opacity=".07"/>
      <stop offset="100%" stop-color="#22d3ee" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glowCyan" cx="12%" cy="88%" r="58%">
      <stop offset="0%" stop-color="#06b6d4" stop-opacity=".26"/>
      <stop offset="100%" stop-color="#06b6d4" stop-opacity="0"/>
    </radialGradient>
    <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse">
      <path d="M30 0H0V30" fill="none" stroke="#9cc3ff" stroke-opacity=".075" stroke-width="1"/>
    </pattern>
    <pattern id="dots" width="14" height="14" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1" fill="#9cc3ff" fill-opacity=".14"/>
    </pattern>
    <filter id="soft" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="26"/>
    </filter>
    <filter id="tight" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="7"/>
    </filter>
    <clipPath id="nameClip">
      <text x="74" y="182" font-family="{FONT}" font-size="68" font-weight="800" letter-spacing="-1.6">RISHI RAJ DEV</text>
    </clipPath>
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="26"/></clipPath>
  </defs>

  <g clip-path="url(#frame)" font-family="{FONT}">
    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    <rect width="{W}" height="{H}" fill="url(#grid)"/>
    <rect width="{W}" height="{H}" fill="url(#glowViolet)"/>
    <rect width="{W}" height="{H}" fill="url(#glowCyan)"/>

    <ellipse cx="1150" cy="92" rx="230" ry="110" fill="#06b6d4" opacity=".13" filter="url(#soft)"/>
    <ellipse cx="980" cy="270" rx="200" ry="96" fill="#a855f7" opacity=".13" filter="url(#soft)"/>

    <!-- generative-model network motif -->
    <g fill="none" stroke="url(#accentSoft)" stroke-width="1.3" stroke-opacity=".85">
{edges}
    </g>
    <g fill="#67e8f9" fill-opacity=".9">
{dots}
    </g>
    <g fill="none" stroke="#a5f3fc" stroke-width="2.2" stroke-opacity=".8" stroke-linecap="round" stroke-linejoin="round">
{traces}
    </g>
    <g fill="#c4b5fd">
      <circle cx="1226" cy="214" r="3" filter="url(#tight)">
        <animate attributeName="opacity" values=".2;1;.2" dur="3.4s" repeatCount="indefinite"/>
      </circle>
      <circle cx="1012" cy="58" r="3" filter="url(#tight)">
        <animate attributeName="opacity" values="1;.2;1" dur="4.2s" repeatCount="indefinite"/>
      </circle>
    </g>
    <rect x="700" y="0" width="740" height="{H}" fill="url(#fadeRight)" opacity=".55"/>

    <!-- monogram medallion: the identity anchor, drawn over the network -->
    <g>
      <circle cx="{MX}" cy="{MY}" r="122" fill="#7c3aed" opacity=".2" filter="url(#soft)"/>
      <circle cx="{MX}" cy="{MY}" r="108" fill="none" stroke="url(#accent)" stroke-opacity=".5" stroke-width="1.6" stroke-dasharray="4 11">
        <animateTransform attributeName="transform" type="rotate" values="0 {MX} {MY};360 {MX} {MY}" dur="46s" repeatCount="indefinite"/>
      </circle>
      <circle cx="{MX}" cy="{MY}" r="95" fill="none" stroke="#22d3ee" stroke-opacity=".22" stroke-width="1" stroke-dasharray="28 16">
        <animateTransform attributeName="transform" type="rotate" values="360 {MX} {MY};0 {MX} {MY}" dur="32s" repeatCount="indefinite"/>
      </circle>
      <circle cx="{MX}" cy="{MY}" r="84" fill="#070c19" fill-opacity=".97" stroke="#8fb3dd" stroke-opacity=".26"/>
      <circle cx="{MX}" cy="{MY}" r="84" fill="url(#medGlow)"/>
      <circle cx="{MX}" cy="{MY}" r="84" fill="none" stroke="url(#accent)" stroke-opacity=".45" stroke-width="2"/>
      <text x="{MX}" y="{MY + 23}" text-anchor="middle" font-size="62" font-weight="800" letter-spacing="-1" fill="url(#accent)">RD</text>
      <circle cx="{MX + 108}" cy="{MY}" r="4.6" fill="#67e8f9">
        <animateTransform attributeName="transform" type="rotate" values="0 {MX} {MY};360 {MX} {MY}" dur="18s" repeatCount="indefinite"/>
      </circle>
      <circle cx="{MX - 95}" cy="{MY}" r="3.4" fill="#c4b5fd">
        <animateTransform attributeName="transform" type="rotate" values="360 {MX} {MY};0 {MX} {MY}" dur="26s" repeatCount="indefinite"/>
      </circle>
      <rect x="{MX - 82}" y="292" width="164" height="26" rx="13" fill="#0b1424" fill-opacity=".92" stroke="#2f4a6d"/>
      <text x="{MX}" y="309" text-anchor="middle" font-size="10.5" font-weight="700" letter-spacing="1.8" fill="#a9c4e4">INDIA · UTC+5:30</text>
    </g>

    <!-- status chip -->
    <rect x="74" y="48" width="330" height="34" rx="17" fill="#0e1a30" stroke="#2f4a6d"/>
    <circle cx="96" cy="65" r="5" fill="#34d399">
      <animate attributeName="opacity" values="1;.25;1" dur="2.1s" repeatCount="indefinite"/>
    </circle>
    <circle cx="96" cy="65" r="5" fill="none" stroke="#34d399" stroke-opacity=".5">
      <animate attributeName="r" values="5;12" dur="2.1s" repeatCount="indefinite"/>
      <animate attributeName="stroke-opacity" values=".5;0" dur="2.1s" repeatCount="indefinite"/>
    </circle>
    <text x="112" y="70" font-size="11.5" font-weight="700" letter-spacing="2.4" fill="#a9c4e4">OPEN TO COLLABORATE</text>
    <rect x="300" y="57" width="90" height="17" rx="8.5" fill="#132a44" stroke="#3a5c82"/>
    <text x="345" y="69" text-anchor="middle" font-size="9.5" font-weight="800" letter-spacing="1.4" fill="#7dd3fc">2026</text>

    <!-- name -->
    <text x="74" y="182" font-size="68" font-weight="800" letter-spacing="-1.6" fill="url(#nameFill)">RISHI RAJ DEV</text>
    <g clip-path="url(#nameClip)">
      <rect x="-340" y="118" width="210" height="80" fill="url(#shine)" opacity=".55">
        <animate attributeName="x" values="-340;{NAME_W + 180}" dur="5.5s" repeatCount="indefinite"/>
      </rect>
    </g>

    <!-- animated gradient rail -->
    <rect x="76" y="202" width="{NAME_W - 2}" height="6" rx="3" fill="url(#accent)"/>

    <!-- role line -->
    <text x="74" y="249" font-size="22" font-weight="600" fill="#e2ecfb">AI / ML / AGI Researcher</text>
    <text x="326" y="249" font-size="22" font-weight="600" fill="#4f6a8c">·</text>
    <text x="346" y="249" font-size="22" font-weight="600" fill="#e2ecfb">Generative Models</text>
    <text x="524" y="249" font-size="22" font-weight="600" fill="#4f6a8c">·</text>
    <text x="544" y="249" font-size="22" font-weight="600" fill="#e2ecfb">Full-Stack Engineering</text>

    <!-- stack tags -->
    <g font-family="{MONO}" font-size="12" font-weight="600" letter-spacing=".2">
      <rect x="74" y="276" width="204" height="30" rx="8" fill="#0d1729" fill-opacity=".9" stroke="#2b4468"/>
      <text x="88" y="296" fill="#7dd3fc">python · pytorch</text>
      <rect x="290" y="276" width="238" height="30" rx="8" fill="#0d1729" fill-opacity=".9" stroke="#2b4468"/>
      <text x="304" y="296" fill="#c4b5fd">typescript · react · node</text>
      <rect x="540" y="276" width="192" height="30" rx="8" fill="#0d1729" fill-opacity=".9" stroke="#2b4468"/>
      <text x="554" y="296" fill="#5eead4">ai / ml research</text>
    </g>
    <text x="74" y="325" font-size="12" font-weight="600" letter-spacing="2.6" fill="#7d97b8">BUILD CAREFULLY   /   MEASURE HONESTLY   /   KEEP SHIPPING</text>

    <!-- stats band -->
    <line x1="60" y1="356" x2="1380" y2="356" stroke="#8fb3dd" stroke-opacity=".16"/>
    <rect x="60" y="357" width="1320" height="72" rx="18" fill="#080e1d" fill-opacity=".55" stroke="#7f9dc4" stroke-opacity=".12"/>
{stats_block}

    <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="25" fill="none" stroke="#9db8dd" stroke-opacity=".22"/>
    <rect x="0" y="{H - 6}" width="{W}" height="6" rx="3" fill="url(#accent)"/>
  </g>
</svg>
'''


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets" / "profile-hero.svg"
    out.write_text(build(), encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size} bytes)")
