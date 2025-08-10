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

    Call the `plan_geometry` tool with the results for this scene. If an object required
    by a beat in this scene is not defined in the object catalog, open a risk instead.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    tools = [
        utils.get_openai_tool_schema("plan_geometry"),
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
            primary_tool_name="plan_geometry",
            primary_tool_arg_keys=["frames"],
            allow_empty_response=True
        )

    except Exception as e:
        print(f"An error occurred during the Layout Designer agent run for scene {scene_id}: {e}")
        raise
