# /kie — Generate or edit images, video, and music with kie.ai

Use this skill to invoke the `kie` CLI for AI generation tasks.

## When $ARGUMENTS is given

Interpret the argument as a generation intent. Examples:
- `/kie a sunset over the ocean` → generate an image with that prompt
- `/kie edit photo.png remove the background` → edit an existing image
- `/kie video of a cat running --image cat.png` → generate a video from a start frame
- `/kie music upbeat indie pop song about summer` → generate a music track
- `/kie credits` → check remaining account credits

Infer the correct subcommand (`generate image`, `generate video`, `generate music`, `edit image`, `credits`) from context.

---

## Commands

### Generate an image
```bash
kie generate image \
  --prompt "<text>" \
  --model default|nano-banana-pro \
  --resolution 1K|2K|4K \
  --ratio 1:1|16:9|9:16|4:3|3:4|21:9 \
  --format png|jpeg \
  --output "<path>"
```
- `--prompt` is required
- Default model: `default`, default ratio: `1:1`, default format: `png`
- `--resolution` is only available with `--model nano-banana-pro`
- Default output: `generated-image-<timestamp>.png` in cwd

### Edit an existing image
```bash
kie edit image \
  --prompt "<what to change>" \
  --image "<source path>" \
  --model default|nano-banana-pro \
  --resolution 1K|2K|4K \
  --ratio 1:1|16:9|9:16|4:3|3:4|21:9 \
  --format png|jpeg \
  --output "<path>"
```
- Both `--prompt` and `--image` are required
- `--image` is repeatable — pass multiple times to supply several reference images
- `--resolution` is only available with `--model nano-banana-pro`
- Use absolute paths for `--image`

### Generate a video
```bash
kie generate video \
  --prompt "<motion description>" \
  --image "<start frame path>" \
  --end-image "<end frame path>" \
  --sound \
  --output "<path>.mp4"
```
- `--prompt` and `--image` are required
- `--end-image` and `--sound` are optional
- Duration is fixed at 5 seconds

### Generate music
```bash
kie generate music \
  --prompt "<lyrics or description>" \
  --style "<musical style>" \
  --title "<track title>" \
  --instrumental \
  --model V4|V4_5|V4_5PLUS|V4_5ALL|V5 \
  --vocal-gender m|f \
  --output "<path>.mp3"
```
- `--prompt` is required
- Use `--custom` when also providing `--style` and `--title`
- Use `--instrumental` to suppress vocals

### Check credits
```bash
kie credits
```

---

## Ratio guide

| Ratio | Use for |
|-------|---------|
| `1:1` | Square — character portraits, avatars |
| `3:4` | Portrait — book pages |
| `4:3` | Landscape — wide scenes |
| `16:9` | Widescreen |
| `9:16` | Vertical / mobile |
| `21:9` | Cinematic |

---

## Rules

- Always use absolute paths for `--image` and `--output` when working inside a project
- After generating, display the output path to the user
- If the output file is an image, show it to the user using the Read tool (images are rendered inline)
- If credits are low, warn the user before running expensive generation tasks
- Prefer `kie edit image` over `kie generate image` when making targeted changes to an existing image — it's faster and preserves character likeness
