# Roadmap

## Done
- [x] Core pipeline: story → style → characters → scenes → PDF
- [x] Scene review with modify vs redo
- [x] Concurrent generation throughout
- [x] PDF assembler (images only)
- [x] Two-repo architecture: tool repo (GitHub) + books repo (local ~/Documents/littledudebooks/)
- [x] Book-agnostic agents: .books-path + .active-book discovery
- [x] Generalized assemble_pdf.py (accepts book path as argument)
- [x] Clean git history: zero personal data in tool repo

## Next — Polish
- [ ] Better promptui forms: rows of images with approve/modify/redo per scene instead of generic text fields
- [ ] Reduce agent verbosity — less nonsense, more actionable UI

## Restyle mode
- [ ] Take an existing finished book and regenerate all scenes in a new style in one shot
- [ ] Same story, same characters, new style → new PDF

## Story archive
- [ ] Once a story is generated, save it to a history/archive
- [ ] Reuse archived stories: pass to a new style, apply modifications, remix
- [ ] Start a new book from an archived story with different characters

## Story modifications
- [ ] Edit an existing story after generation (add pages, change scenes, tweak text)
- [ ] Re-run only the changed pages, keep the rest

## Web UI
- [ ] Local web server that drives the entire pipeline through the browser
- [ ] Visual review: see all scenes/characters as a grid, click to approve/modify/redo
- [ ] Style picker as a visual gallery in the browser
- [ ] Story editor with live preview
- [ ] Agents run in the background, UI updates in real time (websockets)
- [ ] No CLI interaction needed — everything from the browser

## Open source prep
- [x] Clean up repo for public sharing
- [ ] Write setup instructions
- [ ] Document the agent pipeline for contributors
