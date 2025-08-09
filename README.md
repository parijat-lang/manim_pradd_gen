# Agentic PRADD Generator for Manim

This repository contains an agentic, multi-agent generative AI workflow to produce a Production-Ready Animation Design Document (PRADD) for video animations created with the Manim framework.

Given a high-level animation idea, this system orchestrates a series of specialized AI agents to iteratively build a detailed and structured plan. The final output is a `PRADD.md` file and a `pradd_corpus/` directory containing machine-readable JSON artifacts, which together provide a single source of truth for generating Manim code.

## How it Works

The workflow is orchestrated by the `main.py` script, which executes a pipeline of agents in a specific order. Each agent is a Python class powered by a local Large Language Model (LLM) and has a specific responsibility in the PRADD creation process.

The pipeline follows these phases:
1.  **Creative Director**: Establishes the vision, tone, and style guide.
2.  **Story Planner**: Breaks the idea down into scenes and beats.
3.  **Object Librarian**: Defines all the canonical objects (text, shapes, etc.) needed.
4.  **Layout Designer**: Plans the geometry and positioning of objects for each beat.
5.  **Animation Designer**: Designs the specific animations and transforms.
6.  ...and so on, for relationships, timing, polish, and rendering.
7.  **Consistency Critic**: Validates the entire corpus of artifacts for consistency and correctness.
8.  **Compiler**: Generates the final, human-readable `PRADD.md` from all the artifacts.

Each agent reads the current state of the `pradd_corpus/` directory, performs its task by calling a local LLM, and writes its output back to the corpus.

## Setup Instructions

**1. Clone the Repository:**
```bash
git clone <repository-url>
cd <repository-directory>
```

**2. Set up a Python Virtual Environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

**3. Install Dependencies:**
```bash
pip install -r requirements.txt
```

## Configuration

This system requires access to a running local LLM that is compatible with the OpenAI API format (like Ollama or LM Studio).

**1. Run a Local LLM:**
Ensure your local LLM server is running. For example, with Ollama, you can run a model like Llama 3 with:
```bash
ollama run llama3
```

**2. Configure the API Endpoint:**
The script connects to the LLM using an API endpoint defined by an environment variable. You must set this variable before running the application.

- **For Ollama (default):**
  ```bash
  export LLM_API_ENDPOINT="http://localhost:11434/api/chat"
  ```
- **For LM Studio:** The endpoint is typically `http://localhost:1234/v1/chat/completions`.
  ```bash
  export LLM_API_ENDPOINT="http://localhost:1234/v1/chat/completions"
  ```

You can also specify the model you are using (the default is `llama3`):
```bash
export LLM_MODEL="your-model-name"
```

## Usage

1.  Create a text file containing your animation idea. An example is provided in `examples/animation_idea.txt`.
2.  Run the main orchestrator script and pass the path to your idea file:

```bash
python main.py examples/animation_idea.txt
```

The script will start the agent pipeline. You will see logs in your terminal as each agent performs its task. When the process is complete, you will find the final `PRADD.md` in the root directory and all the generated JSON artifacts in the `pradd_corpus/` directory.

## Project Structure
```
.
├── main.py                 # The main orchestrator script
├── README.md               # This file
├── requirements.txt        # Python dependencies
├── examples/
│   └── animation_idea.txt  # A sample animation idea
├── pradd_corpus/           # (Generated) Output directory for JSON artifacts
├── pradd_schemas/          # YAML schemas for validating artifacts
├── agent_prompts/          # System prompts for each AI agent
└── src/
    ├── agents.py           # Definitions for each agent class
    ├── compiler.py         # Logic for compiling the final PRADD.md
    ├── llm_interface.py    # Code for communicating with the local LLM
    ├── tools.py            # The functions (tools) that agents can execute
    └── validator.py        # Logic for validating the corpus
```
