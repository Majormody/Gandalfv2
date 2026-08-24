#Files Imported
from indexing.embedder import Embedder
from data_schemas import Chunk, RetrievedChunk
from typing import Literal

#Packages Imported
import chromadb
import json

class VectorStore:

    def __init__(self, embedder: Embedder,
                 persist_dir: str | None = None,
                 collection_name: str = "datasheet_chunks"):

        self._embedder = embedder
        self._collection_name = collection_name

        if not persist_dir:
            self._client = chromadb.Client()
            
        else:
            self._client = chromadb.PersistentClient(path=persist_dir)

        self._collection = self._client.get_or_create_collection(
            name=self._collection_name,
            configuration={
                "hnsw": {
                    "space": "cosine"} 
                                        })  

    def add_chunks(self, chunks: list[Chunk]):

        if not chunks:
            return
        

        def prepare_metadata(metadata: dict) -> dict:
            return {
                key: json.dumps(value) for key,value in metadata.items()
                }

        embeddings = self._embedder.embed_texts([chunk.content for chunk in chunks])
        ids = []
        documents = []
        metadatas = []

        for chunk in chunks:
            metadata = prepare_metadata(chunk.metadata.copy())
            metadata["chunk_type"] = chunk.chunk_type
            metadata["doc_id"] = chunk.doc_id
            if chunk.page_number is not None:
                metadata["page_number"] = chunk.page_number

            metadatas.append(metadata)
            ids.append(chunk.chunk_id)
            documents.append(chunk.content)

        self._collection.add(
            ids = ids,
            embeddings = embeddings,
            metadatas = metadatas,
            documents = documents
        )


    def clear(self):
        self._client.delete_collection(name=self._collection_name)
        self._collection = self._client.get_or_create_collection(
            name=self._collection_name,
            configuration={
                "hnsw": {
                    "space": "cosine"} 
                                        }) 


    def query(self, query_embedding: list[float], top_k: int,
              chunk_type: Literal["text", "table"]) -> list[RetrievedChunk]:
        
        if not query_embedding:
            return []

        match_count = len(self._collection.get(where={"chunk_type":chunk_type})["ids"])
        effective_k = min(top_k, match_count)
        if effective_k == 0:
            return []
        
        def reconstruct_metadata(metadata: dict, chunk_fields: set) -> dict:
            return {
                key: json.loads(value)
                for key, value in metadata.items()
                if key not in chunk_fields
            }

        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=effective_k,
            where={"chunk_type":chunk_type}
            )
        
        retrieved_chunks = []
        for chunk_id, content, metadata, distance in zip(
            results["ids"][0],results["documents"][0],
            results["metadatas"][0], results["distances"][0]):

                
            chunk_metadata = reconstruct_metadata(metadata.copy(), {"page_number", "chunk_type", "doc_id"})

            chunk = Chunk(
                chunk_id = chunk_id,
                content = content,
                chunk_type = metadata["chunk_type"],
                doc_id = metadata["doc_id"],
                metadata = chunk_metadata,
                page_number = metadata.get("page_number", None)
                )
            retrieved_chunks.append(RetrievedChunk(chunk,1-distance))

        return retrieved_chunks
                


