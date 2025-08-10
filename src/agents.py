import json
from pathlib import Path
from typing import List
import src.tools as tools
from src.llm_interface import get_llm_tool_call

class BaseAgent:
    """
    Base class for an agent in the PRADD pipeline.
    Each subclass represents a specific role, is tied to a primary tool,
    and declares its data dependencies.
    """
    agent_name: str = "Unknown Agent"
    tool_name: str = ""
    prompt_filename: str = ""
    dependencies: List[str] = [] # Files this agent needs as context

    def __init__(self):
        self.system_prompt = self._load_system_prompt()

    def _load_system_prompt(self) -> str:
        """Loads the agent's system prompt."""
        if not self.prompt_filename:
            raise NotImplementedError("Agent must have a prompt_filename.")
        prompt_path = Path("agent_prompts") / self.prompt_filename
        try:
            return prompt_path.read_text()
        except FileNotFoundError:
            print(f"FATAL: System prompt not found for agent '{self.agent_name}' at {prompt_path}")
            raise

    def _get_dependency_context(self) -> str:
        """
        Loads the content of dependency files from the corpus to provide as context.
        """
        if not self.dependencies:
            return "No previous context required. You are the first agent to act on the main task."

        context_parts = []
        for dep_file in self.dependencies:
            filepath = tools.CORPUS_DIR / dep_file
            if filepath.exists():
                try:
                    with open(filepath, "r") as f:
                        content = f.read()
                        context_parts.append(f"--- START OF {dep_file} ---\n{content}\n--- END OF {dep_file} ---")
                except Exception as e:
                    context_parts.append(f"Could not read {dep_file}: {e}")
            else:
                context_parts.append(f"{dep_file} has not been generated yet.")

        return "\n\n".join(context_parts)

    def run(self, task_prompt: str) -> str:
        """
        Runs the agent for a given task.
        1. Loads dependency files to create a rich context.
        2. Constructs a full prompt including the original task and the new context.
        3. Calls the LLM to get a JSON string of arguments.
        4. Extracts and parses the JSON from the potentially messy response.
        5. Executes the agent's designated tool with these arguments.
        """
        print(f"\n--- Running Agent: {self.agent_name} ---")

        context = self._get_dependency_context()
        full_user_prompt = f"TASK: {task_prompt}\n\nPREVIOUSLY GENERATED CONTEXT:\n{context}"

        if not self.tool_name:
            raise NotImplementedError(f"Agent {self.agent_name} must have a tool_name defined.")

        try:
            llm_response_str = get_llm_tool_call(self.system_prompt, full_user_prompt)

            try:
                start_index = llm_response_str.find('{')
                end_index = llm_response_str.rfind('}')
                if start_index != -1 and end_index != -1 and end_index > start_index:
                    json_str = llm_response_str[start_index:end_index+1]
                    args = json.loads(json_str)
                else:
                    raise json.JSONDecodeError("No valid JSON object found in response.", llm_response_str, 0)
            except json.JSONDecodeError as e:
                print(f"ERROR in agent '{self.agent_name}': Failed to decode LLM response as JSON.")
                print(f"Original response was:\n{llm_response_str}")
                raise e

            tool_function = getattr(tools, self.tool_name)

            print(f"Executing tool: {self.tool_name}")
            result = tool_function(**args)
            print(f"Agent {self.agent_name} finished successfully.")
            return result

        except Exception as e:
            error_message = f"ERROR in agent '{self.agent_name}': An exception occurred: {e}"
            print(error_message)
            raise

# --- Agent Definitions with Dependencies ---

class CreativeDirector(BaseAgent):
    agent_name = "Creative Director"
    prompt_filename = "creative_director.md"
    tool_name = "register_north_star"
    dependencies = []

class StoryPlanner(BaseAgent):
    agent_name = "Story Planner"
    prompt_filename = "story_planner.md"
    tool_name = "write_beats"
    dependencies = [] # Depends only on the initial idea

class ObjectLibrarian(BaseAgent):
    agent_name = "Object Librarian"
    prompt_filename = "object_librarian.md"
    tool_name = "catalog_objects"
    dependencies = ['beats.json']

class LayoutDesigner(BaseAgent):
    agent_name = "Layout Designer"
    prompt_filename = "layout_designer.md"
    tool_name = "plan_geometry"
    dependencies = ['beats.json', 'objects.json']

class AnimationDesigner(BaseAgent):
    agent_name = "Animation Designer"
    prompt_filename = "animation_designer.md"
    tool_name = "design_animations"
    dependencies = ['beats.json', 'objects.json']

class RelationshipEngineer(BaseAgent):
    agent_name = "Relationship Engineer"
    prompt_filename = "relationship_engineer.md"
    tool_name = "define_relationships"
    dependencies = ['beats.json', 'objects.json', 'animations.json']

class TimingCameraDirector(BaseAgent):
    agent_name = "Timing & Camera Director"
    prompt_filename = "timing_camera_director.md"
    tool_name = "compose_timeline"
    dependencies = ['beats.json', 'animations.json', 'relationships.json']

class PolishDirector(BaseAgent):
    agent_name = "Polish Director"
    prompt_filename = "polish_director.md"
    tool_name = "add_polish"
    dependencies = ['beats.json', 'objects.json', 'animations.json']

class RenderingStrategist(BaseAgent):
    agent_name = "Rendering Strategist"
    prompt_filename = "rendering_strategist.md"
    tool_name = "set_render_strategy"
    dependencies = ['beats.json']

class ConsistencyCritic(BaseAgent):
    agent_name = "Consistency Critic"
    prompt_filename = "consistency_critic.md"
    tool_name = "validate_corpus"
    # This agent doesn't need context fed into the LLM, as its tool does the reading.
    dependencies = []
