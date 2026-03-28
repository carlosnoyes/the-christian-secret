# Plan: Build an HTML Study Site for *The Christian's Secret of a Happy Life*

## Goal

Create a single-page HTML study site with a sidebar-driven layout. The user navigates chapters via a persistent sidebar, and each chapter has a **Discussion** / **Text** toggle to switch between study material and full chapter text. No build tools or frameworks -- just plain HTML + CSS + vanilla JS.

---

## Architecture

```
site/
├── index.html    ← The entire app: sidebar + content area, all content inlined
└── styles.css    ← All styles
```

Everything lives in one HTML file. All chapter text, summaries, and questions are embedded as hidden `<section>` elements. JavaScript handles showing/hiding content based on sidebar clicks and the Discussion/Text toggle. No server, no fetch calls, no build step.

---

## Layout

```
┌──────────────────────────────────────────────────────────┐
│  Header: "The Christian's Secret of a Happy Life"        │
├─────────────┬────────────────────────────────────────────┤
│  SIDEBAR    │  CONTENT AREA                              │
│             │                                            │
│  Book       │  (changes based on sidebar selection)      │
│  Summary    │                                            │
│  ─────────  │  When "Book Summary" selected:             │
│  Preface    │    → full book summary (no toggle)         │
│  Ch 1       │                                            │
│  Ch 2       │  When a chapter is selected:               │
│  Ch 3       │    → [Discussion] [Text] toggle tabs       │
│  ...        │    → Discussion = summary + questions      │
│  Ch 22      │    → Text = full chapter text              │
│             │                                            │
├─────────────┴────────────────────────────────────────────┤
│  Footer (optional)                                       │
└──────────────────────────────────────────────────────────┘
```

### Sidebar
- Fixed/sticky on the left (~250px wide).
- First item: **"Book Summary"** -- styled distinctly (bold, slightly larger, or with an icon) since it's the top-level overview, not a chapter.
- Divider line.
- Then: **Preface**, **Chapter 1** through **Chapter 22** -- each showing the chapter number and short title.
- Clicking an item highlights it as active and swaps the content area.
- On mobile: sidebar collapses into a hamburger menu or top dropdown.

### Content Area
- Fills remaining width to the right of the sidebar.
- Max-width for readability (~750px), with comfortable padding.
- Content is determined by the active sidebar selection.

### Toggle (Discussion / Text)
- Appears at the top of the content area when any chapter (including Preface) is selected.
- Two tab-style buttons: **Discussion** | **Text**.
- **Discussion** (default): shows the chapter summary followed by the discussion questions.
- **Text**: shows the full chapter text.
- For the **Preface**: Discussion shows the preface summary (no questions exist for it). Text shows the full preface text.
- For the **Book Summary**: no toggle at all -- just the summary content.

---

## Step-by-Step Implementation

### Step 1: Create `site/` directory and `styles.css`

Create the `site/` folder. Write `styles.css` with:

**Typography:**
- Serif font stack (Georgia, "Times New Roman", serif) for body/reading text.
- Sans-serif system font stack for sidebar, headings, toggle buttons, and UI chrome.
- Base font size: 17-18px. Line-height: 1.7 for body text.

**Layout:**
- CSS Grid or Flexbox for the sidebar + content two-column layout.
- Sidebar: fixed position, full viewport height, ~250px wide, scrollable if chapter list overflows.
- Content area: `margin-left: 250px`, centered content with `max-width: 750px` and `padding: 2rem`.

**Sidebar styles:**
- Background: a muted tone (e.g., off-white `#f5f3ef` or light warm gray).
- Chapter links: block-level, padded, with hover highlight.
- Active item: distinct background color and left border accent.
- "Book Summary" entry: visually distinct (e.g., slightly larger font, top position).
- Subtle separator between "Book Summary" and the chapter list.

**Toggle styles:**
- Two tab-style buttons sitting side by side at the top of the content area.
- Active tab: solid background, bold text.
- Inactive tab: outlined/ghost style, clickable.
- Sticky within the content area so it stays visible while scrolling long chapters.

**Content styles:**
- `<h2>`: chapter titles. `<h3>`: sub-sections (Main Idea, Key Points, etc.).
- `<p>`: body paragraphs with comfortable spacing.
- `<ol>`: numbered questions, with extra spacing between items for readability.
- `<ul>`: bullet lists in summaries.
- Subtle `<hr>` or spacing between the summary section and questions section in Discussion view.

