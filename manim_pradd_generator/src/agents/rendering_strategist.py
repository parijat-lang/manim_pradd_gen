import json
from .. import prompts
from .. import utils

def run(llm_client, context, render_constraints):
    """
    Runs the Rendering Strategist agent using an LLM.
    """
    print("-> Running Rendering Strategist Agent (LLM)...")

    system_prompt = prompts.RENDERING_STRATEGIST_SYSTEM_PROMPT

    user_prompt = f"""
    Here is the current context for the project, including the final timeline:
    {json.dumps(context, indent=2)}

    Your task is to decide the render quality, renderer, sections, and previews.

    Render Constraints: {render_constraints}

    Call the `set_render_strategy` tool with the results.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    tools = [utils.get_openai_tool_schema("set_render_strategy")]

    try:
        response = llm_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=tools,
            tool_choice={"type": "function", "function": {"name": "set_render_strategy"}},
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            tool_call = tool_calls[0]
            if tool_call.function.name == "set_render_strategy":
                print("   Rendering Strategist LLM decided to call 'set_render_strategy'.")
                function_args = json.loads(tool_call.function.arguments)
                return "set_render_strategy", function_args
            else:
                raise ValueError(f"LLM called an unexpected tool: {tool_call.function.name}")
        else:
            llm_content = response_message.content
            print(f"LLM did not call a tool. Response content:\n{llm_content}")
            raise ValueError("LLM was expected to call 'set_render_strategy' but did not.")

    except Exception as e:
        print(f"An error occurred during the Rendering Strategist agent run: {e}")
        raise
