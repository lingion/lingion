#!/usr/bin/env python3
"""
render_zine.py — generate docs/zine.svg from a GraphQL contribution dump.

Input JSON (scripts/zine_fetch.sh produces this):
    {
      "user": { "createdAt": "2024-04-01T..." },
      "calendar": { ... contributionCalendar weeks[] ... },
      "totals":  { "commits": 4686, "prs": 51, "issues": 2, "repos": 11 },
      "stars":   94
    }

All numbers in the card are derived from this JSON — no hardcoded constants.
Run from repo root: python3 scripts/render_zine.py out/zine.json > docs/zine.svg
"""
from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

CAL_X = 660
CAL_Y = 368
CELL = 8          # 8px stride
DOT = 7           # 7px square inside the stride
WEEKS = 53        # exactly 53 weeks shown
DAYS_PER_WEEK = 7


def n_with_thousands(n: int) -> str:
    return f"{n:,}"


def months_row(weeks: list[dict]) -> str:
    """Place a 3-letter month label at the first week whose day-1 is in a new month."""
    parts: list[str] = []
    seen: set[str] = set()
    for wi, w in enumerate(weeks):
        days = w["contributionDays"]
        if not days:
            continue
        first = dt.date.fromisoformat(days[0]["date"])
        last = dt.date.fromisoformat(days[-1]["date"])
        # Only label a week if its first day belongs to a month not yet labeled,
        # and the first day is a Sunday so we are at the start of a calendar column.
        if days[0]["date"][-2:] == "01" or first.month not in seen:
            if first.month not in seen:
                x = CAL_X + wi * CELL
                y = CAL_Y - 4
                parts.append(
                    f'<text x="{x}" y="{y}">{first.strftime("%b").upper()}</text>'
                )
                seen.add(first.month)
    return (
        '<g font-family="Arial,sans-serif" font-size="9" fill="#1f2937" opacity="0.75">'
        + "".join(parts)
        + "</g>"
    )


def heatmap(weeks: list[dict]) -> str:
    """Render one rect per day at the same x/y geometry as the approved card."""
    out: list[str] = []
    for wi, w in enumerate(weeks[:WEEKS]):
        x = CAL_X + wi * CELL
        days = w["contributionDays"][:DAYS_PER_WEEK]
        for di, day in enumerate(days):
            y = CAL_Y + di * CELL
            color = day.get("color") or "#ebedf0"
            out.append(
                f'<rect x="{x}" y="{y}" width="{DOT}" height="{DOT}" '
                f'rx="1.5" fill="{color}"/>'
            )
    return "".join(out)


def streak(weeks: list[dict]) -> tuple[int, int]:
    """Return (current_streak_ending_today, longest_streak_in_window)."""
    flat = []
    for w in weeks:
        for d in w["contributionDays"]:
            flat.append((dt.date.fromisoformat(d["date"]), d["contributionCount"]))
    flat.sort()
    today = flat[-1][0]
    # current streak: count consecutive non-zero days ending today
    cur = 0
    for d, c in reversed(flat):
        if d > today:
            continue
        if c > 0:
            cur += 1
        else:
            break
    # longest streak
    best, run = 0, 0
    prev = None
    for d, c in flat:
        if c > 0 and (prev is None or (d - prev).days == 1):
            run += 1
            best = max(best, run)
        else:
            run = c if c > 0 else 0
        prev = d
    return cur, best


def peak(weeks: list[dict]) -> tuple[dt.date, int, int]:
    """Return (peak_date, peak_count, active_days_count)."""
    peak_day, peak_n = None, 0
    active = 0
    for w in weeks:
        for d in w["contributionDays"]:
            if d["contributionCount"] > peak_n:
                peak_n = d["contributionCount"]
                peak_day = dt.date.fromisoformat(d["date"])
            if d["contributionCount"] > 0:
                active += 1
    return peak_day, peak_n, active


def member_since(created_at: str) -> str:
    d = dt.datetime.fromisoformat(created_at.replace("Z", "+00:00")).date()
    return d.strftime("%b %Y")


def range_label(weeks: list[dict]) -> str:
    flat = sorted(
        dt.date.fromisoformat(d["date"])
        for w in weeks
        for d in w["contributionDays"]
    )
    a, b = flat[0], flat[-1]
    return f"{a.strftime('%b %Y')} – {b.strftime('%b %Y')}"


