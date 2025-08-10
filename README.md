# PRADD Generation Workflow for Manim

This repository contains a Python-based framework for an agentic workflow that generates a Production-Ready Animation Design Document (PRADD) for animations made with the Manim library. The system is designed to be stateless, parallelizable, and feedback-safe, following the specifications outlined in the provided Product Requirements Document (PRD).

## Getting Started

This project uses standard Python and has dependencies managed by `pyproject.toml`.

### Prerequisites

- Python 3.9+

### Installation & Running

1.  **Set up a virtual environment (optional but recommended):**
    ```sh
    python -m venv .venv
    source .venv/bin/activate
    ```

2.  **Install dependencies:**
    The necessary dependencies are `pydantic` and `pyyaml`. If you have a build system that reads `pyproject.toml`, they can be installed from there. Otherwise, you can install them manually:
    ```sh
    pip install "pydantic>=2.0" "pyyaml>=6.0"
    ```

3.  **Run the workflow simulation:**
    To execute the main orchestrator script and see the workflow in action, run:
    ```sh
    python -m src.pradd_gen.main
    ```
    This will simulate the entire pipeline, from the Creative Director to the final PRADD compilation. All output files will be placed in the `artifacts/` directory.

## Project Structure

-   `artifacts/`: Output directory for all generated files (e.g., `beats.json`, `PRADD.md`).
-   `examples/`: Contains minimal YAML examples of data artifacts as described in the PRD.
-   `prompts/`: Stores the system prompts for each agent role in the workflow.
-   `schemas/`: Contains YAML schema definitions for all data structures, including the context capsule, tools, and artifacts.
-   `src/pradd_gen/`: The main source code for the project.
    -   `__init__.py`: Marks the directory as a Python package.
    -   `models.py`: Contains all Pydantic data models for validation and type safety.
    -   `tools.py`: Skeleton implementations of the tools that agents can call (e.g., `write_beats`).
    -   `agents.py`: Skeleton implementations of the agents (e.g., `CreativeDirector`).
    -   `main.py`: The main orchestrator script that runs the entire pipeline.
-   `pyproject.toml`: Project metadata and dependencies.
-   `README.md`: This file.
-   `AGENTS.md`: Guidelines for AI agents working on this codebase.

## Workflow Overview

The workflow is orchestrated by `main.py` and follows a series of phases, each handled by a specialized agent.

1.  **Initialization**: A `ContextCapsule` is created to hold the state of the project.
2.  **Pipeline Execution**: A predefined sequence of agents is run. Each agent:
    -   Receives the current `ContextCapsule`.
    -   Performs its specialized task (e.g., writing story beats, defining objects).
    -   Calls a tool to write its output to the `artifacts/` directory.
3.  **Validation**: `ConsistencyCritic` agents are run at key points to ensure the integrity of the data.
4.  **Compilation**: Finally, the `compile_pradd` tool is called to generate a summary `PRADD.md` document from the artifacts.

This structure allows for a clear separation of concerns and a modular, extensible system for generating animation design documents.
