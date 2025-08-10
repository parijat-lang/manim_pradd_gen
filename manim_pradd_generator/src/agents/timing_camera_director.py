from .. import prompts

def run(context, timing_brief):
    """
    Simulates the Timing & Camera Director agent for a specific scene.

    In a real implementation, this would use an LLM with the
    TIMING_CAMERA_DIRECTOR_SYSTEM_PROMPT.
    """
    scene_id = context['phase']['scene_id']
    print(f"-> Running Timing & Camera Director Agent for scene {scene_id}...")

    # Mocked LLM response for S-001
    if scene_id == "S-001":
        mock_llm_response_params = {
            "timeline": [
                {
                    "scene_id": "S-001",
                    "entries": [
                        # Beat 1
                        {"t_start": 0.0, "t_end": 1.0, "mode": "serial", "items": ["A-0001"]},
                        {"t_start": 1.0, "t_end": 3.0, "mode": "serial", "items": ["A-0002"]},
                        {"t_start": 3.0, "t_end": 5.0, "mode": "parallel", "items": ["A-0003", "C-0001"]},
                        # Beat 2
                        {"t_start": 5.0, "t_end": 7.0, "mode": "serial", "items": ["A-0004"]},
                        {"t_start": 7.0, "t_end": 12.0, "mode": "parallel", "items": ["A-0005", "R-0001"]},
                        # Beat 3
                        {"t_start": 12.0, "t_end": 17.0, "mode": "parallel", "items": ["A-0006", "R-0002"]},
                        {"t_start": 17.0, "t_end": 20.0, "mode": "serial", "items": ["A-0007"]},
                    ]
                }
            ],
            "camera": [
                {
                    "cam_id": "C-0001",
                    "scene_id": "S-001",
                    "action": "frame_move",
                    "params": {"x": 1, "y": 0.5},
                    "t_start": 3.5,
                    "t_end": 4.5
                }
            ]
        }
    else:
        mock_llm_response_params = {"timeline": [], "camera": []}

    print(f"   Timing & Camera Director for scene {scene_id} decided to call 'compose_timeline'.")
    return "compose_timeline", mock_llm_response_params
