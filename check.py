import pymupdf4llm
import re

# point this at one of your actual datasheet PDFs
pdf_path = "pic.pdf"

md_text = pymupdf4llm.to_markdown(pdf_path)
lines = md_text.splitlines()

heading_re = re.compile(r"^(#{1,3})\s+(.+)$")
indented_heading_re = re.compile(r"^\s+#{1,6}\s+")

print(f"Total lines: {len(lines)}\n")

print("=== Lines starting with # (flush-left, levels 1-3) ===")
for i, line in enumerate(lines):
    if heading_re.match(line):
        print(f"  [{i}] {line!r}")

print("\n=== Lines with leading whitespace before # (would be MISSED by ^ anchor) ===")
found_indented = False
for i, line in enumerate(lines):
    if indented_heading_re.match(line):
        print(f"  [{i}] {line!r}")
        found_indented = True
if not found_indented:
    print("  none found")

print("\n=== Any '#' at h4+ level (4+ hashes, flush-left) ===")
h4_plus_re = re.compile(r"^#{4,}\s+")
found_h4 = False
for i, line in enumerate(lines):
    if h4_plus_re.match(line):
        print(f"  [{i}] {line!r}")
        found_h4 = True
if not found_h4:
    print("  none found")