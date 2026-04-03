# JKW 2026 Full Volume - Scaffold Setup

## Generated Structure

This directory contains the complete folder structure and QMD scaffolds for the 2026 JKW annual volume (Volume 15, Number 1).

```
outputs/
├── annual-ed/
│   ├── preface.qmd           [GENERATED - Complete]
│   └── pdfs/
│       ├── articles/         [AWAITING: 3 peer-reviewed PDFs]
│       └── Articles-student-scholarship/  [AWAITING: 1 student scholarship PDF]
├── chronicles/
│   ├── _content.qmd          [SCAFFOLD - Placeholder structure]
│   └── 2026_WSKW_Chronicles.qmd  [GENERATED - Includes _content.qmd]
├── full_issue.qmd            [GENERATED - Master assembly file]
├── article-edition.qmd       [GENERATED - Articles only with cover]
├── student-edition.qmd       [GENERATED - Student articles only with cover]
├── annual-conference.qmd     [GENERATED - Conference abstracts edition]
├── annual-conference-preface.qmd  [SCAFFOLD - Conference preface template]
└── new-cover-2026.pdf        [AWAITING USER]
```

## Files Generated

### Complete & Ready to Use

1. **annual-ed/preface.qmd** - Journal masthead, editorial board, and reviewer lists
   - Updated for 2026 volume (Vol 15, No 1)
   - Removed Min Kim from editorial board per your specifications
   - Updated h-index values (2012-2026): 6, (since 2019): 5
   - Reviewer lists updated for Annual and Student editions

2. **full_issue.qmd** - Master assembly file combining all sections
   - Roman numerals for front matter (preface + TOC)
   - Arabic numerals starting at page 3 for articles
   - 3 peer-reviewed articles: pages 1-18, 19-31, 32-44
   - Student scholarship article starting at page 45
   - Chronicles included at end

3. **article-edition.qmd** - Peer-reviewed articles only
   - Includes cover image (new-cover-2026.pdf)
   - Preface + TOC + 3 articles
   - Arabic pages start at 1

4. **student-edition.qmd** - Student scholarship articles only
   - Includes cover image
   - Preface + TOC + 1 student article
   - Arabic pages start at 1

5. **chronicles/2026_WSKW_Chronicles.qmd** - Conference abstracts standalone
   - Page counter set to 56 (starts after page 55 of articles)
   - Includes _content.qmd file

### Placeholder/Scaffold (Awaiting Content)

6. **chronicles/_content.qmd** - Conference abstracts structure
   - Placeholder structure for keynote, E.C. Davis lecture, and abstracts
   - Replace [BRACKETED] sections with actual content from your conference data

7. **annual-conference-preface.qmd** - Conference edition preface
   - Template with placeholders for conference leadership, speakers, etc.
   - Replace [BRACKETED] sections with actual 2026 conference information

## Next Steps

### 1. Place Cover Image
Copy `new-cover-2026.pdf` to the outputs directory root.

### 2. Place Article PDFs
Copy the following PDF files to their respective directories:

**Peer-reviewed articles** → `annual-ed/pdfs/articles/`:
- `01-18-chen-etal-2026-final.pdf` (pages 1-18)
- `19-31-morales-2026-final.pdf` (pages 19-31)
- `32-44-okafor-wu-2026-final.pdf` (pages 32-44)

**Student scholarship** → `annual-ed/pdfs/Articles-student-scholarship/`:
- `s-01-11-patel-etal-2026-pub.pdf` (pages 45-55)

### 3. Fill in Chronicles Content
Edit `chronicles/_content.qmd` with:
- Keynote presentation title and speaker info
- E.C. Davis Lecture speaker info
- All academic presentation abstracts
- Student poster session list
- Faculty poster session list

### 4. Fill in Annual Conference Preface
Edit `annual-conference-preface.qmd` with:
- Conference number and theme
- Conference dates and location
- Conference leadership team (all positions)
- Keynote speaker biography
- E.C. Davis lecturer biography
- Welcome message text

### 5. Render Files
Once all content is in place:

```bash
cd outputs
quarto render annual-ed/preface.qmd
cd chronicles && quarto render 2026_WSKW_Chronicles.qmd
cd .. && quarto render article-edition.qmd
cd .. && quarto render student-edition.qmd
cd .. && quarto render annual-conference.qmd
cd .. && quarto render full_issue.qmd  # Render last - depends on Chronicles PDF
```

## Metadata Summary

- **Volume**: 15
- **Number**: 1
- **Year**: 2026
- **Peer-reviewed articles**: 3 (pages 1-18, 19-31, 32-44)
- **Student scholarship articles**: 1 (pages 45-55)
- **Chronicles start page**: 56
- **Editorial Board**: 5 members (Seung Ho Chang, Gioella Chaparro, Jongil Lim, Laura Robinson-Doyle, Heather Van Mullem)
- **Annual Edition Reviewers**: 7 members
- **Student Edition Reviewers**: 4 members
- **H-index (2012-2026)**: 6
- **H-index (since 2019)**: 5

## Quality Checklist

Before final rendering:

- [ ] `new-cover-2026.pdf` is in outputs directory
- [ ] All 3 peer-reviewed article PDFs are in `annual-ed/pdfs/articles/`
- [ ] Student scholarship PDF is in `annual-ed/pdfs/Articles-student-scholarship/`
- [ ] `chronicles/_content.qmd` has all keynote, E.C. Davis, and abstract content
- [ ] `annual-conference-preface.qmd` has all leadership and speaker information
- [ ] All article PDF filenames match exactly in the QMD `\includepdf` directives
- [ ] `preface.qmd` has correct reviewer lists and h-index values
