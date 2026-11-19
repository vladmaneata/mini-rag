import numpy as np


class DenseSearch:
    def __init__(self, chunks, model):
        self.model = model
        self.chunks = chunks
        self.vectors = self.model.encode(
            [chunk["text"] for chunk in chunks], normalize_embeddings=True
        )

    def search(self, query_vector, top_k=5):
        encoded_query = self.model.encode([query_vector], normalize_embeddings=True)[0]
        scores = np.dot(self.vectors, encoded_query)
        top_indices = np.argsort(-scores)[:top_k]
        return [(self.chunks[i], float(scores[i])) for i in top_indices]
