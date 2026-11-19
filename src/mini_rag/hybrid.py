class HybridSearch:
    def __init__(self, bm25, dense, k_rrf: int = 60, depth: int = 50):
        self.bm25 = bm25
        self.dense = dense
        self.k_rrf = k_rrf
        self.depth = depth

    def search(self, query, k=10):  # CHANGE 1: accept k, like the other two classes
        bm25_results = self.bm25.search(query, self.depth)
        dense_results = self.dense.search(query, self.depth)
        return self._rrf_merge(bm25_results, dense_results, k)

    def _rrf_merge(self, bm25_results, dense_results, k):
        scores = {}
        chunks_by_id = {}  # CHANGE 2: remember the full chunk for each id
        for rank, (chunk, _) in enumerate(bm25_results, start=1):  # CHANGE 3: unpack (chunk, score)
            chunk_id = chunk["id"]
            chunks_by_id[chunk_id] = chunk
            scores[chunk_id] = scores.get(chunk_id, 0) + 1 / (rank + self.k_rrf)
        for rank, (chunk, _) in enumerate(dense_results, start=1):
            chunk_id = chunk["id"]
            chunks_by_id[chunk_id] = chunk
            scores[chunk_id] = scores.get(chunk_id, 0) + 1 / (rank + self.k_rrf)  # CHANGE 4: 1, not k_rrf
        sorted_ids = sorted(scores, key=lambda i: scores[i], reverse=True)
        return [(chunks_by_id[i], scores[i]) for i in sorted_ids[:k]]  # CHANGE 5: top k, as (chunk, score)