---
name: jkw-full-volume
description: >
  JKW annual full volume assembly skill. Use this whenever the user wants to
  build or set up the annual full-volume publication of the Journal of Kinesiology
  and Wellness — including the WSKW Chronicles conference abstracts section.
  Triggers on phrases like "assemble the full volume", "build the annual volume",
  "full issue", "WSKW Chronicles", "conference abstracts", "set up YYYY volume",
  "compile the annual edition", or any mention of assembling multiple JKW articles
  into a combined PDF with the chronicles.
---

# JKW Full Volume Assembly Skill

This skill builds the annual JKW full-volume publication, published each January.
It creates the four edition QMD files (full issue, article edition, student edition,
conference edition), the journal preface/masthead, and the WSKW Chronicles from
the year's conference abstracts.

## Context

The full volume lives in the `jkw-full/` repository (separate from `jkw-manuscripts/`).
It assembles already-rendered article PDFs using LaTeX `\includepdf` directives —
it does NOT re-typeset the articles. Articles must be finalized first.

Each year gets its own subfolder: `jkw-full/YYYY/`.

The 2022 volume is the canonical reference. When in doubt about structure or LaTeX
patterns, read the files in `jkw-full/2022/`.

### Where article PDFs come from

**2022–2025:** Final article PDFs are placed by the editor in `jkw-full/YYYY/sources/manuscripts/`.
All `\includepdf` paths in QMD files should point there (e.g., `sources/manuscripts/filename.pdf`).

**2026 onward:** All source files (manuscripts, article PDFs, reviewer lists) live in
`jkw-manuscripts/2026/`. The skill should reference PDFs from that location.
The final rendered article PDF for each submission is at:
`jkw-manuscripts/2026/SUBMISSION_ID/jkw26-SUBMISSION_ID.pdf`
Copy those PDFs into `jkw-full/2026/sources/manuscripts/` before assembling, then
reference them as `sources/manuscripts/filename.pdf` — this keeps the QMD paths
consistent across all years.

---

## Inputs — What You Need From the User

Before starting, confirm you have (or ask for) all of the following. You can ask
for them in a single structured request rather than one-by-one.

### 1. Year & Volume Metadata
- **Year** (e.g., 2026)
- **Volume number** (e.g., Vol 15) and **Issue number** (e.g., No 1)
- **Cover image filename** (e.g., `new-cover-2026.pdf`) — must already be placed in `jkw-full/YYYY/`

### 2. Article PDFs
For **each peer-reviewed article**, you need:
- PDF filename (as placed in `YYYY/sources/manuscripts/`)
- Exact article title (as it should appear in the TOC)
- Starting page number in the assembled volume

For **each student scholarship article**, same info — also in `YYYY/sources/manuscripts/`.

> Page numbers must be sequential with no gaps. The first article typically
> starts at page 1 in the article-edition, or page 3 in the full_issue (where
> pages i–ii are Roman-numeral front matter, then Arabic restarts). Confirm with
> the user. In 2022, Arabic started at page 3 in full_issue and page 1 in article-edition.

### 3. Journal Masthead / Preface
- WSKW Executive Director (name, institution)
- JKW Editor-in-Chief (name, institution)
- Associate Editor (name, institution)
- JKW Editorial Board members (name, institution — typically 6 members in two columns)
- Reviewer list for **Annual Edition** (name, institution for each)
- Reviewer list for **Student Edition** (name, institution for each)
- Google Scholar h-index values (h index all time since 2012, and since 2019) — or skip if unknown
- Current volume/year for the reviewer section headers

### 4. WSKW Chronicles — Conference Information
- Conference number (e.g., 71st Annual WSKW Conference)
- Conference theme (quoted)
- Conference dates (e.g., October 15–17, 2026)
- Conference location (venue, city, state)
- Conference leadership: President, President-Elect, Past President, Executive Director, Treasurer, Secretary — each with institution
- **Keynote speaker**: name and institution (title of talk if known)
- **E.C. Davis Lecture**: speaker name and institution
- **Academic presentation abstracts** (see format below)
- **Student poster session**: numbered list of (title, authors with institutions)
- **Faculty poster session**: numbered list of (title, authors with institutions)

#### Abstract format
For each academic presentation abstract:
```
## [Full Presentation Title] - [Author Name(s)] ([Institution(s)])

[Full abstract text, 200–400 words]

---
```

---

## Folder Structure

