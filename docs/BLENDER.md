# Blender authoring workflow

Target Blender 4.x or later (qualification pending). Build an installable ZIP with python tools/package_addon.py. In Blender Preferences > Add-ons use Install from Disk (legacy addon), select dist/libsaturn_toolkit.zip and enable it. Open the 3D View sidebar (N) > Saturn. Mark an active object as an entity or mesh; duplicated entities retain their ID until explicitly regenerated and will fail export. Export scene writes JSON and two OBJ files (render and collision). Only explicitly tagged meshes are exported; scene objects outside the active view layer are not a supported authoring configuration yet.

Headless:
```sh
blender --background project.blend --python-exit-code 1 --python tools/export_blender.py -- build/scene.json
blender --background --factory-startup --python-exit-code 1 --python tests/blender_smoke.py
```

The OBJ files contain evaluated triangles/quads in Blender world metres, RH Z-up, with negative-scale winding corrected. This is intermediate **untextured greybox** output, not a hardware-ready file. N-gons fail instead of silently changing topology. Materials, UVs, planarity checks, mirrored-winding qualification, instances, sector/HLOD conversion and SDK coordinate adapter are future work. Do not pass these files to a runtime loader. SDK references: tools/import_model.py, examples/basic_3d_texture/Makefile.inc, tools/build_world_hlod_demo.py and examples/world_lod3d_demo/Makefile.inc. Inspect exact converter flags and axes before baking. No duplicate hardware importer.

MCP setup: install a trusted Blender MCP server in the local harness following its upstream instructions (e.g. https://github.com/ahujasid/mcp-for-blender). Restrict to localhost; use isolated original assets, no auto-executed third-party code. Once connected, the agent may use bpy to assign saturn_id, saturn_kind and saturn_mesh, inspect the scene and save the .blend file. Build/export still runs headlessly with no MCP. No MCP server installation is performed by this repository.
