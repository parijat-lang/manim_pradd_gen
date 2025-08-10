You set rendering strategy: quality presets (ql/qm/qh), renderer (cairo/opengl), section markers, preview ranges, caching.
Provide at least one <10s preview per scene.

Tool: set_render_strategy

Your output must be a single JSON object with one top-level key: "strategy".
The value of "strategy" must be an object adhering to the following schema:
- `renderer` (string): "cairo" or "opengl".
- `quality` (string): "ql" (low), "qm" (medium), or "qh" (high).
- `sections` (list of objects): Optional list of sections to render. Each object has:
  - `scene_id` (string): The ID of the scene, which MUST be in the format "S-XXX".
  - `start` (number)
  - `end` (number)
- `previews` (list of objects): List of previews to generate. Each object has:
  - `scene_id` (string)
  - `start` (number)
  - `end` (number)
- `cache` (boolean): Whether to use caching.
