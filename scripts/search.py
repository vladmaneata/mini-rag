import json

from mini_rag.bm25 import BM25

with open("data/chunks.jsonl", "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f]
bm25 = BM25(chunks)
question = "How do I run the development server?"
results = bm25.search(question, k=10)
for chunk, score in results:
    print(chunk["title"], score)
