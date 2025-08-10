import json
import copy
from pathlib import Path
from openai import OpenAI

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
        try:
            self.llm_client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
            # Check connection
            self.llm_client.models.list()
            print("Successfully connected to LM Studio server.")
        except Exception as e:
            print(f"Error connecting to LM Studio server: {e}")
            print("Please ensure LM Studio is running and the server is enabled.")
            self.llm_client = None


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
            scene_ids = sorted(list(set(b['scene_id'] for b in self.context['corpus_snapshot']['beats'].get('beats', []))))
            if not scene_ids:
                print(f"Warning: No scenes found to shard for phase '{phase_name}'. Skipping.")
                return

            all_tool_params = []
            tool_name = "" # Assume all shards use the same tool

            for scene_id in scene_ids:
                scene_context = copy.deepcopy(self.context)
                scene_context['phase']['scene_id'] = scene_id

                # Run agent for the specific scene
                tool_name, params = agent_runner(self.llm_client, scene_context, brief)
                all_tool_params.append(params)

            # Merge results
            if not tool_name or not all_tool_params:
                print(f"Phase '{phase_name}' produced no tool calls. Skipping execution.")
                return

            merged_params = {}
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
            # The critic agent is a special case that doesn't use the LLM
            if agent_runner == consistency_critic.run:
                 tool_name, params, validation_result = agent_runner(self.context, brief)
                 if validation_result['status'] == 'failure':
                    print("!!! VALIDATION FAILED. Halting pipeline. !!!")
                    exit(1)
                 else:
                    print("Validation successful.")
            else:
                tool_name, params = agent_runner(self.llm_client, self.context, brief)
                self._execute_tool_call(tool_name, params)


    def run_pipeline(self):
        """Runs the full PRADD generation pipeline."""
        if not self.llm_client:
            print("LLM client not available. Cannot run pipeline.")
            return

        print("--- Starting PRADD Generation Pipeline ---")

        # Define more detailed briefs for the agents
        creative_brief = "Create a short, visually engaging explainer video about the Fundamental Theorem of Calculus, aimed at university students. The style should be clean, modern, and inspired by educational content like 3Blue1Brown."

        narrative_outline = """
        Act 1: The Concept of Area. Introduce a simple curve, f(x). Visually represent the concept of the area under the curve from a starting point 'a' to a variable point 'x'. Define this as the 'area function', A(x). Show how A(x) changes as x moves.
        Act 2: The Concept of the Derivative. Briefly recap the derivative as the slope of a function. Show a tangent line to the f(x) curve and illustrate its slope at various points.
        Act 3: The Connection. This is the core of the video. Show that the rate of change of the area function, A'(x), is exactly equal to the original function, f(x). Animate this by showing the area accumulating while simultaneously plotting its derivative, which should trace out the f(x) curve perfectly. Conclude by stating the theorem.
        """

        object_brief = "We will need axes, a function graph for f(x), a shaded area object, a tangent line, and text labels for 'f(x)', 'A(x)', the theorem itself."
        layout_goals = "The main function graph should be centered. Text labels should appear in the corners and not obstruct the main action. The derivative plot in Act 3 can be shown on a secondary, smaller set of axes."
        animation_brief = "Animations should be smooth. Use Create and Write for introductions. The key animation is the simultaneous drawing of the derivative of the area function while the area itself grows."
        dynamics_brief = "The area object and the tangent line must be dynamically linked to the main function graph. A ValueTracker should control the position 'x' along the curve."
        timing_brief = "Pace the video slowly, with pauses for key revelations. Act 1 should be ~30% of the runtime, Act 2 ~20%, and Act 3 ~50%."
        polish_brief = "Add subtle glowing effects to highlight the connection in Act 3. Use smooth fade transitions between acts."
        render_constraints = "Standard HD, 1080p, 60fps. Use a high-quality renderer."

        # Phase 1: Creative Director
        self.run_phase("Creative Direction", creative_director.run, creative_brief)

        # Phase 2: Story Planner
        self.run_phase("Story Planning", story_planner.run, narrative_outline)

        # Phase 3: Object Librarian
        self.run_phase("Object Cataloging", object_librarian.run, object_brief)

        # --- Sharded Phases Start Here ---
        # Phase 4: Layout Designer
        self.run_phase("Layout Design", layout_designer.run, layout_goals, is_sharded=True)

        # Phase 5: Animation Designer
        self.run_phase("Animation Design", animation_designer.run, animation_brief, is_sharded=True)

        # Phase 6: Relationship Engineer
        self.run_phase("Relationship Engineering", relationship_engineer.run, dynamics_brief, is_sharded=True)

        # Phase 7: Timing & Camera Director
        self.run_phase("Timing & Camera", timing_camera_director.run, timing_brief, is_sharded=True)

        # Phase 8: First Strict Validation
        self.run_phase("Validation", lambda client, ctx, brief: consistency_critic.run(ctx, brief, strict=True), "Policy")

        # Phase 9: Polish Director
        self.run_phase("Polish", polish_director.run, polish_brief)

        # Phase 10: Rendering Strategist
        self.run_phase("Rendering Strategy", rendering_strategist.run, render_constraints)

        # Phase 11: Final Strict Validation
        self.run_phase("Validation", lambda client, ctx, brief: consistency_critic.run(ctx, brief, strict=True), "Policy")

        # Phase 12: Compile PRADD
        print("-> Compiling final PRADD.md...")
        self.tools['compile_pradd'](context=self.context, include_appendices=True)

        print("--- PRADD Generation Pipeline Finished Successfully ---")


if __name__ == "__main__":
    # Clean corpus directory for a fresh run
    corpus_path = Path(__file__).parent / ".." / "corpus"
    if corpus_path.exists():
        for p in corpus_path.glob("*"):
            p.unlink()

    initial_ctx = get_initial_context()
    orchestrator = Orchestrator(initial_ctx)
    orchestrator.run_pipeline()
