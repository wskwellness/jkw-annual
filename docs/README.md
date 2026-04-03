# JKW Annual Published PDFs

This folder contains the final underscore-prefixed published PDFs that are served via GitHub Pages from the `docs/` folder.

## Published PDF URLs

### 2022
- [PDF] [2022 Annual Conference](https://wskwellness.github.io/jkw-annual/2022/_2022_annual-conference.pdf)
- [PDF] [2022 Article Edition](https://wskwellness.github.io/jkw-annual/2022/_2022_article-edition.pdf)
- [PDF] [2022 Student Edition](https://wskwellness.github.io/jkw-annual/2022/_2022_student-edition.pdf)

### 2023
- [PDF] [2023 Annual Conference](https://wskwellness.github.io/jkw-annual/2022/_2023_annual-conference.pdf)
- [PDF] [2023 Article Edition](https://wskwellness.github.io/jkw-annual/2022/_2023_article-edition.pdf)
- [PDF] [2023 Student Edition](https://wskwellness.github.io/jkw-annual/2022/_2023_student-edition.pdf)

## Notes

- `.nojekyll` is present to ensure underscore-prefixed files are served.
- Keep only the PDFs you want publicly available in `docs/2022/`.

## PDF-Only Publishing Workflow

1. Render the yearly PDFs in `YYYY/`.
2. Rename each published PDF with the underscore convention:
	 - `_YYYY_annual-conference.pdf`
	 - `_YYYY_article-edition.pdf`
	 - `_YYYY_student-edition.pdf`
3. Copy the renamed files into `docs/2022/` (current public Pages folder).
4. Add links below and commit/push.

## Renaming Instructions

Example for 2023:

```bash
cp 2023/annual-conference.pdf 2023/_2023_annual-conference.pdf
cp 2023/article-edition.pdf 2023/_2023_article-edition.pdf
cp 2023/student-edition.pdf 2023/_2023_student-edition.pdf

cp 2023/_2023_annual-conference.pdf docs/2022/_2023_annual-conference.pdf
cp 2023/_2023_article-edition.pdf docs/2022/_2023_article-edition.pdf
cp 2023/_2023_student-edition.pdf docs/2022/_2023_student-edition.pdf
```

## Website HTML Snippet (Copy/Paste)

```html
<ul>
	<li><a href="https://wskwellness.github.io/jkw-annual/2022/_2022_annual-conference.pdf" target="_blank" rel="noopener noreferrer"><strong>[PDF]</strong> Annual Conference</a></li>
	<li><a href="https://wskwellness.github.io/jkw-annual/2022/_2022_article-edition.pdf" target="_blank" rel="noopener noreferrer"><strong>[PDF]</strong> Article Edition</a></li>
	<li><a href="https://wskwellness.github.io/jkw-annual/2022/_2022_student-edition.pdf" target="_blank" rel="noopener noreferrer"><strong>[PDF]</strong> Student Edition</a></li>
	<li><a href="https://wskwellness.github.io/jkw-annual/2022/_2023_annual-conference.pdf" target="_blank" rel="noopener noreferrer"><strong>[PDF]</strong> Annual Conference</a></li>
	<li><a href="https://wskwellness.github.io/jkw-annual/2022/_2023_article-edition.pdf" target="_blank" rel="noopener noreferrer"><strong>[PDF]</strong> Article Edition</a></li>
	<li><a href="https://wskwellness.github.io/jkw-annual/2022/_2023_student-edition.pdf" target="_blank" rel="noopener noreferrer"><strong>[PDF]</strong> Student Edition</a></li>
</ul>
```

