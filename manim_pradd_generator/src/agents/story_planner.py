import json
from .. import prompts
from .. import utils

def run(llm_client, context, narrative_outline):
    """
    Runs the Story Planner agent using an LLM.
    """
    print("-> Running Story Planner Agent (LLM)...")

    system_prompt = prompts.STORY_PLANNER_SYSTEM_PROMPT

    user_prompt = f"""
    Here is the current context for the project:
    {json.dumps(context, indent=2)}

    Your task is to map the following narrative outline into a series of beats and scenes.
    Narrative Outline: {narrative_outline}

    Please adhere to the North Star and target runtime defined in the context.
    Call the `write_beats` tool with the results, or `open_risk` if the outline is ambiguous.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    tools = [
        utils.get_openai_tool_schema("write_beats"),
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
            primary_tool_name="write_beats",
            primary_tool_arg_keys=["fps", "beats"]
        )

    except Exception as e:
        print(f"An error occurred during the Story Planner agent run: {e}")
        raise
