# Agent Guidelines for the PRADD Generator

Hello, fellow agent! This document provides guidelines for working on this codebase. The goal is to maintain a clean, modular, and extensible system for generating Production-Ready Animation Design Documents (PRADD).

## Core Architecture

The project follows a specific, layered architecture. Understanding this pattern is key to contributing effectively. The flow of data and logic is:

**Schemas -> Models -> Tools -> Agents -> Orchestrator**

1.  **`schemas/`**: This is the Single Source of Truth for all data structures. All data, including the context capsule, tool arguments, and output artifacts, is defined here in YAML format. **Always start here** if you need to change a data structure.

2.  **`src/pradd_gen/models.py`**: This file contains the Pydantic models that are directly derived from the YAML schemas. These models provide runtime data validation and static type checking, preventing many common errors. If you modify a schema in `schemas/`, you **must** update the corresponding Pydantic model here.

3.  **`src/pradd_gen/tools.py`**: These are the functions that agents can call. They are the "hands" of the agents, performing actions like reading from and writing to the `artifacts/` directory. Tool function signatures should be typed using the Pydantic models.

4.  **`src/pradd_gen/agents.py`**: Each agent has a specific role and is responsible for a single phase of the pipeline. The agent's logic (in a real system, this would be an LLM call guided by a system prompt) decides which tool to call and with what arguments. The system prompts are stored in the `prompts/` directory.

5.  **`src/pradd_gen/main.py`**: This is the orchestrator. It defines the sequence of phases (the agent pipeline) and runs the entire workflow from start to finish.

## How to Contribute

### Modifying an Existing Component

-   **To change a data field:**
    1.  Edit the appropriate `.yaml` file in `schemas/`.
    2.  Update the corresponding Pydantic model in `src/pradd_gen/models.py`.
    3.  Update any tools and agents that use this model.

-   **To change an agent's behavior:**
    1.  First, consider if you need to change the agent's prompt in `prompts/`.
    2.  If the agent needs a new capability, you might need to add a new tool in `tools.py`.
    3.  Update the agent's `run` or `_execute_task` method in `agents.py`.

### Adding a New Phase/Agent

1.  **Define the agent's role and capabilities.** What is its purpose? What data does it need? What does it produce?
2.  **Add a new prompt** for the agent in the `prompts/` directory.
3.  **Define the schema** for any new data artifact it produces in the `schemas/` directory.
4.  **Create a new Pydantic model** for the artifact in `models.py`.
5.  **Create a new tool** in `tools.py` for the agent to call.
6.  **Create the new agent class** in `agents.py`.
7.  **Add the new agent** to the pipeline in `src/pradd_gen/main.py`.

## Final Checks

Before finishing your work, ensure the main simulation runs without errors:

```sh
python -m src.pradd_gen.main
```

This will verify that all the components are correctly integrated. Good luck!
