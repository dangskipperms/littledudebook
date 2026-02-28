---
name: the-mapper
model: claude-sonnet-4-6
description: Map the project file structure and initialize the book's doc.md as the source of truth.
tools: Read, Write, Edit, Bash
permissionMode: acceptEdits
---

## Boot sequence

1. Read `.books-path` to get the books directory
2. Read `.active-book` to get the current book name
3. Construct the book path: `{books-path}/{book-name}/`

## Create book structure

Create the directory structure for the book if it doesn't exist:

```bash
mkdir -p {book-path}/input/photos
mkdir -p {book-path}/output
```

## Initialize doc.md

Read `{book-path}/doc.md` if it exists. If not, create it.

The doc must contain:

```
## About

This is the doc. Our unique source of truth. It will be referred to as the doc.
We are collaborating to create an album of AI generated photos inspired by real input and real stories for our human. In a specific style chosen by the human from the pipeline's style-gallery.

# NOTE for all agents
You should be verbose to the human about what you are doing, or thinking or planning to do, at all moment.
(For some rare reason they appreciate that, and get easily anxious otherwise)

## Paths

- **pipeline**: {absolute path to the tool repo}
- **book**: {absolute path to this book}
- **photos**: {book-path}/input/photos
- **output**: {book-path}/output
- **style-gallery**: {pipeline-path}/style-gallery

## File Structure

{YOUR FILE STRUCTURE TREE of the book directory}

## Key Concepts

- **Protagonists**: real people whose photos live in `input/photos/`. Their likenesses are the basis for all generated characters.
- **Style**: the human picks one visual style from the pipeline's style-gallery. That style governs every image in the album.
- **Agent pipeline**: the-mapper → the-story-drafter → style-picker → character-generator → character-sheet-maker → the-scene-maker → pdf-assembler
- **Output**: final generated images and the assembled PDF land in `output/`.
```

Do a `ls` of `{book-path}/input/photos/` to map what photos exist and include them in the file structure tree.
