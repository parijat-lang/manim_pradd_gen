import json
import yaml
import os
from pathlib import Path

# Define the corpus directory relative to this file
CORPUS_DIR = Path(os.path.dirname(__file__)) / ".." / "corpus"
CORPUS_DIR.mkdir(exist_ok=True)

# --- Helper Functions ---

def _get_corpus_path(filename):
    return CORPUS_DIR / filename

def _write_json(filename, data):
    with open(_get_corpus_path(filename), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def _read_json(filename):
    path = _get_corpus_path(filename)
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _write_md(filename, content):
    with open(_get_corpus_path(filename), "w", encoding="utf-8") as f:
        f.write(content)

def _append_md(filename, content):
    with open(_get_corpus_path(filename), "a", encoding="utf-8") as f:
        f.write("\n\n" + content)

# --- Tool Implementations ---

def register_north_star(context, purpose, audience, tone, style_tokens, motion_grammar, constraints, references):
    """Create/replace the vision & style bible."""
    north_star_content = f"""
# North Star

## Purpose
{purpose}

## Audience
{audience}

## Tone
{tone}

## Motion Grammar
{', '.join(motion_grammar)}

## Constraints
{', '.join(constraints)}

## References
{', '.join(references)}
"""
    _write_md("north_star.md", north_star_content)

    glossary = _read_json("glossary.json") or {"tokens": {}, "terms": []}
    glossary["tokens"] = style_tokens
    _write_json("glossary.json", glossary)

    print("Tool: registered north star and glossary tokens.")
    return "North Star registered successfully."

def write_beats(context, fps, beats):
    """Create or update beats & scenes map."""
    beats_data = {"fps": fps, "beats": beats}
    _write_json("beats.json", beats_data)
    print(f"Tool: wrote {len(beats)} beats to beats.json.")
    return "Beats written successfully."

def catalog_objects(context, objects):
    """Define canonical objects (mobject intents)."""
    objects_data = {"objects": objects}
    _write_json("objects.json", objects_data)
    print(f"Tool: cataloged {len(objects)} objects in objects.json.")
    return "Objects cataloged successfully."

def plan_geometry(context, frames):
    """Layout and coordinates per beat."""
    # In a real scenario, this might append or merge, but for now, it overwrites.
    geometry_data = {"frames": frames}
    _write_json("geometry.json", geometry_data)
    print(f"Tool: planned geometry for {len(frames)} frames in geometry.json.")
    return "Geometry planned successfully."

def design_animations(context, animations):
    """Per-beat transforms & effects."""
    animations_data = {"animations": animations}
    _write_json("animations.json", animations_data)
    print(f"Tool: designed {len(animations)} animations in animations.json.")
    return "Animations designed successfully."

def define_relationships(context, relationships):
    """ValueTrackers, updaters, always_redraw, bindings."""
    relationships_data = {"relationships": relationships}
    _write_json("relationships.json", relationships_data)
    print(f"Tool: defined {len(relationships)} relationships in relationships.json.")
    return "Relationships defined successfully."

def compose_timeline(context, timeline, camera):
    """Ordering, groups, waits, and camera cues."""
    timeline_data = {"timeline": timeline}
    camera_data = {"camera": camera}
    _write_json("timeline.json", timeline_data)
    _write_json("camera.json", camera_data)
    print(f"Tool: composed timeline and camera movements.")
    return "Timeline and camera composed successfully."

def add_polish(context, polish):
    """Micro-effects, transitions, accessibility notes."""
    polish_data = {"polish": polish}
    _write_json("polish.json", polish_data)
    print(f"Tool: added {len(polish)} polish effects.")
    return "Polish effects added successfully."

def set_render_strategy(context, strategy):
    """Render quality, sections, previews."""
    strategy_data = {"strategy": strategy}
    _write_json("rendering.json", strategy_data)
    print("Tool: set render strategy.")
    return "Render strategy set successfully."

def open_risk(context, title, risk_level, owner, mitigation):
    """Track assumptions/open questions."""
    risks_data = _read_json("risks.json") or {"risks": []}
    new_risk = {
        "title": title,
        "risk_level": risk_level,
        "owner": owner,
        "mitigation": mitigation
    }
    risks_data["risks"].append(new_risk)
    _write_json("risks.json", risks_data)
    print(f"Tool: opened new risk: {title}")
    return "Risk opened successfully."

import jsonschema
import yaml

# --- Validation Logic ---

def _load_schema(schema_name):
    """Loads a YAML schema from the schemas directory."""
    schema_path = Path(__file__).parent.parent / "schemas" / f"{schema_name}.schema.yaml"
    with open(schema_path, 'r') as f:
        return yaml.safe_load(f)

def validate_corpus(context, strict=False):
    """Run cross-file checks; return errors/warnings."""
    print(f"Tool: running validation (strict={strict})...")
    errors = []
    warnings = []
    corpus = context["corpus_snapshot"]

    # 1. JSON Schema validation for each artifact
    for artifact_name, artifact_data in corpus.items():
        if not artifact_data or artifact_name in ["north_star", "risks", "decisions", "glossary"]:
            continue # Skip non-JSON or simple artifacts for now

        try:
            schema = _load_schema(artifact_name)
            jsonschema.validate(instance=artifact_data, schema=schema)
        except FileNotFoundError:
            warnings.append(f"Schema not found for artifact: {artifact_name}. Skipping validation.")
        except jsonschema.exceptions.ValidationError as e:
            errors.append(f"Validation error in '{artifact_name}.json': {e.message} at path {list(e.path)}")
        except Exception as e:
            errors.append(f"An unexpected error occurred validating '{artifact_name}.json': {e}")

    # 2. Cross-file validation
    if not errors: # Only run if basic schema validation passes
        # Example: Check if all object_ids in geometry exist in objects
        if "objects" in corpus and "geometry" in corpus:
            defined_object_ids = {obj["object_id"] for obj in corpus["objects"].get("objects", [])}
            for frame in corpus["geometry"].get("frames", []):
                for placement in frame.get("placements", []):
                    if placement["object_id"] not in defined_object_ids:
                        errors.append(f"Undefined object_id '{placement['object_id']}' used in geometry frame for beat '{frame['beat_id']}'.")

        # Example: Check total duration against target
        if "beats" in corpus and "project" in context:
            total_duration = sum(b.get('estimated_duration', 0) for b in corpus["beats"].get("beats", []))
            target_runtime = context["project"].get("target_runtime_s", 0)
            if abs(total_duration - target_runtime) > (target_runtime * 0.10):
                warnings.append(f"Total estimated duration ({total_duration}s) deviates more than 10% from target ({target_runtime}s).")

    if not errors:
        print("Validation successful.")
        return {"status": "success", "errors": [], "warnings": warnings}
    else:
        print(f"Validation failed with {len(errors)} errors.")
        return {"status": "failure", "errors": errors, "warnings": warnings}


def commit_decision(context, summary, patches):
    """Record a conflict resolution decision with patches."""
    # This is a complex operation involving JSON Patch (RFC 6902).
    # For this stub, we'll just log the decision.
    decision_log_content = f"""
### Decision Summary
{summary}

#### Patches
```json
{json.dumps(patches, indent=2)}
```
"""
    _append_md("decision_log.md", decision_log_content)
    print(f"Tool: committed decision: {summary}")
    # A real implementation would apply the patches to the respective files.
    return "Decision committed."


def compile_pradd(context, include_appendices=True):
    """Generate PRADD.md from the corpus."""
    print("Tool: compiling PRADD.md...")
    pradd_md = ""

    # Read all corpus files
    corpus_files = [p.name for p in CORPUS_DIR.iterdir()]
    corpus_data = {}
    for filename in corpus_files:
        if filename.endswith(".json"):
            corpus_data[filename.replace(".json", "")] = _read_json(filename)
        elif filename.endswith(".md"):
             with open(_get_corpus_path(filename), "r", encoding="utf-8") as f:
                corpus_data[filename.replace(".md", "")] = f.read()

    # 1. Title & Summary
    pradd_md += f"# PRADD: {context['project']['title']}\n\n"

    # 2. North Star
    if 'north_star' in corpus_data:
        pradd_md += corpus_data['north_star']

    # ... and so on for all sections defined in the PRD.
    # This is a simplified version.

    pradd_md += "\n\n## 4. Story Map (Beats)\n"
    if 'beats' in corpus_data and corpus_data['beats']:
        pradd_md += json.dumps(corpus_data['beats'], indent=2)

    pradd_md += "\n\n## 5. Object Catalog\n"
    if 'objects' in corpus_data and corpus_data['objects']:
        pradd_md += json.dumps(corpus_data['objects'], indent=2)

    # Appendices
    if include_appendices:
        pradd_md += "\n\n# Appendices\n"
        for name, data in corpus_data.items():
            pradd_md += f"\n## {name.replace('_', ' ').title()}\n\n"
            if isinstance(data, str):
                pradd_md += data
            else:
                pradd_md += f"```json\n{json.dumps(data, indent=2)}\n```\n"

    _write_md("PRADD.md", pradd_md)
    print("PRADD.md compiled successfully.")
    return "PRADD.md compiled."

# A dictionary to easily access tools by name
ALL_TOOLS = {
    "register_north_star": register_north_star,
    "write_beats": write_beats,
    "catalog_objects": catalog_objects,
    "plan_geometry": plan_geometry,
    "design_animations": design_animations,
    "define_relationships": define_relationships,
    "compose_timeline": compose_timeline,
    "add_polish": add_polish,
    "set_render_strategy": set_render_strategy,
    "open_risk": open_risk,
    "validate_corpus": validate_corpus,
    "commit_decision": commit_decision,
    "compile_pradd": compile_pradd,
}
