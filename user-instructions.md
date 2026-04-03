# JKW Full Volume Repository

This repository assembles the annual full-volume publication of the
**Journal of Kinesiology & Wellness (JKW)**, including all peer-reviewed articles
and the WSKW Chronicles conference abstracts — output as a single PDF.

---

## Repository Structure

```
jkw-full/
├── user-instructions.md          ← you are here
├── build_full_volume.py          ← single script that builds the PDF
├── volume_config_template.yaml   ← copy this to start a new year
├── info_template.md              ← copy this to start the masthead
├── YYYY/
│   ├── volume_config.yaml        ← fill in titles, files, cover for this year
│   ├── cover-YYYY.pdf/.png       ← cover image (user provides)
│   ├── JKW_YYYY_Full_Volume.pdf  ← output: the finished single PDF
│   └── sources/
│       ├── manuscripts/
│       │   ├── info.md           ← masthead: editors, board, reviewers (optional)
│       │   └── *.pdf             ← final article PDFs
│       └── conference/           ← WSKW Chronicles PDF
```

**Output page order:** Cover → Masthead (if info.md present) → TOC → Articles → WSKW Chronicles

---

## How to Build a New Issue

### Step 1 — Create the year folder

```bash
mkdir -p YYYY/sources/manuscripts
mkdir -p YYYY/sources/conference
```

---

### Step 2 — Drop the files in place

| File | Where to put it |
|------|-----------------|
| Cover image (`.pdf` or `.png`) | `YYYY/cover-YYYY.pdf` (or `.png`) |
| Final article PDFs | `YYYY/sources/manuscripts/` |
| WSKW Chronicles PDF | `YYYY/sources/conference/` |
| Masthead info (optional) | `YYYY/sources/manuscripts/info.md` |

Filenames should have no spaces. Example: `eastman-etal-2025.pdf`

#### About `info.md` (optional but recommended)

If `sources/manuscripts/info.md` is present, the script automatically generates a
formatted masthead page and inserts it between the cover and the TOC. It includes
the About / Open Access / Copyright boilerplate, the h-index, editorial team, and
reviewer lists. Copy `info_template.md` from the repo root to get started:

```bash
cp info_template.md YYYY/sources/manuscripts/info.md
```

Then fill in the fields. If no `info.md` is present the build still runs — the
masthead page is simply omitted.

---

### Step 3 — Create `YYYY/volume_config.yaml`

Copy the template and fill it in:

```bash
cp volume_config_template.yaml YYYY/volume_config.yaml
```

Edit `volume_config.yaml` and fill in:

| Field | What to enter |
|-------|--------------|
| `year` | e.g., `2025` |
| `volume` | e.g., `14` |
| `issue` | e.g., `1` |
| `cover_image` | filename of the cover PNG (e.g., `cover-2025.png`) |
| `output_file` | desired output filename (e.g., `JKW_2025_Full_Volume.pdf`) |
| `articles` | list of articles in order — file path and exact title |
| `chronicles.file` | path to the Chronicles PDF |
| `chronicles.qmd` | *(preferred, 2022-style)* curated Chronicles QMD generated from selected pages |
| `chronicles.title` | TOC label for the Chronicles section |
| `chronicles.start_page` | *(optional)* first Chronicles page to include (1-based) |
| `chronicles.end_page` | *(optional)* last Chronicles page to include (1-based, inclusive) |

Articles appear in the PDF in the order they are listed here. Prefix your PDF
filenames with numbers (`01_`, `02_`, …) so the order is visible in the folder,
then list them in that same order. The TOC is a flat list — no sections.

---

### Step 4 — Build the PDF

Run from the repo root (`jkw-full/`):

```bash
python3 build_full_volume.py YYYY/volume_config.yaml
```

