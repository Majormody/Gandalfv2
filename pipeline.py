from config import NUMBER_OF_TABLE_CHUNKS, NUMBER_OF_TEXT_CHUNKS
from indexing.embedder import Embedder
from indexing.vector_store import VectorStore
from retrieval.retriever import Retriever
from generation.llm_client import LLMClient
from generation.prompts import build_system_prompt,build_user_prompt
from ingestion.parser import parse_pdf
from ingestion.table_chunker import chunk_tables
from ingestion.text_chunker import chunk_markdown
from data_schemas import IngestSummary,GenerationResult


from typing import Callable
import tempfile
import os



class RagPipeline:
    def __init__(self, embedder: Embedder):
        self.vector_store = VectorStore(embedder=embedder)
        self.retriever = Retriever(vector_store=self.vector_store, embedder=embedder)
        self.llm_client = LLMClient()

    def ingest(self, pdf_bytes: bytes, file_name: str,
               status_fn: Callable[[str], None] | None = None)->IngestSummary:

        def save_pdf_bytes_to_tempfiles(pdf_bytes: bytes)-> str :
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False ) as temp_file:
                temp_file.write(pdf_bytes)
                return temp_file.name

        file_path = None
        try:
            file_path = save_pdf_bytes_to_tempfiles(pdf_bytes)

            if status_fn: status_fn("Parsing PDF!")

            parsed_document = parse_pdf(file_path)
           
            text_chunks = chunk_markdown(md_text=parsed_document.markdown_text, doc_id=file_name)
            table_chunks = chunk_tables(raw_tables=parsed_document.raw_tables, doc_id=file_name)


            if status_fn: status_fn("Storing Chunks!")

            self.vector_store.clear()
            self.vector_store.add_chunks(text_chunks + table_chunks)
        finally:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)


        return IngestSummary(
            document=file_name,
            n_text=len(text_chunks),
            n_table=len(table_chunks)
        )

    def ask(self, query: str, n_text: int = NUMBER_OF_TEXT_CHUNKS , n_table: int = NUMBER_OF_TABLE_CHUNKS)-> GenerationResult:

        retrieval_results = self.retriever.retrieve(query=query,
                                                   n_text=n_text,
                                                   n_table= n_table)
        system_prompt = build_system_prompt()
        user_prompt = build_user_prompt(query=query,
                                        retrieval=retrieval_results)
        while True:
            answer = self.llm_client.generate(system_prompt=system_prompt,
                                          user_prompt=user_prompt)
            if answer and answer.strip():

                return GenerationResult(
                answer=answer,
                sources=retrieval_results
                            )

        
        
        

        
        

