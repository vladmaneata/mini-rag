import json

import pandas as pd

from mini_rag.bm25 import BM25

with open("eval/eval_draft.jsonl", "r", encoding="utf-8") as f:
    eval_questions = [json.loads(line) for line in f]
with open("data/chunks.jsonl", "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f]
bm25 = BM25(chunks)

results = []
for question in eval_questions:
    query = question["question"]
    source_id = question.get("source_id")
    bm25_results = bm25.search(query, k=5)
    id_set = {chunk["id"] for chunk, _ in bm25_results}
    if source_id and source_id not in id_set:
        results.append({
            "question": query,
            "Prediction": "missed"
        })
    else:
        results.append({
            "question": query,
            "Prediction": "found"
        })


df = pd.DataFrame(results)
df.to_csv("eval/eval_results.csv", index=False)
predicted = df[df["Prediction"] == "found"]["Prediction"].count()
total = df["Prediction"].count()
print(f"Predicted: {predicted}, Total: {total}")
print(predicted / total) 
