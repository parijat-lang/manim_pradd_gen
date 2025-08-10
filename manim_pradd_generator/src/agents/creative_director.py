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

    Please call the `register_north_star` tool with the results.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    # This agent is only allowed to call one tool
    tools = [utils.get_openai_tool_schema("register_north_star")]

    try:
        response = llm_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=tools,
            tool_choice={"type": "function", "function": {"name": "register_north_star"}},
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            tool_call = tool_calls[0]
            if tool_call.function.name == "register_north_star":
                print("   Creative Director LLM decided to call 'register_north_star'.")
                function_args = json.loads(tool_call.function.arguments)
                return "register_north_star", function_args
            else:
                raise ValueError(f"LLM called an unexpected tool: {tool_call.function.name}")
        else:
            # If the model doesn't call a tool, maybe it just returns content.
            # For this agent, we strictly expect a tool call.
            llm_content = response_message.content
            print(f"LLM did not call a tool. Response content:\n{llm_content}")
            raise ValueError("LLM was expected to call 'register_north_star' but did not.")

    except Exception as e:
        print(f"An error occurred during the Creative Director agent run: {e}")
        raise
