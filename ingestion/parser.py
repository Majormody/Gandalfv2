from data_schemas import RawTable, ParsedDocument
import pymupdf4llm, pymupdf
from error_classes import PDFParsingError

def parse_pdf(file_path : str) -> ParsedDocument:
    try:
        with pymupdf.open(file_path) as doc:

            tables_extracted = []
            table_index = 0
            for page_index, page in enumerate(doc, start = 1):
                try:
                    tables = page.find_tables(use_layout = False) 

                    for table in tables.tables:
                        table_index +=1
                        raw_table = RawTable(
                            cells = table.extract(),
                            page_number = page_index,
                            table_index = table_index
                        )
                        tables_extracted.append(raw_table)
                except Exception as e:
                    continue

            headers = pymupdf4llm.IdentifyHeaders(doc, max_levels=3)
            md = pymupdf4llm.to_markdown(doc, hdr_info = headers, embed_images=False)
    except(RuntimeError, TypeError, ValueError) as e:
        raise PDFParsingError(
            f"Failed to parse pdf: {file_path}", file_path, e) from e
            

    return ParsedDocument(
        raw_tables = tables_extracted,
        markdown_text = md
        )
    