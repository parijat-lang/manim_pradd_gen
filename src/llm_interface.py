import os
import requests
import json

# --- Configuration ---
# Users can override these defaults by setting environment variables.
# This example is for Ollama's chat API.
# For LM Studio, the endpoint might be "http://localhost:1234/v1/chat/completions"
LLM_API_ENDPOINT = os.getenv("LLM_API_ENDPOINT", "http://localhost:11434/api/chat")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3")  # The model to use, e.g., "llama3", "mistral"

def get_llm_tool_call(system_prompt: str, user_prompt: str) -> str:
    """
    Sends a prompt to the local LLM and expects a response formatted as a tool call.

    This function is designed to work with local LLM servers like Ollama.
    It sends a system prompt and a user prompt, and the LLM is expected to respond
    with a JSON string that represents a function call with arguments.

    Args:
        system_prompt: The system message that defines the agent's role and tools.
        user_prompt: The user's request or the task for the agent.

    Returns:
        A string containing the LLM's response, which should be a parsable JSON string
        representing a tool call.

    Raises:
        requests.exceptions.RequestException: If the API call fails.
    """
    headers = {"Content-Type": "application/json"}

    # This payload is for Ollama. You may need to adjust it for other servers.
    # We request JSON output to make parsing the tool call reliable.
    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
        "format": "json",  # Request JSON output from Ollama
        "options": {
            "temperature": 0.0,  # For reproducibility
        }
    }

    print(f"Sending request to LLM ({LLM_MODEL})...")

    try:
        response = requests.post(LLM_API_ENDPOINT, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        # Ollama's response for a chat completion is nested.
        # The 'content' is a JSON string that we need to return.
        response_data = response.json()
        message_content_str = response_data.get("message", {}).get("content", "")

        if not message_content_str:
            raise ValueError("LLM returned an empty message content.")

        return message_content_str

    except requests.exceptions.RequestException as e:
        print(f"Error: Could not communicate with LLM API at {LLM_API_ENDPOINT}.")
        print("Please ensure your local LLM server (e.g., Ollama) is running and accessible.")
        raise
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from LLM response: {response.text}")
        raise
    except ValueError as e:
        print(f"Error: {e}")
        raise
