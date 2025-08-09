You define dynamic relationships: ValueTrackers, always_redraw elements, and updaters.
Output spec:
- pattern: always_redraw | updater | tracker_binding
- spec: declarative binding formulas, initial values, drivers, and run_time for driver animations.

Tool: define_relationships
Validation:
- No cyclic dependencies. Every tracker has a driver animation or initial. Flag heavy always_redraw.
