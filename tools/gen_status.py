#!/usr/bin/env python3
"""Generate a LIVE status pill for the profile README.

Unlike every other badge on GitHub, this one is not a static claim: a scheduled
workflow (.github/workflows/status.yml) re-runs this script every hour against
the public GitHub REST API and publishes the result to the orphan `live`
branch, so the profile states today's facts — local time in Kolkata, days into
the journey, current repo / star / follower counts — forever, with zero manual
effort.

Usage:
    python3 tools/gen_status.py --out dist/status.svg

No authentication required (public REST, unauthenticated rate limit is ample
for an hourly job).
"""
import argparse
import json
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from xml.sax.saxutils import escape

USER = "Rishidev-20thcenturey"
API = f"https://api.github.com/users/{USER}"
MONO = "'JetBrains Mono', 'SF Mono', Menlo, Consolas, monospace"
IST = timezone(timedelta(hours=5, minutes=30))

W, H = 980, 64


def get(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "profile-status-badge",
                                               "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def fetch() -> dict:
    user = get(API)
    repos = get(API + "/repos?per_page=100")
    created = datetime.fromisoformat(user["created_at"].replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    return {
        "local": datetime.now(IST).strftime("%H:%M"),
        "day": (now - created).days,
        "repos": user["public_repos"],
        "stars": sum(r["stargazers_count"] for r in repos),
        "followers": user["followers"],
        "stamp": now.strftime("%Y-%m-%d %H:%M UTC"),
    }


def build(d: dict) -> str:
    segs = [
        ("LIVE", "#34d399", True),
        (f"KOLKATA {d['local']} IST", "#7dd3fc", False),
        (f"DAY {d['day']}", "#c4b5fd", False),
        (f"{d['repos']} REPOS", "#e2ecfb", False),
        (f"{d['stars']} STARS", "#fcd34d", False),
        (f"{d['followers']} FOLLOWERS", "#5eead4", False),
    ]
    fs = 12.5
    adv = fs * 0.62
    pad = 26                      # segment horizontal padding
    gap = 34                      # space around separators
    widths = [len(t) * adv + pad for t, _, _ in segs]
    tail = len("REFRESHED HOURLY BY CI") * adv + pad
    total = 58 + sum(widths) + gap * (len(segs) - 1) + 40 + tail + 24
    w = max(int(total), W)

    x = 58.0
    body = []
    for i, (text, colour, live) in enumerate(segs):
        if live:
            body.append(f'    <circle cx="{x - 16:.0f}" cy="{H / 2:.0f}" r="4.5" fill="{colour}">'
                        f'<animate attributeName="opacity" values="1;.25;1" dur="2s" repeatCount="indefinite"/></circle>'
                        f'<circle cx="{x - 16:.0f}" cy="{H / 2:.0f}" r="4.5" fill="none" stroke="{colour}" stroke-opacity=".6">'
                        f'<animate attributeName="r" values="4.5;11" dur="2s" repeatCount="indefinite"/>'
                        f'<animate attributeName="stroke-opacity" values=".6;0" dur="2s" repeatCount="indefinite"/></circle>')
        body.append(f'    <text x="{x:.0f}" y="{H / 2 + 4.5:.0f}" font-family="{MONO}" font-size="{fs}" '
                    f'font-weight="700" letter-spacing="1.1" fill="{colour}">{escape(text)}</text>')
        x += widths[i]
        if i < len(segs) - 1:
            body.append(f'    <line x1="{x + gap / 2 - 8:.0f}" y1="18" x2="{x + gap / 2 - 8:.0f}" y2="{H - 18}" '
                        f'stroke="#7f9dc4" stroke-opacity=".25"/>')
            x += gap
    body.append(f'    <line x1="{x + 12:.0f}" y1="18" x2="{x + 12:.0f}" y2="{H - 18}" stroke="#7f9dc4" stroke-opacity=".25"/>')
    body.append(f'    <text x="{x + 26:.0f}" y="{H / 2 + 4:.0f}" font-family="{MONO}" font-size="10" '
                f'font-weight="600" letter-spacing="1.2" fill="#5c7595">REFRESHED HOURLY BY CI</text>')

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{H}" viewBox="0 0 {w} {H}" role="img" aria-labelledby="st sd">
  <title id="st">Live status: Kolkata local time, days since the journey started, public repositories, stars and followers</title>
  <desc id="sd">Regenerated every hour by GitHub Actions from the public GitHub API, so the numbers are always current. Snapshot taken {escape(d["stamp"])}.</desc>
  <defs>
    <linearGradient id="sbg" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#0c1322"/>
      <stop offset="70%" stop-color="#0b1120"/>
      <stop offset="100%" stop-color="#08131f"/>
    </linearGradient>
    <linearGradient id="sedge" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#22d3ee"/>
      <stop offset="50%" stop-color="#a855f7"/>
      <stop offset="100%" stop-color="#2dd4bf"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="-260 0;260 0;-260 0" dur="8s" repeatCount="indefinite"/>
    </linearGradient>
  </defs>
  <rect x="1" y="1" width="{w - 2}" height="{H - 2}" rx="16" fill="url(#sbg)" stroke="#8fb3dd" stroke-opacity=".22"/>
{chr(10).join(body)}
  <rect x="0" y="{H - 4}" width="{w}" height="4" rx="2" fill="url(#sedge)"/>
</svg>
'''


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="dist/status.svg")
    args = ap.parse_args()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(fetch()), encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
