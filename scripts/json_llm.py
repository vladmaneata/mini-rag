import json

from anthropic import Anthropic
from anthropic.types import TextBlock
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()

response = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=128,
    messages=[{"role": "user", "content": "Ce este FastAPI?"}],
    system="Reply only with a JSON object with two keys: 'language' (the language of the question) and 'answer' (a short answer). No other text.",
)

if response.stop_reason == "max_tokens":
    raise SystemExit(f"Response cut off at max_tokens={response.usage.output_tokens}")

for block in response.content:
    if not isinstance(block, TextBlock):
        continue
    try:
        data = json.loads(block.text)
        print(f"Language: {data['language']}")
        print(f"Answer: {data['answer']}")
    except json.JSONDecodeError:
        print(f"Failed to parse JSON: {block.text}")
