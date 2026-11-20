# LibSaturn Blender Toolkit

Hardware-aware authoring for Sega Saturn games built with [LibSaturn](https://github.com/celsowm/libsaturn).

**Status:** initial addon and headless authoring exporter; Blender/SDK runtime qualification pending. No production texture or HLOD adapter yet.

```sh
python -m unittest discover -s tests
python tools/validate_scene.py examples/fixture.scene.json
python tools/package_addon.py
```

Install the generated ZIP as a legacy addon, then open the 3D View > Sidebar > Saturn. Tag entities and mesh roles, export JSON plus separate render and collision OBJ. Headless export is independent of MCP. Use original or explicitly licensed assets.

- [Blender workflow and MCP](docs/BLENDER.md)
- [Architecture and roadmap](docs/ROADMAP.md)
- [Scene contract v0](docs/SCENE_CONTRACT.md)
- [Agent instructions](AGENTS.md)
- [First consumer: Sonic X-treme: Lost Adventure](https://github.com/celsowm/sonic-xtreme-saturn)
