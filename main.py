import argparse
import sys
from pathlib import Path

# To ensure src modules can be imported
from src.agents import (
    CreativeDirector, StoryPlanner, ObjectLibrarian, LayoutDesigner,
    AnimationDesigner, RelationshipEngineer, TimingCameraDirector,
    PolishDirector, RenderingStrategist, ConsistencyCritic
)
from src.tools import validate_corpus, compile_pradd

def run_pipeline(idea_prompt: str):
    """
    Executes the full agentic pipeline to generate a PRADD.
    """
    print("--- Starting PRADD Generation Pipeline ---")
    print(f"Based on initial idea: '{idea_prompt[:100]}...'")

    # The pipeline of agents, as defined in the PRD.
    # The Consistency Critic runs after the main content generation.
    pipeline = [
        ("Phase 1: North Star", CreativeDirector()),
        ("Phase 2: Beats & Scenes", StoryPlanner()),
        ("Phase 3: Canonical Objects", ObjectLibrarian()),
        ("Phase 4: Geometry & Layout", LayoutDesigner()),
        ("Phase 5: Animation Design", AnimationDesigner()),
        ("Phase 6: Dynamics & Relationships", RelationshipEngineer()),
        ("Phase 7: Timeline & Camera", TimingCameraDirector()),
        ("Phase 8: Polish", PolishDirector()),
        ("Phase 9: Render Strategy", RenderingStrategist()),
    ]

    try:
        # Run the main content-generation agents
        for phase_name, agent in pipeline:
            print(f"\n{'='*20}\n{phase_name}\n{'='*20}")
            agent.run(task_prompt=idea_prompt)

        # Phase 10: Global Validation
        print(f"\n{'='*20}\nPhase 10: Global Validation\n{'='*20}")
        validation_result = validate_corpus(strict=True)
        print(validation_result)
        if "FAILED" in validation_result:
            print("\nValidation failed. Halting before final compilation.")
            print("Please review the errors and the generated corpus.")
            sys.exit(1)

        # Phase 11: Compile final PRADD.md
        print(f"\n{'='*20}\nPhase 11: Compile PRADD.md\n{'='*20}")
        compilation_result = compile_pradd(include_appendices=True)
        print(compilation_result)

    except Exception as e:
        print(f"\n--- A critical error occurred in the pipeline ---")
        print(f"Error: {e}")
        print("The pipeline has been halted. Please check the logs and the state of the pradd_corpus.")
        sys.exit(1)

    print("\n--- PRADD Generation Pipeline Finished Successfully! ---")
    print("You can find the final document in PRADD.md")

def main():
    parser = argparse.ArgumentParser(description="Generate a PRADD document from a video animation idea.")
    parser.add_argument(
        "idea_file",
        type=Path,
        help="Path to a text file containing the animation idea."
    )
    args = parser.parse_args()

    if not args.idea_file.is_file():
        print(f"Error: The file '{args.idea_file}' does not exist.")
        sys.exit(1)

    animation_idea = args.idea_file.read_text()
    run_pipeline(animation_idea)

if __name__ == "__main__":
    main()
