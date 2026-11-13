import json
import random

with open("data/chunks.jsonl", "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f]
    long_chunks = [c for c in chunks if len(c["text"]) >= 300]
print(f"Found {len(long_chunks)} long chunks")
random.seed(42)  # for reproducibility
sample = random.sample(long_chunks, 50)
with open("data/eval_seed_chunks.jsonl", "w", encoding="utf-8") as out_f:
    out_f.writelines(json.dumps(record, ensure_ascii=False) + "\n" for record in sample)