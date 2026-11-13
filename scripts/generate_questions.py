import json

from anthropic import Anthropic
from anthropic.types import TextBlock
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError

SYSTEM_PROMPT = """You write evaluation questions for a search system over the FastAPI documentation.
Given a documentation section, write one question that a developer who has NOT read
this section would ask, and that this section answers. Use your own words: do not
copy distinctive phrases from the section. Ask about exactly one thing in one question. Do not mention version numbers, dates, or other
details that only someone who already read the section would know. Reply only with JSON: {"question": "..."}"""


class Question(BaseModel):
    question: str


load_dotenv()
client = Anthropic()

with open("eval/eval_seed_chunks.jsonl", "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f]

print(f"Loaded {len(chunks)} chunks")


def generate_question(chunk) -> str | None:
    response = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=100,
        messages=[
            {"role": "user", "content": f"Title: {chunk['title']}\n\n{chunk['text']}"}
        ],
        system=SYSTEM_PROMPT,
    )

    if response.stop_reason == "max_tokens":
        print(f"Cut off: {chunk['id']}")
        return None

    for block in response.content:
        if isinstance(block, TextBlock):
            try:
                question = Question.model_validate_json(block.text)
                return question.question
            except ValidationError as e:
                print(f"Invalid response: {block.text}\nError: {e}")
    return None

success_count = 0
with open("eval/eval_draft.jsonl", "w", encoding='utf-8') as f:
    for chunk in chunks:
        question = generate_question(chunk)
        if question:
            print(f"Title: {chunk['title']}, Generated question: {question}")
            f.write(json.dumps({"question": question, "source_id": chunk["id"]}, ensure_ascii=False) + "\n")
            success_count += 1
        else:
            print(f"Title: {chunk['title']}, No valid question generated")

print(f"Successfully generated questions for {success_count} chunks")