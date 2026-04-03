# JKW Full Volume Repository

This repository assembles the annual full-volume publication of the
**Journal of Kinesiology & Wellness (JKW)**, including all editions and the
WSKW Chronicles conference abstracts.

---

## Repository Structure

```
jkw-full/
├── README.md                   ← you are here
├── YYYY/                       ← one folder per year
│   ├── render-YYYY.sh          ← run this to build everything
│   ├── cover-YYYY.pdf/.png     ← cover image (user provides)
│   ├── full_issue.qmd          ← master PDF: preface + articles + chronicles
│   ├── article-edition.qmd     ← cover + preface + articles only
│   ├── student-edition.qmd     ← cover + preface + student articles only
│   ├── annual-conference.qmd   ← conference preface + chronicles
│   ├── annual-conference-preface.qmd  ← conference welcome, speakers, leadership
│   ├── annual-ed/
│   │   └── preface.qmd         ← journal masthead, about, reviewers
│   ├── chronicles/
│   │   ├── _content.qmd        ← all conference abstract content
│   │   └── YYYY_WSKW_Chronicles.qmd  ← standalone chronicles PDF
│   └── sources/
│       ├── manuscripts/        ← drop final article PDFs here
│       ├── reviewers/          ← reviewer lists (index.md)
│       └── conference/         ← raw conference program/abstract docs
```

---

## How to Compile a New Issue

### Step 1 — Set up the year folder

Copy the previous year's folder as a starting point:

```bash
cp -r 2023/ 2024/
```

Then rename the year-specific files:

```bash
cd 2024/
mv chronicles/2023_WSKW_Chronicles.qmd chronicles/2024_WSKW_Chronicles.qmd
mv render-2023.sh render-2024.sh
```

Update the year references inside the renamed files.

---

### Step 2 — Drop article PDFs into `sources/manuscripts/`

Place all finalized article PDFs in `YYYY/sources/manuscripts/`.  
Filenames should be clean (no spaces). Example: `eastman-etal-2024.pdf`

---

### Step 3 — Update `annual-ed/preface.qmd`

Fill in for the new year:

| Field | Where |
|---|---|
| Volume & year | Reviewer section headers (`Vol XX, No 1, YYYY`) |
| Editor-in-Chief | Masthead block |
| Associate Editor | Masthead block (omit section if none) |
| WSKW Executive Director | Masthead block |
| Editorial board members | Two-column board block |
| Annual edition reviewers | `Reviewers for Vol XX, No 1` block |
| Student edition reviewers | `Reviewers for Vol XX, No 2` block (omit if none) |
| Google Scholar h-index | `Journal Qualification` section |
| Editor contact email | Last line of About section |

> **Reference:** See `2022/annual-ed/preface.qmd` for the canonical layout.

---

### Step 4 — Update `chronicles/_content.qmd`

Replace all abstract content with the new year's conference abstracts:

- Keynote speaker header
- E.C. Davis Lecture header
- Each abstract as a `##` section followed by the abstract text and a `---` divider
- Student Poster Session table (if applicable)
- Faculty Poster Session table (if applicable)

---

### Step 5 — Update `chronicles/YYYY_WSKW_Chronicles.qmd`

Update:
- `title`, `subtitle`, `date`, `author` in the YAML front matter
- `\setcounter{page}{N}` — set to the page number where the chronicles begin
  in the full issue (i.e., the page after the last article ends)

---

### Step 6 — Update `annual-conference-preface.qmd`

Fill in:
- Conference number (e.g., 68th Annual)
- Conference theme, dates, location
- Welcome message from the President-Elect
- Featured speakers (Keynote + E.C. Davis Lecture) with bios
- WSKW Leadership Team

---

### Step 7 — Update edition QMDs

In `full_issue.qmd`, `article-edition.qmd`, `student-edition.qmd`:

- Update `\includepdf` paths to point to the new article PDF filenames
- Update `addtotoc` titles to match the exact published article titles
- Update `\setcounter{page}{N}` values so page numbers are continuous
- Update the cover image filename

> **Page numbering rules:**
> - `full_issue.qmd`: Arabic starts at page **3** (pages i–ii are Roman front matter)
> - `article-edition.qmd` and `student-edition.qmd`: Arabic starts at page **1**
> - The WSKW Chronicles `\setcounter` must match the page after the last article in `full_issue`

---

### Step 8 — Render everything

Run from the **repo root** (`jkw-full/`):

```bash
bash YYYY/render-YYYY.sh
```

This renders all 6 files in the correct dependency order:

