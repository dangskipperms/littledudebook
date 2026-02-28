# 031 — Repo Separation Discussion

Discussion about how to split the tool and the user's books into separate git repos.

## Options Considered

1. **True siblings** — tool and books side by side in the same parent directory
2. **Hybrid** — books folder nested inside the tool repo, gitignored, with its own .git
3. **Home folder** — books live in the user's home directory (e.g. ~/Documents/littledudebooks/)

## Hybrid Inconveniences (discussed)

- Nested git repos cause confusion for tools, IDEs, and agents
- Agent confusion: which repo to commit to when working across both
- Accidental deletion on re-clone (books are gitignored, lost if tool dir is deleted)
- Coupling despite appearance of separation (user data inside tool directory)
- Gitignore is a fragile privacy boundary (one bad `git add -A` leaks photos to GitHub)
- IDE/tooling awkwardness with nested .git directories

## Decision Direction

**Home folder approach** — a variant of the sibling approach where the books live in a natural personal location on the user's machine:

```
~/Documents/littledudebooks/    <- user's books repo (local git, never pushed by tool)
  {book-name}/
  marie/
  ...

~/projects/.../littledudebook/  <- the tool (cloned from GitHub, pushed to GitHub)
```

### Why this wins
- No nested git — completely separate directory trees
- Zero risk of accidentally pushing private photos to GitHub
- Books survive tool re-clone
- Follows macOS convention (personal files in ~/Documents/)
- Clean ownership boundary: user's data is in their space, tool is in dev space
- Tool discovers books path via config file or first-run prompt

## Refinement: Strict Separation Principle

**If it's about a book or the user's work, it goes in the books folder. Only pure tool/codebase stays in the tool repo.**

This means `agents-workspace/` (runtime state, doc.md) is NOT part of the tool — it IS the book. It moves to the books folder as the book's own `doc.md`.

### Tool repo contains ONLY:
- `.claude/agents/`, `.claude/commands/`, `.claude/skills/` — agent definitions
- `style-gallery/` — style references
- `assemble_pdf.py` — scripts
- `agents-plan.md`, `roadmap.md`, `git-architecture.md` — design docs
- `CLAUDE.md`, `package.json` — project config

### Books folder contains ALL user/book data:
- `{book-name}/doc.md` — what is currently `agents-workspace/doc.md`
- `{book-name}/input/photos/` — real photos
- `{book-name}/output/` — characters, scenes, PDFs, character sheets
- `{book-name}/manifest.md` — timeline (maintained by git-keeper)
- Any prompt history or conversation logs
- `$nothing/` and any other working/scratch content

### The test: hand the tool repo to a stranger
There should be zero trace of the book subject, his photos, his story, or his book. Just code.
