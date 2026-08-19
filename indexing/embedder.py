import config
from sentence_transformers import SentenceTransformer
import numpy
class Embedder:
    def __init__(self, model_name: str = config.EMBED_MODEL_NAME):

        self._model = SentenceTransformer(model_name)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        
        embeddings = self._model.encode(texts)
        return embeddings.tolist()

    def embed_query(self, query: str) -> list[float]: 

        return self._model.encode_query(query).tolist()

