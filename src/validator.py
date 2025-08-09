import json
import yaml
from pathlib import Path
from jsonschema import validate, ValidationError

SCHEMA_DIR = Path("pradd_schemas")
CORPUS_DIR = Path("pradd_corpus")

def load_schemas():
    """Loads all .schema.yaml files from the schema directory."""
    schemas = {}
    for schema_file in SCHEMA_DIR.glob("*.schema.yaml"):
        with open(schema_file, "r") as f:
            # e.g., 'beats.schema.yaml' -> 'beats.json'
            key = schema_file.name.replace(".schema.yaml", ".json")
            schemas[key] = yaml.safe_load(f)
    return schemas

def load_corpus():
    """Loads all .json files from the corpus directory."""
    corpus = {}
    if not CORPUS_DIR.is_dir():
        return corpus, ["Corpus directory not found."]

    for data_file in CORPUS_DIR.glob("*.json"):
        with open(data_file, "r") as f:
            try:
                corpus[data_file.name] = json.load(f)
            except json.JSONDecodeError:
                return None, [f"Invalid JSON in {data_file.name}"]
    return corpus, []

def run_validation(strict: bool = True):
    """
    Runs a full validation suite on the PRADD corpus.

    1. Validates each artifact against its YAML schema.
    2. Performs cross-file consistency checks (Quality Gates).
    """
    print("\n--- Running Corpus Validation ---")
    schemas = load_schemas()
    corpus, errors = load_corpus()
    warnings = []

    if not corpus:
        print("Validation failed: Corpus is empty or could not be loaded.")
        return errors, warnings

    # 1. Schema Validation
    print("Step 1: Validating against schemas...")
    for filename, data in corpus.items():
        if filename in schemas:
            try:
                validate(instance=data, schema=schemas[filename])
                print(f"  - {filename}: OK")
            except ValidationError as e:
                error_msg = f"Schema validation failed for {filename}: {e.message}"
                print(f"  - {filename}: FAILED")
                errors.append(error_msg)
        else:
            warnings.append(f"No schema found for {filename}. Skipping schema validation.")

    # 2. Cross-File Validation (Quality Gates)
    print("Step 2: Performing cross-file consistency checks...")

    # Collect all IDs for easy lookup
    try:
        beat_ids = {b['beat_id'] for b in corpus.get('beats.json', {}).get('beats', [])}
        scene_ids = {b['scene_id'] for b in corpus.get('beats.json', {}).get('beats', [])}
        object_ids = {o['object_id'] for o in corpus.get('objects.json', {}).get('objects', [])}
        anim_ids = {a['anim_id'] for a in corpus.get('animations.json', {}).get('animations', [])}
    except KeyError as e:
        errors.append(f"Could not collect IDs for validation due to missing key: {e}")
        # Stop further validation if basic structure is missing
        return errors, warnings

    # Rule: Every A-#### belongs to exactly one B-###.
    if 'animations.json' in corpus:
        for anim in corpus['animations.json'].get('animations', []):
            if anim.get('beat_id') not in beat_ids:
                errors.append(f"Animation {anim['anim_id']} belongs to non-existent beat {anim['beat_id']}.")

    # Rule: Objects placed before animated; IDs resolvable.
    if 'geometry.json' in corpus:
        for frame in corpus['geometry.json'].get('frames', []):
            for placement in frame.get('placements', []):
                if placement.get('object_id') not in object_ids:
                    errors.append(f"Geometry placement for beat {frame['beat_id']} uses non-existent object {placement['object_id']}.")

    # Rule: Check animation targets exist
    if 'animations.json' in corpus:
        for anim in corpus['animations.json'].get('animations', []):
            for target in anim.get('targets', []):
                if target not in object_ids:
                    errors.append(f"Animation {anim['anim_id']} targets non-existent object {target}.")

    # Rule: Total runtime within ±10% of target (placeholder, needs a target).
    # For now, we just sum the durations.
    if beat_ids:
        total_duration = sum(b.get('estimated_duration', 0) for b in corpus['beats.json']['beats'])
        print(f"  - Calculated total estimated duration: {total_duration:.2f} seconds.")
        # A full implementation would compare this to a target from north_star or similar.

    print(f"--- Validation Complete ---")
    if errors or warnings:
        print(f"Found {len(errors)} errors and {len(warnings)} warnings.")
        for err in errors:
            print(f"  [ERROR] {err}")
        for warn in warnings:
            print(f"  [WARNING] {warn}")
    else:
        print("SUCCESS: Corpus is valid.")

    return errors, warnings

if __name__ == '__main__':
    # Allow running this script directly for testing
    run_validation()
