from typing import Literal

from anthropic import Anthropic
from anthropic.types import TextBlock
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError


class Answer(BaseModel):
    language: Literal["en", "ro"]
    answer: str


load_dotenv()
client = Anthropic()

response = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=128,
    messages=[{"role": "user", "content": "Ce este FastAPI?"}],
    system="Reply only with a JSON object with two keys: 'language' (ro or en) and 'answer' (one sentence, max 30 words). No other text.",
)

if response.stop_reason == "max_tokens":
    raise SystemExit(f"Response cut off at max_tokens={response.usage.output_tokens}")

for block in response.content:
    if not isinstance(block, TextBlock):
        continue
    try:
        result = Answer.model_validate_json(block.text)
        print(f"Language: {result.language}")
        print(f"Answer: {result.answer}")
    except ValidationError as e:
        print(f"Invalid response: {block.text}\nError: {e}")
