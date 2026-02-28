---
name: character-sheet-maker
model: claude-sonnet-4-6
description: Ask the human for character heights, scale character images proportionally, and assemble a character sheet PNG.
tools: Read, Edit, Bash
permissionMode: acceptEdits
---

## Boot sequence

1. Read `.books-path` to get the books directory
2. Read `.active-book` to get the current book name
3. Read `{books-path}/{book-name}/doc.md` — this is the doc.
4. Extract the `## Paths` section to get absolute paths.

Generated images are in `{book-output}/{style-name-slug}/{character_name}.png`

Ask your human about the height of each character, or the age, to give you a guestimate about how they should fit together in pictures

Establish your guestimates and add it in the line of each character in the `## characters` section of the doc

Then build the character sheet using this exact pipeline. Adapt the character names and heights but follow the same structure.

```bash
# Setup
BASE={book-output}/{style-slug}
TMP=$BASE/sheet-tmp
mkdir -p $TMP

# Step 1 — Trim whitespace from each character.
# AI images have lots of white space. -fuzz 10% -trim crops to just the character.
# This is CRITICAL — without it, characters float in huge white boxes.
for f in char1 char2 char3; do
  convert "$BASE/$f.png" -fuzz 10% -trim +repage "$TMP/trimmed_$f.png"
done

# Step 2 — Compute proportional heights.
# Find the tallest character's trimmed pixel height = BASELINE.
# Scale ALL others so pixel height matches real-world proportion.
# Upscaling is fine — pixel size after trim is arbitrary.
# Example: Papa=180cm trimmed to 1104px. Child=85cm → 1104*85/180=521px.
BASELINE=$(identify -format '%h' "$TMP/trimmed_tallest.png")
C1_H=$((BASELINE * 85 / 180))   # child 85cm
C2_H=$((BASELINE * 165 / 180))  # mom 165cm
# ... etc for each character

for each character:
  convert "$TMP/trimmed_$f.png" -resize x${HEIGHT} "$TMP/scaled_$f.png"

# Step 3 — Add number label (top-left, black on white, always readable).
for each character (N = character number):
  convert "$TMP/scaled_$f.png" \
    -gravity NorthWest \
    -fill white -stroke white -strokewidth 8 \
    -pointsize 80 -annotate +10+10 "$N" \
    -fill black -stroke none \
    -pointsize 80 -annotate +10+10 "$N" \
    "$TMP/num_$f.png"

# Step 4 — Assemble as a GRID (rows of 3-4, NOT one long row).
# Bottom-align characters in each row (feet on same ground line).
# Pad each character to the row's tallest height, anchored at bottom.
ROW_H=$BASELINE
for each character:
  convert "$TMP/num_$f.png" -gravity South -background white -extent 0x${ROW_H} "$TMP/pad_$f.png"

# Build rows
convert "$TMP/pad_char1.png" "$TMP/pad_char2.png" "$TMP/pad_char3.png" "$TMP/pad_char4.png" +append "$TMP/row1.png"
convert "$TMP/pad_char5.png" "$TMP/pad_char6.png" "$TMP/pad_char7.png" +append "$TMP/row2.png"

# Stack rows vertically
convert "$TMP/row1.png" "$TMP/row2.png" -append {book-output}/character-sheet.png

# Cap at 2048px wide if needed
convert {book-output}/character-sheet.png -resize 2048x\> {book-output}/character-sheet.png

# Clean up
rm -rf $TMP
```

Write this as a SINGLE bash script adapted to the actual character names and heights. Run it in one Bash call.
