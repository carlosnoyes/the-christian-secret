"""
Build script: generates site/index.html from the source text files.
Run: python build.py
"""

import os
import re
import html

ROOT = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR = os.path.join(ROOT, "chapters")
SUMMARIES_DIR = os.path.join(ROOT, "Summaries")
QUESTIONS_DIR = os.path.join(ROOT, "Questions")
BOOK_SUMMARY = os.path.join(ROOT, "book_summary.txt")
OUT = os.path.join(ROOT, "index.html")


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def esc(text):
    """HTML-escape text."""
    return html.escape(text)


def text_to_paragraphs(text, css_class=""):
    """Convert plain text (blank-line separated) into <p> tags."""
    paragraphs = re.split(r'\n\s*\n', text.strip())
    cls = f' class="{css_class}"' if css_class else ''
    out = []
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        # Join wrapped lines into one paragraph
        p = ' '.join(line.strip() for line in p.splitlines())
        out.append(f"<p{cls}>{esc(p)}</p>")
    return '\n'.join(out)


def parse_summary_file(text):
    """Parse a summary .txt file into HTML with h3 headings, lists, and paragraphs."""
    lines = text.splitlines()
    out = []
    i = 0
    in_list = False
    list_type = None

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Skip the title and underline (first two non-empty lines)
        # We handle the title separately

        # Check if next line is an underline (for heading detection)
        next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""

        # Heading with === underline -> skip (we handle title outside)
        if next_line and all(c == '=' for c in next_line) and len(next_line) >= 3:
            i += 2
            continue

        # Heading with --- underline -> h3
        if next_line and all(c == '-' for c in next_line) and len(next_line) >= 3 and stripped:
            if in_list:
                out.append(f"</{list_type}>")
                in_list = False
            out.append(f"<h3>{esc(stripped)}</h3>")
            i += 2
            continue

        # Bullet list item
        if stripped.startswith("- "):
            if not in_list or list_type != "ul":
                if in_list:
                    out.append(f"</{list_type}>")
                out.append("<ul>")
                in_list = True
                list_type = "ul"
            # Collect continuation lines (indented lines that follow)
            item_text = stripped[2:]
            while i + 1 < len(lines) and lines[i + 1].startswith("  ") and not lines[i + 1].strip().startswith("- "):
                i += 1
                item_text += " " + lines[i].strip()
            out.append(f"<li>{esc(item_text)}</li>")
            i += 1
            continue

        # Numbered list item
        m = re.match(r'^(\d+)\.\s+(.+)', stripped)
        if m:
            if not in_list or list_type != "ol":
                if in_list:
                    out.append(f"</{list_type}>")
                out.append("<ol>")
                in_list = True
                list_type = "ol"
            item_text = m.group(2)
            # Collect continuation lines
            while i + 1 < len(lines) and lines[i + 1].strip() and not re.match(r'^\d+\.\s', lines[i + 1].strip()) and not lines[i + 1].strip().startswith("- "):
                next_s = lines[i + 1].strip()
                # Stop if it looks like a heading
                if i + 2 < len(lines) and (all(c == '-' for c in lines[i + 2].strip()) or all(c == '=' for c in lines[i + 2].strip())) and len(lines[i + 2].strip()) >= 3:
                    break
                i += 1
                item_text += " " + next_s
            out.append(f"<li>{esc(item_text)}</li>")
            i += 1
            continue

        # Empty line
        if not stripped:
            if in_list:
                out.append(f"</{list_type}>")
                in_list = False
            i += 1
            continue

        # Regular text - collect into paragraph
        if in_list:
            out.append(f"</{list_type}>")
            in_list = False
        para_lines = [stripped]
        while i + 1 < len(lines):
            next_s = lines[i + 1].strip()
            if not next_s:
                break
            # Check if next-next line is underline (meaning next line is a heading)
            if i + 2 < len(lines):
                nn = lines[i + 2].strip()
                if nn and (all(c == '-' for c in nn) or all(c == '=' for c in nn)) and len(nn) >= 3:
                    break
            if next_s.startswith("- ") or re.match(r'^\d+\.\s', next_s):
                break
            i += 1
            para_lines.append(next_s)
        out.append(f"<p>{esc(' '.join(para_lines))}</p>")
        i += 1

    if in_list:
        out.append(f"</{list_type}>")

    return '\n'.join(out)


def parse_book_summary(text):
    """Parse book_summary.txt into HTML."""
    # Skip first 5 lines (title, author, blank, "Complete Book Summary", ===)
    lines = text.splitlines()
    # Find content start after the === line
    start = 0
    for i, line in enumerate(lines):
        if line.strip().startswith("===="):
            start = i + 1
            break
    return parse_summary_file('\n'.join(lines[start:]))


