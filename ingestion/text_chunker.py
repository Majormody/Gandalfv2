from data_schemas import Chunk
import re

HEADING_RE = re.compile(r"^(#{1,3})\s+(.+)$")

def _window_text(text: str, doc_id: str, metadata: dict,
                  max_chars: int, overlap: int, id_prefix: str) -> list[Chunk]:
    """Shared splitter — same slice-based windowing used by both the
    flat-fallback and heading-aware paths."""
    chunks = []
    eof = len(text)
    for start in range(0, eof, max_chars - overlap):
        end = min(start + max_chars, eof)
        chunks.append(Chunk(
            doc_id=doc_id,
            content=text[start:end],
            chunk_id=f"{doc_id}_{id_prefix}_st_{start}",
            chunk_type="text",
            page_number=None,
            metadata=dict(metadata),  # copy — don't share one dict across chunks
        ))
        if end == eof:
            break
    return chunks


def chunk_markdown(md_text: str, doc_id: str, max_chars: int = 1000, overlap: int = 100) -> list[Chunk]:
    if not md_text:
        return []

    lines = md_text.splitlines()
    has_heading = any(HEADING_RE.match(line) for line in lines)

    if not has_heading:
        return _window_text(md_text, doc_id, {"h1": None, "h2": None, "full_path": None},
                             max_chars, overlap, "flat")

    chunks = []
    h1, h2 = None, None
    buffer_lines = []
    section_index = 0

    def flush():
        nonlocal buffer_lines, section_index, chunks
        text = "\n".join(buffer_lines).strip()
        if text:
            full_path = " > ".join(p for p in (h1, h2) if p) or None
            metadata = {"h1": h1, "h2": h2, "full_path": full_path}
            chunks.extend(_window_text(text, doc_id, metadata, max_chars, overlap, f"sec{section_index}"))
            section_index += 1
        buffer_lines = []

    for line in lines:
        match = HEADING_RE.match(line)
        if match:
            flush()
            level = len(match.group(1))
            title = match.group(2).strip()
            if level == 1:
                h1, h2 = title, None
            elif level == 2:
                h2 = title
           
        else:
            buffer_lines.append(line)
    flush()  

    return chunks