The script will:
1. Process the cover image → single PDF page
2. Count pages in every article and the Chronicles PDF
3. Auto-generate a formatted Table of Contents with correct page numbers
4. Merge everything into one PDF: **Cover → TOC → Articles → WSKW Chronicles**

Output is saved to `YYYY/JKW_YYYY_Full_Volume.pdf`.

### Step 5 — Chronicles Extraction (2022-Consistent Workflow)

For better consistency and scaling, generate a curated Chronicles QMD from
selected conference-program pages (same pattern used in 2022):

```bash
python3 scripts/build/extract-chronicles-qmd.py \
  --input YYYY/sources/conference/YYYY-WSKW-Conference-Program.pdf \
  --output YYYY/sources/conference/YYYY_WSKW_Chronicles.qmd \
  --year YYYY \
  --volume VV \
  --issue 1 \
  --start-page SS \
  --end-page EE \
  --set-page PP
```

Then set in `YYYY/volume_config.yaml`:

```yaml
chronicles:
  qmd: sources/conference/YYYY_WSKW_Chronicles.qmd
  title: "WSKW Chronicles: YYYY WSKW Annual Conference"
```

Notes:
- Use 2022 as the formatting reference for headings, spacing, and section structure.
- `--set-page` controls the LaTeX page counter at the start of the Chronicles section.
- If needed, you can still use a raw conference PDF with `chronicles.file` plus `start_page/end_page`.

---

## Year Index

| Year | Volume | Config file | Output |
|------|--------|-------------|--------|
| 2022 | Vol 11, No 1 | `2022/volume_config.yaml` | [`2022/JKW_2022_Full_Volume.pdf`](https://wskwellness.github.io/jkw-annual/2022/_2022_full-volume.pdf) |
| 2023 | Vol 12, No 1 | `2023/volume_config.yaml` | `2023/JKW_2023_Full_Volume.pdf` |
| 2024 | Vol 13, No 1 | *(pending)* | — |
| 2025 | Vol 14, No 1 | *(pending)* | — |
| 2026 | Vol 15, No 1 | *(pending)* | — |

---

## Publishing to GitHub Pages

Once the full-volume PDF is built, publish it for distribution.

### Rename and copy to `docs/`

```bash
cp YYYY/JKW_YYYY_Full_Volume.pdf docs/YYYY/_YYYY_full-volume.pdf
```

### Ensure `.nojekyll` exists

```bash
touch docs/.nojekyll
```

### Commit and push

```bash
git add docs/YYYY/
git commit -m "Publish YYYY full volume"
git push
```

### URL pattern

```
https://wskwellness.github.io/jkw-annual/YYYY/_YYYY_full-volume.pdf
```

### Website HTML snippet (copy/paste)

```html
<a href="https://wskwellness.github.io/jkw-annual/YYYY/_YYYY_full-volume.pdf"
   target="_blank" rel="noopener noreferrer">
  <strong>[PDF]</strong> Full Volume (Vol XX, No 1, YYYY)
</a>
```

---

## Previous Years (Legacy — Quarto/LaTeX Builds)

Years 2022–2023 were assembled using Quarto `.qmd` files and a LaTeX render
pipeline. Those files remain in their year folders for archival reference but
are no longer part of the active workflow. The 2023 volume has been re-built
using the new script and is available as `2023/JKW_2023_Full_Volume.pdf`.

---

## Troubleshooting

**`ERROR: Cover not found`**
→ Check the filename in `volume_config.yaml` matches the actual file in `YYYY/`.

**`ERROR: Article N not found`**
→ Verify the PDF was placed in `sources/manuscripts/` and the filename in the
config matches exactly (case-sensitive, no spaces).

**`ERROR: Chronicles not found`**
→ Confirm the Chronicles PDF is in `sources/conference/` and the path in the
config is correct.

**TOC page numbers look wrong**
→ The script calculates page numbers automatically from actual PDF page counts —
no manual counting needed. If numbers look off, check that no article PDF is
missing or duplicated in the config.
