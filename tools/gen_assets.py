#!/usr/bin/env python3
"""Generate the animated section headers used by the profile README.

Each header is a small self-contained SVG (dark glass pill, gradient accent bar,
animated highlight, pulsing dot) so section titles match the hero banner exactly
instead of relying on emoji + markdown headings.

Usage:
    python3 tools/gen_assets.py

The profile README is intentionally a banner/profile page — it carries no
project cards. If a project showcase is ever wanted again, the per-project
card generator lives in this file's git history (see `git log -- tools/`).
"""
from pathlib import Path
from xml.sax.saxutils import escape

ASSETS = Path(__file__).resolve().parent.parent / "assets"
FONT = "Inter, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"

HEADERS = [
    ("about", "ABOUT ME", "#22d3ee", "#a855f7"),
    ("stack", "TECH STACK", "#2dd4bf", "#22d3ee"),
    ("activity", "GITHUB ACTIVITY", "#818cf8", "#22d3ee"),
    ("collaborate", "LET'S COLLABORATE", "#34d399", "#22d3ee"),
]


def build_header(label: str, accent: str, accent2: str) -> str:
    fs = 24
    # Inter Bold uppercase averages ~0.70em per glyph plus explicit tracking.
    text_w = int(len(label) * fs * 0.70 + len(label) * 6)
    w = text_w + 96
    h = 66
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">
  <defs>
    <linearGradient id="hbg" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#0c1322"/>
      <stop offset="100%" stop-color="#0c1322" stop-opacity=".25"/>
    </linearGradient>
    <linearGradient id="hacc" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{accent}"/>
      <stop offset="100%" stop-color="{accent2}"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="-120 0;120 0;-120 0" dur="7s" repeatCount="indefinite"/>
    </linearGradient>
  </defs>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="15" fill="url(#hbg)" stroke="{accent}" stroke-opacity=".26"/>
  <rect x="14" y="18" width="6" height="30" rx="3" fill="url(#hacc)"/>
  <text x="34" y="43" font-family="{FONT}" font-size="{fs}" font-weight="800" letter-spacing="2.6" fill="#eef4ff">{escape(label)}</text>
  <circle cx="{w - 26}" cy="33" r="4" fill="{accent}">
    <animate attributeName="opacity" values="1;.2;1" dur="2.6s" repeatCount="indefinite"/>
  </circle>
</svg>
'''


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    for slug, label, accent, accent2 in HEADERS:
        out = ASSETS / f"header-{slug}.svg"
        out.write_text(build_header(label, accent, accent2), encoding="utf-8")
        print(f"wrote {out.name} ({out.stat().st_size:,} bytes)")

    # the profile README no longer references project cards or a projects header
    for stale in ("header-projects.svg",):
        p = ASSETS / stale
        if p.exists():
            p.unlink()
            print(f"removed unused {stale}")
    for stale in sorted(ASSETS.glob("card-*.svg")):
        stale.unlink()
        print(f"removed unused {stale.name}")


if __name__ == "__main__":
    main()
