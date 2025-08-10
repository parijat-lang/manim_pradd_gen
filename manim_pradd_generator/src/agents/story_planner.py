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
    Call the `write_beats` tool with the results.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    # This agent can either write beats or open a risk if the input is ambiguous.
    tools = [
        utils.get_openai_tool_schema("write_beats"),
        utils.get_openai_tool_schema("open_risk")
    ]

    try:
        response = llm_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=tools,
            tool_choice="auto", # Let the model choose
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            tool_call = tool_calls[0]
            tool_name = tool_call.function.name
            print(f"   Story Planner LLM decided to call '{tool_name}'.")
            function_args = json.loads(tool_call.function.arguments)
            return tool_name, function_args
        else:
            llm_content = response_message.content
            print(f"LLM did not call a tool. Response content:\n{llm_content}")
            raise ValueError("LLM was expected to call a tool but did not.")

    except Exception as e:
        print(f"An error occurred during the Story Planner agent run: {e}")
        raise
