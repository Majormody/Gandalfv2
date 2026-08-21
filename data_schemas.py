from dataclasses import dataclass
from typing import Literal

@dataclass
class RawTable:
    page_number: int
    table_index: int
    cells: list[list]

@dataclass
class ParsedDocument:
    markdown_text: str
    raw_tables: list[RawTable]

@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    content: str
    chunk_type: Literal["text", "table"]
    page_number: int | None
    metadata: dict  # for H1,H2

@dataclass
class RetrievedChunk():
    chunk: Chunk
    score: float

@dataclass
class RetrievalResult:
    text_chunks: list[RetrievedChunk]
    table_chunks: list[RetrievedChunk]

@dataclass
class GenerationResult:
    answer: str
    sources: RetrievalResult

@dataclass
class IngestSummary:
    document: str
    n_text: int
    n_table: int