**Responsive (mobile):**
- Below ~768px: sidebar becomes a collapsible overlay or top-bar dropdown.
- Toggle buttons stack or stay side by side (they're small enough).
- Content area takes full width.

**Print styles:**
- `@media print`: hide sidebar and toggle, just print the currently visible content.

### Step 2: Create `site/index.html` -- Structure and Shell

Write the HTML skeleton:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The Christian's Secret of a Happy Life</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>

  <!-- SIDEBAR -->
  <nav id="sidebar">
    <div class="sidebar-header">
      <h1>The Christian's Secret of a Happy Life</h1>
      <p class="author">Hannah Whitall Smith</p>
    </div>
    <ul>
      <li><a href="#summary" class="active">Book Summary</a></li>
      <hr>
      <li><a href="#preface">Preface</a></li>
      <li><a href="#ch1">Ch 1: God's Side and Man's Side</a></li>
      <!-- ... through Ch 22 -->
    </ul>
  </nav>

  <!-- MOBILE MENU TOGGLE -->
  <button id="menu-toggle" aria-label="Toggle navigation">☰</button>

  <!-- CONTENT AREA -->
  <main id="content">
    <!-- Toggle tabs (hidden for Book Summary) -->
    <div id="view-toggle">
      <button class="toggle-btn active" data-view="discussion">Discussion</button>
      <button class="toggle-btn" data-view="text">Text</button>
    </div>

    <!-- All content sections are embedded here, shown/hidden by JS -->
    <!-- See Steps 3-6 for what goes inside -->
  </main>

  <script src="app.js"></script>  <!-- or inline <script> -->
</body>
</html>
```

### Step 3: Embed the Book Summary Content

Inside `<main>`, add:

```html
<section id="summary" class="content-section active">
  <h2>Complete Book Summary</h2>
  <!-- Parsed content from book_summary.txt -->
  <h3>Overview</h3>
  <p>...</p>
  <h3>Part One: The Foundation (Chapters 1-4)</h3>
  <p>...</p>
  <!-- etc. -->
</section>
```

**Source:** `book_summary.txt`

**Parsing:**
- Title/author lines -> skip (already in sidebar header).
- "Complete Book Summary" / `====` -> skip (we use our own `<h2>`).
- ALL-CAPS headings like "OVERVIEW" or "PART ONE: ..." followed by `----` -> `<h3>`.
- Blank-line-separated paragraphs -> `<p>` tags.

This section has **no toggle** -- the Discussion/Text toggle is hidden when the Book Summary is active.

### Step 4: Embed Each Chapter's Discussion Content

For each chapter (Preface + Chapters 1-22), add a Discussion section:

```html
<section id="preface-discussion" class="content-section discussion" data-chapter="preface" hidden>
  <!-- SUMMARY (from Summaries/00_preface_summary.txt) -->
  <h2>Preface</h2>
  <h3>Main Idea</h3>
  <p>...</p>
  <h3>Key Points</h3>
  <ul><li>...</li></ul>
  <!-- No questions for preface -->
</section>

<section id="ch1-discussion" class="content-section discussion" data-chapter="ch1" hidden>
  <!-- SUMMARY (from Summaries/01_chapter_1_summary.txt) -->
  <h2>Chapter 1: God's Side and Man's Side</h2>
  <h3>Main Idea</h3>
  <p>...</p>
  <h3>Key Points</h3>
  <ul><li>...</li></ul>
  <h3>Illustrations and Examples</h3>
  <ul><li>...</li></ul>
  <h3>References</h3>
  <ul><li>...</li></ul>

  <hr>

  <!-- QUESTIONS (from Questions/01_chapter_1_questions.txt) -->
  <h3>Discussion Questions</h3>
  <ol>
    <li>...</li>
    <li>...</li>
    <!-- 5 questions -->
  </ol>
</section>

<!-- Repeat for ch2 through ch22 -->
```

**Sources:**
- Summary: `Summaries/XX_*_summary.txt` (23 files)
- Questions: `Questions/XX_chapter_X_questions.txt` (22 files, skip `_old`)

**Parsing for summaries:**
- Line 1 (title) + `====` -> `<h2>` (extract clean chapter title, drop "Summary:" label).
- Sub-headings + `----` -> `<h3>`.
- Lines starting with `- ` -> `<li>` in `<ul>`.
- Other text -> `<p>`.

**Parsing for questions:**
- Skip the title line and `====` (already have the heading from the summary section).
- Add `<h3>Discussion Questions</h3>` as a divider.
- Lines starting with `N. ` -> `<li>` in `<ol>`.

**Special case -- Preface:** Has a summary but no questions file. The Discussion view just shows the summary.

### Step 5: Embed Each Chapter's Text Content

For each chapter (Preface + Chapters 1-22), add a Text section:

```html
<section id="preface-text" class="content-section text" data-chapter="preface" hidden>
  <h2>Preface</h2>
  <p>This is not a theological book. I frankly confess...</p>
  <!-- Full preface text -->
</section>

<section id="ch1-text" class="content-section text" data-chapter="ch1" hidden>
  <h2>Chapter 1: God's Side and Man's Side</h2>
  <p>In introducing this subject of the life and walk of faith...</p>
  <!-- Full chapter 1 text -->
</section>

<!-- Repeat for ch2 through ch22 -->
```

**Source:** `chapters/XX_*.txt` (23 files)

**Parsing:**
- Lines 1-2: chapter number + title -> combine into `<h2>` (e.g., "Chapter 1: God's Side and Man's Side").
- Line 3 (`====`): skip.
- Any repeated heading lines within the body (some chapters echo the title): skip.
- Blank-line-separated paragraphs -> `<p>` tags.
- Everything else: inline text.

### Step 6: Write the JavaScript

Either inline in `index.html` or as a separate small file. Handles three things:

**1. Sidebar navigation:**
```js
// When a sidebar link is clicked:
// - Remove 'active' class from all sidebar links, add to clicked one.
// - Hide all .content-section elements.
// - Determine which chapter was selected (from href hash).
// - Show the appropriate section based on current toggle state.
// - If "Book Summary" was clicked, show #summary and hide the toggle.
// - If a chapter was clicked, show the toggle and show the discussion or text
//   section based on which toggle tab is active.
```

**2. Discussion/Text toggle:**
```js
// When a toggle button is clicked:
// - Update active toggle button styling.
// - Determine the currently selected chapter from the active sidebar link.
// - Hide the current content section.
// - Show the other one (e.g., swap #ch1-discussion for #ch1-text).
```

**3. Mobile menu:**
```js
// When hamburger button is clicked:
// - Toggle sidebar visibility (slide in/out or overlay).
// - Close sidebar when a nav item is clicked (on mobile).
```

**4. URL hash support (nice-to-have):**
- Update `location.hash` when navigating so users can bookmark/share links to specific chapters.
- On page load, read `location.hash` and navigate to that chapter.

### Step 7: Assemble and Test

Since all content is inlined in one HTML file, this step is about building the actual file:

1. **Read all source files** (23 chapter texts, 23 summaries, 22 question files, 1 book summary).
2. **Parse each file** according to the rules in Steps 3-5.
3. **Assemble** the parsed HTML into the `index.html` skeleton from Step 2.
4. **Open in browser** and verify:
   - Sidebar navigation works: clicking each chapter shows the right content.
   - Toggle works: switching between Discussion and Text shows correct content for the selected chapter.
   - Book Summary has no toggle.
   - Preface Discussion has summary but no questions.
   - All 22 chapter discussions have both summary and questions.
   - All text renders with proper paragraph breaks, no broken characters.
   - Mobile: sidebar collapses, hamburger menu works.
   - Scrolling: long chapters scroll smoothly, toggle stays accessible.
5. **Fix** any issues found.

---

## Content Parsing Rules

| Source Pattern | HTML Output |
|---|---|
| Line followed by `====...` on next line | `<h2>` |
| Line followed by `----...` on next line | `<h3>` |
| Blank line | Paragraph break (`</p><p>`) |
| Line starting with `- ` | `<li>` inside `<ul>` |
| Line starting with `N. ` (digit + dot) | `<li>` inside `<ol>` |
| Everything else | Inline text within current `<p>` |

---

## Design Decisions

- **Single HTML file.** All content is inlined. The full book text (~1,650 lines) plus summaries and questions will make the HTML file large (~5,000+ lines), but the browser only renders what's visible. This avoids fetch calls, routing libraries, and multiple-file complexity.
- **No framework.** Vanilla JS for show/hide logic is trivial here. The "app" is just toggling `hidden` attributes.
- **Sidebar navigation over top-nav.** A sidebar gives persistent access to all 23 chapters without scrolling through a long dropdown. It also makes the site feel like a proper study tool / e-reader.
- **Discussion as default view.** Since this is a study site, the summary + questions is the primary use case. Full text is available but secondary.
- **No build step.** The HTML is generated once by hand (by Claude). If new questions are added later, we just re-embed that chapter's questions section.

---

## File Dependencies

| Content Section | Source Files |
|---|---|
| Book Summary | `book_summary.txt` (1 file) |
| Chapter Discussions (summary part) | `Summaries/00_preface_summary.txt` through `Summaries/22_chapter_22_summary.txt` (23 files) |
| Chapter Discussions (questions part) | `Questions/01_chapter_1_questions.txt` through `Questions/22_chapter_22_questions.txt` (22 files, skip `_old`) |
| Chapter Text | `chapters/00_preface.txt` through `chapters/22_chapter_22.txt` (23 files) |

---

## Section ID Naming Convention

| Sidebar Item | Discussion Section ID | Text Section ID |
|---|---|---|
| Book Summary | `summary` | *(none)* |
| Preface | `preface-discussion` | `preface-text` |
| Chapter N | `chN-discussion` | `chN-text` |

---

## Estimated Output

- `styles.css`: ~200-250 lines
- `index.html`: ~5,000-6,000 lines (all content inlined + JS)

Total: 2 files.
