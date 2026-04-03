#!/usr/bin/env python3
"""
JKW Full Volume Builder
=======================
Assembles the annual Journal of Kinesiology & Wellness full-volume PDF from:
  • Cover image (.png or .pdf)
  • Masthead/preface page (generated from sources/manuscripts/info.md — optional)
  • Article PDFs — numbered prefix controls order (01_paper.pdf, 02_paper.pdf …)
  • WSKW Chronicles PDF

Output order:  Cover → Masthead → TOC → Articles (in filename order) → WSKW Chronicles

Usage:
  python3 build_full_volume.py YYYY/volume_config.yaml

Output:
  A single merged PDF written to the path specified in `output_file` in the config.

Requirements:
  pip install pypdf reportlab pillow pyyaml --break-system-packages
"""

import sys
import os
import io
import re
import subprocess
import tempfile
from pathlib import Path

import yaml
from PIL import Image
from pypdf import PdfWriter, PdfReader, Transformation
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable,
    KeepTogether
)
from reportlab.pdfgen import canvas

# ── Constants ────────────────────────────────────────────────────────────────

JOURNAL_NAME  = "Journal of Kinesiology & Wellness"
JOURNAL_ISSN  = "ISSN# 2332-4503"
PAGE_W, PAGE_H = letter   # 612 × 792 pt

ABOUT_P1 = (
    "The Journal of Kinesiology &amp; Wellness (JKW) is an anonymous peer-reviewed "
    "online journal that covers issues in physical education, physical activity &amp; "
    "health promotion, wellness, biomechanics, motor behavior, exercise physiology, "
    "sport, and dance. The JKW is a publication of the Western Society for Kinesiology "
    "and Wellness (WSKW)."
)
ABOUT_P2 = (
    "The JKW does not charge a publication fee, and the journal has an open-access "
    "policy, meaning all articles are freely available online for anyone to read, "
    "download, and share. The JKW aims to promote scholarly communication and "
    "disseminate high-quality knowledge to the academic community and the public."
)
ABOUT_P3 = "Accepted papers are published on a rolling basis. Papers are published under these sections:"
ABOUT_SECTIONS = [
    ("<b>Experimental &amp; Quantitative Research:</b> consists of scholarly papers "
     "based on original quantitative research (experimental or observational)."),
    ("<b>Qualitative &amp; Mixed-Methods Research:</b> consists of scholarly papers "
     "using qualitative or mixed-methods approaches."),
    ("<b>Systematic Reviews &amp; Meta-Analyses:</b> includes systematic reviews "
     "(with or without meta-analysis) and related evidence syntheses."),
    ("<b>Student-Led Research:</b> reserved for scholarly papers, of any of the above "
     "types, in which a student (undergraduate or graduate) is the lead author."),
    ("<b>John Massengale Paper:</b> an exclusive publication written by a distinguished "
     "scholar.<super>1</super>"),
]
ABOUT_P4 = (
    "The full volume, published each January, includes the WSKW Chronicles, which "
    "include post-conference proceedings, such as conference abstracts."
)
MASSENGALE_FOOTNOTE = (
    "<super>1</super>The John Massengale Paper is an exclusive publication written by "
    "a distinguished scholar. Contact us to suggest an author, or nominate yourself."
)

OPEN_ACCESS_TEXT = (
    "This is an open-access journal, which means that all content is freely available "
    "without charge to the user or his/her institution. Users are allowed to read, "
    "download, copy, distribute, print, search, or link to the full texts of the "
    "articles or use them for any other lawful purpose without asking the publisher's "
    "or the author's prior permission."
)
COPYRIGHT_TEXT  = "The authors hold the copyright of the published content."
REPOSITORY_TEXT = (
    "Authors can deposit all versions of their work, including submitted, accepted, "
    "and published versions, in their preferred institutional or other repository."
)

# ── Helpers ──────────────────────────────────────────────────────────────────

def pdf_page_count(path: str) -> int:
    """Return the number of pages in a PDF file."""
    reader = PdfReader(path)
    return len(reader.pages)


