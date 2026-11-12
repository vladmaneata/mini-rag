from anthropic import Anthropic
from anthropic.types import TextBlock
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()

response = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=128,
    messages=[{"role": "user", "content": "Hi, I'm Vlad, how are you?"}]
)

for message in response.content:
    if not isinstance(message, TextBlock):
        continue
    print(message.text)
    print(response.usage)