def parse_chapter_text(text):
    """Parse a chapter text file into HTML paragraphs."""
    lines = text.splitlines()
    # Skip header lines: chapter number, title, === underline, and any
    # repeated uppercase heading lines
    start = 0
    for i, line in enumerate(lines):
        if line.strip().startswith("====") or line.strip().startswith("===="):
            start = i + 1
            break
    if start == 0:
        start = 3  # fallback

    # Skip blank lines and repeated uppercase headings after the underline
    content_lines = lines[start:]
    # Remove leading blank lines
    while content_lines and not content_lines[0].strip():
        content_lines.pop(0)

    # Check if first non-blank lines are uppercase repeats of the title
    cleaned = []
    skip_count = 0
    for line in content_lines:
        s = line.strip()
        if skip_count < 3 and s and s == s.upper() and len(s) > 3 and not s.startswith('"'):
            skip_count += 1
            continue
        else:
            skip_count = 999  # stop skipping
            cleaned.append(line)

    return text_to_paragraphs('\n'.join(cleaned), css_class="")


def parse_questions_file(text):
    """Parse a questions .txt file into HTML <ol> list."""
    lines = text.splitlines()
    # Skip title and === underline
    start = 0
    for i, line in enumerate(lines):
        if line.strip().startswith("===="):
            start = i + 1
            break

    content = '\n'.join(lines[start:])
    # Split by numbered pattern
    questions = re.split(r'\n\s*\d+\.\s+', content)
    # First split is usually empty or preamble
    questions = [q.strip() for q in questions if q.strip()]

    if not questions:
        return "<p><em>Questions coming soon.</em></p>"

    out = ['<ol class="questions-list">']
    for q in questions:
        # Join multi-line question into one
        q = ' '.join(line.strip() for line in q.splitlines())
        out.append(f"<li>{esc(q)}</li>")
    out.append('</ol>')
    return '\n'.join(out)


def get_chapter_title(text):
    """Extract chapter title from a chapter text file."""
    lines = text.splitlines()
    if len(lines) >= 2:
        return lines[1].strip()
    return lines[0].strip()


def get_chapter_number_label(text):
    """Extract 'Chapter N' from first line."""
    return text.splitlines()[0].strip()


def get_summary_title(text):
    """Extract title from summary file (first line, remove 'Summary: ' prefix)."""
    first = text.splitlines()[0].strip()
    # e.g. "Chapter 1 Summary: God's Side and Man's Side"
    first = re.sub(r'\s*Summary:', ':', first)
    return first


# ============================================================
# Gather all content
# ============================================================

# Chapter files
chapter_files = sorted(
    [f for f in os.listdir(CHAPTERS_DIR) if f.endswith('.txt')],
    key=lambda x: int(x.split('_')[0])
)

# Summary files
summary_files = sorted(
    [f for f in os.listdir(SUMMARIES_DIR) if f.endswith('.txt')],
    key=lambda x: int(x.split('_')[0])
)

# Question files (skip _old)
question_files = sorted(
    [f for f in os.listdir(QUESTIONS_DIR) if f.endswith('.txt') and '_old' not in f],
    key=lambda x: int(x.split('_')[0])
)

# Build chapter info
chapters = []
for cf in chapter_files:
    num = int(cf.split('_')[0])
    text = read_file(os.path.join(CHAPTERS_DIR, cf))

    if num == 0:
        ch_id = "preface"
        label = "Preface"
        title = "Preface"
        sidebar_label = "Preface"
    else:
        ch_id = f"ch{num}"
        label = get_chapter_number_label(text)
        title = get_chapter_title(text)
        sidebar_label = f"Ch {num}: {title}"
        if len(sidebar_label) > 40:
            sidebar_label = f"Ch {num}: {title[:30]}..."

    # Find matching summary
    summary_text = ""
    for sf in summary_files:
        snum = int(sf.split('_')[0])
        if snum == num:
            summary_text = read_file(os.path.join(SUMMARIES_DIR, sf))
            break

    # Find matching questions
    questions_text = ""
    for qf in question_files:
        qnum = int(qf.split('_')[0])
        if qnum == num:
            questions_text = read_file(os.path.join(QUESTIONS_DIR, qf))
            break

    chapters.append({
        'num': num,
        'id': ch_id,
        'label': label,
        'title': title,
        'sidebar_label': sidebar_label,
        'text': text,
        'summary_text': summary_text,
        'questions_text': questions_text,
    })

# Parse book summary
book_summary_text = read_file(BOOK_SUMMARY)
book_summary_html = parse_book_summary(book_summary_text)

# ============================================================
# Build HTML
# ============================================================

# Sidebar links
sidebar_links = ['<li><a href="#summary" data-target="summary" class="active">Book Summary</a></li>']
sidebar_links.append('<li class="sidebar-divider-item"><div class="sidebar-divider"></div></li>')
for ch in chapters:
    sidebar_links.append(f'<li><a href="#{ch["id"]}" data-target="{ch["id"]}">{esc(ch["sidebar_label"])}</a></li>')

sidebar_html = '\n'.join(sidebar_links)

# Content sections
sections = []

# Book summary section
sections.append(f'''
<section id="section-summary" class="content-section active book-summary">
  <div class="content-wrap">
    <h2>The Christian's Secret of a Happy Life</h2>
    <p style="font-style: italic; color: #6a6050; margin-bottom: 2rem;">Complete Book Summary</p>
    {book_summary_html}
  </div>
</section>
''')