```
jkw-full/YYYY/
├── new-cover-YYYY.pdf            (user provides)
├── full_issue.qmd                (you generate)
├── article-edition.qmd           (you generate)
├── student-edition.qmd           (you generate)
├── annual-conference.qmd         (you generate)
├── sources/
│   ├── manuscripts/              (user drops article PDFs here — already created)
│   ├── reviewers/                (reviewer lists, assignments — already created)
│   └── conference/               (conference program, abstract docs — already created)
├── annual-ed/
│   └── preface.qmd               (you generate)
└── chronicles/
    ├── _content.qmd              (you generate — all abstract content)
    └── YYYY_WSKW_Chronicles.qmd  (you generate — standalone chronicles PDF)
```

The `sources/` subfolders already exist for 2022–2025. For new years, create them with:
```bash
mkdir -p jkw-full/YYYY/sources/{manuscripts,reviewers,conference}
```

---

## Step-by-Step Assembly

### Step 1: Scaffold the folder structure

For **2022–2025**, the `sources/` subfolders already exist. Just create:
```bash
mkdir -p jkw-full/YYYY/annual-ed
mkdir -p jkw-full/YYYY/chronicles
```

For **new years (2026+)**:
```bash
mkdir -p jkw-full/YYYY/sources/{manuscripts,reviewers,conference}
mkdir -p jkw-full/YYYY/annual-ed
mkdir -p jkw-full/YYYY/chronicles
```

Then tell the user exactly which PDF files to place in `YYYY/sources/manuscripts/`
(listing each expected filename), and wait for confirmation before generating the QMD files.

For **2026**, remind the user to copy the final rendered article PDFs from
`jkw-manuscripts/2026/SUBMISSION_ID/jkw26-SUBMISSION_ID.pdf` into
`jkw-full/2026/sources/manuscripts/` before proceeding.

---

### Step 2: Generate `preface.qmd`

Path: `jkw-full/YYYY/annual-ed/preface.qmd`

Use this structure (adapted from 2022):

```markdown
---
format:
  pdf:
    geometry:
      - top=1in
      - bottom=1in
      - left=1in
      - right=1in
    keep-tex: true
    header-includes:
      - \usepackage{multicol}
      - \usepackage{xcolor}
---

ISSN# 2332-4503

\pagenumbering{roman}

## About the Journal

The Journal of Kinesiology & Wellness (JKW) is an anonymous peer-reviewed online
journal that covers issues in physical education, physical activity & health promotion,
wellness, biomechanics, motor behavior, exercise physiology, sport, and dance. The JKW
is a publication of the Western Society for Kinesiology and Wellness (WSKW).

[... standard boilerplate paragraphs from 2022 preface ...]

## Open Access
[... standard boilerplate ...]

## Copyrights
[... standard boilerplate ...]

## Repository Policy
[... standard boilerplate ...]

## Journal Qualification

Google Scholar h index (2012-[YEAR]): [VALUE]
Google Scholar h index (since 2019): [VALUE]

Visit the JKW website for more information:
https://jkw.wskw.org/index.php/jkw/about

[... contact info ...]

\newpage

\begin{center}
    \textbf{\Large \textcolor{blue!60!black}{Journal of Kinesiology and Wellness}} \\
    ...
\end{center}

[... masthead with two-column layout for editors, board, reviewers ...]
```

Keep all standard boilerplate text identical to 2022 (`jkw-full/2022/annual-ed/preface.qmd`).
Only update: year, volume number, names, reviewer lists, h-index values.

After generating, render preface to PDF:
```bash
cd jkw-full/YYYY/annual-ed && quarto render preface.qmd
```

---

### Step 3: Generate `chronicles/_content.qmd`

Path: `jkw-full/YYYY/chronicles/_content.qmd`

This file is the modular content block included by the Chronicles QMD files.
Structure:

```markdown
## Keynote Presentation: [Title] - [Speaker], [Institution]

## E.C. Davis Lecture - [Speaker], [Institution]

---

# ABSTRACTS

## [Presentation Title] - [Author(s)] ([Institution(s)])

[Abstract text]

---

## [Next Presentation] ...

[Continue for all academic presentations]

---

## Student Poster Session

| # | Poster Title | Author(s) |
|---|---|---|
| 1 | [Title] | [Authors (Institution)] |
...

---

## Faculty Poster Session

| # | Poster Title | Author(s) |
|---|---|---|
| 1 | [Title] | [Authors (Institution)] |
...
```

---

### Step 4: Generate `chronicles/YYYY_WSKW_Chronicles.qmd`

Path: `jkw-full/YYYY/chronicles/YYYY_WSKW_Chronicles.qmd`

```yaml
---
title: "WSKW Chronicles"
subtitle: "YYYY WSKW Conference Abstracts"
date: "YYYY-01-01"
author: "Journal of Kinesiology and Wellness, Volume [N], Number 1, YYYY"
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
      - \usepackage{titling}
      - \pretitle{\begin{center}\LARGE\bfseries}
      - \posttitle{\end{center}}
      - \preauthor{\begin{center}\large}
      - \postauthor{\end{center}}
      - \predate{\begin{center}\large}
      - \postdate{\end{center}}
      - \postdate{\end{center}}
---

\setcounter{page}{[CHRONICLES_START_PAGE]}
{{< include _content.qmd >}}
```

