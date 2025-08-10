You enumerate canonical objects used across beats. Do not duplicate semantic objects under different IDs without rationale.

Tool: catalog_objects

Your output must be a single JSON object with one top-level key: "objects".
The "objects" key must contain a list of object definitions. Each object definition must adhere to the following schema:
- `object_id` (string): A unique ID for the object, in the format "O-XXXX" (e.g., "O-0010", "O-0020").
- `name` (string): A human-readable name for the object (e.g., "Main Title Text").
- `type` (string): The Manim object type. Must be one of: "Text", "MathTex", "VMobject", "SVGMobject", "ImageMobject", "Axes", "NumberPlane", "Graph", "Other".
- `tags` (list of strings): A list of tags for categorization.
- `beats_used_in` (list of strings): A list of beat IDs (e.g., "B-010", "B-020") where this object appears.
- `properties` (object): An object containing style properties that reference tokens from the North Star/Glossary (e.g., `{"color": "brand.primary"}`).

Example of a valid object definition:
```json
{
  "object_id": "O-0011",
  "name": "Sine Curve Graph",
  "type": "VMobject",
  "tags": ["function", "plot"],
  "beats_used_in": ["B-010", "B-020"],
  "properties": {
    "color": "brand.primary",
    "stroke_width": "stroke.sm"
  }
}
```

Validation: all beat IDs referenced must exist. All style items must be tokens from North Star/Glossary.
