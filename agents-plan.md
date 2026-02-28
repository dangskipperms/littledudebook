# Agent plan
to execute with main claude with /build-agent

Each ## is an agent

All agents share a common boot sequence:
1. Read `.books-path` to get the books directory
2. Read `.active-book` to get the current book name
3. Read `{books-path}/{book-name}/doc.md` — this is the doc, the source of truth

## 1 The orchestrator
Reads `.books-path` and `.active-book` to find the active book.
If no active book is set, asks the human.
Reads the doc and agent-plan to evaluate where we are in the process.
Proposes the user a starting point. Dispatches agents accordingly.

## 2 The mapper
Creates the book directory structure in the books repo.
Initializes `{book}/doc.md` as the source of truth.
Maps `{book}/input/photos/` and writes the file structure tree.

## 3 The story drafter
Reads the doc.
Interviews the human to build characters + storyboard.
Writes `## characters` and `## Story` to the doc.

## 4 Style picker
Reads the doc.
Uses `/promptui --pre-built style-gallery` to show all styles.
Writes choice to `## Style` in the doc.

## 5 Character generator
Reads the doc. Gets paths from `## Paths`.
Generates all characters concurrently via kie using:
- style reference from `{pipeline}/style-gallery/pictures/`
- character photos from `{book}/input/photos/`
- output to `{book}/output/{style-slug}/`

## 6 Character sheet maker
Reads the doc. Gets paths from `## Paths`.
Asks human for heights, builds proportionally-scaled character sheet.
Saves to `{book}/output/character-sheet.png`.

## 7 The scene maker
Reads the doc. Gets paths from `## Paths`.
Writes prompts, builds generation prompts (name→number), generates scenes.
Uses `{book}/output/character-sheet.png` as reference.
Saves scenes to `{book}/output/scenes/`.

## 8 PDF assembler
Reads the doc. Gets paths from `## Paths`.
Runs `assemble_pdf.py {book-path}` to build the PDF.
Saves to `{book}/output/{book-name}.pdf`.
