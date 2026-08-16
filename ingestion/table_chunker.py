from data_schemas import  RawTable, Chunk
from ingestion.header_resolver import resolve_headers


def chunk_tables(raw_tables: list[RawTable], doc_id: str, rows_per_chunk: int = 5) -> list[Chunk]:
    if not raw_tables:
        return []

    list_of_chunks = []
    for table in raw_tables:
        if not table.cells or not table.cells[0] or all(c in ("", None) for c in table.cells[0]):
            continue
        header, data = resolve_headers(table.cells)

        for window_start in range(0, len(data), rows_per_chunk):
            row_window = data[window_start : window_start + rows_per_chunk]

            row_texts = []
            for row in row_window:
                pairs = " ".join(f"{h} : {v}" for h, v in zip(header, row))
                row_texts.append(pairs)
            content = "\n".join(row_texts)

            chunk = Chunk(
                chunk_id=f"{doc_id}_ti_{table.table_index}_ws_{window_start}",      
                doc_id=doc_id,
                content=content,
                chunk_type='table',
                page_number=table.page_number,
                metadata= {
                    "headers" : header,
                    "rows"    : row_window ,
                    "structured" : [{f : h for f, h in zip(header,row) }
                    for row in row_window
                    ]

                }
            )
            list_of_chunks.append(chunk)

    return list_of_chunks