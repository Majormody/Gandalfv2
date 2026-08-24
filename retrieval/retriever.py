from indexing.vector_store import VectorStore
from indexing.embedder import Embedder

from data_schemas import RetrievalResult

class Retriever:
    def __init__(self, vector_store: VectorStore, embedder: Embedder):
        self._vector_store = vector_store
        self._embedder = embedder


    def retrieve(self, query: str, n_text: int, n_table: int,)-> RetrievalResult:
        query_embedding = self._embedder.embed_query(query)

        table_chunks = self._vector_store.query(
            query_embedding=query_embedding,
            top_k=n_table,
            chunk_type="table"
        )

        text_chunks = self._vector_store.query(
            query_embedding = query_embedding,
            top_k=n_text,
            chunk_type="text"
        )

        return RetrievalResult(table_chunks=table_chunks, text_chunks=text_chunks)

      




