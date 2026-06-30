#!/usr/bin/env python3
"""
render_svg.py - 把 GH user/repos JSON 渲成一张 GitHub Stats SVG 卡。
设计目标：避开 vercel.app / 任何外部 SaaS，纯本机 string-template，
输出等价于 github-readme-stats 风格卡片（暗色主题、扁平）。
"""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path


def esc(x) -> str:
    if x is None:
        return "—"
    return html.escape(str(x))


def top_langs(repos: list[dict], n: int = 5) -> list[tuple[str, int, float]]:
    """按语言聚合（owner-contributed），按字节占比取 top N。返回 (lang, weighted_count, pct)。"""
    counts: dict[str, int] = {}
    for r in repos:
        lang = r.get("language")
        if not lang:
            continue
        size = r.get("size", 0) or 0
        if r.get("fork"):
            size = 0
        if size <= 0:
            size = 1
        counts[lang] = counts.get(lang, 0) + size
    items = sorted(counts.items(), key=lambda kv: -kv[1])
    total = sum(c for _, c in items) or 1
    return [(name, count, count / total * 100.0) for name, count in items[:n]]


def render(user: dict, repos: list[dict]) -> str:
    name = esc(user.get("login") or "lingion")
    public_repos = user.get("public_repos", 0) or 0
    followers = user.get("followers", 0) or 0
    following = user.get("following", 0) or 0
    bio = esc(user.get("bio") or "")
    star_total = sum((r.get("stargazers_count") or 0) for r in repos)

    langs = top_langs(repos, 5)

    # 横向条形 lang 占比
    bar_parts = []
    palette = ["#2f80ed", "#4c71f2", "#7c3aed", "#10b981", "#f59e0b"]
    x_cursor = 60
    bar_y = 170
    bar_w_max = 360
    for i, (lang, _count, pct) in enumerate(langs):
        seg_w = max(8.0, bar_w_max * pct / 100.0)
        color = palette[i % len(palette)]
        bar_parts.append(
            f'<rect x="{x_cursor:.1f}" y="{bar_y}" width="{seg_w:.1f}" height="8" fill="{color}" rx="4"/>'
        )
        x_cursor += seg_w + 2

    lang_labels = " &nbsp;·&nbsp; ".join(
        f'<tspan fill="{palette[i % len(palette)]}">{esc(lang)}</tspan> {pct:.1f}%'
        for i, (lang, _c, pct) in enumerate(langs)
    )

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="466" height="220" viewBox="0 0 466 220" fill="none">
  <style>
    .card {{ fill: #1a1b21; stroke: #383b43; stroke-width: 1; }}
    .title {{ font: 600 18px 'Segoe UI', Ubuntu, sans-serif; fill: #2f80ed; }}
    .bio   {{ font: 400 12px 'Segoe UI', Ubuntu, sans-serif; fill: #a9b1bb; }}
    .stat-label {{ font: 500 11px 'Segoe UI', Ubuntu, sans-serif; fill: #8b95a1; }}
    .stat-num   {{ font: 600 22px 'Segoe UI', Ubuntu, sans-serif; fill: #ffffff; }}
    .lang       {{ font: 500 11px 'Segoe UI', Ubuntu, sans-serif; fill: #a9b1bb; }}
  </style>
  <rect class="card" width="466" height="220" rx="6"/>
  <text x="20" y="38" class="title">GitHub Stats · {name}</text>
  <text x="20" y="60" class="bio">{bio or " "}</text>

  <!-- 三连 stat -->
  <text x="20"  y="100" class="stat-num">{public_repos}</text>
  <text x="20"  y="118" class="stat-label">Public repos</text>
  <text x="170" y="100" class="stat-num">{star_total}</text>
  <text x="170" y="118" class="stat-label">Total stars</text>
  <text x="320" y="100" class="stat-num">{followers}</text>
  <text x="320" y="118" class="stat-label">Followers</text>

  <!-- lang bar -->
  <text x="20" y="158" class="stat-label">Top languages</text>
  {''.join(bar_parts)}
  <text x="20" y="200" class="lang">{lang_labels or "no public repos with recognized languages yet"}</text>
</svg>
'''
    return svg


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: render_svg.py stats.json", file=sys.stderr)
        return 2
    src = Path(sys.argv[1])
    data = json.loads(src.read_text())
    user = data.get("user") or {}
    repos = data.get("repos") or []
    sys.stdout.write(render(user, repos))
    return 0


if __name__ == "__main__":
    sys.exit(main())
