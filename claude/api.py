import anthropic
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

CLIENT = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def request_message(input: str) -> str:
    response = CLIENT.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=[{"role": "user", "content": input}],
    )

    return response.model_dump_json()


input_text = input("Enter question:")

if len(input_text) > 0:
    response = request_message(input_text)
    print(response)
