#!/usr/bin/env python3
"""
PDF Assembler — book-agnostic.
Assembles scene images into a PDF, optionally with text overlays from a YAML file.

Usage:
    python3 assemble_pdf.py <book-path>
    python3 assemble_pdf.py              # reads from .books-path + .active-book

The book path should contain:
    output/scenes/   — scene images (cover.png, page-01.png ... back.png)
    doc.md           — source of truth (## Story section determines page order)
    text-overlays.yaml (optional) — text overlay definitions per page
"""

import os
import sys
import re
import glob

from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import white, Color

# Page size: square to match 1024x1024 images
PAGE_SIZE = (8.5 * inch, 8.5 * inch)
W, H = PAGE_SIZE


def resolve_book_path():
    """Resolve the book path from CLI args or config files."""
    if len(sys.argv) > 1:
        return sys.argv[1]

    # Fall back to .books-path + .active-book
    script_dir = os.path.dirname(os.path.abspath(__file__))
    books_path_file = os.path.join(script_dir, ".books-path")
    active_book_file = os.path.join(script_dir, ".active-book")

    if not os.path.exists(books_path_file) or not os.path.exists(active_book_file):
        print("Usage: python3 assemble_pdf.py <book-path>")
        print("Or create .books-path and .active-book in the tool directory.")
        sys.exit(1)

    with open(books_path_file) as f:
        books_dir = f.read().strip()
    with open(active_book_file) as f:
        book_name = f.read().strip()

    return os.path.join(books_dir, book_name)


def parse_page_order(doc_path):
    """Parse ## Story section from doc.md to determine page order."""
    if not os.path.exists(doc_path):
        return None

    with open(doc_path) as f:
        content = f.read()

    # Find ## Story section
    match = re.search(r"## Story\s*\n(.*?)(?=\n##|\Z)", content, re.DOTALL)
    if not match:
        return None

    pages = []
    for line in match.group(1).strip().split("\n"):
        line = line.strip()
        if not line.startswith("- "):
            continue
        # Extract page key: "- cover :", "- page 1 :", "- back page :"
        key_match = re.match(r"- ([\w\s]+?) :", line)
        if key_match:
            key = key_match.group(1).strip().lower()
            if key == "cover":
                pages.append("cover.png")
            elif key == "back page":
                pages.append("back.png")
            elif key.startswith("page "):
                num = key.replace("page ", "").strip()
                pages.append(f"page-{int(num):02d}.png")
    return pages


def load_text_overlays(book_path):
    """Load text overlays from YAML file if it exists."""
    yaml_path = os.path.join(book_path, "text-overlays.yaml")
    if not os.path.exists(yaml_path):
        return {}

    try:
        import yaml
        with open(yaml_path) as f:
            return yaml.safe_load(f) or {}
    except ImportError:
        print("WARNING: PyYAML not installed. Skipping text overlays.")
        return {}


def draw_text_with_shadow(c, text, x, y, font, size, color, align="center"):
    """Draw text with drop shadow for readability."""
    lines = text.split("\n")
    line_height = size * 1.4
    total_height = len(lines) * line_height

    for i, line in enumerate(lines):
        ly = y + total_height - (i * line_height)

        if align == "center":
            text_width = c.stringWidth(line, font, size)
            lx = x - text_width / 2
        else:
            lx = x

        # Shadow
        c.setFillColor(Color(0, 0, 0, 0.7))
        c.setFont(font, size)
        c.drawString(lx + 1.5, ly - 1.5, line)
        c.drawString(lx + 0.8, ly - 0.8, line)

        # Main text
        c.setFillColor(color)
        c.setFont(font, size)
        c.drawString(lx, ly, line)


def build_pdf(book_path):
    """Build the PDF book."""
    scenes_dir = os.path.join(book_path, "output", "scenes")
    book_name = os.path.basename(book_path)
    output_pdf = os.path.join(book_path, "output", f"{book_name}.pdf")
    doc_path = os.path.join(book_path, "doc.md")

    if not os.path.isdir(scenes_dir):
        print(f"ERROR: Scenes directory not found: {scenes_dir}")
        sys.exit(1)

    # Determine page order
    page_order = parse_page_order(doc_path)
    if not page_order:
        # Fall back to alphabetical with cover first, back last
        all_images = sorted(glob.glob(os.path.join(scenes_dir, "*.png")))
        all_images = [os.path.basename(p) for p in all_images]
        # Exclude subdirectories' files
        all_images = [f for f in all_images if os.path.isfile(os.path.join(scenes_dir, f))]

        cover = [f for f in all_images if f == "cover.png"]
        back = [f for f in all_images if f == "back.png"]
        pages = sorted([f for f in all_images if f not in ("cover.png", "back.png")])
        page_order = cover + pages + back

    # Load optional text overlays
    overlays = load_text_overlays(book_path)

    # Build PDF
    c = canvas.Canvas(output_pdf, pagesize=PAGE_SIZE)
    c.setTitle(book_name.capitalize())

    page_count = 0
    for image_file in page_order:
        img_path = os.path.join(scenes_dir, image_file)
        if not os.path.exists(img_path):
            print(f"WARNING: Missing image {img_path}")
            continue

        c.drawImage(img_path, 0, 0, width=W, height=H, preserveAspectRatio=True, anchor='c')

        # Apply text overlay if defined
        page_key = image_file.replace(".png", "")
        if page_key in overlays:
            for txt in overlays[page_key]:
                draw_text_with_shadow(
                    c,
                    txt.get("text", ""),
                    txt.get("x", W / 2),
                    txt.get("y", 0.7 * inch),
                    txt.get("font", "Helvetica"),
                    txt.get("size", 14),
                    white,
                    txt.get("align", "center"),
                )

        c.showPage()
        page_count += 1

    c.save()
    print(f"PDF saved to {output_pdf}")
    print(f"Total pages: {page_count}")


if __name__ == "__main__":
    book = resolve_book_path()
    print(f"Building PDF for: {book}")
    build_pdf(book)
