# Plan: Build an HTML Study Site for *The Christian's Secret of a Happy Life*

## Goal

Create a multi-page, static HTML website that presents the full book text, book summary, chapter summaries, and discussion questions in a clean, readable, well-formatted layout. No build tools or frameworks -- just plain HTML + CSS (+ minimal JS for navigation).

---

## Architecture

```
site/
├── index.html          ← Landing page with navigation to the four sections
├── book.html           ← Full book text, separated by chapter
├── summary.html        ← Full book summary
├── chapter-summaries.html  ← All individual chapter summaries
├── questions.html      ← All chapter discussion questions
└── styles.css          ← Shared stylesheet
```

Single shared CSS file. Each HTML page links to it. No frameworks, no bundler.

---

## Step-by-Step Implementation

### Step 1: Create `site/` directory and `styles.css`

Create the `site/` folder at the repo root.

Write `site/styles.css` with:
- A clean, book-friendly serif font stack (Georgia, Garamond, serif) for body text.
- Sans-serif (system font stack) for headings and navigation.
- Max-width container (~750px) centered on the page for comfortable reading.
- Responsive design: readable on desktop and mobile (media queries for smaller screens).
- A sticky/fixed top navigation bar with links to all four pages.
- Styles for:
  - `<h1>` (book title), `<h2>` (chapter titles), `<h3>` (section headings within summaries).
  - Paragraphs: comfortable line-height (~1.7), adequate spacing.
  - Ordered lists (for questions): spaced out so each question is easy to read.
  - A table of contents sidebar or jump-links section on the book page (for navigating between chapters).
  - Active/current page indicator in the nav bar.
  - Subtle chapter dividers (horizontal rule or decorative border).
  - Print-friendly styles (`@media print`) so users can print chapters cleanly.

### Step 2: Create `site/index.html` -- Landing Page

This is the home page. It should contain:

- The book title: "The Christian's Secret of a Happy Life"
- Author: "By Hannah Whitall Smith"
- A brief description (1-2 sentences, can be pulled from the preface).
- Four navigation cards/links, one for each section:
  1. **Full Book Text** -- "Read the complete text, chapter by chapter" -> `book.html`
  2. **Book Summary** -- "A comprehensive summary of the entire book" -> `summary.html`
  3. **Chapter Summaries** -- "Individual summaries for each chapter" -> `chapter-summaries.html`
  4. **Discussion Questions** -- "Thought-provoking questions for group study" -> `questions.html`
- The shared nav bar at the top (consistent across all pages).

### Step 3: Create `site/book.html` -- Full Book Text

This is the largest page. It should contain:

1. **A chapter table of contents at the top** -- a list of anchor links to each chapter section on the page:
   - Preface
   - Chapter 1: God's Side and Man's Side
   - Chapter 2: The Scripturalness of This Life
   - ... through Chapter 22

2. **Each chapter as its own `<section>` element** with an `id` attribute for anchor linking (e.g., `id="chapter-1"`).

3. **For each chapter section:**
   - Read the corresponding file from `chapters/XX_*.txt`.
   - Use line 1 as a secondary label (e.g., "Chapter 1").
   - Use line 2 as the chapter title in an `<h2>`.
   - Skip the `========` underline (line 3).
   - Convert the remaining body text into `<p>` tags. The text files use blank lines to separate paragraphs, so split on double-newlines.
   - Preserve any quoted Scripture passages -- wrap lines that begin with quotation marks or are clearly block quotes in `<blockquote>` tags where feasible, or simply let them flow as normal paragraphs (simpler approach).
   - Add a "Back to top" link at the end of each chapter.

4. **Special handling for the Preface** (`00_preface.txt`):
   - Title is "Preface" (from line 4 of the file).
   - Author attribution line at the end: "Hannah Whitall Smith, Germantown, Pennsylvania."

**How to build this content:**
- Read each of the 23 text files in `chapters/`.
- Parse them into structured HTML.
- Assemble them sequentially into one HTML page.

### Step 4: Create `site/summary.html` -- Full Book Summary

1. Read `book_summary.txt`.
2. Parse the structure:
   - Line 1-2: Title and author (use as page header).
   - "Complete Book Summary" heading.
   - Section headings like "OVERVIEW", "PART ONE: THE FOUNDATION (Chapters 1-4)", etc. -- these become `<h2>` elements.
   - Body paragraphs separated by blank lines become `<p>` tags.
   - Dash-underlined headings (lines followed by `---...`) become `<h3>` elements.
   - Equal-sign-underlined headings (lines followed by `===...`) become `<h2>` elements.