def render_qmd_to_pdf(qmd_path: Path) -> Path:
    """Render a QMD file to PDF and return the generated PDF path."""
    if not qmd_path.exists():
        raise FileNotFoundError(f"Chronicles QMD not found: {qmd_path}")

    out_pdf = qmd_path.with_suffix(".pdf")
    cmd = ["quarto", "render", str(qmd_path), "--to", "pdf"]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        msg = (proc.stderr or proc.stdout or "").strip()
        raise RuntimeError(f"Failed rendering chronicles QMD: {qmd_path}\n{msg}")
    if not out_pdf.exists():
        raise RuntimeError(f"Quarto render did not create expected PDF: {out_pdf}")
    return out_pdf


def png_to_pdf_bytes(image_path: str) -> bytes:
    """Convert a PNG to a single-page letter PDF, stretched to fill full page."""
    img = Image.open(image_path)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    img = img.resize((int(PAGE_W), int(PAGE_H)), Image.LANCZOS)

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        tmp_path = tmp.name
        img.save(tmp_path, format="JPEG", quality=95)

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    c.drawImage(tmp_path, 0, 0, width=PAGE_W, height=PAGE_H)
    c.save()
    os.unlink(tmp_path)
    return buf.getvalue()


def normalize_cover_to_letter(pdf_bytes: bytes) -> bytes:
    """Scale a PDF cover to letter size (612×792 pt) edge-to-edge."""
    reader = PdfReader(io.BytesIO(pdf_bytes))
    page   = reader.pages[0]
    orig_w = float(page.mediabox.width)
    orig_h = float(page.mediabox.height)

    if abs(orig_w - PAGE_W) < 2 and abs(orig_h - PAGE_H) < 2:
        return pdf_bytes  # already letter — nothing to do

    # Stretch mode: no crop, no bars.
    sx = PAGE_W / orig_w
    sy = PAGE_H / orig_h

    writer   = PdfWriter()
    new_page = writer.add_blank_page(width=PAGE_W, height=PAGE_H)
    new_page.merge_transformed_page(
        page,
        Transformation().scale(sx, sy)
    )
    buf = io.BytesIO()
    writer.write(buf)
    return buf.getvalue()


def parse_info_md(info_path: Path) -> dict:
    """Parse YAML frontmatter from info.md and return it as a dict."""
    text = info_path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        raise ValueError(f"No YAML frontmatter found in {info_path}")
    return yaml.safe_load(match.group(1)) or {}


