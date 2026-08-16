
from data_schemas import Chunk
import re

def	chunk_markdown(md_text:	str, doc_id: str, max_chars: int = 1000,	
                   overlap:	int	= 100)->	list[Chunk]:
    if not md_text:
        return []
    
    eof = len(md_text)
    lines = md_text.splitlines()

    structured = False
    chunks = []
    chunk_text = ""

    pattern = r"#+.*?#+"
    for line in lines:
        if re.search(pattern,line): 
            structured = True
            break
    if not structured:
        for start in range(0, eof, max_chars - overlap):
            end = min(start + max_chars, eof)
            chunk = Chunk(
                doc_id = doc_id,
                content = md_text[start:end],
                chunk_id = "",
                chunk_type = "text",
                meta_data = {}
                )
            chunks.append(chunk)
            if end == eof:
                break
        return chunks



     
    