import json
from pathlib import Path
from typing import Dict, Any

CORPUS_DIR = Path("pradd_corpus")
OUTPUT_FILE = Path("PRADD.md")

def _load_json_or_default(filename: str, default: Dict = None) -> Dict:
    """Safely loads a JSON file from the corpus, returning a default if it doesn't exist."""
    filepath = CORPUS_DIR / filename
    if not filepath.exists():
        return default if default is not None else {}
    with open(filepath, "r") as f:
        return json.load(f)

def _load_md_or_default(filename: str, default: str = "") -> str:
    """Safely loads a Markdown file from the corpus."""
    filepath = CORPUS_DIR / filename
    if not filepath.exists():
        return default
    with open(filepath, "r") as f:
        return f.read()

def _format_objects_table(data: Dict) -> str:
    """Formats the object catalog into a Markdown table."""
    lines = ["| O-ID | Name | Type | Properties | Beats Used In |", "|---|---|---|---|---|"]
    for obj in data.get("objects", []):
        props = json.dumps(obj.get("properties", {}))
        beats = ", ".join(obj.get("beats_used_in", []))
        lines.append(f"| {obj.get('object_id')} | {obj.get('name')} | {obj.get('type')} | `{props}` | {beats} |")
    return "\n".join(lines)

def _format_beats_table(data: Dict) -> str:
    """Formats the story map into a Markdown table."""
    lines = ["| Beat ID | Scene ID | Duration (s) | Goal |", "|---|---|---|---|"]
    for beat in data.get("beats", []):
        lines.append(f"| {beat.get('beat_id')} | {beat.get('scene_id')} | {beat.get('estimated_duration')} | {beat.get('goal')} |")
    return "\n".join(lines)

def _format_animations_table(data: Dict) -> str:
    """Formats the animation plan into a Markdown table."""
    lines = ["| A-ID | Beat ID | Kind | Targets | Parameters |", "|---|---|---|---|---|"]
    for anim in data.get("animations", []):
        targets = ", ".join(anim.get("targets", []))
        params = json.dumps(anim.get("params", {}))
        lines.append(f"| {anim.get('anim_id')} | {anim.get('beat_id')} | {anim.get('kind')} | {targets} | `{params}` |")
    return "\n".join(lines)

def run_compilation(include_appendices: bool = True):
    """
    Generates the final PRADD.md document from the corpus artifacts.
    """
    print("\n--- Compiling PRADD.md ---")

    # Load all data
    north_star = _load_md_or_default("north_star.md", default="# North Star\n*Not yet generated.*")
    beats = _load_json_or_default("beats.json")
    objects = _load_json_or_default("objects.json")
    animations = _load_json_or_default("animations.json")
    # Add other files as needed for other sections...
    risks = _load_json_or_default("risks.json")
    decision_log = _load_md_or_default("decision_log.md", default="*No decisions logged.*")

    # Start building the document
    doc = ["# PRADD: Production-Ready Animation Design Document"]

    # 1. Title & Summary (part of North Star)
    # 2. North Star
    doc.append(north_star)

    # 3. Global Constraints (part of North Star)

    # 4. Story Map
    doc.append("## 4. Story Map (Beats & Scenes)")
    doc.append(_format_beats_table(beats))

    # 5. Object Catalog
    doc.append("## 5. Object Catalog")
    doc.append(_format_objects_table(objects))

    # 6. Layout Plan (For brevity, we'll just link to the appendix for now)
    doc.append("## 6. Layout Plan\n*See `geometry.json` in appendices.*")

    # 7. Animation Plan
    doc.append("## 7. Animation Plan")
    doc.append(_format_animations_table(animations))

    # ... Skipping other sections for brevity in this initial implementation ...
    # A full implementation would add sections 8-11 here.

    # 12. Risks & Assumptions
    doc.append("## 12. Risks & Assumptions")
    risk_lines = ["| Level | Owner | Title | Mitigation |", "|---|---|---|---|"]
    for risk in risks.get("risks", []):
        risk_lines.append(f"| {risk.get('risk_level')} | {risk.get('owner')} | {risk.get('title')} | {risk.get('mitigation')} |")
    doc.append("\n".join(risk_lines))

    # 13. Decision Log
    doc.append("## 13. Decision Log")
    doc.append(decision_log)

    # 14. Appendices
    if include_appendices:
        doc.append("\n---\n## 14. Appendices (Raw Artifacts)")
        for file in sorted(CORPUS_DIR.glob("*.json")):
            doc.append(f"\n### `{file.name}`")
            doc.append(f"```json\n{file.read_text()}\n```")

    # Write the final document
    final_content = "\n\n".join(doc)
    with open(OUTPUT_FILE, "w") as f:
        f.write(final_content)

    print(f"--- Compilation Complete ---")
    print(f"SUCCESS: PRADD.md has been generated.")

if __name__ == '__main__':
    run_compilation()
