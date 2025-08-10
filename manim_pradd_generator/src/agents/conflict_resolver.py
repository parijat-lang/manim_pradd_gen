import json
from .. import prompts
from .. import utils

def run(llm_client, context, conflicts):
    """
    Runs the Conflict Resolver agent using an LLM.
    """
    print("-> Running Conflict Resolver Agent (LLM)...")

    system_prompt = prompts.CONFLICT_RESOLVER_SYSTEM_PROMPT

    user_prompt = f"""
    Here is the current context for the project:
    {json.dumps(context, indent=2)}

    The validation process has failed with the following errors:
    {json.dumps(conflicts, indent=2)}

    Your task is to analyze these conflicts and propose the smallest possible patches
    to resolve them. Provide a clear rationale for your decision.

    Call the `commit_decision` tool with the summary and patches.
    If a resolution is not possible, call the `open_risk` tool instead.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    # This agent can decide between two tools
    tools = [
        utils.get_openai_tool_schema("commit_decision"),
        utils.get_openai_tool_schema("open_risk")
    ]

    try:
        response = llm_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=tools,
            tool_choice="auto", # Let the model choose between committing a fix or opening a risk
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            tool_call = tool_calls[0]
            tool_name = tool_call.function.name
            print(f"   Conflict Resolver LLM decided to call '{tool_name}'.")
            function_args = json.loads(tool_call.function.arguments)
            return tool_name, function_args
        else:
            llm_content = response_message.content
            print(f"LLM did not call a tool. Response content:\n{llm_content}")
            raise ValueError("LLM was expected to call a tool but did not.")

    except Exception as e:
        print(f"An error occurred during the Conflict Resolver agent run: {e}")
        raise
