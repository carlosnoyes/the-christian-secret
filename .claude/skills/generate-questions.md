# generate-questions

Generates 5 deep, thought-provoking discussion questions for a single chapter of *The Christian's Secret of a Happy Life*.

## When to trigger

When the user asks to generate questions for a chapter (e.g., "/generate-questions 3" or "generate questions for chapter 5").

## Arguments

- **chapter_number**: The chapter number (0 for preface, 1-22 for chapters). Can be passed as the first argument (e.g., `/generate-questions 3`).

## Instructions

Follow these steps in order:

### 1. Determine the chapter number

Parse the chapter number from the argument. If no argument is given, ask the user which chapter.

### 2. Build the file paths

- Book summary: `book_summary.txt`
- Full chapter text: `chapters/{NN}_{name}.txt` where `{NN}` is the zero-padded chapter number
  - Chapter 0 → `00_preface.txt`
  - Chapter 1 → `01_chapter_1.txt`
  - Chapter N → `{NN}_chapter_{N}.txt`
- Questions output: `Questions/{NN}_{name}_questions.txt` using the same naming stem as the chapter file

### 3. Read context (in parallel)

Use the Read tool to load all three of these **in parallel**:

1. **Book summary** — `book_summary.txt`
2. **Full chapter text** — find the matching file in `chapters/` using Glob with pattern `chapters/{NN}_*.txt` (NOT the summary — read the complete chapter)
3. **All previously generated question files** — use Glob for `Questions/*_questions.txt`, then read every file found. These provide context so questions don't repeat themes already covered.

### 4. Draft the questions

Write exactly **5** discussion questions that meet ALL of these criteria:

- **Deep and thought-provoking** — they should push participants beyond surface-level recall into reflection, application, and honest self-examination.
- **Open-ended** — no yes/no answers; each question should invite multiple perspectives and genuine discussion.
- **Appropriate for well-educated adults** — assume a thoughtful small-group setting; reference real-life tensions, intellectual objections, and practical struggles.
- **Grounded in the chapter** — each question should connect to a specific idea, metaphor, or argument from the full chapter text.
- **Non-redundant** — avoid overlapping with questions already generated for other chapters. If a theme recurs across chapters, find the angle unique to *this* chapter.

### 5. Format and save

Write the output file to `Questions/{NN}_{name}_questions.txt` using this format:

```
Chapter {N}: {Chapter Title} — Discussion Questions
====================================================

1. {Question}

2. {Question}

3. {Question}

4. {Question}

5. {Question}
```

Extract the chapter title from the first line of the chapter text file.

### 6. Report

Tell the user the questions have been saved and list them in the response.