# Chapter sections (discussion + text)
for ch in chapters:
    # Discussion section
    discussion_parts = []
    if ch['summary_text']:
        # Parse summary, skip the first heading (we provide our own)
        summary_html = parse_summary_file(ch['summary_text'])
        discussion_parts.append(summary_html)

    if ch['questions_text']:
        discussion_parts.append('<hr>')
        discussion_parts.append('<h3>Discussion Questions</h3>')
        discussion_parts.append(f'<div class="questions-section">{parse_questions_file(ch["questions_text"])}</div>')

    disc_html = '\n'.join(discussion_parts)

    # Display title
    if ch['num'] == 0:
        display_title = "Preface"
    else:
        display_title = f"Chapter {ch['num']}: {ch['title']}"

    sections.append(f'''
<section id="section-{ch['id']}-discussion" class="content-section" data-chapter="{ch['id']}" data-view="discussion">
  <div class="content-wrap">
    <h2>{esc(display_title)}</h2>
    {disc_html}
  </div>
</section>
''')

    # Text section
    chapter_html = parse_chapter_text(ch['text'])

    sections.append(f'''
<section id="section-{ch['id']}-text" class="content-section chapter-text" data-chapter="{ch['id']}" data-view="text">
  <div class="content-wrap">
    <h2>{esc(display_title)}</h2>
    {chapter_html}
  </div>
</section>
''')

sections_html = '\n'.join(sections)

# Full page
page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The Christian's Secret of a Happy Life — Study Site</title>
  <link rel="stylesheet" href="site/styles.css">
</head>
<body>

  <!-- Mobile overlay -->
  <div class="sidebar-overlay" id="sidebar-overlay"></div>

  <!-- Mobile menu button -->
  <button id="menu-toggle" aria-label="Toggle navigation">&#9776;</button>

  <!-- Sidebar -->
  <aside id="sidebar">
    <div class="sidebar-header">
      <h1>The Christian's Secret of a Happy Life</h1>
      <p class="author">Hannah Whitall Smith</p>
    </div>
    <nav>
      <ul>
        {sidebar_html}
      </ul>
    </nav>
  </aside>

  <!-- Main content -->
  <main id="content">
    <!-- Discussion / Text toggle -->
    <div id="view-toggle" class="hidden">
      <button data-view="discussion" class="active">Discussion</button>
      <button data-view="text">Text</button>
    </div>

    {sections_html}
  </main>

  <script>
  (function() {{
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    const menuBtn = document.getElementById('menu-toggle');
    const toggle = document.getElementById('view-toggle');
    const toggleBtns = toggle.querySelectorAll('button');
    const navLinks = sidebar.querySelectorAll('nav a');
    const sections = document.querySelectorAll('.content-section');

    let currentTarget = 'summary';
    let currentView = 'discussion';

    function showSection(target, view) {{
      currentTarget = target;
      currentView = view;

      // Hide all sections
      sections.forEach(s => s.classList.remove('active'));

      if (target === 'summary') {{
        // Show book summary, hide toggle
        toggle.classList.add('hidden');
        document.getElementById('section-summary').classList.add('active');
      }} else {{
        // Show toggle
        toggle.classList.remove('hidden');
        // Update toggle buttons
        toggleBtns.forEach(b => {{
          b.classList.toggle('active', b.dataset.view === view);
        }});
        // Show the right section
        const sectionId = 'section-' + target + '-' + view;
        const el = document.getElementById(sectionId);
        if (el) el.classList.add('active');
      }}

      // Update sidebar active state
      navLinks.forEach(a => {{
        a.classList.toggle('active', a.dataset.target === target);
      }});

      // Update URL hash
      history.replaceState(null, '', '#' + target + (target !== 'summary' ? '/' + view : ''));

      // Scroll to top of content
      window.scrollTo(0, 0);
    }}

    // Sidebar nav clicks
    navLinks.forEach(a => {{
      a.addEventListener('click', function(e) {{
        e.preventDefault();
        const target = this.dataset.target;
        showSection(target, currentView);
        // Close mobile menu
        sidebar.classList.remove('open');
        overlay.classList.remove('open');
      }});
    }});

    // Toggle button clicks
    toggleBtns.forEach(btn => {{
      btn.addEventListener('click', function() {{
        showSection(currentTarget, this.dataset.view);
      }});
    }});

    // Mobile menu
    menuBtn.addEventListener('click', function() {{
      sidebar.classList.toggle('open');
      overlay.classList.toggle('open');
    }});

    overlay.addEventListener('click', function() {{
      sidebar.classList.remove('open');
      overlay.classList.remove('open');
    }});

    // Handle initial hash
    const hash = location.hash.slice(1);
    if (hash) {{
      const parts = hash.split('/');
      const target = parts[0] || 'summary';
      const view = parts[1] || 'discussion';
      showSection(target, view);
    }}
  }})();
  </script>

</body>
</html>
'''

# Write output
os.makedirs(os.path.join(ROOT, "site"), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(page)

print(f"Built {OUT}")
print(f"  Chapters: {len(chapters)}")
print(f"  Sections: {len(sections)}")
