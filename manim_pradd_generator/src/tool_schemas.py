# This file stores the raw tool definitions as described in the PRD.
# It will be used by the utility functions to generate schemas for the LLM.

TOOLS_PRD = {
    "register_north_star": {
        "description": "Create/replace the vision & style bible.",
        "args_schema": {
            "type": "object",
            "required": ["context", "purpose", "audience", "tone", "style_tokens", "motion_grammar", "constraints", "references"],
            "properties": {
                "context": { "$ref": "context_capsule.schema.yaml" },
                "purpose": { "type": "string" },
                "audience": { "type": "string" },
                "tone": { "type": "string" },
                "style_tokens": { "type": "object", "additionalProperties": True },
                "motion_grammar": { "type": "array", "items": { "type": "string" } },
                "constraints": { "type": "array", "items": { "type": "string" } },
                "references": { "type": "array", "items": { "type": "string" } }
            }
        }
    },
    "write_beats": {
        "description": "Create or update beats & scenes map.",
        "args_schema": {
            "type": "object",
            "required": ["context", "fps", "beats"],
            "properties": {
                "context": { "$ref": "context_capsule.schema.yaml" },
                "fps": { "type": "integer", "minimum": 12, "maximum": 120 },
                "beats": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["beat_id", "scene_id", "goal", "summary", "success_criteria", "estimated_duration"],
                        "properties": {
                            "beat_id": { "type": "string", "pattern": "^B-\\d{3}$" },
                            "scene_id": { "type": "string", "pattern": "^S-\\d{3}$" },
                            "goal": { "type": "string" },
                            "summary": { "type": "string" },
                            "success_criteria": { "type": "array", "items": { "type": "string" } },
                            "estimated_duration": { "type": "number", "minimum": 0.1 }
                        }
                    }
                }
            }
        }
    },
    "catalog_objects": {
        "description": "Define canonical objects (mobject intents).",
        "args_schema": {
            "type": "object",
            "required": ["context", "objects"],
            "properties": {
                "context": { "$ref": "context_capsule.schema.yaml" },
                "objects": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["object_id", "name", "type", "tags", "beats_used_in", "properties"],
                        "properties": {
                            "object_id": { "type": "string", "pattern": "^O-\\d{4}$" },
                            "name": { "type": "string" },
                            "type": { "type": "string", "enum": ["Text", "MathTex", "VMobject", "SVGMobject", "ImageMobject", "Axes", "NumberPlane", "Graph", "Other"] },
                            "tags": { "type": "array", "items": { "type": "string" } },
                            "beats_used_in": { "type": "array", "items": { "type": "string", "pattern": "^B-\\d{3}$" } },
                            "properties": { "type": "object", "additionalProperties": True }
                        }
                    }
                }
            }
        }
    },
    "plan_geometry": {
        "description": "Layout and coordinates per beat.",
        "args_schema": {
            "type": "object",
            "required": ["context", "frames"],
            "properties": {
                "context": { "$ref": "context_capsule.schema.yaml" },
                "frames": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["beat_id", "placements"],
                        "properties": {
                            "beat_id": { "type": "string", "pattern": "^B-\\d{3}$" },
                            "placements": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "required": ["object_id", "position", "z", "group"],
                                    "properties": {
                                        "object_id": { "type": "string", "pattern": "^O-\\d{4}$" },
                                        "position": {
                                            "type": "object",
                                            "required": ["x", "y", "scale", "rotation"],
                                            "properties": {
                                                "x": { "type": "number" },
                                                "y": { "type": "number" },
                                                "scale": { "type": "number", "minimum": 0.01 },
                                                "rotation": { "type": "number" }
                                            }
                                        },
                                        "z": { "type": "integer" },
                                        "group": { "type": "string", "nullable": True }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    "design_animations": {
        "description": "Per-beat transforms & effects.",
        "args_schema": {
            "type": "object",
            "required": ["context", "animations"],
            "properties": {
                "context": { "$ref": "context_capsule.schema.yaml" },
                "animations": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["anim_id", "beat_id", "kind", "targets", "params"],
                        "properties": {
                            "anim_id": { "type": "string", "pattern": "^A-\\d{4}$" },
                            "beat_id": { "type": "string", "pattern": "^B-\\d{3}$" },
                            "kind": { "type": "string", "enum": ["Create", "Write", "FadeIn", "FadeOut", "Transform", "ReplacementTransform", "Rotate", "MoveAlongPath", "GrowFromCenter", "Indicate", "Flash", "Wiggle", "Circumscribe", "Custom"] },
                            "targets": { "type": "array", "items": { "type": "string", "pattern": "^O-\\d{4}$" } },
                            "params": {
                                "type": "object",
                                "properties": {
                                    "run_time": { "type": "number", "minimum": 0.05 },
                                    "lag_ratio": { "type": "number", "minimum": 0, "maximum": 1 },
                                    "rate_func": { "type": "string" },
                                    "path": { "type": "string", "pattern": "^O-\\d{4}$" },
                                    "angle": { "type": "number" },
                                    "to_state": { "type": "string" },
                                    "notes": { "type": "string" }
                                },
                                "additionalProperties": True
                            }
                        }
                    }
                }
            }
        }
    },
    "define_relationships": {
        "description": "ValueTrackers, updaters, always_redraw, bindings.",
        "args_schema": {
            "type": "object",
            "required": ["context", "relationships"],
            "properties": {
                "context": { "$ref": "context_capsule.schema.yaml" },
                "relationships": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["rel_id", "beat_id", "pattern", "spec"],
                        "properties": {
                            "rel_id": { "type": "string", "pattern": "^R-\\d{4}$" },
                            "beat_id": { "type": "string", "pattern": "^B-\\d{3}$" },
                            "pattern": { "type": "string", "enum": ["always_redraw", "updater", "tracker_binding"] },
                            "spec": { "type": "object", "additionalProperties": True }
                        }
                    }
                }
            }
        }
    },
    "compose_timeline": {
        "description": "Ordering, groups, waits, and camera cues.",
        "args_schema": {
            "type": "object",
            "required": ["context", "timeline", "camera"],
            "properties": {
                "context": { "$ref": "context_capsule.schema.yaml" },
                "timeline": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["scene_id", "entries"],
                        "properties": {
                            "scene_id": { "type": "string", "pattern": "^S-\\d{3}$" },
                            "entries": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "required": ["t_start", "t_end", "mode", "items"],
                                    "properties": {
                                        "t_start": { "type": "number" },
                                        "t_end": { "type": "number" },
                                        "mode": { "type": "string", "enum": ["parallel", "serial"] },
                                        "items": { "type": "array", "items": { "type": "string", "pattern": "^(A|R|C)-\\d{4}$" } }
                                    }
                                }
                            }
                        }
                    }
                },
                "camera": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["cam_id", "scene_id", "action", "params", "t_start", "t_end"],
                        "properties": {
                            "cam_id": { "type": "string", "pattern": "^C-\\d{4}$" },
                            "scene_id": { "type": "string", "pattern": "^S-\\d{3}$" },
                            "action": { "type": "string", "enum": ["frame_move", "frame_width", "set_euler_angles", "animate_to", "ambient_light", "restore"] },
                            "params": { "type": "object", "additionalProperties": True },
                            "t_start": { "type": "number" },
                            "t_end": { "type": "number" }
                        }
                    }
                }
            }
        }
    },
    "add_polish": {
        "description": "Micro-effects, transitions, accessibility notes.",
        "args_schema": {
            "type": "object",
            "required": ["context", "polish"],
            "properties": {
                "context": { "$ref": "context_capsule.schema.yaml" },
                "polish": { "type": "array", "items": { "type": "object", "additionalProperties": True } }
            }
        }
    },
    "set_render_strategy": {
        "description": "Render quality, sections, previews.",
        "args_schema": {
            "type": "object",
            "required": ["context", "strategy"],
            "properties": {
                "context": { "$ref": "context_capsule.schema.yaml" },
                "strategy": {
                    "type": "object",
                    "properties": {
                        "renderer": { "type": "string", "enum": ["cairo", "opengl"] },
                        "quality": { "type": "string", "enum": ["ql", "qm", "qh"], "default": "ql" },
                        "sections": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["scene_id", "start", "end"],
                                "properties": {
                                    "scene_id": { "type": "string", "pattern": "^S-\\d{3}$" },
                                    "start": { "type": "number" },
                                    "end": { "type": "number" }
                                }
                            }
                        },
                        "previews": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["scene_id", "start", "end"],
                                "properties": {
                                    "scene_id": { "type": "string", "pattern": "^S-\\d{3}$" },
                                    "start": { "type": "number" },
                                    "end": { "type": "number" }
                                }
                            }
                        },
                        "cache": { "type": "boolean", "default": True }
                    },
                    "additionalProperties": True
                }
            }
        }
    },
    "open_risk": {
        "description": "Track assumptions/open questions.",
        "args_schema": {
            "type": "object",
            "required": ["context", "title", "risk_level", "owner", "mitigation"],
            "properties": {
                "context": { "$ref": "context_capsule.schema.yaml" },
                "title": { "type": "string" },
                "risk_level": { "type": "string", "enum": ["low", "medium", "high"] },
                "owner": { "type": "string" },
                "mitigation": { "type": "string" }
            }
        }
    },
    "validate_corpus": {
        "description": "Run cross-file checks; return errors/warnings.",
        "args_schema": {
            "type": "object",
            "required": ["context"],
            "properties": {
                "context": { "$ref": "context_capsule.schema.yaml" },
                "strict": { "type": "boolean", "default": False }
            }
        }
    },
    "commit_decision": {
        "description": "Record a conflict resolution decision with patches.",
        "args_schema": {
            "type": "object",
            "required": ["context", "summary", "patches"],
            "properties": {
                "context": { "$ref": "context_capsule.schema.yaml" },
                "summary": { "type": "string" },
                "patches": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["file", "path", "op", "value"],
                        "properties": {
                            "file": { "type": "string" },
                            "path": { "type": "string" },
                            "op": { "type": "string", "enum": ["add", "replace", "remove"] },
                            "value": {}
                        }
                    }
                }
            }
        }
    },
    "compile_pradd": {
        "description": "Generate PRADD.md from the corpus.",
        "args_schema": {
            "type": "object",
            "required": ["context"],
            "properties": {
                "context": { "$ref": "context_capsule.schema.yaml" },
                "include_appendices": { "type": "boolean", "default": True }
            }
        }
    }
}
