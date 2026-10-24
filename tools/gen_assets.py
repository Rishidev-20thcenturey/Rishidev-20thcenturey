#!/usr/bin/env python3
"""Generate the profile README's supporting artwork.

Three kinds of asset, all self-contained vector + SMIL (animates when served as
an <img> source on GitHub, makes no external requests, crisp at any width):

  header-NN-<slug>.svg   numbered section headers  -> the design system
  divider.svg            animated hairline         -> connective tissue
  terminal.svg           typewriter terminal card  -> the signature moment

Usage:  python3 tools/gen_assets.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

ASSETS = Path(__file__).resolve().parent.parent / "assets"
FONT = "Inter, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'SF Mono', Menlo, Consolas, monospace"

HEADERS = [
    ("01", "about", "ABOUT ME", "#22d3ee", "#a855f7"),
    ("02", "how", "HOW I WORK", "#a855f7", "#f0abfc"),
    ("03", "stack", "TECH STACK", "#2dd4bf", "#22d3ee"),
    ("04", "activity", "GITHUB ACTIVITY", "#818cf8", "#22d3ee"),
    ("05", "collaborate", "LET'S COLLABORATE", "#34d399", "#22d3ee"),
]


# --------------------------------------------------------------------------- #
# numbered section headers
# --------------------------------------------------------------------------- #
def build_header(num: str, label: str, accent: str, accent2: str) -> str:
    fs = 23
    text_w = int(len(label) * fs * 0.70 + len(label) * 5.6)
    w = 76 + text_w + 132
    h = 62
    rule_x = 76 + text_w + 20
    rule_w = max(w - rule_x - 30, 20)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Section {num}: {escape(label)}">
  <defs>
    <linearGradient id="hbg" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#0c1322"/>
      <stop offset="72%" stop-color="#0c1322" stop-opacity=".45"/>
      <stop offset="100%" stop-color="#0c1322" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="hnum" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{accent}"/>
      <stop offset="100%" stop-color="{accent2}"/>
    </linearGradient>
    <linearGradient id="hrule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{accent}" stop-opacity=".75"/>
      <stop offset="60%" stop-color="{accent2}" stop-opacity=".22"/>
      <stop offset="100%" stop-color="{accent2}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect x="0" y="0" width="{w}" height="{h}" rx="14" fill="url(#hbg)"/>
  <rect x="14" y="14" width="46" height="34" rx="10" fill="url(#hnum)" fill-opacity=".16" stroke="{accent}" stroke-opacity=".5"/>
  <text x="37" y="37" text-anchor="middle" font-family="{MONO}" font-size="14" font-weight="700" fill="{accent2}">{num}</text>
  <text x="76" y="40" font-family="{FONT}" font-size="{fs}" font-weight="800" letter-spacing="2.4" fill="#eef4ff">{escape(label)}</text>
  <rect x="{rule_x}" y="30" width="{rule_w}" height="2.5" rx="1.25" fill="url(#hrule)"/>
  <circle cx="{w - 16}" cy="31" r="3.6" fill="{accent}">
    <animate attributeName="opacity" values="1;.15;1" dur="2.8s" repeatCount="indefinite"/>
  </circle>
  <rect x="0" y="{h - 1}" width="{w * 0.42:.0f}" height="1" fill="{accent}" opacity=".35"/>
</svg>
'''


# --------------------------------------------------------------------------- #
# animated divider (contains no text, so it stays correct at any scale)
# --------------------------------------------------------------------------- #
def build_divider() -> str:
    w, h = 1200, 14
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="presentation" aria-hidden="true">
  <defs>
    <linearGradient id="dfade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#22d3ee" stop-opacity="0"/>
      <stop offset="18%" stop-color="#22d3ee" stop-opacity=".5"/>
      <stop offset="50%" stop-color="#a855f7" stop-opacity=".65"/>
      <stop offset="82%" stop-color="#2dd4bf" stop-opacity=".5"/>
      <stop offset="100%" stop-color="#2dd4bf" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="dsweep" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="50%" stop-color="#ffffff" stop-opacity=".95"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="dclip"><rect x="0" y="6" width="{w}" height="2"/></clipPath>
  </defs>
  <rect x="0" y="6" width="{w}" height="2" fill="url(#dfade)"/>
  <g clip-path="url(#dclip)">
    <rect x="-260" y="6" width="260" height="2" fill="url(#dsweep)">
      <animate attributeName="x" values="-260;{w}" dur="4.6s" repeatCount="indefinite"/>
    </rect>
  </g>
  <g transform="translate(600 7)">
    <rect x="-4.5" y="-4.5" width="9" height="9" rx="1.5" fill="#0b1020" stroke="#a855f7" stroke-opacity=".85">
      <animateTransform attributeName="transform" type="rotate" values="45;225" dur="9s" repeatCount="indefinite"/>
    </rect>
  </g>
  <circle cx="562" cy="7" r="2" fill="#22d3ee" opacity=".8"/>
  <circle cx="638" cy="7" r="2" fill="#2dd4bf" opacity=".8"/>
</svg>
'''


# --------------------------------------------------------------------------- #
# typewriter terminal card
# --------------------------------------------------------------------------- #
P, C, V, M, W, D = "#34d399", "#7dd3fc", "#c4b5fd", "#9fb4cf", "#e8f0fc", "#5c7595"
OK, WAIT = "#34d399", "#fbbf24"

# (indent_in_chars, [(text, colour), ...])
LINES = [
    (0, [("rishi@dev", P), (" ~ ", D), ("%", W), ("  whoami", C)]),
    (2, [("→", V), ("  ai / ml researcher", W), ("   ·", D), ("   full-stack engineer", W)]),
    (0, []),
    (0, [("rishi@dev", P), (" ~ ", D), ("%", W), ("  cat focus.txt", C)]),
    (2, [("generative models", M), ("        ", D), ("diffusion research", M)]),
    (2, [("typed realtime systems", M), ("    ", D), ("low-compute training", M)]),
    (0, []),
    (0, [("rishi@dev", P), (" ~ ", D), ("%", W), ("  ./ship --honest", C)]),
    (2, [("[ok]", OK), (" build carefully", M), ("      ", D), ("[ok]", OK), (" measure honestly", M)]),
    (2, [("[ok]", OK), (" keep shipping", M), ("         ", D), ("[..]", WAIT), (" status: open to collaborate", V)]),
]

FS = 14.5
CW = FS * 0.602          # monospace advance width
LH = 26
X0 = 30
Y0 = 80
CYCLE = 15.0             # seconds per full typing loop
TW, TH = 900, 400        # terminal card size


def _chars(line) -> int:
    return sum(len(t) for t, _ in line[1])


def build_terminal() -> str:
    # The script types across 0..0.74 of the loop, each line taking a slice
    # proportional to its character count; everything then holds until the loop.
    weights = [max(_chars(ln), 3) for ln in LINES]
    total = sum(weights)
    spans, cursor = [], 0.0
    for wt in weights:
        share = (wt / total) * 0.74
        spans.append((cursor, min(cursor + share, 0.74)))
        cursor += share

    body = []
    for i, ((indent, segs), (s, e)) in enumerate(zip(LINES, spans)):
        y = Y0 + i * LH
        if not _chars((indent, segs)):
            continue                                   # spacer line: draw nothing

        line_chars = indent + _chars((indent, segs))
        parts, x = [], X0 + indent * CW
        for text, colour in segs:
            if text:
                parts.append(f'<tspan x="{x:.1f}" fill="{colour}">{escape(text)}</tspan>')
                x += len(text) * CW

        body.append(
            f'    <g clip-path="url(#t{i})">\n'
            f'      <text x="{X0}" y="{y}" font-family="{MONO}" font-size="{FS}" font-weight="500">'
            + "".join(parts)
            + "</text>\n    </g>"
        )

        # caret rides the reveal, then disappears once its line is finished
        xs, xe = X0 + indent * CW, X0 + line_chars * CW
        s_vis = max(s, 0.0015)
        body.append(
            f'    <rect x="{xs:.1f}" y="{y - 13}" width="8" height="17" fill="#67e8f9" opacity="0">\n'
            f'      <animate attributeName="x" values="{xs:.1f};{xs:.1f};{xe:.1f};{xe:.1f}" '
            f'keyTimes="0;{s_vis:.4f};{e:.4f};1" dur="{CYCLE}s" repeatCount="indefinite"/>\n'
            f'      <animate attributeName="opacity" values="0;0;.9;.9;0" '
            f'keyTimes="0;{s_vis * 0.999:.4f};{s_vis:.4f};{e:.4f};{min(e + 0.004, 1):.4f}" '
            f'dur="{CYCLE}s" repeatCount="indefinite"/>\n'
            f'    </rect>'
        )

    clips = "\n".join(
        f'''    <clipPath id="t{i}">
      <rect x="0" y="{Y0 + i * LH - 19}" width="0" height="{LH}">
        <animate attributeName="width" values="0;0;{TW};{TW}" keyTimes="0;{s:.4f};{e:.4f};1" dur="{CYCLE}s" repeatCount="indefinite"/>
      </rect>
    </clipPath>'''
        for i, (s, e) in enumerate(spans)
    )

    prompt_y = Y0 + len(LINES) * LH
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{TW}" height="{TH}" viewBox="0 0 {TW} {TH}" role="img" aria-labelledby="tterm dterm">
  <title id="tterm">A terminal session introducing Rishi Raj DEV</title>
  <desc id="dterm">An animated terminal typing out whoami, current focus areas, and a status line reading build carefully, measure honestly, keep shipping, status open to collaborate.</desc>
  <defs>
    <linearGradient id="tbg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#070c18"/>
      <stop offset="60%" stop-color="#0b1120"/>
      <stop offset="100%" stop-color="#08131f"/>
    </linearGradient>
    <linearGradient id="tbar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#111c30"/>
      <stop offset="100%" stop-color="#0d1526"/>
    </linearGradient>
    <linearGradient id="tedge" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#22d3ee"/>
      <stop offset="50%" stop-color="#a855f7"/>
      <stop offset="100%" stop-color="#2dd4bf"/>
    </linearGradient>
    <radialGradient id="tglow" cx="82%" cy="12%" r="66%">
      <stop offset="0%" stop-color="#a855f7" stop-opacity=".2"/>
      <stop offset="100%" stop-color="#a855f7" stop-opacity="0"/>
    </radialGradient>
    <pattern id="tgrid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M24 0H0V24" fill="none" stroke="#9cc3ff" stroke-opacity=".05" stroke-width="1"/>
    </pattern>
    <filter id="tblur" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="20"/></filter>
{clips}
  </defs>

  <rect x="1" y="1" width="{TW - 2}" height="{TH - 2}" rx="16" fill="url(#tbg)"/>
  <rect x="1" y="1" width="{TW - 2}" height="{TH - 2}" rx="16" fill="url(#tgrid)"/>
  <rect x="1" y="1" width="{TW - 2}" height="{TH - 2}" rx="16" fill="url(#tglow)"/>
  <ellipse cx="{TW - 130}" cy="60" rx="150" ry="70" fill="#22d3ee" opacity=".08" filter="url(#tblur)"/>

  <path d="M1 17 a16 16 0 0 1 16 -16 h {TW - 34} a16 16 0 0 1 16 16 v 27 h -{TW - 2} z" fill="url(#tbar)"/>
  <line x1="1" y1="44" x2="{TW - 1}" y2="44" stroke="#2b4468" stroke-opacity=".8"/>
  <circle cx="26" cy="23" r="5.6" fill="#ff5f57"/>
  <circle cx="46" cy="23" r="5.6" fill="#febc2e"/>
  <circle cx="66" cy="23" r="5.6" fill="#28c840"/>
  <text x="{TW / 2:.0f}" y="28" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="600" letter-spacing=".4" fill="#7d95b5">rishi@dev — zsh — 96×24</text>
  <g font-family="{MONO}" font-size="11" font-weight="600">
    <rect x="{TW - 156}" y="14" width="136" height="19" rx="9.5" fill="#0a1424" stroke="#2dd4bf" stroke-opacity=".4"/>
    <circle cx="{TW - 143}" cy="23.5" r="3.4" fill="#2dd4bf">
      <animate attributeName="opacity" values="1;.25;1" dur="2.2s" repeatCount="indefinite"/>
    </circle>
    <text x="{TW - 133}" y="27.5" fill="#5eead4">available for work</text>
  </g>

{chr(10).join(body)}

  <text x="{X0}" y="{prompt_y}" font-family="{MONO}" font-size="{FS}" font-weight="500"><tspan fill="{P}">rishi@dev</tspan><tspan fill="{D}"> ~ </tspan><tspan fill="{W}">%</tspan></text>
  <rect x="{X0 + 9 * CW:.1f}" y="{prompt_y - 13}" width="9" height="17" fill="#67e8f9">
    <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/>
  </rect>

  <line x1="24" y1="{TH - 34}" x2="{TW - 24}" y2="{TH - 34}" stroke="#8fb3dd" stroke-opacity=".13"/>
  <text x="{X0}" y="{TH - 13}" font-family="{MONO}" font-size="11" font-weight="600" letter-spacing="1.2" fill="#5c7595">IST / UTC+5:30</text>
  <text x="{TW / 2:.0f}" y="{TH - 13}" text-anchor="middle" font-family="{MONO}" font-size="11" font-weight="600" letter-spacing="1.2" fill="#5c7595">BUILD CAREFULLY · MEASURE HONESTLY · KEEP SHIPPING</text>
  <text x="{TW - X0}" y="{TH - 13}" text-anchor="end" font-family="{MONO}" font-size="11" font-weight="600" letter-spacing="1.2" fill="#5c7595">exit 0</text>

  <rect x="1" y="1" width="{TW - 2}" height="{TH - 2}" rx="16" fill="none" stroke="#8fb3dd" stroke-opacity=".2"/>
  <rect x="0" y="{TH - 5}" width="{TW}" height="5" rx="2.5" fill="url(#tedge)"/>
</svg>
'''


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)

    for num, slug, label, a, b in HEADERS:
        out = ASSETS / f"header-{num}-{slug}.svg"
        out.write_text(build_header(num, label, a, b), encoding="utf-8")
        print(f"wrote {out.name} ({out.stat().st_size:,} bytes)")

    for name, builder in (("divider.svg", build_divider), ("terminal.svg", build_terminal)):
        out = ASSETS / name
        out.write_text(builder(), encoding="utf-8")
        print(f"wrote {out.name} ({out.stat().st_size:,} bytes)")

    # retire the unnumbered headers this supersedes
    for stale in sorted(ASSETS.glob("header-*.svg")):
        if not stale.name.split("-")[1].isdigit():
            stale.unlink()
            print(f"removed superseded {stale.name}")


if __name__ == "__main__":
    main()