`CHRONICLES_START_PAGE` = the page after the last student article ends.

---

### Step 5: Generate `full_issue.qmd`

Path: `jkw-full/YYYY/full_issue.qmd`

This is the master QMD that assembles everything into one PDF. Roman numerals
for front matter, then Arabic starting at page 3 (or wherever the first article
begins after the TOC).

```yaml
---
format:
  pdf:
    documentclass: scrartcl
    classoption:
      - numbers=noendperiod
      - DIV=15
    variable:
      geometry: "margin=0cm"
    header-includes:
      - \usepackage{pdfpages}
---
```

Then the body:

```latex
\pagenumbering{roman}
\includepdf[pages=-]{annual-ed/preface.pdf}

\newpage
\tableofcontents

\newpage
\pagenumbering{arabic}
\setcounter{page}{3}

\addcontentsline{toc}{section}{Articles}

\includepdf[pages=-,addtotoc={1,subsection,1,{[ARTICLE TITLE]},art1}]{sources/manuscripts/[filename].pdf}

[... repeat for each article, incrementing key: art1, art2, art3 ...]

\addcontentsline{toc}{section}{Articles (Student Scholarship)}
\setcounter{page}{[STUDENT_START_PAGE]}
\includepdf[pages=-,addtotoc={1,subsection,1,{[STUDENT TITLE]},art_s1}]{sources/manuscripts/[filename].pdf}

\includepdf[pages=-,addtotoc={1,section,1,{WSKW Chronicles: YYYY WSKW Conference Abstracts},chronicles}]{chronicles/YYYY_WSKW_Chronicles.pdf}
```

> **Important**: `\setcounter{page}{N}` before the student section ensures
> pagination continues correctly from where regular articles end. The Chronicles
> PDF already has its own page counter set; just include it directly with `\includepdf`.

---

### Step 6: Generate `article-edition.qmd`

Like `full_issue.qmd` but:
- Includes the cover image as page 1 (gobble pagination)
- Arabic starts at page 1 (not 3)
- Excludes student articles and chronicles

```latex
\pagenumbering{gobble}
\includepdf[pages=1,width=\paperwidth,height=\paperheight]{new-cover-YYYY.pdf}
\pagenumbering{roman}
\includepdf[pages=-]{annual-ed/preface.pdf}

\newpage
\tableofcontents

\newpage
\pagenumbering{arabic}
\setcounter{page}{1}

\addcontentsline{toc}{section}{Articles}
\includepdf[pages=-,addtotoc={1,subsection,1,{[ARTICLE TITLE]},art1}]{sources/manuscripts/[filename].pdf}
[... repeat for each article ...]
```

---

### Step 7: Generate `student-edition.qmd`

Same as `article-edition.qmd` but:
- Contains only student scholarship articles under `\addcontentsline{toc}{section}{Articles (Student Scholarship)}`
- Arabic pages start at 1

---

### Step 8: Generate `annual-conference.qmd`

For the conference abstracts standalone edition (preface + TOC + chronicles):

```yaml
---
format:
  pdf:
    documentclass: scrartcl
    classoption:
      - numbers=noendperiod
      - DIV=15
    variable:
      geometry: "margin=0cm"
    header-includes:
      - \usepackage{pdfpages}
---
```

```latex
[include annual-conference-preface content inline or as a separate .qmd]

\newpage
\tableofcontents

\newpage
{{< include chronicles/_content.qmd >}}
```

> In 2022, this edition had a `annual-conference-preface.qmd` with a separate
> conference-oriented preface. If you have that content, generate it as a
> separate file and include it.

---

### Step 9: Create and run the render script

Each year's folder contains a `render-YYYY.sh` script that renders all files in
the correct dependency order. Create it at `jkw-full/YYYY/render-YYYY.sh`:

```bash
#!/usr/bin/env bash
# render-YYYY.sh
set -e

YEAR_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "==> Rendering JKW YYYY volume in: $YEAR_DIR"

echo "[1/6] Rendering annual-ed/preface.qmd..."
cd "$YEAR_DIR/annual-ed" && quarto render preface.qmd

echo "[2/6] Rendering chronicles/YYYY_WSKW_Chronicles.qmd..."
cd "$YEAR_DIR/chronicles" && quarto render YYYY_WSKW_Chronicles.qmd

echo "[3/6] Rendering full_issue.qmd..."
cd "$YEAR_DIR" && quarto render full_issue.qmd

echo "[4/6] Rendering article-edition.qmd..."
quarto render article-edition.qmd

echo "[5/6] Rendering student-edition.qmd..."
quarto render student-edition.qmd

echo "[6/6] Rendering annual-conference.qmd..."
quarto render annual-conference.qmd

echo "==> All YYYY files rendered successfully."
```

