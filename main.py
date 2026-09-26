import argparse
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from call_function import available_functions, call_function
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if not api_key:
    raise RuntimeError("Couldnt find any API KEY in .env")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", )
args = parser.parse_args()
user_prompt: str = args.user_prompt

messages: list[dict[str, str]] = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

for _ in range(20):

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
        temperature=0,
    )
    query_tokens = f"Prompt tokens: {response.usage.prompt_tokens}"
    response_tokens = f"Response tokens: {response.usage.completion_tokens}"

    if args.verbose:
        print(f"User prompt: {user_prompt}")
        print(query_tokens)
        print(response_tokens)

    message = response.choices[0].message
    messages.append(message)

    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, args.verbose)
            messages.append(result_message)

            if not result_message["content"]:
                raise Exception(f"Empty result from function {tool_call.function.name}")

            if args.verbose:
                print(f"-> {result_message['content']}")
    else:
        print(message.content)
        break
else:
    print("Maximum number of iterations is reached")
    exit(code=1)