import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
vectors = model.encode(
    [
        "How do I share setup logic between my endpoints?",
        "Dependencies let you reuse code across path operations.",
        "Build a Docker image for your app.",
    ]
)


def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

print(cosine_similarity(vectors[0], vectors[1]))
print(cosine_similarity(vectors[0], vectors[2]))