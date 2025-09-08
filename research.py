# Python
import json, logging, os
# Open AI
from openai import OpenAI
from openai.types.chat import ChatCompletionMessage
# Resonate HQ
from resonate import Context, Resonate

resonate = Resonate(log_level=logging.DEBUG)

aiclient = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# --- Tool Definitions ---
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "research",
            "description": "Research a given topic",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic to research"
                    }
                },
                "required": ["topic"]
            }
        }
    }
]

def prompt(ctx: Context, messages, has_tool_access: bool) -> ChatCompletionMessage:
    params = {
        "model": "gpt-5",
        "messages": messages
    }

    if has_tool_access:
        params["tools"] = TOOLS

    response = aiclient.chat.completions.create(**params)
    return response.choices[0].message

SYSTEM_PROMPT = """
You are a recursive research agent.

When given a broad or high-level topic, break it down into 2–3 semantically meaningful subtopics and call the "research" tool for each one individually.

Do not call the research tool if the topic is already well understood or deeply specific. Instead, summarize the topic directly instead of calling the tool.

Always respond with either:
1. A summary paragraph of the topic, or
2. One or more tool calls, each with a single subtopic to be researched.

Be concise and respond in plain English. Avoid repeating the topic verbatim in the subtopics.
"""

@resonate.register
def research(ctx: Context, topic: str, depth: int):

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Research {topic}"}
    ]

    while True:
        # Prompt the LLM
        # Only allow tool access if depth > 0
        message = yield ctx.lfc(prompt, messages, depth > 0)

        messages.append(message)

        # Handle parallel tool calls by recursively starting the deep research agent
        # and subsequently awaiting the results
        if message.tool_calls:
            handles = []
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                if tool_name == "research":
                    handle = yield ctx.rfi(research, tool_args["topic"], depth - 1)
                    handles.append((tool_call, handle))
            for (tool_call, handle) in handles:
                result = yield handle
                messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})
        else:
            return message.content

if __name__ == "__main__":
    # Run the research
    result = research.run("research.1", "What are distributed systems", 1)
    print(result)