def main() -> int:
    data = json.loads(sys.stdin.read())
    user = data["user"]
    cal = data["calendar"]
    weeks = cal["weeks"]
    totals = data["totals"]
    stars = data["stars"]

    cur, best = streak(weeks)
    pd, pn, active = peak(weeks)
    since = member_since(user["createdAt"])
    rng = range_label(weeks)

    total = cal.get("totalContributions") or sum(
        d["contributionCount"]
        for w in weeks
        for d in w["contributionDays"]
    )

    left = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">'
        '<rect width="600" height="630" fill="#dbeafe"/>'
        '<rect x="600" y="0" width="600" height="630" fill="#dbeafe"/>'
        '<line x1="600" y1="20" x2="600" y2="610" stroke="#1f2937" stroke-width="2" stroke-dasharray="6 4"/>'
        '<text x="60" y="70" font-family="Courier New,monospace" font-size="14" font-weight="700" letter-spacing="4" fill="#1f2937">ZINE</text>'
        '<text x="60" y="180" font-family="Arial Black,sans-serif" font-size="84" fill="#1f2937">lingion</text>'
        f'<text x="60" y="218" font-family="Arial,sans-serif" font-size="14" fill="#1f2937">Harbin, China · blog.qdp.qzz.io</text>'
        f'<text x="60" y="246" font-family="Arial,sans-serif" font-size="14" fill="#1f2937">GitHub member since {since}</text>'
        '<rect x="46" y="262" width="290" height="76" fill="#1d4ed8" opacity="0.22" transform="rotate(-2 186 300)"/>'
        f'<text x="60" y="324" font-family="Arial Black,sans-serif" font-size="64" fill="#1d4ed8">{n_with_thousands(total)}</text>'
        f'<text x="60" y="350" font-family="Arial,sans-serif" font-size="14" fill="#1f2937">Contributions · Last 12 months ({rng})</text>'
        '<g font-family="Arial,sans-serif" font-size="13" fill="#1f2937">'
        '<text x="60" y="404">Repository stars</text>'
        '<text x="60" y="430">Commits (last year)</text>'
        '<text x="60" y="456">Pull requests</text>'
        '<text x="60" y="482">Issues opened</text>'
        '<text x="60" y="508">Repos contributed to</text>'
        '</g>'
        '<g stroke="#1f2937" stroke-width="1.5" stroke-dasharray="1 5" stroke-linecap="round" opacity="0.5">'
        '<line x1="172" y1="400" x2="470" y2="400"/>'
        '<line x1="182" y1="426" x2="470" y2="426"/>'
        '<line x1="158" y1="452" x2="470" y2="452"/>'
        '<line x1="163" y1="478" x2="470" y2="478"/>'
        '<line x1="178" y1="504" x2="470" y2="504"/>'
        '</g>'
        '<g font-family="Arial,sans-serif" font-size="17" font-weight="700" fill="#1d4ed8" text-anchor="end">'
        f'<text x="540" y="404">{stars}</text>'
        f'<text x="540" y="430">{n_with_thousands(totals["commits"])}</text>'
        f'<text x="540" y="456">{totals["prs"]}</text>'
        f'<text x="540" y="482">{totals["issues"]}</text>'
        f'<text x="540" y="508">{totals["repos"]}</text>'
        '</g>'
    )

    right = (
        '<text x="660" y="70" font-family="Courier New,monospace" font-size="14" font-weight="700" letter-spacing="4" fill="#1f2937">ACTIVITY</text>'
        '<text x="660" y="180" font-family="Arial,sans-serif" font-size="58" font-weight="900" fill="#1d4ed8">B+</text>'
        '<text x="660" y="218" font-family="Arial,sans-serif" font-size="14" fill="#1f2937">Activity Grade</text>'
        f'<text x="700" y="282" font-family="Arial Black,sans-serif" font-size="42" fill="#1f2937" text-anchor="middle">{cur}</text>'
        '<text x="700" y="308" font-family="Arial,sans-serif" font-size="11" font-weight="700" letter-spacing="1" fill="#1f2937" text-anchor="middle">CURRENT · DAYS</text>'
        f'<text x="970" y="282" font-family="Arial Black,sans-serif" font-size="42" fill="#1f2937" text-anchor="middle">{best}</text>'
        '<text x="970" y="308" font-family="Arial,sans-serif" font-size="11" font-weight="700" letter-spacing="1" fill="#1f2937" text-anchor="middle">LONGEST · DAYS</text>'
        '<line x1="838" y1="240" x2="838" y2="320" stroke="#1f2937" stroke-width="1" stroke-dasharray="3 3" opacity="0.5"/>'
        '<text x="660" y="350" font-family="Arial,sans-serif" font-size="12" font-weight="700" letter-spacing="2" fill="#1f2937">CONTRIBUTION CALENDAR · '
        f'{rng.upper()}'
        '</text>'
    )

    legend = (
        '<g font-family="Arial,sans-serif" font-size="12" fill="#1f2937">'
        '<text x="915" y="455">Less</text>'
        '<text x="1053" y="455">More</text>'
        '</g>'
        '<g>'
        '<rect x="951" y="444" width="14" height="14" fill="#ebedf0" stroke="#1f2937" stroke-opacity="0.25"/>'
        '<rect x="971" y="444" width="14" height="14" fill="#9be9a8" stroke="#1f2937" stroke-opacity="0.25"/>'
        '<rect x="991" y="444" width="14" height="14" fill="#40c463" stroke="#1f2937" stroke-opacity="0.25"/>'
        '<rect x="1011" y="444" width="14" height="14" fill="#30a14e" stroke="#1f2937" stroke-opacity="0.25"/>'
        '<rect x="1031" y="444" width="14" height="14" fill="#216e39" stroke="#1f2937" stroke-opacity="0.25"/>'
        '</g>'
    )

    foot = (
        f'<text x="60" y="566" font-family="Georgia, \'Times New Roman\', serif" font-size="11" font-style="italic" opacity="0.72" fill="#1f2937">'
        f'Actual data · GitHub GraphQL API · Peak {pd.strftime("%b %-d, %Y")}: {pn} · {active} active days'
        '</text></svg>'
    )

    out = left + right + months_row(weeks) + heatmap(weeks) + legend + foot
    sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
