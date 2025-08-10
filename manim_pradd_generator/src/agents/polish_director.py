import json
from .. import prompts
from .. import utils

def run(llm_client, context, polish_brief):
    """
    Runs the Polish Director agent using an LLM.
    """
    print("-> Running Polish Director Agent (LLM)...")

    system_prompt = prompts.POLISH_DIRECTOR_SYSTEM_PROMPT

    user_prompt = f"""
    Here is the current context for the project, including the merged timeline:
    {json.dumps(context, indent=2)}

    Your task is to add finishing touches, micro-effects, and accessibility notes to the project.

    Polish Brief: {polish_brief}

    Call the `add_polish` tool with the results.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    tools = [utils.get_openai_tool_schema("add_polish")]

    try:
        response = llm_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=tools,
            tool_choice={"type": "function", "function": {"name": "add_polish"}},
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            tool_call = tool_calls[0]
            if tool_call.function.name == "add_polish":
                print("   Polish Director LLM decided to call 'add_polish'.")
                function_args = json.loads(tool_call.function.arguments)
                return "add_polish", function_args
            else:
                raise ValueError(f"LLM called an unexpected tool: {tool_call.function.name}")
        else:
            llm_content = response_message.content
            print(f"LLM did not call a tool. Response content:\n{llm_content}")
            raise ValueError("LLM was expected to call 'add_polish' but did not.")

    except Exception as e:
        print(f"An error occurred during the Polish Director agent run: {e}")
        raise
