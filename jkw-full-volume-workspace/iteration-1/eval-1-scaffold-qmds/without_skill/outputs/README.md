# JKW 2026 Volume 15, Number 1 - Scaffold Structure

## Overview
This is the scaffolded directory structure for the **Journal of Kinesiology and Wellness (JKW)** 2026 annual volume (Volume 15, Number 1), published by the Western Society for Kinesiology and Wellness (WSKW).

**Publication Date:** January 2026  
**Total Articles:** 4 (3 peer-reviewed + 1 student scholarship)  
**Total Pages:** 56 (plus cover, preface, TOC, and chronicles)

---

## Generated Files

### Root-Level QMD Files

1. **full_issue.qmd**
   - Combines all content with preface front matter and roman numerals
   - Includes cover-front sequence, preface, TOC, all articles, and chronicles
   - Produces the complete annual volume with all sections
   - Page counter starts at 3 (after preface and TOC)

2. **article-edition.qmd**
   - Includes cover (from `new-cover-2026.pdf`)
   - Preface with editorial board and reviewer lists
   - Only peer-reviewed articles (articles 1-3)
   - Used when student scholarship papers are published separately
   - Page counter starts at 1

3. **student-edition.qmd**
   - Includes cover (from `new-cover-2026.pdf`)
   - Preface with editorial board and reviewer lists
   - Only student scholarship articles
   - Published in Vol 15, No 2
   - Page counter starts at 1

### Directory Structure

```
outputs/
├── annual-ed/
│   ├── preface.qmd          [Editorial preface with h-index, editorial board, reviewers]
│   └── pdfs/
│       ├── articles/        [Peer-reviewed article PDFs]
│       │   ├── 01-18-chen-etal-2026-final.pdf       [pages 1-18]
│       │   ├── 19-31-morales-2026-final.pdf         [pages 19-31]
│       │   └── 32-44-okafor-wu-2026-final.pdf       [pages 32-44]
│       └── Articles-student-scholarship/
│           └── s-01-11-patel-etal-2026-pub.pdf      [pages 45-55]
├── chronicles/
│   └── [Chronicles content - placeholder for WSKW conference abstracts]
├── full_issue.qmd
├── article-edition.qmd
├── student-edition.qmd
└── README.md [this file]
```

---

## Key Content Information

### Editorial Team
- **WSKW Executive Director:** Cathy Inouye (California State University, East Bay)
- **JKW Editor-in-Chief:** Jeff Bernard, Ph.D. (California State University, Stanislaus)
- **Associate Editor:** Ovande Furtado, Jr., Ph.D. (California State University, Northridge)

### Editorial Board (Vol 15, 2026)
- Seung Ho Chang, Ph.D. (San Jose State University)
- Gioella Chaparro, Ph.D. (California State University, Dominguez Hills)
- Jongil Lim, Ph.D. (Texas A&M University- San Antonio)
- Laura Robinson-Doyle, M.S. (Southern Methodist University)
- Heather Van Mullem, Ph.D. (Lewis-Clark State College)

### Reviewers - Annual Edition
- Ovande Furtado (California State University, Northridge)
- Seung Ho Chang (San Jose State University)
- Jeff Bernard (California State University, Stanislaus)
- Jongil Lim (Texas A&M University -- San Antonio)
- Gioella Chaparro (California State University, Dominguez Hills)
- Heather Van Mullem (Lewis-Clark State College)
- Laura Robinson-Doyle (Southern Methodist University)

### Reviewers - Student Edition
- Ovande Furtado (California State University, Northridge)
- Seung Ho Chang (San Jose State University)
- Jeff Bernard (California State University, Stanislaus)
- Gioella Chaparro (California State University, Dominguez Hills)

### Google Scholar Metrics
- h-index (2012-2026): 6
- h-index (since 2019): 5

---

## Article Listing

### Peer-Reviewed Articles (Vol 15, No 1)

1. **Resistance training frequency and hypertrophy in older adults: a systematic review**
   - Pages: 1-18
   - File: `01-18-chen-etal-2026-final.pdf`

2. **Motivational climate and dropout in youth soccer: a longitudinal study**
   - Pages: 19-31
   - File: `19-31-morales-2026-final.pdf`

3. **Sedentary behavior and cardiometabolic risk markers in college students**
   - Pages: 32-44
   - File: `32-44-okafor-wu-2026-final.pdf`

### Student Scholarship (Vol 15, No 2)

4. **Effects of foam rolling duration on flexibility and perceived soreness in recreational runners**
   - Pages: 45-55 (45-56 with padding)
   - File: `s-01-11-patel-etal-2026-pub.pdf`

---

## Next Steps

### Before Rendering

1. **Place Article PDFs:** Copy the three peer-reviewed article PDFs to `annual-ed/pdfs/articles/`
2. **Place Student PDF:** Copy the student scholarship PDF to `annual-ed/pdfs/Articles-student-scholarship/`
3. **Place Cover:** Ensure `new-cover-2026.pdf` is in the root directory (already available per task notes)
4. **Add Chronicles:** Generate `2026_WSKW_Chronicles.pdf` and place in `chronicles/` directory

### Rendering

```bash
# Render the complete volume with all content
quarto render full_issue.qmd

# Render the peer-reviewed articles edition
quarto render article-edition.qmd

# Render the student scholarship edition
quarto render student-edition.qmd
```

### Output Files

After rendering, you will have:
- `full_issue.pdf` - Complete volume with cover, preface, all articles, and chronicles
- `article-edition.pdf` - Peer-reviewed articles only (with cover)
- `student-edition.pdf` - Student scholarship articles only (with cover)

---

## Technical Notes

- **Document Class:** `scrartcl` (Koma-Script article)
- **Page Numbering:** 
  - `full_issue.qmd`: Roman numerals for front matter (i, ii, ...), arabic starting at page 3 for content
  - `article-edition.qmd`: No numbering for cover, roman for preface/TOC, arabic from page 1
  - `student-edition.qmd`: No numbering for cover, roman for preface/TOC, arabic from page 1
- **PDF Assembly:** Uses `pdfpages` LaTeX package for `\includepdf` directives
- **Cover:** Full-bleed cover image (1 page only)

---

## File Status

- [x] `full_issue.qmd` - Generated
- [x] `article-edition.qmd` - Generated
- [x] `student-edition.qmd` - Generated
- [x] `annual-ed/preface.qmd` - Generated with updated h-index and editorial board
- [ ] `annual-ed/pdfs/articles/*.pdf` - **Needs to be added**
- [ ] `annual-ed/pdfs/Articles-student-scholarship/*.pdf` - **Needs to be added**
- [ ] `new-cover-2026.pdf` - Already available in source
- [ ] `chronicles/2026_WSKW_Chronicles.pdf` - **Awaiting separate generation**

---

## Notes for Chronicles

You mentioned you'll provide Chronicles info separately. When ready:

1. Generate the `2026_WSKW_Chronicles.qmd` content file
2. Render it to produce `2026_WSKW_Chronicles.pdf`
3. Place the PDF in the `chronicles/` directory
4. The `full_issue.qmd` will automatically include it in the TOC and final assembly

---

## Checklist for Final Assembly

- [ ] All article PDFs placed in correct directories
- [ ] Cover image verified and in place
- [ ] Chronicles PDF generated and placed
- [ ] All `*.qmd` files render without errors
- [ ] Output PDFs verified for:
  - Correct page numbers
  - Complete table of contents
  - All articles included in correct order
  - Cover displays properly
  - No missing content or blank pages
