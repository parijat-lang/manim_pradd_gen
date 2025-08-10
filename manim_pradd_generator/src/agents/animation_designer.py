from .. import prompts

def run(context, animation_brief):
    """
    Simulates the Animation Designer agent for a specific scene.

    In a real implementation, this would use an LLM with the
    ANIMATION_DESIGNER_SYSTEM_PROMPT.
    """
    scene_id = context['phase']['scene_id']
    print(f"-> Running Animation Designer Agent for scene {scene_id}...")

    # Mocked LLM response for S-001
    if scene_id == "S-001":
        mock_llm_response_params = {
            "animations": [
                # Beat 1: Introduce integral
                {"anim_id": "A-0001", "beat_id": "B-001", "kind": "Create", "targets": ["O-0001"], "params": {"run_time": 1}},
                {"anim_id": "A-0002", "beat_id": "B-001", "kind": "Create", "targets": ["O-0002"], "params": {"run_time": 2}},
                {"anim_id": "A-0003", "beat_id": "B-001", "kind": "FadeIn", "targets": ["O-0003"], "params": {"run_time": 2}},

                # Beat 2: Introduce derivative
                {"anim_id": "A-0004", "beat_id": "B-002", "kind": "Create", "targets": ["O-0004"], "params": {"run_time": 2, "rate_func": "smooth"}},
                # Imagine an animation where the tangent line moves along the curve
                {"anim_id": "A-0005", "beat_id": "B-002", "kind": "Custom", "targets": ["O-0004"], "params": {"run_time": 5, "notes": "Move tangent point from x=3 to x=7"}},

                # Beat 3: Connect them
                {"anim_id": "A-0006", "beat_id": "B-003", "kind": "Create", "targets": ["O-0005"], "params": {"run_time": 5, "notes": "Draw derivative of area function"}},
                {"anim_id": "A-0007", "beat_id": "B-003", "kind": "Indicate", "targets": ["O-0002", "O-0005"], "params": {"run_time": 3, "color": "color.brand.secondary"}}
            ]
        }
    else:
        mock_llm_response_params = {"animations": []}

    print(f"   Animation Designer for scene {scene_id} decided to call 'design_animations'.")
    return "design_animations", mock_llm_response_params
