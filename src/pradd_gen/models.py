"""
Pydantic models for the PRADD generation workflow.
These models define the structure and validation for all data artifacts,
including the context capsule and the various corpus files.
"""

from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field, constr, conint, confloat

# Regex patterns from schemas
BEAT_ID_PATTERN = r'^B-\d{3}$'
SCENE_ID_PATTERN = r'^S-\d{3}$'
OBJECT_ID_PATTERN = r'^O-\d{4}$'
ANIM_ID_PATTERN = r'^A-\d{4}$'
REL_ID_PATTERN = r'^R-\d{4}$'
CAM_ID_PATTERN = r'^C-\d{4}$'
TIMELINE_ITEM_PATTERN = r'^(A|R|C)-\d{4}$'

# --- Context Capsule Models ---

class Project(BaseModel):
    project_id: str
    title: str
    target_runtime_s: float
    fps: int
    version: str  # PRADD workflow spec version

class Phase(BaseModel):
    name: str  # e.g., "layout", "animations"
    attempt: int
    scene_id: Optional[str] = Field(None, pattern=SCENE_ID_PATTERN)

class CorpusSnapshot(BaseModel):
    north_star: Dict[str, Any]
    beats: Dict[str, Any]
    objects: Dict[str, Any]
    geometry: Dict[str, Any]
    animations: Dict[str, Any]
    relationships: Dict[str, Any]
    timeline: Dict[str, Any]
    camera: Dict[str, Any]
    polish: Dict[str, Any]
    rendering: Dict[str, Any]
    glossary: Dict[str, Any]
    risks: Dict[str, Any]
    decisions: List[Dict[str, Any]]

class IDPrefixes(BaseModel):
    beat: str = "B-"
    scene: str = "S-"
    object: str = "O-"
    anim: str = "A-"
    rel: str = "R-"
    cam: str = "C-"

class IDs(BaseModel):
    prefixes: IDPrefixes
    counters: Dict[str, int]

class ComplexityBudget(BaseModel):
    max_parallel_per_beat: int = 6

class Policy(BaseModel):
    style_token_policy: str
    overlap_policy: str
    complexity_budget: ComplexityBudget

class ManimPrimitives(BaseModel):
    animations: List[str]
    composition: List[str]
    dynamics: List[str]
    camera_actions: List[str]

class ManimProfile(BaseModel):
    manim_version: str
    flavor: Literal["ManimCE"]
    modes: List[Literal["cairo", "opengl", "2d", "3d"]]
    primitives: ManimPrimitives

class ContextCapsule(BaseModel):
    project: Project
    phase: Phase
    corpus_snapshot: CorpusSnapshot
    ids: IDs
    policy: Policy
    manim_profile: ManimProfile


# --- Data Artifact Models ---

class Beat(BaseModel):
    beat_id: constr(pattern=BEAT_ID_PATTERN)
    scene_id: constr(pattern=SCENE_ID_PATTERN)
    goal: str
    summary: str
    success_criteria: List[str]
    estimated_duration: confloat(min=0.1)

class Beats(BaseModel):
    fps: conint(ge=12, le=120)
    beats: List[Beat]

class ManimObject(BaseModel):
    object_id: constr(pattern=OBJECT_ID_PATTERN)
    name: str
    type: Literal["Text", "MathTex", "VMobject", "SVGMobject", "ImageMobject", "Axes", "NumberPlane", "Graph", "Other"]
    tags: List[str]
    beats_used_in: List[constr(pattern=BEAT_ID_PATTERN)]
    properties: Dict[str, Any]

class Objects(BaseModel):
    objects: List[ManimObject]

class Position(BaseModel):
    x: float
    y: float
    scale: confloat(min=0.01)
    rotation: float # radians

class Placement(BaseModel):
    object_id: constr(pattern=OBJECT_ID_PATTERN)
    position: Position
    z: int
    group: Optional[str] = None

class Frame(BaseModel):
    beat_id: constr(pattern=BEAT_ID_PATTERN)
    placements: List[Placement]

class Geometry(BaseModel):
    frames: List[Frame]

class AnimationParams(BaseModel):
    run_time: Optional[confloat(min=0.05)] = None
    lag_ratio: Optional[confloat(ge=0, le=1)] = None
    rate_func: Optional[str] = None
    path: Optional[constr(pattern=OBJECT_ID_PATTERN)] = None
    angle: Optional[float] = None
    to_state: Optional[str] = None
    notes: Optional[str] = None
    # For additionalProperties: true
    extra_params: Dict[str, Any] = Field(default_factory=dict)

class Animation(BaseModel):
    anim_id: constr(pattern=ANIM_ID_PATTERN)
    beat_id: constr(pattern=BEAT_ID_PATTERN)
    kind: Literal[
        "Create", "Write", "FadeIn", "FadeOut", "Transform", "ReplacementTransform",
        "Rotate", "MoveAlongPath", "GrowFromCenter", "Indicate", "Flash", "Wiggle",
        "Circumscribe", "Custom"
    ]
    targets: List[constr(pattern=OBJECT_ID_PATTERN)]
    params: AnimationParams

class Animations(BaseModel):
    animations: List[Animation]

class Relationship(BaseModel):
    rel_id: constr(pattern=REL_ID_PATTERN)
    beat_id: constr(pattern=BEAT_ID_PATTERN)
    pattern: Literal["always_redraw", "updater", "tracker_binding"]
    spec: Dict[str, Any]

class Relationships(BaseModel):
    relationships: List[Relationship]

class TimelineEntry(BaseModel):
    t_start: float
    t_end: float
    mode: Literal["parallel", "serial"]
    items: List[constr(pattern=TIMELINE_ITEM_PATTERN)]

class SceneTimeline(BaseModel):
    scene_id: constr(pattern=SCENE_ID_PATTERN)
    entries: List[TimelineEntry]

class Timeline(BaseModel):
    timeline: List[SceneTimeline]

class CameraAction(BaseModel):
    cam_id: constr(pattern=CAM_ID_PATTERN)
    scene_id: constr(pattern=SCENE_ID_PATTERN)
    action: Literal["frame_move", "frame_width", "set_euler_angles", "animate_to", "ambient_light", "restore"]
    params: Dict[str, Any]
    t_start: float
    t_end: float

class Camera(BaseModel):
    camera: List[CameraAction]

class Polish(BaseModel):
    polish: List[Dict[str, Any]]

class RenderSection(BaseModel):
    scene_id: constr(pattern=SCENE_ID_PATTERN)
    start: float
    end: float

class RenderPreview(BaseModel):
    scene_id: constr(pattern=SCENE_ID_PATTERN)
    start: float
    end: float

class RenderStrategy(BaseModel):
    renderer: Optional[Literal["cairo", "opengl"]] = None
    quality: Optional[Literal["ql", "qm", "qh"]] = "ql"
    sections: Optional[List[RenderSection]] = None
    previews: Optional[List[RenderPreview]] = None
    cache: Optional[bool] = True
    extra_strategy: Dict[str, Any] = Field(default_factory=dict)

class Rendering(BaseModel):
    strategy: RenderStrategy

class Risk(BaseModel):
    title: str
    risk_level: Literal["low", "medium", "high"]
    owner: str
    mitigation: str

class Risks(BaseModel):
    risks: List[Risk]

class GlossaryTerm(BaseModel):
    term: str
    definition: str

class Glossary(BaseModel):
    tokens: Optional[Dict[str, Any]] = None
    terms: Optional[List[GlossaryTerm]] = None
