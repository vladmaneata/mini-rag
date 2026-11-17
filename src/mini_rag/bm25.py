import math
import re
from collections import Counter


def words(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


class BM25:
    def __init__(self, chunks: list[dict], k1: float = 1.5, b: float = 0.75):
        self.chunks = chunks
        self.k1 = k1
        self.b = b
        self.tfs = [Counter(words(chunk["text"])) for chunk in chunks]
        self.lengths = [sum(tf.values()) for tf in self.tfs]
        self.avg_len = sum(self.lengths) / len(self.lengths)
        self.df = Counter()
        for tf in self.tfs:
            self.df.update(tf.keys())
        self.n = len(chunks)

    def idf(self, word: str) -> float:
        return math.log((self.n - self.df[word] + 0.5) / (self.df[word] + 0.5) + 1)

    def score(self, query_words: set[str], i: int) -> float:
        score = 0.0
        tf = self.tfs[i]
        length = self.lengths[i]
        for word in query_words:
            f = tf[word]
            if f == 0:
                continue
            idf = self.idf(word)
            score += (
                idf
                * f
                * (self.k1 + 1)
                / (f + self.k1 * (1 - self.b + self.b * length / self.avg_len))
            )
        return score

    def search(self, query: str, k: int = 5) -> list[tuple[dict, float]]:
        query_words = set(words(query))
        scores = [(self.chunks[i], self.score(query_words, i)) for i in range(self.n)]
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:k]
