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

    body_blocks = []
    for i, block in enumerate(extracted_blocks, start=start_page):
        body_blocks.append(f"## Conference Program Extract — Source Page {i}\n\n{block}")

    body = "\n\n---\n\n".join(body_blocks)

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
