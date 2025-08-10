from .. import prompts

def run(context, narrative_outline):
    """
    Simulates the Story Planner agent.

    In a real implementation, this would use an LLM with the
    STORY_PLANNER_SYSTEM_PROMPT to generate the beats.
    """
    print("-> Running Story Planner Agent...")

    # Mocked LLM response
    mock_llm_response_params = {
        "fps": 60,
        "beats": [
            {
                "beat_id": "B-001",
                "scene_id": "S-001",
                "goal": "Introduce the concept of an integral as the area under a curve.",
                "summary": "Show a function graph, highlight the area under a segment.",
                "success_criteria": ["Viewer understands the area represents the integral."],
                "estimated_duration": 10
            },
            {
                "beat_id": "B-002",
                "scene_id": "S-001",
                "goal": "Introduce the derivative as the slope of the tangent line.",
                "summary": "Show the same graph, with a point and its tangent line. Move the point along the curve.",
                "success_criteria": ["Viewer understands the tangent's slope is the derivative."],
                "estimated_duration": 12
            },
            {
                "beat_id": "B-003",
                "scene_id": "S-001",
                "goal": "Connect the two concepts by showing the rate of change of the area.",
                "summary": "Animate the area function growing and simultaneously plot its derivative, showing it matches the original function.",
                "success_criteria": ["Viewer sees that the derivative of the area function is the original function."],
                "estimated_duration": 15
            }
        ]
    }

    print("   Story Planner decided to call 'write_beats'.")
    return "write_beats", mock_llm_response_params