def build_masthead_pdf(info: dict, config: dict) -> bytes:
    """
    Generate the journal preface/masthead as a multi-page PDF matching the
    layout of the published article-edition.pdf example:
      Page i   — ISSN, About, Open Access, Copyrights, Repository Policy
      Page ii  — Journal Qualification (website, submission, editor contact)
      Page iii — Masthead (centered): Executive Director, EiC, Board, Reviewers
    """
    buf = io.BytesIO()

    year   = config.get("year", "")
    volume = config.get("volume", "")
    issue  = config.get("issue", "")

    eic  = info.get("editor_in_chief",    {})
    assoc = info.get("associate_editor",  {})
    exec_ = info.get("executive_director",{})
    board = info.get("editorial_board",   [])

    eic_name  = eic.get("name", "")
    eic_inst  = eic.get("institution", "")
    eic_email = eic.get("email", "")

    # ── Shared styles ──────────────────────────────────────────────────────────
    body_font = "Times-Roman"      # matches the LaTeX/serif look of the original
    bold_font = "Times-Bold"
    ital_font = "Times-Italic"

    def s(name, **kw):
        defaults = dict(fontName=body_font, fontSize=10, leading=14)
        defaults.update(kw)
        return ParagraphStyle(name, **defaults)

    s_issn     = s("issn",    fontSize=10, spaceAfter=14)
    s_head     = s("head",    fontName=bold_font, fontSize=10, leading=14,
                   spaceBefore=12, spaceAfter=4)
    s_body     = s("body",    fontSize=10, leading=14, spaceAfter=6,
                   alignment=TA_JUSTIFY)
    s_bullet   = s("bullet",  fontSize=10, leading=14, leftIndent=18,
                   firstLineIndent=-12, spaceAfter=4, alignment=TA_JUSTIFY)
    s_footnote = s("fn",      fontSize=8, leading=11, spaceAfter=0)

    # ── PAGE i: About / Open Access / Copyrights / Repository ─────────────────
    # Text pulled from info.md fields only — if a field is absent (deleted),
    # that section is omitted entirely. No fallback to hardcoded defaults.
    about_p1       = info.get("about_p1")          # None if deleted
    about_p2       = info.get("about_p2")
    about_p3       = info.get("about_p3")
    about_sections = info.get("about_sections")     # None if deleted
    about_p4       = info.get("about_p4")
    massengale_fn  = info.get("massengale_footnote")
    open_access    = info.get("open_access")
    copyright_txt  = info.get("copyright")
    repository_txt = info.get("repository_policy")

    story_p1 = []
    story_p1.append(Paragraph(JOURNAL_ISSN, s_issn))

    # About the Journal — only rendered if at least one sub-field is present
    about_items = [about_p1, about_p2, about_p3, about_sections, about_p4]
    if any(x is not None for x in about_items):
        story_p1.append(Paragraph("About the Journal", s_head))
        if about_p1:
            story_p1.append(Paragraph(about_p1, s_body))
        if about_p2:
            story_p1.append(Paragraph(about_p2, s_body))
        if about_p3:
            story_p1.append(Paragraph(about_p3, s_body))
        if about_sections:
            for item in about_sections:
                story_p1.append(Paragraph(f"• &nbsp; {item}", s_bullet))
        if about_p4:
            story_p1.append(Paragraph(about_p4, s_body))

    if massengale_fn:
        story_p1.append(Spacer(1, 4))
        story_p1.append(HRFlowable(width="100%", thickness=0.5,
                                   color=colors.HexColor("#aaaaaa")))
        story_p1.append(Paragraph(massengale_fn, s_footnote))

    if open_access is not None:
        story_p1.append(Paragraph("Open Access", s_head))
        story_p1.append(Paragraph(open_access, s_body))

    if copyright_txt is not None:
        story_p1.append(Paragraph("Copyrights", s_head))
        story_p1.append(Paragraph(copyright_txt, s_body))

    if repository_txt is not None:
        story_p1.append(Paragraph("Repository Policy", s_head))
        story_p1.append(Paragraph(repository_txt, s_body))

    # ── PAGE ii: Journal Qualification ────────────────────────────────────────
    story_p2 = []
    story_p2.append(Paragraph("Journal Qualification", s_head))
    story_p2.append(Paragraph(
        "Visit the JKW website for more information:<br/>"
        "https://jkw.wskw.org/index.php/jkw/about", s_body))
    story_p2.append(Paragraph(
        "Note to authors: Manuscripts can be submitted through the JKW website:<br/>"
        "https://jkw.wskw.org/index.php/jkw/submission", s_body))
    if eic_name:
        contact = eic_name
        if eic_email:
            contact += f", Editor-in-Chief at {eic_email}"
        story_p2.append(Paragraph(
            f"Questions can be directed to {contact}.", s_body))

    # ── PAGE iii: Masthead (centered) ─────────────────────────────────────────
    story_p3 = []

    s_title   = s("title",  fontName=bold_font, fontSize=14, leading=18,
                  alignment=TA_CENTER, spaceAfter=2,
                  textColor=colors.HexColor("#1a3a5c"))
    s_subtitle= s("sub",    fontSize=11, leading=14, alignment=TA_CENTER,
                  spaceAfter=28)
    s_pname   = s("pname",  fontSize=11, leading=15, alignment=TA_CENTER,
                  spaceAfter=1)
    s_pinst   = s("pinst",  fontName=ital_font, fontSize=11, leading=15,
                  alignment=TA_CENTER, spaceAfter=1)
    s_prole   = s("prole",  fontName=bold_font, fontSize=11, leading=15,
                  alignment=TA_CENTER, spaceAfter=20)
    s_bhead   = s("bhead",  fontName=bold_font, fontSize=11, leading=15,
                  alignment=TA_CENTER, spaceBefore=8, spaceAfter=8)
    s_bcell   = s("bcell",  fontSize=10, leading=14, alignment=TA_CENTER)
    s_bicell  = s("bicell", fontName=ital_font, fontSize=10, leading=13,
                  alignment=TA_CENTER)
    s_rhead   = s("rhead",  fontName=bold_font, fontSize=10, leading=14,
                  alignment=TA_CENTER, spaceBefore=14, spaceAfter=6)
    s_rcell   = s("rcell",  fontSize=9, leading=13, alignment=TA_CENTER)

    story_p3.append(Paragraph("Journal of Kinesiology and Wellness", s_title))
    story_p3.append(Paragraph(
        "A Publication of the Western Society for Kinesiology and Wellness",
        s_subtitle))

    # Executive Director first (matches the example layout)
    for person, role_label in [
        (exec_, "WSKW Executive Director"),
        (eic,   "JKW Editor-in-Chief"),
        (assoc, "Associate Editor"),
    ]:
        if not person or not person.get("name"):
            continue
        story_p3.append(Paragraph(person.get("name", ""), s_pname))
        if person.get("institution"):
            story_p3.append(Paragraph(person["institution"], s_pinst))
        story_p3.append(Paragraph(role_label, s_prole))

    # Editorial board — two columns, name bold + institution italic, centered
    if board:
        story_p3.append(Paragraph("JKW Editorial Board", s_bhead))
        board_rows = []
        for i in range(0, len(board), 2):
            left  = board[i]
            right = board[i+1] if i+1 < len(board) else None

            def board_cell(m):
                if not m:
                    return Paragraph("", s_bcell)
                lines = f'<b>{m.get("name","")}</b>'
                if m.get("institution"):
                    lines += f'<br/><i>{m["institution"]}</i>'
                return Paragraph(lines, s_bcell)

            board_rows.append([board_cell(left), board_cell(right)])

        tbl = Table(board_rows, colWidths=[3.25*inch, 3.25*inch])
        tbl.setStyle(TableStyle([
            ("VALIGN",        (0, 0), (-1, -1), "TOP"),
            ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
            ("TOPPADDING",    (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        story_p3.append(tbl)

    # Reviewers — single centered column, sorted by first name
    def add_reviewers_centered(key, heading):
        reviewers = info.get(key, [])
        if not reviewers:
            return
        reviewers = sorted(
            [str(r) for r in reviewers],
            key=lambda r: r.split(",", 1)[0].strip().split()[0].lower()
            if r.split(",", 1)[0].strip() else ""
        )
        story_p3.append(Paragraph(heading, s_rhead))
        rev_rows = []
        # Split "Name, Institution" into name + italic institution
        def fmt_rev(r):
            if ", " in r:
                parts = r.split(", ", 1)
                return f'{parts[0]}, <i>{parts[1]}</i>'
            return r

        for reviewer in reviewers:
            rev_rows.append([Paragraph(fmt_rev(reviewer), s_rcell)])

        tbl = Table(rev_rows, colWidths=[6.0*inch])
        tbl.setStyle(TableStyle([
            ("VALIGN",        (0, 0), (-1, -1), "TOP"),
            ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
            ("TOPPADDING",    (0, 0), (-1, -1), 1),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
        ]))
        story_p3.append(tbl)

    add_reviewers_centered(
        "reviewers_annual",
        f"Reviewers for Vol {volume}, No 1, {year}- Annual Edition")
    add_reviewers_centered(
        "reviewers_student",
        f"Reviewers for Vol {volume}, No 2, {year}- Student Edition")

    # ── Render each page into its own PDF, then stitch together ───────────────
    def render_page(story, page_num_roman):
        """Render a single story to PDF bytes."""
        pbuf = io.BytesIO()
        doc = SimpleDocTemplate(
            pbuf,
            pagesize=letter,
            leftMargin=1.25*inch, rightMargin=1.25*inch,
            topMargin=1*inch, bottomMargin=0.75*inch,
        )
        doc.build(story)
        return pbuf.getvalue()

    def stamp_roman_page_number(pdf_bytes, roman):
        """Stamp a fixed-position roman numeral at the physical bottom-center."""
        overlay = io.BytesIO()
        c = canvas.Canvas(overlay, pagesize=letter)
        c.setFont("Times-Roman", 10)
        c.drawRightString(PAGE_W - 40, 16, roman)
        c.save()
        overlay.seek(0)

        base_reader = PdfReader(io.BytesIO(pdf_bytes))
        ov_reader = PdfReader(overlay)
        writer = PdfWriter()
        page = base_reader.pages[0]
        page.merge_page(ov_reader.pages[0])
        writer.add_page(page)
        out = io.BytesIO()
        writer.write(out)
        return out.getvalue()

    pages_pdf = [
        stamp_roman_page_number(render_page(story_p1, "i"), "i"),
        stamp_roman_page_number(render_page(story_p2, "ii"), "ii"),
        stamp_roman_page_number(render_page(story_p3, "iii"), "iii"),
    ]

    # Merge the three pages into one PDF
    writer = PdfWriter()
    for pdf_bytes in pages_pdf:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        for page in reader.pages:
            writer.add_page(page)

    out = io.BytesIO()
    writer.write(out)
    return out.getvalue()


def build_toc_pdf(config: dict, page_map: list) -> bytes:
    """Generate the Table of Contents page as PDF bytes (flat list, no sections)."""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        leftMargin=1*inch, rightMargin=1*inch,
        topMargin=0.9*inch, bottomMargin=0.9*inch,
    )

    year   = config.get("year", "")
    volume = config.get("volume", "")
    issue  = config.get("issue", "")

    heading = ParagraphStyle(
        "Heading", fontName="Helvetica-Bold", fontSize=15, leading=20,
        alignment=TA_CENTER, spaceAfter=2)
    subheading = ParagraphStyle(
        "Subheading", fontName="Helvetica", fontSize=9, leading=12,
        alignment=TA_CENTER, spaceAfter=16,
        textColor=colors.HexColor("#555555"))
    toc_title = ParagraphStyle(
        "TocTitle", fontName="Helvetica-Bold", fontSize=12, leading=16,
        alignment=TA_CENTER, spaceBefore=4, spaceAfter=14)
    article_style = ParagraphStyle(
        "Article", fontName="Helvetica", fontSize=8.5, leading=12,
        spaceAfter=3)
    chron_style = ParagraphStyle(
        "Chronicles", fontName="Helvetica-Bold", fontSize=9.5, leading=13,
        spaceBefore=10, spaceAfter=3,
        textColor=colors.HexColor("#1a3a5c"))
    page_num_style = ParagraphStyle(
        "PageNum", fontName="Helvetica", fontSize=8.5, leading=12,
        alignment=TA_RIGHT)

    story = []
    story.append(Paragraph(JOURNAL_NAME, heading))
    story.append(Paragraph(
        f"Vol {volume}, No {issue} &nbsp;&nbsp;|&nbsp;&nbsp; {year} &nbsp;&nbsp;|&nbsp;&nbsp; {JOURNAL_ISSN}",
        subheading,
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1a3a5c")))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Table of Contents", toc_title))

    toc_data = []
    col_widths = [5.5*inch, 0.8*inch]

    for entry in page_map:
        if entry["type"] == "article":
            toc_data.append([
                Paragraph(entry["label"], article_style),
                Paragraph(str(entry["page"]), page_num_style),
            ])
        elif entry["type"] == "chronicles":
            toc_data.append(["", ""])   # small gap before chronicles
            toc_data.append([
                Paragraph(entry["label"], chron_style),
                Paragraph(str(entry["page"]), page_num_style),
            ])

    if toc_data:
        tbl = Table(toc_data, colWidths=col_widths)
        tbl.setStyle(TableStyle([
            ("VALIGN",        (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING",    (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("LINEBELOW",     (0, -1), (-1, -1), 0.5,
             colors.HexColor("#cccccc")),
        ]))
        story.append(tbl)

    doc.build(story)
    return buf.getvalue()


# ── Main ─────────────────────────────────────────────────────────────────────

def main(config_path: str):
    config_file = Path(config_path).resolve()
    if not config_file.exists():
        sys.exit(f"ERROR: Config file not found: {config_path}")

    with open(config_file) as f:
        config = yaml.safe_load(f)

    base = config_file.parent

    year        = config.get("year", "UNKNOWN")
    output_name = config.get("output_file", f"JKW_{year}_Full_Volume.pdf")
    output_path = base / output_name

    cover_src  = config.get("cover_image", "")
    articles   = config.get("articles", [])
    chronicles = config.get("chronicles", {})

    # Optional info.md
    info_path = base / "sources" / "manuscripts" / "info.md"
    has_info  = info_path.exists()

    print(f"\n{'='*60}")
    print(f"  JKW Full Volume Builder — {year}")
    print(f"{'='*60}")

    # ── Validate files ────────────────────────────────────────────────────────
    errors = []

    cover_path = base / cover_src if cover_src else None
    if not cover_path or not cover_path.exists():
        errors.append(f"  Cover not found: {cover_src}")

    for i, art in enumerate(articles):
        p = base / art["file"]
        if not p.exists():
            errors.append(f"  Article {i+1} not found: {art['file']}")

    chron_qmd = chronicles.get("qmd")
    chron_file = chronicles.get("file")
    chron_path = base / chron_file if chron_file else None
    chron_qmd_path = base / chron_qmd if chron_qmd else None

    if chron_qmd_path:
        if not chron_qmd_path.exists():
            errors.append(f"  Chronicles QMD not found: {chron_qmd}")
    else:
        if not chron_path or not chron_path.exists():
            errors.append(f"  Chronicles not found: {chronicles.get('file', '(not set)')}")

    chron_reader = None
    chron_total_pages = 0
    chron_start = 1
    chron_end = 0
    chron_source_label = chron_qmd if chron_qmd else chron_file
    if chron_qmd_path and chron_qmd_path.exists():
        # Render curated conference content from QMD for consistency.
        chron_pdf_path = render_qmd_to_pdf(chron_qmd_path)
        chron_reader = PdfReader(str(chron_pdf_path))
        chron_total_pages = len(chron_reader.pages)
        chron_start = 1
        chron_end = chron_total_pages
    elif chron_path and chron_path.exists():
        chron_reader = PdfReader(str(chron_path))
        chron_total_pages = len(chron_reader.pages)
        chron_start = int(chronicles.get("start_page", 1))
        chron_end = int(chronicles.get("end_page", chron_total_pages))
        if chron_start < 1 or chron_end < chron_start or chron_end > chron_total_pages:
            errors.append(
                f"  Chronicles page range invalid: start_page={chron_start}, "
                f"end_page={chron_end}, file has {chron_total_pages} pages")

    if errors:
        print("\nERRORS — fix these before building:\n")
        for e in errors:
            print(e)
        sys.exit(1)

    # ── Step 1: Cover ─────────────────────────────────────────────────────────
    print("\n[1/5] Processing cover...")
    suffix = Path(cover_src).suffix.lower()
    if suffix == ".pdf":
        cover_bytes = normalize_cover_to_letter(cover_path.read_bytes())
    else:
        cover_bytes = png_to_pdf_bytes(str(cover_path))
    cover_reader = PdfReader(io.BytesIO(cover_bytes))
    cover_pages  = len(cover_reader.pages)
    print(f"      {cover_src} → {cover_pages} page(s)")

    # ── Step 2: Masthead (optional) ───────────────────────────────────────────
    masthead_reader = None
    masthead_pages  = 0
    if has_info:
        print("\n[2/5] Generating masthead from info.md...")
        try:
            info = parse_info_md(info_path)
            masthead_bytes  = build_masthead_pdf(info, config)
            masthead_reader = PdfReader(io.BytesIO(masthead_bytes))
            masthead_pages  = len(masthead_reader.pages)
            print(f"      info.md → {masthead_pages} page(s)")
        except Exception as e:
            print(f"      WARNING: Could not parse info.md ({e}) — skipping masthead")
    else:
        print("\n[2/5] No info.md found — skipping masthead")
        print(f"      (Add sources/manuscripts/info.md to include the journal masthead)")

    # ── Step 3: Count article pages & build TOC map ───────────────────────────
    print("\n[3/5] Counting pages and building TOC map...")

    # Two-pass TOC: first build with an estimated TOC size, then correct if needed.
    # Page layout: cover | masthead (if any) | TOC (N pages) | articles | chronicles
    def build_page_map(toc_pages):
        rp = cover_pages + masthead_pages + toc_pages + 1
        pm, af = [], []
        for art in articles:
            title      = art.get("title", "(Untitled)")
            fpath      = base / art["file"]
            n          = pdf_page_count(str(fpath))
            # If the article specifies its original printed start page, use that
            # for the TOC so readers can cross-reference the printed page numbers.
            toc_page   = art.get("page_start", rp)
            pm.append({"type": "article", "label": title, "page": toc_page})
            af.append((str(fpath), n))
            rp += n
        c_start     = rp
        c_title     = chronicles.get("title", "WSKW Chronicles")
        chron_toc_p = chronicles.get("page_start", c_start)
        pm.append({"type": "chronicles", "label": c_title, "page": chron_toc_p})
        return pm, af

    page_map, art_files = build_page_map(toc_pages=1)
    # Build a draft TOC to find the real page count
    draft_toc  = build_toc_pdf(config, page_map)
    actual_toc_pages = len(PdfReader(io.BytesIO(draft_toc)).pages)
    if actual_toc_pages != 1:
        # Recalculate with the correct TOC page count
        page_map, art_files = build_page_map(toc_pages=actual_toc_pages)

    running_page = cover_pages + masthead_pages + actual_toc_pages + 1  # for display only

    for entry, (fpath, n) in zip([e for e in page_map if e["type"] == "article"], art_files):
        end = entry["page"] + n - 1
        print(f"      p{entry['page']}\u2013{end}  ({n} pp)  {Path(fpath).relative_to(base)}")

    chron_entry = next(e for e in page_map if e["type"] == "chronicles")
    chron_pages = chron_end - chron_start + 1
    print(f"      p{chron_entry['page']}\u2013{chron_entry['page'] + chron_pages - 1}  ({chron_pages} pp)  {chron_source_label}")

    # ── Step 4: Build TOC (final, with correct page numbers) ──────────────────
    print("\n[4/5] Generating Table of Contents...")
    toc_bytes  = build_toc_pdf(config, page_map)
    toc_reader = PdfReader(io.BytesIO(toc_bytes))

    # ── Step 5: Merge everything ──────────────────────────────────────────────
    print("\n[5/5] Merging all PDFs...")
    writer = PdfWriter()

    for page in cover_reader.pages:
        writer.add_page(page)

    if masthead_reader:
        for page in masthead_reader.pages:
            writer.add_page(page)

    for page in toc_reader.pages:
        writer.add_page(page)

    for fpath, _ in art_files:
        reader = PdfReader(fpath)
        for page in reader.pages:
            writer.add_page(page)

    for i in range(chron_start - 1, chron_end):
        writer.add_page(chron_reader.pages[i])

    total_pages = len(writer.pages)

    with open(output_path, "wb") as out:
        writer.write(out)

    print(f"\n{'='*60}")
    print(f"  ✓ Done!  {total_pages} total pages")
    if has_info and masthead_reader:
        print(f"  Masthead included ({masthead_pages} pp from info.md)")
    print(f"  Output → {output_path}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} YYYY/volume_config.yaml")
        sys.exit(1)
    main(sys.argv[1])
