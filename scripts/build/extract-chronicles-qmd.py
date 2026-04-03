#!/usr/bin/env python3
"""Extract selected conference PDF pages into a chronicles QMD scaffold.

This helps keep yearly chronicles formatting consistent with the 2022 pattern:
- A standalone QMD that can be rendered to a curated chronicles PDF.
- Optional LaTeX page counter support when embedding into full volume.

Usage:
  python3 scripts/build/extract-chronicles-qmd.py \
    --input 2023/sources/conference/2023-WSKW-Conference-Program-100423.pdf \
    --output 2023/sources/conference/2023_WSKW_Chronicles.qmd \
    --year 2023 \
    --volume 12 \
    --issue 1 \
    --start-page 13 \
    --end-page 24 \
    --set-page 75
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from pypdf import PdfReader


def clean_page_text(text: str) -> str:
    """Normalize extracted PDF text for markdown readability."""
    if not text:
        return ""
    lines = [ln.rstrip() for ln in text.splitlines()]

    # Collapse excessive blank lines while preserving paragraph breaks.
    cleaned = []
    blank = False
    for ln in lines:
        if ln.strip() == "":
            if not blank:
                cleaned.append("")
            blank = True
        else:
            cleaned.append(ln)
            blank = False

    return "\n".join(cleaned).strip()


def format_conference_text(raw_text: str) -> str:
    """Apply markdown-friendly structure to extracted conference text."""
    lines = [ln.strip() for ln in raw_text.splitlines()]
    out: list[str] = []

    time_re = re.compile(r"^\d{1,2}:\d{2}")
    poster_re = re.compile(r"^(\d{1,2})\s+(.+)$")
    session_re = re.compile(r"^Conference Sessions\s+[–-]\s+.+")

    for ln in lines:
        if not ln:
            if out and out[-1] != "":
                out.append("")
            continue

        # Drop standalone page numbers from source PDF extraction.
        if re.fullmatch(r"\d+", ln):
            continue

        if session_re.match(ln):
            if out and out[-1] != "":
                out.append("")
            out.append(f"## {ln}")
            out.append("")
            continue

        if ln.startswith("Title:"):
            title = ln.replace("Title:", "", 1).strip()
            if out and out[-1] != "":
                out.append("")
            out.append(f"### {title}")
            out.append("")
            continue

        if ln.startswith("Presenter:") or ln.startswith("Presenters:"):
            label, value = ln.split(":", 1)
            out.append(f"**{label}:** {value.strip()}")
            out.append("")
            continue

        if ln.startswith("Abstract:"):
            value = ln.replace("Abstract:", "", 1).strip()
            out.append(f"**Abstract:** {value}")
            out.append("")
            continue

        if "Poster Session" in ln and "Session" in ln:
            if out and out[-1] != "":
                out.append("")
            out.append(f"## {ln}")
            out.append("")
            continue

        # Avoid converting schedule times to poster items.
        if not time_re.match(ln):
            m = poster_re.match(ln)
            if m and m.group(1) not in {"2023", "2022", "2024", "2025", "2026"}:
                if out and out[-1] != "":
                    out.append("")
                out.append(f"### Poster {m.group(1)}")
                out.append(m.group(2).strip())
                out.append("")
                continue

        out.append(ln)

    # Collapse repeated blank lines.
    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def build_qmd(
    year: int,
    volume: int,
    issue: int,
    start_page: int,
    end_page: int,
    set_page: int | None,
    extracted_blocks: list[str],
) -> str:
    page_counter_line = f"\\setcounter{{page}}{{{set_page}}}" if set_page else ""

    raw_body = "\n\n".join(extracted_blocks)
    body = format_conference_text(raw_body)

    return f'''---
title: "WSKW Chronicles"
subtitle: "{year} WSKW Conference Abstracts"
date: "{year}-01-01"
author: "Journal of Kinesiology and Wellness, Volume {volume}, Number {issue}, {year}"
format:
  pdf:
    documentclass: article
    fontsize: 11pt
    geometry:
      - top=1in
      - bottom=1in
      - left=1in
      - right=1in
    header-includes:
      - \\usepackage{{titling}}
      - \\pretitle{{\\begin{{center}}\\LARGE\\bfseries}}
      - \\posttitle{{\\end{{center}}}}
      - \\preauthor{{\\begin{{center}}\\large}}
      - \\postauthor{{\\end{{center}}}}
      - \\predate{{\\begin{{center}}\\large}}
      - \\postdate{{\\end{{center}}}}
---

## Keynote Presentation

## E.C. Davis Lecture

---

# ABSTRACTS

{page_counter_line}

{body}
'''


def main() -> int:
    ap = argparse.ArgumentParser(description="Extract selected conference pages into chronicles QMD")
    ap.add_argument("--input", required=True, help="Source conference PDF path")
    ap.add_argument("--output", required=True, help="Output chronicles QMD path")
    ap.add_argument("--year", type=int, required=True)
    ap.add_argument("--volume", type=int, required=True)
    ap.add_argument("--issue", type=int, default=1)
    ap.add_argument("--start-page", type=int, required=True, help="1-based inclusive")
    ap.add_argument("--end-page", type=int, required=True, help="1-based inclusive")
    ap.add_argument("--set-page", type=int, default=None, help="Optional LaTeX page counter value")
    args = ap.parse_args()

    in_pdf = Path(args.input)
    out_qmd = Path(args.output)

    if not in_pdf.exists():
        raise FileNotFoundError(f"Input PDF not found: {in_pdf}")

    reader = PdfReader(str(in_pdf))
    total = len(reader.pages)
    if args.start_page < 1 or args.end_page < args.start_page or args.end_page > total:
        raise ValueError(
            f"Invalid page range {args.start_page}-{args.end_page}; PDF has {total} pages")

    blocks = []
    for i in range(args.start_page - 1, args.end_page):
        txt = reader.pages[i].extract_text() or ""
        blocks.append(clean_page_text(txt))

    qmd = build_qmd(
        year=args.year,
        volume=args.volume,
        issue=args.issue,
        start_page=args.start_page,
        end_page=args.end_page,
        set_page=args.set_page,
        extracted_blocks=blocks,
    )

    out_qmd.parent.mkdir(parents=True, exist_ok=True)
    out_qmd.write_text(qmd, encoding="utf-8")
    print(f"Wrote {out_qmd} from pages {args.start_page}-{args.end_page} of {in_pdf}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
