# Architecture and roadmap

Baseline inspected: LibSaturn commit af86f8518f0d014f2a752ca43035d2278bc9bf8f. Reference: examples/world_lod3d_demo, include/saturn/scene.h, include/saturn/physics3_world.h, existing OBJ/MTL and GLB tools. Check exact versions before implementation.

## Boundaries
Blender authoring -> canonical intermediate scene -> deterministic offline SDK adapters -> Saturn payload -> game. Blender and MCP edit sources; neither participates in runtime. Do not reinvent texture quantization, mesh baking, skeleton clips, HLOD or disc packing where the SDK already has a working tool.

## Milestones
1. M0: semantic contract v0, original fixtures and validation (bootstrap).
2. M1: Blender addon with scene/collection roles, persistent IDs, entity types, inspector and headless export. Test in a pinned Blender version; run twice and compare checksums. Record actual MCP install instructions after testing.
3. M2: geometry adapter: evaluated meshes, preserve material and UV seams, planarity/winding checks, quad-first output, explicit triangle strategy, texture width/alignment and formats checked against SDK. Validate transforms with an asymmetric fixture.
4. M3: sector partition and HLOD via the existing world_lod3d_demo approach; collision mesh separate, surface tags, adjacency, stable object IDs. Compare silhouettes and seams, preserve gameplay surfaces.
5. M4: texture residency, deterministic pack layout, disc-prefetch hints, measured workload reports (face counts != commands, actual bytes != estimates). Include WRAM-H/L, VDP1 VRAM commands/textures, VDP2 VRAM, sound RAM as distinct pools. No required RAM cart.
6. M5: animation and model adapter through existing GLB tooling; distinguish CPU skinning, pre-baked poses, bounds and memory cost. Camera paths and triggers exported independently.
7. M6: Sonic vertical slice acceptance, Ymir/Mednafen screenshots and metrics; physical Saturn separately. Return generic runtime improvements upstream via focused tests.

## MCP
Evaluate official Blender MCP and community integrations for the installed harness. Keep credentials out of version control; localhost only, isolated project directory, no remote script execution. An agent edits via MCP, exports using a reviewed script and checks reports. CI uses headless Blender, never an MCP connection.

## Acceptance
Byte-identical repeated exports for pinned inputs/tools, deterministic IDs, strict limits, clear errors, reproducible manifests with source hashes, no hidden asset downloads. Budget thresholds are provisional until the console benchmark establishes them.
