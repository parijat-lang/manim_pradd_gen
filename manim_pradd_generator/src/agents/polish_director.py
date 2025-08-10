import json
from .. import prompts
from .. import utils

def run(llm_client, context, polish_brief):
    """
    Runs the Polish Director agent using an LLM.
    """
    print("-> Running Polish Director Agent (LLM)...")

    system_prompt = prompts.POLISH_DIRECTOR_SYSTEM_PROMPT

    user_prompt = f"""
    Here is the current context for the project, including the merged timeline:
    {json.dumps(context, indent=2)}

    Your task is to add finishing touches, micro-effects, and accessibility notes to the project.

    Polish Brief: {polish_brief}

    Call the `add_polish` tool with the results.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    tools = [utils.get_openai_tool_schema("add_polish")]

    try:
        response = llm_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=tools,
            tool_choice="required",
        )

        return utils.parse_llm_response(
            response_message=response.choices[0].message,
            primary_tool_name="add_polish",
            primary_tool_arg_keys=["polish"]
        )

    except Exception as e:
        print(f"An error occurred during the Polish Director agent run: {e}")
        raise
