import os
import requests
import json

# --- Configuration ---
# Users can override these defaults by setting environment variables.
# Default is now for LM Studio, as requested.
# For Ollama, the endpoint is typically "http://localhost:11434/api/chat"
LLM_API_ENDPOINT = os.getenv("LLM_API_ENDPOINT", "http://localhost:1234/v1/chat/completions")
# For LM Studio, the model name is often the file name or a name set in the UI.
# For the new OpenAI model, this might be 'gpt-oss-20b'.
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-oss-20b")

def get_llm_tool_call(system_prompt: str, user_prompt: str) -> str:
    """
    Sends a prompt to the local LLM and expects a response formatted as a tool call.

    This function is designed to work with OpenAI-compatible servers (like LM Studio)
    and falls back to handle Ollama's native format, making it flexible.

    Args:
        system_prompt: The system message that defines the agent's role and tools.
        user_prompt: The user's request or the task for the agent.

    Returns:
        A string containing the LLM's response, which should be a parsable JSON string
        representing a tool call's arguments.

    Raises:
        requests.exceptions.RequestException: If the API call fails.
        ValueError: If the response format is unrecognized or empty.
    """
    # For OpenAI-compatible endpoints (like LM Studio), the API key is often not needed.
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('LLM_API_KEY', 'not-needed')}"
    }

    # Standard OpenAI-compatible payload
    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.0,
        "response_format": {"type": "json_object"} # Use standard JSON mode
    }

    print(f"Sending request to LLM ({LLM_MODEL}) at {LLM_API_ENDPOINT}...")

    try:
        response = requests.post(LLM_API_ENDPOINT, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        response_data = response.json()

        # Adaptive response parsing
        message_content_str = ""
        # 1. Try OpenAI / LM Studio format
        if "choices" in response_data and response_data["choices"]:
            message = response_data["choices"][0].get("message", {})
            if message.get("content"):
                message_content_str = message["content"]

        # 2. Fallback to Ollama's native format
        elif "message" in response_data and response_data["message"].get("content"):
            message_content_str = response_data["message"]["content"]

        if not message_content_str:
            raise ValueError("LLM response was empty or in an unrecognized format.")

        return message_content_str.strip()

    except requests.exceptions.RequestException as e:
        print(f"Error: Could not communicate with LLM API at {LLM_API_ENDPOINT}.")
        print("Please ensure your local LLM server (e.g., LM Studio, Ollama) is running and the endpoint is correct.")
        raise
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        print(f"Error: Failed to parse LLM response. Error: {e}")
        print(f"Received response: {response.text}")
        raise
    except ValueError as e:
        print(f"Error: {e}")
        raise
