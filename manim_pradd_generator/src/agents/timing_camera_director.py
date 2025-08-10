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

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            tool_call = tool_calls[0]
            if tool_call.function.name == "compose_timeline":
                print(f"   Timing & Camera Director LLM for scene {scene_id} decided to call 'compose_timeline'.")
                function_args = json.loads(tool_call.function.arguments)
                return "compose_timeline", function_args
            else:
                raise ValueError(f"LLM called an unexpected tool: {tool_call.function.name}")
        else:
            llm_content = response_message.content
            print(f"LLM did not call a tool. Response content:\n{llm_content}")
            raise ValueError("LLM was expected to call 'compose_timeline' but did not.")

    except Exception as e:
        print(f"An error occurred during the Timing & Camera Director agent run for scene {scene_id}: {e}")
        raise
