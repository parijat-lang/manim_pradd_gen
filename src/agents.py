import json
from pathlib import Path
import src.tools as tools
from src.llm_interface import get_llm_tool_call

class BaseAgent:
    """
    Base class for an agent in the PRADD pipeline.
    Each subclass represents a specific role and is tied to a primary tool.
    """
    agent_name: str = "Unknown Agent"
    tool_name: str = ""  # Each subclass must define its primary tool.
    prompt_filename: str = "" # The filename of the agent's system prompt.

    def __init__(self):
        self.system_prompt = self._load_system_prompt()

    def _load_system_prompt(self) -> str:
        """Loads the agent's system prompt and appends instructions for JSON output."""
        if not self.prompt_filename:
            raise NotImplementedError("Agent must have a prompt_filename.")

        prompt_path = Path("agent_prompts") / self.prompt_filename
        try:
            base_prompt = prompt_path.read_text()
            # Instruct the LLM to return only the JSON arguments for its designated tool.
            instruction = (
                "\n\nYour task is to generate the arguments for your designated tool based on the "
                "request and the current state of the corpus. You must respond with a single, valid "
                "JSON object that contains the arguments for the tool. Do not add any commentary."
            )
            return base_prompt + instruction
        except FileNotFoundError:
            print(f"FATAL: System prompt not found for agent '{self.agent_name}' at {prompt_path}")
            raise

    def _get_corpus_state_summary(self) -> str:
        """Gets a summary of the current state of the PRADD corpus."""
        if not tools.CORPUS_DIR.exists() or not any(tools.CORPUS_DIR.iterdir()):
            return "The PRADD corpus is currently empty. You are the first agent to act."

        files = [f.name for f in tools.CORPUS_DIR.glob("*.json")]
        return f"The following corpus files already exist: {', '.join(files)}. You should review them if necessary to inform your work."

    def run(self, task_prompt: str) -> str:
        """
        Runs the agent for a given task.
        1. Constructs a full prompt including the corpus state.
        2. Calls the LLM to get a JSON string of arguments.
        3. Executes the agent's designated tool with these arguments.
        """
        print(f"\n--- Running Agent: {self.agent_name} ---")

        full_user_prompt = f"TASK: {task_prompt}\n\nCONTEXT: {self._get_corpus_state_summary()}"

        if not self.tool_name:
            raise NotImplementedError(f"Agent {self.agent_name} must have a tool_name defined.")

        try:
            # 1. Get the JSON arguments string from the LLM
            llm_response_str = get_llm_tool_call(self.system_prompt, full_user_prompt)

            # 2. Parse the JSON string into a Python dictionary
            args = json.loads(llm_response_str)

            # 3. Get the tool function from the tools module
            tool_function = getattr(tools, self.tool_name)

            print(f"Executing tool: {self.tool_name}")
            result = tool_function(**args)
            print(f"Agent {self.agent_name} finished successfully.")
            return result

        except json.JSONDecodeError as e:
            error_message = f"ERROR in agent '{self.agent_name}': Failed to decode LLM response as JSON. Response was:\n{llm_response_str}"
            print(error_message)
            raise
        except Exception as e:
            error_message = f"ERROR in agent '{self.agent_name}': {e}"
            print(error_message)
            raise

# --- Agent Definitions ---

class CreativeDirector(BaseAgent):
    agent_name = "Creative Director"
    prompt_filename = "creative_director.md"
    tool_name = "register_north_star"

class StoryPlanner(BaseAgent):
    agent_name = "Story Planner"
    prompt_filename = "story_planner.md"
    tool_name = "write_beats"

class ObjectLibrarian(BaseAgent):
    agent_name = "Object Librarian"
    prompt_filename = "object_librarian.md"
    tool_name = "catalog_objects"

class LayoutDesigner(BaseAgent):
    agent_name = "Layout Designer"
    prompt_filename = "layout_designer.md"
    tool_name = "plan_geometry"

class AnimationDesigner(BaseAgent):
    agent_name = "Animation Designer"
    prompt_filename = "animation_designer.md"
    tool_name = "design_animations"

class RelationshipEngineer(BaseAgent):
    agent_name = "Relationship Engineer"
    prompt_filename = "relationship_engineer.md"
    tool_name = "define_relationships"

class TimingCameraDirector(BaseAgent):
    agent_name = "Timing & Camera Director"
    prompt_filename = "timing_camera_director.md"
    tool_name = "compose_timeline"

class PolishDirector(BaseAgent):
    agent_name = "Polish Director"
    prompt_filename = "polish_director.md"
    tool_name = "add_polish"

class RenderingStrategist(BaseAgent):
    agent_name = "Rendering Strategist"
    prompt_filename = "rendering_strategist.md"
    tool_name = "set_render_strategy"

class ConsistencyCritic(BaseAgent):
    agent_name = "Consistency Critic"
    prompt_filename = "consistency_critic.md"
    tool_name = "validate_corpus"

# Note: The Orchestrator and Conflict Resolver have special roles and are not
# implemented as simple tool-calling agents here. The Orchestrator is the main
# script, and the Conflict Resolver would require a more complex loop.
