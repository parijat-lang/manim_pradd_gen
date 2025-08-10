import json
from .. import prompts
from .. import utils

def run(llm_client, context, timing_brief):
    """
    Runs the Timing & Camera Director agent for a specific scene using an LLM.
    """
    scene_id = context['phase']['scene_id']
    print(f"-> Running Timing & Camera Director Agent for scene {scene_id} (LLM)...")

    system_prompt = prompts.TIMING_CAMERA_DIRECTOR_SYSTEM_PROMPT

    user_prompt = f"""
    Here is the current context for the project:
    {json.dumps(context, indent=2)}

    Your task is to compose the timeline and define camera movements for scene `{scene_id}` only.
    You must create a timeline with absolute t_start and t_end values for all animations and relationships in this scene.

    Timing Brief: {timing_brief}

    Call the `compose_timeline` tool with the results for this scene.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    tools = [utils.get_openai_tool_schema("compose_timeline")]

    try:
        response = llm_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=tools,
            tool_choice="required",
        )

        return utils.parse_llm_response(
            response_message=response.choices[0].message,
            primary_tool_name="compose_timeline",
            primary_tool_arg_keys=["timeline", "camera"]
        )

    except Exception as e:
        print(f"An error occurred during the Timing & Camera Director agent run for scene {scene_id}: {e}")
        raise
