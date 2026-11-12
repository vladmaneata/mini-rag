import json
from pathlib import Path

EXCLUDED = {"release-notes.md"}

def split_in_chunks(lines):
    chunks = []
    title = "start"
    current = []
    in_code = False
    for line in lines:
        if line.startswith("```"):
            in_code = not in_code
            current.append(line)
            continue
        if line.startswith("#") and not in_code:
            line = line.lstrip("#").strip()
            if current:
                text = "\n".join(current)
                if text.strip():
                    chunks.append((title, text))
            title = line.split(" { #")[0]
            current = []
        else:
            current.append(line)

    if current:
        text = "\n".join(current)
        if text.strip():
            chunks.append((title, text))
    return chunks


with open("data/chunks.jsonl", "w", encoding="utf-8") as f:
    for path in sorted(Path("data/raw").rglob("*.md")):
        if path.name in EXCLUDED:
            continue
        chunk_path = path.relative_to("data/raw").as_posix()
        chunks = split_in_chunks(path.read_text(encoding="utf-8").splitlines())
        for i, (title, text) in enumerate(chunks):
            record = {
                "source": chunk_path,
                "id": f"{chunk_path}#{i}",
                "title": title,
                "text": text,
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    