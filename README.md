# AI Agent

A small command-line AI coding agent written in Python. You give it a task in plain English, and it uses a set of tools to explore, read, run and edit code until it has an answer.

Built as part of the [Boot.dev](https://www.boot.dev) Backend Developer track ("Build an AI Agent" course).

## How it works

The agent talks to an LLM through [OpenRouter](https://openrouter.ai) using the OpenAI-compatible Chat Completions API with **function calling**.

It runs a feedback loop (up to 20 iterations):

1. Send the conversation history and the available tools to the model.
2. If the model requests tool calls, execute them and append each result as a `tool` message.
3. Repeat until the model replies without tool calls. That reply is the final answer.

```
User:      "Explain how the calculator renders the result"
Assistant: calls get_files_info
Tool:      <directory listing>
Assistant: calls get_file_content
Tool:      <file contents>
Assistant: "The calculator formats the result as JSON in pkg/render.py..."
```

## Tools

| Tool | Description |
|------|-------------|
| `get_files_info` | List files in a directory with their size and whether they are directories |
| `get_file_content` | Read a file (truncated at 10,000 characters) |
| `run_python_file` | Run a `.py` file with optional arguments (30 s timeout) and return stdout/stderr |
| `write_file` | Create or overwrite a file |

For safety, every tool is restricted to a fixed working directory (`./calculator`). The working directory is injected by the program, not chosen by the model, and any path that resolves outside it is rejected.

## Project structure

```
.
├── main.py              # CLI entry point and agent loop
├── call_function.py     # Dispatches tool calls to Python functions
├── prompts.py           # System prompt
├── config.py            # Settings (MAX_CHARS)
├── functions/           # Tool implementations and their JSON schemas
└── calculator/          # Sample project the agent works on
```

## Getting started

Requirements: Python 3.14+ and [uv](https://docs.astral.sh/uv/).

1. Clone the repo:

   ```bash
   git clone https://github.com/tortilicious/ai-agent.git
   cd ai-agent
   ```

2. Create a `.env` file with your OpenRouter API key:

   ```
   OPENROUTER_API_KEY=your_key_here
   ```

3. Run the agent:

   ```bash
   uv run main.py "Explain how the calculator renders the result to the console"
   ```

   Add `--verbose` to see the token usage, the tool call arguments and the tool results:

   ```bash
   uv run main.py "Fix the bug in the calculator" --verbose
   ```

## Warning

This agent can write files and execute Python code. It is a learning project, so only run it against code you are happy for it to modify.