3. Wrap everything in the standard page template with nav bar.

### Step 5: Create `site/chapter-summaries.html` -- Individual Chapter Summaries

1. **A table of contents at the top** linking to each chapter's summary section.

2. **For each chapter (Preface through Chapter 22):**
   - Read the corresponding file from `Summaries/XX_*_summary.txt`.
   - Parse the structure:
     - Line 1: Chapter title (e.g., "Chapter 1 Summary: God's Side and Man's Side") -> `<h2>`.
     - Skip the `=====` underline.
     - Sub-headings like "Main Idea", "Key Points", "Illustrations and Examples", "References" -> `<h3>`.
     - Dash-underlined headings -> `<h3>`.
     - Lines starting with `- ` -> list items in a `<ul>`.
     - Other lines -> `<p>` tags.
   - Each summary is a `<section>` with an anchor `id`.
   - Add a "Back to top" link after each summary.

3. Summaries are read from all 23 files:
   - `00_preface_summary.txt`
   - `01_chapter_1_summary.txt` through `22_chapter_22_summary.txt`

### Step 6: Create `site/questions.html` -- Discussion Questions

1. **A table of contents at the top** linking to each chapter's questions section.

2. **For each chapter (1 through 22):**
   - Read the corresponding file from `Questions/XX_chapter_X_questions.txt`.
   - **Skip** `01_chapter_1_questions_old.txt` (ignore the old file).
   - Parse the structure:
     - Line 1: Chapter title (e.g., "Chapter 1: God's Side and Man's Side -- Discussion Questions") -> `<h2>`.
     - Skip the `=====` underline.
     - Numbered questions (lines starting with `1.`, `2.`, etc.) -> `<ol>` with `<li>` items.
   - Each chapter's questions is a `<section>` with an anchor `id`.
   - Add a "Back to top" link after each set.

3. Questions are read from 22 files (chapters 1-22; no questions for the preface).

### Step 7: Review and Polish

- Open each HTML page in a browser and verify:
  - All chapter text renders correctly with proper paragraph breaks.
  - Navigation links work (both the top nav and in-page anchor links).
  - The table of contents on book.html, chapter-summaries.html, and questions.html all jump to the correct sections.
  - The site is readable on a narrow viewport (mobile).
  - No broken characters or encoding issues (curly quotes, em-dashes, etc. -- ensure `<meta charset="UTF-8">`).
- Fix any formatting issues found.

---

## Content Parsing Rules (shared across all pages)

Since the source files are plain text with a consistent format, these are the parsing conventions:

| Pattern | HTML |
|---|---|
| Line followed by `====...` on next line | `<h2>` |
| Line followed by `----...` on next line | `<h3>` |
| Blank line | Paragraph break (close `</p>`, open `<p>`) |
| Line starting with `- ` | `<li>` inside `<ul>` |
| Line starting with `N. ` (digit + dot) | `<li>` inside `<ol>` |
| Everything else | Inline text within current `<p>` |

---

## Design Decisions

- **No JavaScript framework.** This is a static reading site. Vanilla HTML/CSS is sufficient. Minimal JS only for highlighting the active nav link.
- **Single-page-per-section**, not a single-page app. Each of the four sections is its own HTML file. This keeps page sizes manageable (the full book text page will be large but still under 200KB of HTML).
- **No build step.** The HTML files are hand-authored (by Claude) with the content inlined. No templating engine needed for a one-time generation.
- **Responsive.** Readable on phones and tablets, not just desktop.
- **Accessible.** Semantic HTML (`<nav>`, `<main>`, `<section>`, `<article>`), proper heading hierarchy, good contrast.

---

## File Dependencies

| HTML Page | Source Files |
|---|---|
| `book.html` | `chapters/00_preface.txt` through `chapters/22_chapter_22.txt` (23 files) |
| `summary.html` | `book_summary.txt` (1 file) |
| `chapter-summaries.html` | `Summaries/00_preface_summary.txt` through `Summaries/22_chapter_22_summary.txt` (23 files) |
| `questions.html` | `Questions/01_chapter_1_questions.txt` through `Questions/22_chapter_22_questions.txt` (22 files, skip `_old`) |

---

## Estimated Output

- `styles.css`: ~150-200 lines
- `index.html`: ~80 lines
- `book.html`: ~2,500-3,000 lines (full book text is ~1,650 lines of source, plus HTML markup)
- `summary.html`: ~400 lines
- `chapter-summaries.html`: ~800-1,000 lines
- `questions.html`: ~400-500 lines

Total: ~6 HTML/CSS files, roughly 4,000-5,000 lines.
