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

This system requires access to a local LLM. It is configured by default to work with **LM Studio**.

**1. Setup LM Studio:**
- Download and install [LM Studio](https://lmstudio.ai/download).
- In the LM Studio application, search for and download the `openai/gpt-oss-20b` model.
- Load the model and navigate to the "Local Server" tab.
- Click "Start Server". This will expose an OpenAI-compatible API endpoint.

**2. Configure Environment Variables:**
The script connects to the LLM using an API endpoint and model name defined by environment variables. You must set these before running the application.

- **For LM Studio (Default):**
  The code defaults to the standard LM Studio endpoint and the `gpt-oss-20b` model. If your setup is standard, you may not need to set these variables. However, it is best practice to set them explicitly:
  ```bash
  # The server address from the LM Studio "Local Server" tab
  export LLM_API_ENDPOINT="http://localhost:1234/v1/chat/completions"

  # The model identifier you see loaded in LM Studio
  export LLM_MODEL="gpt-oss-20b"
  ```

- **For Ollama (Alternative):**
  If you are using Ollama, you will need to override the default environment variables:
  ```bash
  export LLM_API_ENDPOINT="http://localhost:11434/api/chat"
  export LLM_MODEL="llama3" # Or another model you have downloaded
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
