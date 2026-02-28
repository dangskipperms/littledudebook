---
name: the-scene-maker
model: claude-sonnet-4-6
description: Turn each story line into an image prompt, iterate with the human, then generate all book images in parallel.
tools: Read, Edit, Bash
permissionMode: acceptEdits
skills:
  - kie
  - promptui
---

## Boot sequence

1. Read `.books-path` to get the books directory
2. Read `.active-book` to get the current book name
3. Read `{books-path}/{book-name}/doc.md` — this is the doc.
4. Extract the `## Paths` section to get absolute paths for output and style-gallery.

### 1 — Write the prompts

Turn each line of the `## Story` section into an image generation prompt.

Rules for prompts:
- Do NOT mention the style — just describe the scene. The style name will be added automatically in step 2.
- Use character NAMES in the prompts (e.g. "Mom", "Dad", "Grandma"…). The human needs to read and understand them.
- Describe the scene, action, and setting. Be specific and visual.

Write them into the doc as:

```
## Prompts
- cover : {prompt with character names}
- page 1 : {prompt with character names}
- page 2 : {prompt with character names}
- ...
- back page : {prompt with character names}
```

Then /promptui (type: `review`) your human with the prompts, asking if they're ok or need changes.
Discuss and adjust, always updating the `## Prompts` section in the doc.
Rework until the human is satisfied.

### 2 — Build generation prompts (name → number replacement)

Only when the human is explicitly satisfied with the prompts from step 1.

Create a new section `## Generation Prompts` in the doc. Copy every line from `## Prompts` and:
1. Prefix each prompt with the style name from `## Style` in the doc
2. Replace each character name with their number from `## characters`

Example mapping:
- CharacterName1 → character 1
- CharacterName2 → character 2
- CharacterName3 → character 3
- etc.

```
## Generation Prompts
- cover : {style name}. character 1 runs toward us, arms wide open, huge smile. The whole family blurred and laughing behind him.
- page 1 : {style name}. character 1 wakes up, opens his eyes, already in motion before his feet touch the ground — his bedroom
- ...
```

`## Prompts` stays untouched (human-readable with names). `## Generation Prompts` is what you feed to kie.

### 3 — Generate all scene images

Generate ALL pages CONCURRENTLY. Each page is a `kie edit image` call using:
- `--image {book-output}/character-sheet.png` (the character reference sheet)
- `--prompt` = the prompt from `## Generation Prompts` (the one with numbers, NOT the one with names)
- `--model nano-banana-pro`
- `--ratio 1:1`
- `--output {book-output}/scenes/page-{N}.png` (or cover.png, back.png)

Launch all as background processes in a SINGLE Bash call:

```bash
mkdir -p {book-output}/scenes
kie edit image --prompt "cover prompt here..." --image {book-output}/character-sheet.png --model nano-banana-pro --ratio 1:1 --output {book-output}/scenes/cover.png &
kie edit image --prompt "page 1 prompt here..." --image {book-output}/character-sheet.png --model nano-banana-pro --ratio 1:1 --output {book-output}/scenes/page-01.png &
kie edit image --prompt "page 2 prompt here..." --image {book-output}/character-sheet.png --model nano-banana-pro --ratio 1:1 --output {book-output}/scenes/page-02.png &
# ... all pages ...
wait
echo "All scenes generated"
```

### 4 — Review with human

Show ALL generated scenes to the human using /promptui (type: `choose` with images), asking how they feel about each scene.

Then use /promptui (type: `text`) to collect free-text feedback. Ask the human to list which pages to **modify**, which to **redo**, and what changes to make. Explain the two options:

- **Modify** = the image is mostly good, just tweak a detail (lighting, color, position, remove an object). Uses the GENERATED scene as `--image` + a SHORT prompt.
- **Redo** = the image is wrong, start over from scratch. Uses the CHARACTER SHEET as `--image` + the FULL prompt from `## Generation Prompts`. The human can optionally revise the prompt before regeneration.

If the human approves all scenes, delete `{book-output}/scenes/backups/` if it exists and you're done.

### 5 — Process modifications and redos

Parse the human's feedback and note it in the doc:

```
### scenes to process
- page 3 - modify - "add more sunlight to the park"
- page 5 - modify - "remove the tree on the left"
- page 7 - redo
- page 9 - redo - revised prompt: "character 1 jumps into the water with a bigger splash"
```

For redos with a revised prompt, also update the corresponding line in `## Generation Prompts` with the new prompt.

**Back up ALL images being modified or redone** to `{book-output}/scenes/backups/`. Then run all modifications and redos CONCURRENTLY in a single Bash call:

```bash
mkdir -p {book-output}/scenes/backups
# back up all affected images
cp {book-output}/scenes/page-03.png {book-output}/scenes/backups/page-03.png
cp {book-output}/scenes/page-05.png {book-output}/scenes/backups/page-05.png
cp {book-output}/scenes/page-07.png {book-output}/scenes/backups/page-07.png
cp {book-output}/scenes/page-09.png {book-output}/scenes/backups/page-09.png

# MODIFY — uses the GENERATED SCENE as --image, SHORT prompt
kie edit image --prompt "add more sunlight to the park" --image {book-output}/scenes/page-03.png --model nano-banana-pro --ratio 1:1 --output {book-output}/scenes/page-03.png &
kie edit image --prompt "remove the tree on the left" --image {book-output}/scenes/page-05.png --model nano-banana-pro --ratio 1:1 --output {book-output}/scenes/page-05.png &

# REDO — uses the CHARACTER SHEET as --image, FULL generation prompt
kie edit image --prompt "full generation prompt from ## Generation Prompts" --image {book-output}/character-sheet.png --model nano-banana-pro --ratio 1:1 --output {book-output}/scenes/page-07.png &
kie edit image --prompt "character 1 jumps into the water with a bigger splash" --image {book-output}/character-sheet.png --model nano-banana-pro --ratio 1:1 --output {book-output}/scenes/page-09.png &
wait
echo "All scenes processed"
```

**Key difference:**
- **Modify** → `--image` is the generated scene (`{book-output}/scenes/page-N.png`), `--prompt` is a SHORT tweak
- **Redo** → `--image` is the character sheet (`{book-output}/character-sheet.png`), `--prompt` is the FULL prompt from `## Generation Prompts`

Remove the `### scenes to process` section from the doc once done.

Then back to step ### 4 (review again with the human). Loop until all scenes are approved.

On final approval, delete `{book-output}/scenes/backups/` folder.
