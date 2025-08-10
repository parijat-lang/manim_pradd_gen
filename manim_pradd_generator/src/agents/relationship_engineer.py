import json
from .. import prompts
from .. import utils

def run(llm_client, context, dynamics_brief):
    """
    Runs the Relationship Engineer agent for a specific scene using an LLM.
    """
    scene_id = context['phase']['scene_id']
    print(f"-> Running Relationship Engineer Agent for scene {scene_id} (LLM)...")

    system_prompt = prompts.RELATIONSHIP_ENGINEER_SYSTEM_PROMPT

    user_prompt = f"""
    Here is the current context for the project:
    {json.dumps(context, indent=2)}

    Your task is to define the dynamic relationships (ValueTrackers, updaters, etc.)
    for all beats within scene `{scene_id}` only.

    Dynamics Brief: {dynamics_brief}

    Call the `define_relationships` tool with the results for this scene.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    tools = [utils.get_openai_tool_schema("define_relationships")]

    try:
        response = llm_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=tools,
            tool_choice="required",
        )

        return utils.parse_llm_response(
            response_message=response.choices[0].message,
            primary_tool_name="define_relationships",
            primary_tool_arg_keys=["relationships"],
            allow_empty_response=True
        )

    except Exception as e:
        print(f"An error occurred during the Relationship Engineer agent run for scene {scene_id}: {e}")
        raise
