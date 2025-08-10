from .. import prompts
from .. import tool_definitions

def run(context, checks_policy, strict=False):
    """
    Simulates the Consistency Critic agent.

    This agent doesn't use an LLM. It directly calls the validation tool.
    """
    print(f"-> Running Consistency Critic Agent (strict={strict})...")

    # The Consistency Critic directly calls the validation tool.
    validation_result = tool_definitions.validate_corpus(context, strict=strict)

    print(f"   Consistency Critic finished validation with status: {validation_result['status']}.")
    # The orchestrator will need to inspect this result.
    return "validate_corpus", {"strict": strict}, validation_result
