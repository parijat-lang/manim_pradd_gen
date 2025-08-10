import json
from .. import prompts
from .. import utils

def run(llm_client, context, creative_brief, constraints_hint=""):
    """
    Runs the Creative Director agent using an LLM.
    """
    print("-> Running Creative Director Agent (LLM)...")

    system_prompt = prompts.CREATIVE_DIRECTOR_SYSTEM_PROMPT

    user_prompt = f"""
    Here is the current context for the project:
    {json.dumps(context, indent=2)}

    Your task is to define the creative direction based on this brief.
    Creative Brief: {creative_brief}
    Constraints Hint: {constraints_hint}

    Please call the `register_north_star` tool with the results, or `open_risk` if the brief is too ambiguous.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    tools = [
        utils.get_openai_tool_schema("register_north_star"),
        utils.get_openai_tool_schema("open_risk")
    ]

    try:
        response = llm_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

        return utils.parse_llm_response(
            response_message=response.choices[0].message,
            primary_tool_name="register_north_star",
            primary_tool_arg_keys=["purpose", "audience", "tone", "style_tokens"]
        )

    except Exception as e:
        print(f"An error occurred during the Creative Director agent run: {e}")
        raise
