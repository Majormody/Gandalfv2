import config
from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self, model_name: str = config.EMBED_MODEL_NAME):

        self._model = SentenceTransformer(model_name)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        
        embeddings = self._model.encode(texts, show_progress_bar=False)
        return embeddings.tolist()

    def embed_query(self, query: str) -> list[float]: 

        return self._model.encode([query], show_progress_bar=False)[0].tolist()


def get_embedder()-> Embedder:
    return Embedder()