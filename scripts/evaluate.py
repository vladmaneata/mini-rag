import json

import pandas as pd

from mini_rag.bm25 import BM25

with open("eval/eval_draft.jsonl", "r", encoding="utf-8") as f:
    eval_questions = [json.loads(line) for line in f]
with open("data/chunks.jsonl", "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f]
bm25 = BM25(chunks, stem = False)
bm25withStem = BM25(chunks, stem = True)

results = []
for question in eval_questions:
    query = question["question"]
    source_id = question.get("source_id")
    bm25_results = bm25.search(query, k=5)
    id_set = {chunk["id"] for chunk, _ in bm25_results}
    if source_id and source_id not in id_set:
        results.append({"question": query, "Prediction": "missed"})
    elif source_id and source_id in id_set:
        results.append({"question": query, "Prediction": "found"})


df_plain = pd.DataFrame(results)
df_plain.to_csv("eval/eval_results.csv", index=False)
predicted = df_plain[df_plain["Prediction"] == "found"]["Prediction"].count()
total = df_plain["Prediction"].count()
print(f"Predicted: {predicted}, Total: {total}")
print(predicted / total)
df_plain[df_plain["Prediction"] == "missed"].to_csv("eval/eval_missed.csv", index=False)

df_stem = pd.DataFrame([
    {"question": question["question"], "Prediction": "found" if question.get("source_id") in {chunk["id"] for chunk, _ in bm25withStem.search(question["question"], k=5)} else "missed"}
    for question in eval_questions
])
df_stem.to_csv("eval/eval_results_with_stem.csv", index=False)
predicted_with_stem = df_stem[df_stem["Prediction"] == "found"]["Prediction"].count()
total_with_stem = df_stem["Prediction"].count()
print(f"Predicted with stem: {predicted_with_stem}, Total: {total_with_stem}")
print(predicted_with_stem / total_with_stem)
df_stem[df_stem["Prediction"] == "missed"].to_csv("eval/eval_missed_with_stem.csv", index=False)

both = df_plain.merge(df_stem, on="question", suffixes=("_plain", "_stem"))
both[both["Prediction_plain"] != both["Prediction_stem"]]
both[both["Prediction_plain"] != both["Prediction_stem"]].to_csv("eval/eval_discrepancies.csv", index=False)

