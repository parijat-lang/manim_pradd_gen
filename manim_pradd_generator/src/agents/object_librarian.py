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

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            tool_call = tool_calls[0]
            if tool_call.function.name == "catalog_objects":
                print("   Object Librarian LLM decided to call 'catalog_objects'.")
                function_args = json.loads(tool_call.function.arguments)
                return "catalog_objects", function_args
            else:
                raise ValueError(f"LLM called an unexpected tool: {tool_call.function.name}")
        else:
            llm_content = response_message.content
            print(f"LLM did not call a tool. Response content:\n{llm_content}")
            raise ValueError("LLM was expected to call 'catalog_objects' but did not.")

    except Exception as e:
        print(f"An error occurred during the Object Librarian agent run: {e}")
        raise
