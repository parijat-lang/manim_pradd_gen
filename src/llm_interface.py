import os
from openai import OpenAI, OpenAIError

# --- Configuration ---
# Users can override these defaults by setting environment variables.
# Default is for LM Studio, which exposes an OpenAI-compatible API.
# Note: The base_url should point to the server version, e.g., http://localhost:1234/v1
LLM_API_BASE_URL = os.getenv("LLM_API_BASE_URL", "http://localhost:1234/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-oss-20b")
LLM_API_KEY = os.getenv("LLM_API_KEY", "not-needed") # API key is not needed for LM Studio

# --- OpenAI Client Initialization ---
# The client is initialized once and can be reused.
try:
    client = OpenAI(base_url=LLM_API_BASE_URL, api_key=LLM_API_KEY)
except OpenAIError as e:
    print(f"Error initializing OpenAI client: {e}")
    client = None

def get_llm_tool_call(system_prompt: str, user_prompt: str) -> str:
    """
    Sends a prompt to a local, OpenAI-compatible LLM server and expects a
    JSON response for a tool call.

    This function uses the official `openai` library.

    Args:
        system_prompt: The system message that defines the agent's role and tools.
        user_prompt: The user's request or the task for the agent.

    Returns:
        A string containing the LLM's response, which should be a parsable JSON string
        representing a tool call's arguments.

    Raises:
        OpenAIError: If the API call fails or the client is not initialized.
        ValueError: If the response is empty.
    """
    if not client:
        raise OpenAIError("OpenAI client is not initialized. Check configuration.")

    print(f"Sending request to LLM ({LLM_MODEL}) at {LLM_API_BASE_URL}...")

    try:
        result = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.0,
            response_format={"type": "json_object"}
        )

        message_content = result.choices[0].message.content

        if not message_content:
            raise ValueError("LLM returned an empty message content.")

        return message_content.strip()

    except OpenAIError as e:
        print(f"An error occurred while communicating with the LLM API: {e}")
        print("Please ensure your local LLM server (e.g., LM Studio) is running and the environment variables are set correctly.")
        raise
    except (KeyError, IndexError) as e:
        print(f"Error parsing LLM response. Unexpected format. Error: {e}")
        print(f"Received result object: {result}")
        raise
