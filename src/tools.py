import json
import os
from pathlib import Path
from typing import Dict, Any, List

# The single source of truth for all generated artifacts.
CORPUS_DIR = Path("pradd_corpus")

# Ensure the output directory exists at import time
CORPUS_DIR.mkdir(exist_ok=True)

# --- Helper Functions ---

def _write_json(filename: str, data: Dict[str, Any]):
    """Helper function to write a dictionary to a JSON file in the corpus."""
    filepath = CORPUS_DIR / filename
    try:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        print(f"SUCCESS: Wrote data to {filepath}")
    except IOError as e:
        print(f"ERROR: Could not write to file {filepath}: {e}")
        raise

def _append_to_json_list(filename: str, list_key: str, item: Dict[str, Any]):
    """Helper to append an item to a list within a JSON file."""
    filepath = CORPUS_DIR / filename
    if not filepath.exists():
        data = {list_key: []}
    else:
        with open(filepath, "r") as f:
            data = json.load(f)

    data[list_key].append(item)
    _write_json(filename, data)

def _write_md(filename: str, content: str):
    """Helper function to write content to a Markdown file in the corpus."""
    filepath = CORPUS_DIR / filename
    try:
        with open(filepath, "w") as f:
            f.write(content)
        print(f"SUCCESS: Wrote content to {filepath}")
    except IOError as e:
        print(f"ERROR: Could not write to file {filepath}: {e}")
        raise

# --- Tool Implementations based on PRD ---

def register_north_star(purpose: str, audience: str, tone: str, style_tokens: Dict, motion_grammar: List[str], constraints: List[str], references: List[str]) -> str:
    """Creates the north_star.md and seeds the glossary.json with style tokens."""
    glossary_data = {"tokens": style_tokens, "terms": []}
    _write_json("glossary.json", glossary_data)

    md_content = f"""# North Star

## Purpose
{purpose}

## Audience
{audience}

## Tone
{tone}

## Motion Grammar
- {"\n- ".join(motion_grammar)}

## Constraints
- {"\n- ".join(constraints)}

## References
- {"\n- ".join(references)}
"""
    _write_md("north_star.md", md_content.strip())
    return "North Star (north_star.md) and style tokens (glossary.json) have been registered."

def write_beats(fps: int, beats: List[Dict]) -> str:
    """Creates or replaces the beats.json file."""
    data = {"fps": fps, "beats": beats}
    _write_json("beats.json", data)
    return f"SUCCESS: Wrote {len(beats)} beats to beats.json."

def catalog_objects(objects: List[Dict]) -> str:
    """Creates or replaces the objects.json file."""
    data = {"objects": objects}
    _write_json("objects.json", data)
    return f"SUCCESS: Cataloged {len(objects)} objects in objects.json."

def plan_geometry(frames: List[Dict]) -> str:
    """Creates or replaces the geometry.json file."""
    data = {"frames": frames}
    _write_json("geometry.json", data)
    return f"SUCCESS: Planned geometry for {len(frames)} frames in geometry.json."

def design_animations(animations: List[Dict]) -> str:
    """Creates or replaces the animations.json file."""
    data = {"animations": animations}
    _write_json("animations.json", data)
    return f"SUCCESS: Designed {len(animations)} animations in animations.json."

def define_relationships(relationships: List[Dict]) -> str:
    """Creates or replaces the relationships.json file."""
    data = {"relationships": relationships}
    _write_json("relationships.json", data)
    return f"SUCCESS: Defined {len(relationships)} relationships in relationships.json."

def compose_timeline(timeline: List[Dict], camera: List[Dict]) -> str:
    """Creates or replaces timeline.json and camera.json."""
    _write_json("timeline.json", {"timeline": timeline})
    _write_json("camera.json", {"camera": camera})
    return f"SUCCESS: Composed timeline with {len(timeline)} scenes and {len(camera)} camera cues."

def add_polish(polish: List[Dict]) -> str:
    """Creates or replaces the polish.json file."""
    data = {"polish": polish}
    _write_json("polish.json", data)
    return f"SUCCESS: Added {len(polish)} polish items to polish.json."

def set_render_strategy(strategy: Dict) -> str:
    """Creates or replaces the rendering.json file."""
    data = {"strategy": strategy}
    _write_json("rendering.json", data)
    return "SUCCESS: Render strategy has been set in rendering.json."

def open_risk(title: str, risk_level: str, owner: str, mitigation: str) -> str:
    """Adds a new risk to risks.json."""
    risk_item = {
        "title": title,
        "risk_level": risk_level,
        "owner": owner,
        "mitigation": mitigation,
    }
    _append_to_json_list("risks.json", "risks", risk_item)
    return f"SUCCESS: Opened risk '{title}' and logged to risks.json."

def commit_decision(summary: str, patches: List[Dict]) -> str:
    """Logs a decision to decision_log.md."""
    filepath = CORPUS_DIR / "decision_log.md"

    patch_str = json.dumps(patches, indent=2)

    log_entry = f"""
## Decision Logged

**Summary:** {summary}

**Patches Applied:**
```json
{patch_str}
```
---
"""

    try:
        with open(filepath, "a") as f:
            f.write(log_entry)
        # For this tool, we don't apply the patches automatically.
        # The Conflict Resolver agent is responsible for that.
        # This tool's job is just to log the decision.
        return f"SUCCESS: Logged decision to {filepath}."
    except IOError as e:
        print(f"ERROR: Could not write to {filepath}: {e}")
        return f"FAILURE: Could not log decision. Error: {e}"

# Note: `validate_corpus` and `compile_pradd` are more complex and will be handled
# by their own dedicated modules (`validator.py` and `compiler.py`).
# We will create a placeholder here to be called by the agent.

def validate_corpus(strict: bool = True) -> str:
    """Placeholder for the validation tool."""
    # The actual logic will be in validator.py
    # This is just to satisfy the agent's tool-calling mechanism.
    from validator import run_validation
    errors, warnings = run_validation(strict=strict)
    if not errors and not warnings:
        return "SUCCESS: Corpus validation passed."
    else:
        return f"VALIDATION FAILED: {len(errors)} errors, {len(warnings)} warnings found. See logs."


def compile_pradd(include_appendices: bool = True) -> str:
    """Placeholder for the PRADD compilation tool."""
    # The actual logic will be in compiler.py
    from compiler import run_compilation
    run_compilation(include_appendices=include_appendices)
    return "SUCCESS: PRADD.md has been compiled."
