import json
import copy
from pathlib import Path

from . import tool_definitions
from .agents import (
    creative_director,
    story_planner,
    object_librarian,
    layout_designer,
    animation_designer,
    relationship_engineer,
    timing_camera_director,
    consistency_critic,
    polish_director,
    rendering_strategist,
    conflict_resolver,
)

# --- Initial Context ---
def get_initial_context():
    return {
        "project": {
            "project_id": "proj_calculus_intro_001",
            "title": "Introduction to the Fundamental Theorem of Calculus",
            "target_runtime_s": 180,
            "fps": 60,
            "version": "0.1.0"
        },
        "phase": {"name": "kickoff", "attempt": 1, "scene_id": None},
        "corpus_snapshot": {
            "north_star": {}, "beats": {}, "objects": {}, "geometry": {},
            "animations": {}, "relationships": {}, "timeline": {}, "camera": {},
            "polish": {}, "rendering": {}, "glossary": {}, "risks": {}, "decisions": []
        },
        "ids": {
            "prefixes": {"beat": "B-", "scene": "S-", "object": "O-", "anim": "A-", "rel": "R-", "cam": "C-"},
            "counters": {"beat": 0, "scene": 0, "object": 0, "anim": 0, "rel": 0, "cam": 0}
        },
        "policy": {
            "style_token_policy": "no raw colors outside North Star",
            "overlap_policy": "same-target overlaps must be parallel-grouped",
            "complexity_budget": {"max_parallel_per_beat": 6}
        },
        "manim_profile": {
            "manim_version": "0.19.0", "flavor": "ManimCE",
            "modes": ["cairo", "2d"],
            "primitives": {
                "animations": ["Create", "Write", "FadeIn", "FadeOut", "Transform"],
                "composition": ["AnimationGroup", "LaggedStart", "Succession"],
                "dynamics": ["ValueTracker", "always_redraw", "add_updater"],
                "camera_actions": ["frame_move", "frame_width"]
            }
        }
    }

# --- Orchestrator Logic ---

class Orchestrator:
    def __init__(self, initial_context):
        self.context = initial_context
        self.tools = tool_definitions.ALL_TOOLS

    def _update_corpus_snapshot(self):
        """Reloads all corpus files into the context snapshot."""
        print("...Updating corpus snapshot...")
        for filename in self.context["corpus_snapshot"].keys():
            # decisions is an array, not a file
            if filename == 'decisions': continue

            filepath = tool_definitions.CORPUS_DIR / f"{filename}.json"
            if filepath.exists():
                with open(filepath, 'r') as f:
                    self.context["corpus_snapshot"][filename] = json.load(f)
            else: # Handle .md files
                filepath = tool_definitions.CORPUS_DIR / f"{filename}.md"
                if filepath.exists():
                     with open(filepath, 'r') as f:
                        self.context["corpus_snapshot"][filename] = {"content": f.read()}

    def _execute_tool_call(self, tool_name, params):
        """Executes a tool and updates the context."""
        if tool_name not in self.tools:
            raise ValueError(f"Unknown tool: {tool_name}")

        # Add context to the parameters before calling the tool
        params_with_context = params.copy()
        params_with_context["context"] = self.context

        result = self.tools[tool_name](**params_with_context)
        print(f"   Tool '{tool_name}' executed, result: {result}")

        # After execution, update the corpus snapshot to reflect changes
        self._update_corpus_snapshot()
        return result

    def run_phase(self, phase_name, agent_runner, brief=None, is_sharded=False):
        """Runs a single phase of the pipeline."""
        self.context["phase"]["name"] = phase_name
        self.context["phase"]["attempt"] = 1

        if is_sharded:
            # --- Sharded Phase ---
            # Get all unique scene IDs from the beats file
            scene_ids = sorted(list(set(b['scene_id'] for b in self.context['corpus_snapshot']['beats'].get('beats', []))))
            if not scene_ids:
                print(f"Warning: No scenes found to shard for phase '{phase_name}'. Skipping.")
                return

            # Store results from each shard
            all_tool_params = []

            for scene_id in scene_ids:
                scene_context = copy.deepcopy(self.context)
                scene_context['phase']['scene_id'] = scene_id

                # Run agent for the specific scene
                tool_name, params = agent_runner(scene_context, brief)

                # In a real parallel system, results would be collected.
                # Here, we just append them to be processed serially.
                all_tool_params.append(params)

            # Merge results (simple concatenation for lists)
            # This is a simplification. A real merge might be more complex.
            merged_params = {}
            if all_tool_params:
                first_item = all_tool_params[0]
                merged_params = copy.deepcopy(first_item)
                for key in merged_params:
                    if isinstance(merged_params[key], list):
                        for i in range(1, len(all_tool_params)):
                            merged_params[key].extend(all_tool_params[i][key])

            self._execute_tool_call(tool_name, merged_params)

        else:
            # --- Non-Sharded Phase ---
            self.context["phase"]["scene_id"] = None
            tool_name, params, *extra = agent_runner(self.context, brief)

            # The critic agent returns the validation result directly
            if tool_name == 'validate_corpus':
                validation_result = extra[0]
                if validation_result['status'] == 'failure':
                    print("!!! VALIDATION FAILED. Halting pipeline. !!!")
                    # In a real scenario, would trigger conflict resolution here.
                    exit(1)
                else:
                    print("Validation successful.")
            else:
                self._execute_tool_call(tool_name, params)


    def run_pipeline(self):
        """Runs the full PRADD generation pipeline."""
        print("--- Starting PRADD Generation Pipeline ---")

        # Phase 1: Creative Director
        self.run_phase("Creative Direction", creative_director.run, "A brief about calculus.")

        # Phase 2: Story Planner
        self.run_phase("Story Planning", story_planner.run, "A narrative outline.")

        # Phase 3: Object Librarian
        self.run_phase("Object Cataloging", object_librarian.run, "A list of required objects.")

        # --- Sharded Phases Start Here ---
        # Phase 4: Layout Designer
        self.run_phase("Layout Design", layout_designer.run, "Layout goals", is_sharded=True)

        # Phase 5: Animation Designer
        self.run_phase("Animation Design", animation_designer.run, "Animation brief", is_sharded=True)

        # Phase 6: Relationship Engineer
        self.run_phase("Relationship Engineering", relationship_engineer.run, "Dynamics brief", is_sharded=True)

        # Phase 7: Timing & Camera Director
        self.run_phase("Timing & Camera", timing_camera_director.run, "Timing brief", is_sharded=True)

        # Phase 8: First Strict Validation
        self.run_phase("Validation", lambda ctx, brief: consistency_critic.run(ctx, brief, strict=True), "Policy")

        # Phase 9: Polish Director
        self.run_phase("Polish", polish_director.run, "Polish brief")

        # Phase 10: Rendering Strategist
        self.run_phase("Rendering Strategy", rendering_strategist.run, "Render constraints")

        # Phase 11: Final Strict Validation
        self.run_phase("Validation", lambda ctx, brief: consistency_critic.run(ctx, brief, strict=True), "Policy")

        # Phase 12: Compile PRADD
        print("-> Compiling final PRADD.md...")
        self.tools['compile_pradd'](context=self.context, include_appendices=True)

        print("--- PRADD Generation Pipeline Finished Successfully ---")


if __name__ == "__main__":
    # Clean corpus directory for a fresh run
    for p in tool_definitions.CORPUS_DIR.glob("*"):
        p.unlink()

    initial_ctx = get_initial_context()
    orchestrator = Orchestrator(initial_ctx)
    orchestrator.run_pipeline()
