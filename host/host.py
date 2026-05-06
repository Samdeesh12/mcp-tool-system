# host/host.py

from groq import Groq
import os
import json
from dotenv import load_dotenv

load_dotenv()

from server.server import (
    get_weather,
    add_expense,
    list_expenses,
    summarize_expenses,
    analyze_sentiment,
    convert_currency,
    get_news
)

# ─── TOOL MANIFEST ────────────────────────────────────────────────────────────

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for any city in the world.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name e.g. Mumbai"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_expense",
            "description": "Add a new expense entry to the database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date":        {"type": "string", "description": "Date YYYY-MM-DD"},
                    "amount":      {"type": "number", "description": "Amount spent"},
                    "category":    {"type": "string", "description": "e.g. Food, Transport"},
                    "subcategory": {"type": "string", "description": "Optional subcategory"},
                    "note":        {"type": "string", "description": "Optional note"}
                },
                "required": ["date", "amount", "category"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_expenses",
            "description": "List all expenses between two dates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_date": {"type": "string", "description": "Start date YYYY-MM-DD"},
                    "end_date":   {"type": "string", "description": "End date YYYY-MM-DD"}
                },
                "required": ["start_date", "end_date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "summarize_expenses",
            "description": "Show total spending grouped by category between two dates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_date": {"type": "string", "description": "Start date YYYY-MM-DD"},
                    "end_date":   {"type": "string", "description": "End date YYYY-MM-DD"},
                    "category":   {"type": "string", "description": "Optional category filter"}
                },
                "required": ["start_date", "end_date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_sentiment",
            "description": "Analyze whether a piece of text is POSITIVE or NEGATIVE.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to analyze"}
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "convert_currency",
            "description": "Convert an amount from one currency to another using live rates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount":        {"type": "number", "description": "Amount to convert"},
                    "from_currency": {"type": "string", "description": "Source currency e.g. USD"},
                    "to_currency":   {"type": "string", "description": "Target currency e.g. INR"}
                },
                "required": ["amount", "from_currency", "to_currency"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_news",
            "description": "Get the latest 5 news headlines for any topic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "Topic to search news for"}
                },
                "required": ["topic"]
            }
        }
    }
]

# ─── TOOL EXECUTOR ────────────────────────────────────────────────────────────

def execute_tool(tool_name: str, tool_input: dict):
    """Run the tool the AI chose and return the result."""
    print(f"\n[Tool called: {tool_name}]")
    print(f"[Arguments: {tool_input}]")

    if tool_name == "get_weather":
        return get_weather(**tool_input)
    elif tool_name == "add_expense":
        return add_expense(**tool_input)
    elif tool_name == "list_expenses":
        return list_expenses(**tool_input)
    elif tool_name == "summarize_expenses":
        return summarize_expenses(**tool_input)
    elif tool_name == "analyze_sentiment":
        return analyze_sentiment(**tool_input)
    elif tool_name == "convert_currency":
        return convert_currency(**tool_input)
    elif tool_name == "get_news":
        return get_news(**tool_input)
    else:
        return {"error": f"Unknown tool: {tool_name}"}

# ─── MAIN CHAT FUNCTION ───────────────────────────────────────────────────────

def chat(user_message: str, conversation_history: list) -> str:
    """
    Send a message to Groq AI, let it decide which tool to use,
    run that tool, and return the final answer.
    """
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # Add user message to history
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    # Keep looping until AI gives a final text answer
    while True:
        response = client.chat.completions.create(
          model="openai/gpt-oss-120b",
            max_tokens=1024,
            tools=TOOLS,
            tool_choice="auto",  # AI decides whether to use a tool or not
            messages=[
                {
                    "role": "system",
                    "content": """You are a helpful AI assistant with access to several tools.
When a user asks something, use the appropriate tool to get real data.
Always give a friendly, clear, conversational answer based on the tool results.
Today's date is 2025-05-06."""
                }
            ] + conversation_history
        )

        message = response.choices[0].message

        # CASE 1: AI wants to use a tool
        if message.tool_calls:
            tool_call    = message.tool_calls[0]
            tool_name    = tool_call.function.name
            tool_input   = json.loads(tool_call.function.arguments)
            tool_call_id = tool_call.id

            # Run the tool
            tool_result = execute_tool(tool_name, tool_input)

            # Add AI's tool request to history
            conversation_history.append({
                "role": "assistant",
                "content": None,
                "tool_calls": message.tool_calls
            })

            # Add tool result to history so AI can read it
            conversation_history.append({
                "role": "tool",
                "tool_call_id": tool_call_id,
                "content": json.dumps(tool_result)
            })

            # Loop back — AI will now read the result and respond

        # CASE 2: AI gives a final text answer
        else:
            final_answer = message.content

            conversation_history.append({
                "role": "assistant",
                "content": final_answer
            })

            return final_answer