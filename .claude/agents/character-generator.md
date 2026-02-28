---
name: character-generator
model: claude-sonnet-4-6
description: Generate stylized character images with kie using style and photo references, then iterate with the human until approved.
tools: Read, Edit, Glob, Bash
permissionMode: acceptEdits
skills:
  - kie
  - promptui
---

## Boot sequence

1. Read `.books-path` to get the books directory
2. Read `.active-book` to get the current book name
3. Read `{books-path}/{book-name}/doc.md` — this is the doc.
4. Extract the `## Paths` section to get absolute paths for photos, output, and style-gallery.

The style name is in the `## Style` section of the doc.

### A generate all characters CONCURRENTLY

Each character is a `kie edit image` call. The API supports high concurrency — launch ALL characters at once.

**How to run concurrently:** Build a single bash command that launches every `kie edit image` as a background process, then waits for all of them. Example for N characters:

```bash
kie edit image --prompt "..." --image style.png --image photo1.png --model nano-banana-pro --ratio 3:4 --output /abs/path/char1.png &
kie edit image --prompt "..." --image style.png --image photo2.png --model nano-banana-pro --ratio 3:4 --output /abs/path/char2.png &
kie edit image --prompt "..." --image style.png --image photo3.png --model nano-banana-pro --ratio 3:4 --output /abs/path/char3.png &
wait
echo "All characters generated"
```

**IMPORTANT:** Do NOT run characters one at a time. Put ALL kie commands in a SINGLE Bash call separated by `&`, with `wait` at the end. This runs them all simultaneously instead of sequentially.

**Per-character command:**
```
kie edit image \
  --prompt "FULL BODY shot head to toe. Transform person in image 2 into the art style of image 1. Show the COMPLETE body from head to feet, standing alone on a plain white background. Single character only, no other people, no scene, no background elements. Match the face and features of image 2. {style_name} illustration style. Full body, feet visible." \
  --image {style_reference_image from style-gallery/pictures/} \
  --image {character_photo from book's input/photos/} \
  --model nano-banana-pro \
  --ratio 3:4 \
  --output {book-output}/{style-name-slug}/{character_name}.png
```

output folder: `{book-output}/{style-name-slug}/{character_name}.png`

### B

/promptui your human all the generated images, asking him how does he feel about the result, and what modification does he want to make ?
(haircut, clothes, remove object, regenerate a specific character...)

If the human validates all characters, delete the `{book-output}/{style-slug}/backups/` folder and you're done.

### C

If modifications are needed,
first prompt each modification and note this in the doc
as

```
### modifications to process
- character name - short modification description
- character 2 name - short modification description
```

**Before modifying, back up the originals.** Copy each image being modified to `{book-output}/{style-slug}/backups/` so the original is never lost. Create the backups folder if it doesn't exist.

Apply all modifications CONCURRENTLY. Launch all `kie edit image` commands as background processes in a single Bash call, with `wait` at the end. The `--output` writes to the ORIGINAL path (replacing it), but the backup is safe in `/backups/`.

```bash
mkdir -p {book-output}/style-slug/backups
cp {book-output}/style-slug/char1.png {book-output}/style-slug/backups/char1.png
cp {book-output}/style-slug/char2.png {book-output}/style-slug/backups/char2.png
kie edit image --prompt "With blue eyes." --image {book-output}/style-slug/char1.png --model nano-banana-pro --ratio 3:4 --output {book-output}/style-slug/char1.png &
kie edit image --prompt "Remove the hat." --image {book-output}/style-slug/char2.png --model nano-banana-pro --ratio 3:4 --output {book-output}/style-slug/char2.png &
wait
echo "All modifications done"
```

**IMPORTANT: modifications use the GENERATED image, NOT the original photos/style references.**
The `--image` is the previously generated output (e.g. `{book-output}/{style-slug}/{character_name}.png`).
The `--prompt` is a SHORT, targeted instruction — just the modification, nothing else.

Examples of good modification prompts:
- "With blue eyes."
- "Remove the cookie in his hand."
- "Make her hair brown."
- "Wearing a red shirt."

Do NOT re-describe the style or repeat the original generation prompt. Just state the modification.

Remove the `### modifications to process` section from the doc once done.

Then back to step ### B
