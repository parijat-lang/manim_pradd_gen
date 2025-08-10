# Manim PRADD Generator

This repository contains a Python-based implementation of a stateless, multi-agent pipeline designed to generate a **Production-Ready Animation Design Document (PRADD)** for animations made with the [Manim Community Edition](https://www.manim.community/).

The workflow is based on the detailed PRD provided, orchestrating a series of specialized agents to move from a high-level creative brief to a complete set of specification files ready for code generation.

## Project Structure

The repository is organized as follows:

-   `corpus/`: This directory is where all the output artifacts of the pipeline are stored. After a successful run, it will contain all the `.json` and `.md` files that constitute the PRADD. It is empty by default and gets populated when you run the main script.
-   `schemas/`: Contains the YAML definitions for all data structures used in the project, including the `context_capsule` and all data artifacts. These schemas define the contract for data passed between agents and tools.
-   `src/`: The main source code for the agentic pipeline.
    -   `agents/`: Contains the implementation for each specialized agent (e.g., `CreativeDirector`, `StoryPlanner`). These are currently implemented as mock runners that simulate an LLM's output.
    -   `prompts.py`: Stores the detailed system prompts for each agent.
    -   `tool_definitions.py`: Implements the set of tools (e.g., `write_beats`, `catalog_objects`) that agents can call to create and modify the corpus artifacts.
    -   `main.py`: The orchestrator script that runs the entire pipeline from start to finish.
-   `requirements.txt`: A list of the Python dependencies required to run the project.
-   `.gitignore`: Standard Python gitignore file.
-   `README.md`: This file.

## Setup and Execution

### 1. Prerequisites

-   Python 3.8+
-   `pip` for installing packages

### 2. Installation

Clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd manim_pradd_generator
pip install -r requirements.txt
```

### 3. Running the Pipeline

To run the entire PRADD generation pipeline, execute the `main.py` script from the root directory of the project:

```bash
python -m src.main
```

You will see log messages in your console indicating which agent is running and which tools are being called.

### 4. Outputs

After the script finishes, the `corpus/` directory will be populated with all the generated artifact files, such as:
- `north_star.md`
- `beats.json`
- `objects.json`
- `animations.json`
- ...and all other files defined in the PRD.

Additionally, a final compiled `PRADD.md` will be created in the project's root directory. This file aggregates all the information from the corpus into a single, human-readable document.

## Integrating with a Live LLM (e.g., LM Studio)

This repository is set up with mock agent runners that simulate LLM responses. To connect this pipeline to a real LLM running via LM Studio, you would need to:

1.  **Start the LM Studio Server**: Ensure your model is loaded and the local server is running.
2.  **Modify Agent Runners**: Go into each agent file in `src/agents/`.
3.  **Replace Mock Logic**: Replace the hardcoded `mock_llm_response_params` dictionary with actual calls to the LLM. You would use the `lmstudio` Python SDK to:
    a.  Construct a prompt using the system prompt from `src.prompts` and the context/brief passed to the agent.
    b.  Send the prompt to the LLM.
    c.  Parse the LLM's response to extract the tool call name and its parameters.
    d.  Return the extracted tool name and parameters, just as the mock implementation does now.

This modular design allows you to easily plug in any LLM that supports a tool-calling or function-calling API.
