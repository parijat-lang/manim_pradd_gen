"""
Main orchestrator for the PRADD generation workflow.

This script simulates the entire agentic pipeline from start to finish,
as defined in the PRD. It initializes a context, instantiates agents,
and runs them in the specified phase order.
"""

import json
from pathlib import Path

from . import agents
from . import models
from . import tools

def get_initial_context() -> models.ContextCapsule:
    """Creates a default context capsule to kick off the workflow."""
    # In a real system, this would be created from a kickoff request.
    project = models.Project(
        project_id="proj_pythagoras_01",
        title="Visualizing the Pythagorean Theorem",
        target_runtime_s=60.0,
        fps=30,
        version="0.1.0"
    )
    phase = models.Phase(name="kickoff", attempt=1, scene_id=None)

    # Empty corpus snapshot to start
    corpus_snapshot = models.CorpusSnapshot(
        north_star={}, beats={}, objects={}, geometry={}, animations={},
        relationships={}, timeline={}, camera={}, polish={}, rendering={},
        glossary={}, risks={}, decisions=[]
    )

    ids = models.IDs(
        prefixes=models.IDPrefixes(),
        counters={"beat": 0, "scene": 0, "object": 0, "anim": 0, "rel": 0, "cam": 0}
    )

    policy = models.Policy(
        style_token_policy="no raw colors outside North Star",
        overlap_policy="same-target overlaps must be parallel-grouped",
        complexity_budget=models.ComplexityBudget()
    )

    manim_profile = models.ManimProfile(
        manim_version="0.19.0",
        flavor="ManimCE",
        modes=["cairo", "2d"],
        primitives=models.ManimPrimitives(
            animations=["Create", "Write", "Transform"],
            composition=["AnimationGroup", "Succession"],
            dynamics=["ValueTracker", "add_updater"],
            camera_actions=["frame_move"]
        )
    )

    return models.ContextCapsule(
        project=project,
        phase=phase,
        corpus_snapshot=corpus_snapshot,
        ids=ids,
        policy=policy,
        manim_profile=manim_profile
    )

def update_context_snapshot(context: models.ContextCapsule) -> models.ContextCapsule:
    """
    Simulates reading all artifact files to update the corpus snapshot.
    In a real system, this would be a more robust process.
    """
    print("\nUpdating context snapshot from artifacts...")
    for artifact_file in tools.ARTIFACTS_DIR.glob("*.json"):
        key = artifact_file.stem
        if hasattr(context.corpus_snapshot, key):
            try:
                setattr(context.corpus_snapshot, key, json.loads(artifact_file.read_text()))
            except (json.JSONDecodeError, AttributeError):
                print(f"  - Could not update '{key}' from {artifact_file}")
    print("Context updated.")
    return context


def main():
    """Runs the full PRADD generation pipeline."""
    print("--- Starting PRADD Generation Workflow ---")

    context = get_initial_context()

    # The pipeline of agents to run, in order.
    # Note: Sharding is not implemented in this skeleton.
    pipeline = [
        agents.CreativeDirector(),
        agents.StoryPlanner(),
        agents.ObjectLibrarian(),
        agents.LayoutDesigner(),       # Per-scene shard would begin here
        agents.AnimationDesigner(),
        agents.RelationshipEngineer(),
        agents.TimingCameraDirector(),
        agents.ConsistencyCritic(),      # First validation pass
        agents.PolishDirector(),
        agents.RenderingStrategist(),
        agents.ConsistencyCritic(),      # Second (strict) validation pass
    ]

    for i, agent in enumerate(pipeline):
        # Update context phase
        context.phase.name = agent.role.lower().replace(' ', '_')
        context.phase.attempt = 1

        # In a real system, the context would be updated more intelligently
        # between each step. Here, we do a full refresh for simplicity.
        context = update_context_snapshot(context)

        # For the second critic run, we pass strict=True
        run_kwargs = {}
        if isinstance(agent, agents.ConsistencyCritic) and i > 8:
             run_kwargs['strict'] = True

        result = agent.run(context, **run_kwargs)
        print(f"Agent '{agent.role}' finished with result: {result.get('status', 'unknown')}")

    # Final step: compile the PRADD.md document
    print("\n--- Pipeline Complete. Compiling Final PRADD.md ---")
    context = update_context_snapshot(context)
    tools.compile_pradd(context, include_appendices=True)

    print("\n--- PRADD Generation Finished ---")
    print(f"All artifacts are available in the '{tools.ARTIFACTS_DIR}' directory.")


if __name__ == "__main__":
    main()