1. `annual-ed/preface.qmd` → `preface.pdf`
2. `chronicles/YYYY_WSKW_Chronicles.qmd` → `YYYY_WSKW_Chronicles.pdf`
3. `full_issue.qmd` → `full_issue.pdf`
4. `article-edition.qmd` → `article-edition.pdf`
5. `student-edition.qmd` → `student-edition.pdf`
6. `annual-conference.qmd` → `annual-conference.pdf`

> `preface.pdf` and `YYYY_WSKW_Chronicles.pdf` **must** exist before the
> edition QMDs render — the script handles this automatically.

---

## Common Issues

**`compilation failed — error: Cannot find file 'annual-ed/preface.pdf'`**  
→ The preface hasn't been rendered yet. Run `render-YYYY.sh` (not individual files).

**`Paragraph ended before \addcontentsline was complete`**  
→ A `% comment` line in the QMD body is being escaped to `\%` by Pandoc.
Remove any `%`-style comments from the raw LaTeX sections of QMD files.

**Wrong page numbers in the TOC**  
→ The `\setcounter{page}{N}` values are off. Open the final PDF, count actual
pages per article, then update the counters and re-render.

**Cover page appearing in TOC**  
→ Ensure `\pagenumbering{gobble}` appears before the cover `\includepdf` line.

---

## Year Index

| Year | Volume | Render script |
|------|--------|---------------|
| 2022 | Vol 11, No 1 | *(no script — assembled manually)* |
| 2023 | Vol 12, No 1 | `2023/render-2023.sh` |
| 2024 | Vol 13, No 1 | *(pending)* |
| 2025 | Vol 14, No 1 | *(pending)* |
| 2026 | Vol 15, No 1 | *(pending)* |

---

## PDF-Only Publishing Workflow (GitHub Pages)

Use this workflow when the user only needs direct PDF links (no HTML viewer pages).

1. Render yearly PDFs in `YYYY/`.
2. Rename each publication PDF:
  - `_YYYY_annual-conference.pdf`
  - `_YYYY_article-edition.pdf`
  - `_YYYY_student-edition.pdf`
3. Copy each renamed PDF into `docs/YYYY/`.
4. Ensure `docs/.nojekyll` exists.
5. Commit and push.

### Renaming Example (2023)

```bash
cp 2023/annual-conference.pdf 2023/_2023_annual-conference.pdf
cp 2023/article-edition.pdf 2023/_2023_article-edition.pdf
cp 2023/student-edition.pdf 2023/_2023_student-edition.pdf

mkdir -p docs/2023
cp 2023/_2023_annual-conference.pdf docs/2023/_2023_annual-conference.pdf
cp 2023/_2023_article-edition.pdf docs/2023/_2023_article-edition.pdf
cp 2023/_2023_student-edition.pdf docs/2023/_2023_student-edition.pdf
```

### URL Pattern

```text
https://wskwellness.github.io/jkw-annual/YYYY/_YYYY_<edition>.pdf
```

---

## Website HTML Snippets (Copy/Paste)

Use these as separate snippets for easier copy and paste.

### 2022 Annual Conference

```html
<a href="https://wskwellness.github.io/jkw-annual/2022/_2022_annual-conference.pdf" target="_blank" rel="noopener noreferrer"><strong>[PDF]</strong> Annual Conference</a>
```

### 2022 Article Edition

```html
<a href="https://wskwellness.github.io/jkw-annual/2022/_2022_article-edition.pdf" target="_blank" rel="noopener noreferrer"><strong>[PDF]</strong> Article Edition</a>
```

### 2022 Student Edition

```html
<a href="https://wskwellness.github.io/jkw-annual/2022/_2022_student-edition.pdf" target="_blank" rel="noopener noreferrer"><strong>[PDF]</strong> Article (Student Scholarship)</a>
```

### 2023 Annual Conference

```html
<a href="https://wskwellness.github.io/jkw-annual/2023/_2023_annual-conference.pdf" target="_blank" rel="noopener noreferrer"><strong>[PDF]</strong> Annual Conference</a>
```

### 2023 Article Edition

```html
<a href="https://wskwellness.github.io/jkw-annual/2023/_2023_article-edition.pdf" target="_blank" rel="noopener noreferrer"><strong>[PDF]</strong> Article Edition</a>
```

### 2023 Student Edition

```html
<a href="https://wskwellness.github.io/jkw-annual/2023/_2023_student-edition.pdf" target="_blank" rel="noopener noreferrer"><strong>[PDF]</strong> Article (Student Scholarship)</a>
```
