from .. import prompts

def run(context, creative_brief, constraints_hint):
    """
    Simulates the Creative Director agent.

    In a real implementation, this function would use an LLM with the
    CREATIVE_DIRECTOR_SYSTEM_PROMPT to generate the parameters for the tool call
    based on the creative_brief and constraints_hint.
    """
    print("-> Running Creative Director Agent...")

    # This is a mocked response that would normally come from an LLM.
    mock_llm_response_params = {
        "purpose": "To visually explain the fundamental theorem of calculus.",
        "audience": "University students in introductory calculus courses.",
        "tone": "Authoritative, clear, and insightful.",
        "style_tokens": {
            "color.brand.primary": "#58C4DD",
            "color.brand.secondary": "#F0AD4E",
            "color.background.main": "#222222",
            "color.text.light": "#EAEAEA",
            "color.text.dark": "#333333",
            "font.main": "Helvetica",
            "font.math": "Computer Modern",
            "stroke_width.thin": 2,
            "stroke_width.medium": 4,
            "spacing.unit": 0.25,
        },
        "motion_grammar": [
            "Use smooth, continuous transformations.",
            "Emphasize key moments with slow-motion or pauses.",
            "Avoid jarring cuts or excessive motion.",
        ],
        "constraints": [
            "ManimCE v0.19.0",
            "2D scene",
            "Target 1080p resolution at 60fps",
        ],
        "references": [
            "Inspired by the visual style of 3Blue1Brown."
        ]
    }

    # The 'context' is not part of the LLM response, but is required by the tool.
    # The orchestrator will add it to the parameters before calling the tool.
    print("   Creative Director decided to call 'register_north_star'.")
    return "register_north_star", mock_llm_response_params