Make it executable and run:
```bash
chmod +x jkw-full/YYYY/render-YYYY.sh
bash jkw-full/YYYY/render-YYYY.sh
```

**Dependency order is critical:**
1. `annual-ed/preface.qmd` → `preface.pdf` (required by all editions)
2. `chronicles/YYYY_WSKW_Chronicles.qmd` → `YYYY_WSKW_Chronicles.pdf` (required by `full_issue.qmd`)
3. All edition QMDs (`full_issue`, `article-edition`, `student-edition`, `annual-conference`)

---

### Step 10: Optional GitHub Pages PDF Viewer

If the user wants shareable browser links that open PDFs in a viewer page instead
of a GitHub blob page or a forced raw download, publish a minimal Quarto HTML site
from `docs/`.

Use this pattern:

```text
jkw-full/
├── docs/
│   ├── .nojekyll
│   ├── index.qmd
│   ├── index.html
│   ├── styles.css
│   └── YYYY/
│       ├── article-name.qmd
│       ├── article-name.html
│       └── _article-name.pdf
```

Requirements:

- Keep `docs/.nojekyll` present. This is required when published PDF filenames
  begin with `_`, otherwise GitHub Pages will not serve them.
- Copy only the PDFs meant for public viewing into `docs/YYYY/`.
- Create Quarto viewer pages (`.qmd`) that embed the PDF with an `iframe`.
- Render the QMD files to HTML before committing.
- In GitHub repository settings, enable GitHub Pages from branch `main` and folder `docs/`.

Example viewer page:

```markdown
---
title: "2026 Full Issue"
format:
  html:
    toc: false
    css: ../styles.css
page-layout: full
---

[Back to viewer index](../index.html)

<div class="pdf-frame-shell">
  <iframe src="_full_issue.pdf" title="2026 Full Issue PDF" class="pdf-frame"></iframe>
</div>
```

Example render commands:

```bash
quarto render docs/index.qmd
quarto render docs/YYYY/full-issue.qmd
```

Resulting URL pattern:

```text
https://OWNER.github.io/REPO/YYYY/full-issue.html
```

This is the preferred approach when the user needs a browser-viewer experience
for final PDFs distributed from the `jkw-full` repository.

---

## Common Issues

**`% TODO:` comments break LaTeX via Pandoc** → In QMD files, raw LaTeX `%` comment
characters get escaped to `\%` by Pandoc, which then executes as broken LaTeX.
**Never use `% comment` lines in the body of QMD files.** Use HTML comments
`<!-- TODO: ... -->` above the YAML front matter block instead, or simply delete
placeholder comments before rendering.
reports page 1 of the included PDF as the reference page. Page numbers in the TOC
reflect the assembled document's pagination via `\setcounter`. Always verify the
final PDF manually.

**Chronicles page counter reset** → The Chronicles standalone QMD has
`\setcounter{page}{N}` set explicitly. If this number is wrong, the in-text page
refs in the full_issue TOC will be off. Recalculate from the actual article PDFs'
page counts.

**Cover page shows in TOC** → Use `\pagenumbering{gobble}` before `\includepdf`
for the cover page. This suppresses numbering so the cover doesn't appear in TOC.

**preface.pdf not found** → Must render `preface.qmd` first (Step 2) before
trying to render the edition QMDs that include it.

**Table of contents too short** → If an article title is very long, the `addtotoc`
string may get clipped. Use the exact published title but you can shorten it slightly
for TOC if it wraps badly — just keep it recognizable.

---

## Quality Checklist

Before handing off the assembled volume, verify:

- [ ] All article PDFs are in `YYYY/sources/manuscripts/` and filenames match `\includepdf` paths exactly
- [ ] `preface.pdf` has been rendered from `preface.qmd`
- [ ] `YYYY_WSKW_Chronicles.pdf` has been rendered before `full_issue.qmd`
- [ ] Page numbers are continuous across all sections (check in final PDF)
- [ ] TOC entries match actual article titles
- [ ] All four edition QMDs render without LaTeX errors
- [ ] Cover image displays full-bleed (no white border) in the editions that include it
- [ ] `_content.qmd` abstracts include all presentations, student posters, and faculty posters
- [ ] Reviewer lists in preface are correct for this volume/year
- [ ] Volume/Year numbers are updated everywhere (YAML, masthead, reviewer headers)
