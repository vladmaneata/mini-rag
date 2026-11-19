import json

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

from mini_rag.bm25 import BM25
from mini_rag.dense import DenseSearch

with open("eval/eval_draft.jsonl", "r", encoding="utf-8") as f:
    eval_questions = [json.loads(line) for line in f]
with open("data/chunks.jsonl", "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f]
bm25 = BM25(chunks, stem=False)
model = SentenceTransformer("all-MiniLM-L6-v2")
dense = DenseSearch(chunks, model)

results_for_bm25 = []

for question in eval_questions:
    query = question["question"]
    source_id = question["source_id"]
    bm25_results = bm25.search(query, k=10)
    for index, (chunk, _) in enumerate(bm25_results):
        if source_id == chunk["id"]:
            results_for_bm25.append(
                {"question": query, "Prediction": "found", "Rank": index + 1}
            )
            break
    else:
        results_for_bm25.append({"question": query, "Prediction": "missed", "Rank": None})


df = pd.DataFrame(results_for_bm25)
df.to_csv("eval/recall_results.csv", index=False)


def recall_at_k(df, k):
    found_at_k = df[(df["Prediction"] == "found") & (df["Rank"] <= k)][
        "Prediction"
    ].count()
    total = df["Prediction"].count()
    return found_at_k / total if total > 0 else 0


for k in range(1, 11):
    print(f"Recall at {k}: {recall_at_k(df, k)}")

mrr_bm25 = (1 / df["Rank"]).fillna(0).mean()

print(f"Mean Reciprocal Rank: {mrr_bm25}")

ndcg10_bm25 = pd.Series(1 / np.log2(df["Rank"] + 1)).fillna(0).mean()
print(f"Normalized Discounted Cumulative Gain: {ndcg10_bm25}")

results_for_dense = []

for question in eval_questions:
    query = question["question"]
    source_id = question["source_id"]
    dense_results = dense.search(query, top_k=10)
    for index, (chunk, _) in enumerate(dense_results):
        if source_id == chunk["id"]:
            results_for_dense.append(
                {"question": query, "Prediction": "found", "Rank": index + 1}
            )
            break
    else:
        results_for_dense.append({"question": query, "Prediction": "missed", "Rank": None})

df_dense = pd.DataFrame(results_for_dense)
df_dense.to_csv("eval/recall_results_dense.csv", index=False)

for k in range(1, 11):
    print(f"Dense Recall at {k}: {recall_at_k(df_dense, k)}")

mrr_dense = (1 / df_dense["Rank"]).fillna(0).mean()
print(f"Dense Mean Reciprocal Rank: {mrr_dense}")

ndcg10_dense = pd.Series(1 / np.log2(df_dense["Rank"] + 1)).fillna(0).mean()
print(f"Dense Normalized Discounted Cumulative Gain: {ndcg10_dense}")
