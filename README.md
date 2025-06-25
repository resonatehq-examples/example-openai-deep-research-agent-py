# Deep Research Assistant

A distributed, recursive Deep Research Agent powered by Resonate and OpenAI. This example demonstrates how complex, distributed agentic applications can be implemented with simple, composable code.

## Use Case

Given a topic, the Deep Research Agent decomposes the topic into subtopics, and recursively invokes itself (via OpenAI parallel tool calling) on each subtopic.

---

## Installation & Usage

This project uses uv, a popular Python package manager and virtual environment tool. To run this project you need an [OpenAI API Key](https://platform.openai.com)

### 1. Clone the repository

```
git clone https://github.com/resonatehq-examples/openai-deep-research-agent-py
cd openai-deep-research-agent-py
```

### 2. Set your OpenAI API Key

```
export OPENAI_API_KEY="sk-..."
```

### 3. Run the Agent

```
uv run research.py
```

## Trouble Shooting

The Deep Research Agent depends on OpenAI and the OpenAI Python SDK. If you are having trouble, verify that your OpenAI credentials are configured correctly and the model is accessible by running the following command in the project's directory:

```
uv run python -c 'import os; from openai import OpenAI; client = OpenAI(api_key=os.environ["OPENAI_API_KEY"]); print(client.chat.completions.create(model="gpt-4.1", messages=[{"role": "user", "content": "knock knock"}]))'
```

If everything is configured correctly, you will see a response from OpenAI such as:

```
ChatCompletion(choices=[message=ChatCompletionMessage(content='Who’s there?', ...), ...], ...)
```

If you are still having trouble, please open an issue on the [GitHub repository](https://github.com/resonatehq-examples/openai-deep-research-agent-py/issues).
