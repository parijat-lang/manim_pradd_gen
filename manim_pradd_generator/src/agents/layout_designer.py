import json
from .. import prompts
from .. import utils

def run(llm_client, context, layout_goals):
    """
    Runs the Layout Designer agent for a specific scene using an LLM.
    """
    scene_id = context['phase']['scene_id']
    print(f"-> Running Layout Designer Agent for scene {scene_id} (LLM)...")

    system_prompt = prompts.LAYOUT_DESIGNER_SYSTEM_PROMPT

    user_prompt = f"""
    Here is the current context for the project:
    {json.dumps(context, indent=2)}

    Your task is to plan the geometry (positions, scale, rotation, z-index, and groups)
    for all objects within scene `{scene_id}` only.

    Layout Goals: {layout_goals}

    Call the `plan_geometry` tool with the results for this scene.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    # This agent can either plan geometry or open a risk if an object is missing.
    tools = [
        utils.get_openai_tool_schema("plan_geometry"),
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
            print(f"   Layout Designer LLM for scene {scene_id} decided to call '{tool_name}'.")
            function_args = json.loads(tool_call.function.arguments)
            return tool_name, function_args
        else:
            llm_content = response_message.content
            print(f"LLM did not call a tool. Response content:\n{llm_content}")
            raise ValueError("LLM was expected to call a tool but did not.")

    except Exception as e:
        print(f"An error occurred during the Layout Designer agent run for scene {scene_id}: {e}")
        raise
