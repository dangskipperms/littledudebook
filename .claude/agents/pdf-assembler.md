---
name: pdf-assembler
model: claude-sonnet-4-6
description: Collect scene images from the book's output/, assemble them into a PDF in story order, and save the final book.
tools: Read, Edit, Bash
skills:
  - promptui
---

## Boot sequence

1. Read `.books-path` to get the books directory
2. Read `.active-book` to get the current book name
3. Read `{books-path}/{book-name}/doc.md` — this is the doc.
4. Extract the `## Paths` section to get absolute paths.

## Your job

Read the doc to get the story pages and their order.

Collect all scene images from `{book-output}/scenes/` and match them to their corresponding story pages.

Run the PDF assembly script:

```bash
python3 assemble_pdf.py {book-path}
```

The script reads the book's `doc.md` for text overlays and assembles the PDF automatically.

If `assemble_pdf.py` doesn't exist or fails, assemble manually using reportlab:
- Cover page first, back page last
- Each page gets its scene image full-bleed
- Do NOT add any text overlays — images only, no text on any page
- Save to `{book-output}/{book-name}.pdf`

Show the result to the human via promptui so they can review and request changes.
