# Intermediate scene contract v0

This is an authoring metadata contract, not a Saturn binary format. Geometry, collision data and textures are intentionally not implemented in v0. Coordinates are right-handed Blender world XYZ (Z up), metres; conversion into SDK coordinates must be explicit and validated with an asymmetric fixture. Entity positions are finite triples. IDs are stable unique strings across all entities. Version integer 0. Unknown top-level and entity keys are rejected for now. JSON uses UTF-8.

Required top-level keys: version, units ("m"), axes ("RH_Z_UP"), entities (array).
Each entity has id, kind, position. Kinds: player_spawn, ring, spring, checkpoint, enemy, goal, camera_anchor, prop. Game-specific semantics can extend the contract in a later version; no game-specific code in the generic validator.

Future versions must specify transforms, sector ownership, render and collision references, surface flags, materials, UVs, dependency hashes and format negotiation. A validation pass does not imply that a scene fits hardware.
