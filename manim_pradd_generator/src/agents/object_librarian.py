import json
from .. import prompts
from .. import utils

def run(llm_client, context, object_brief):
    """
    Runs the Object Librarian agent using an LLM.
    """
    print("-> Running Object Librarian Agent (LLM)...")

    system_prompt = prompts.OBJECT_LIBRARIAN_SYSTEM_PROMPT

    user_prompt = f"""
    Here is the current context for the project, including the beats map:
    {json.dumps(context, indent=2)}

    Your task is to define the canonical objects (mobject intents) required for the animation.
    Object Brief: {object_brief}

    Ensure you only use style tokens defined in the North Star/Glossary. Do not use raw values for colors, fonts, etc.
    Call the `catalog_objects` tool with the results.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    tools = [utils.get_openai_tool_schema("catalog_objects")]

    try:
        response = llm_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=tools,
            tool_choice="required",
        )

        return utils.parse_llm_response(
            response_message=response.choices[0].message,
            primary_tool_name="catalog_objects",
            primary_tool_arg_keys=["objects"]
        )

    except Exception as e:
        print(f"An error occurred during the Object Librarian agent run: {e}")
        raise
