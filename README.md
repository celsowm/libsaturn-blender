# LibSaturn Blender Toolkit

A reusable, hardware-aware authoring pipeline for Sega Saturn games built with [LibSaturn](https://github.com/celsowm/libsaturn).

**Status:** bootstrap; no production exporter or Blender integration qualified yet.

## Quick start
Run the standalone contract tests (Python 3.10+):
```sh
python -m unittest discover -s tests
python tools/validate_scene.py examples/fixture.scene.json
```

The canonical build must work headlessly, without MCP. Use a sibling LibSaturn checkout or installed SDK. The Blender addon will author semantic scene metadata; existing LibSaturn converters remain responsible for hardware-ready payloads.

- [Architecture and roadmap](docs/ROADMAP.md)
- [Scene contract v0](docs/SCENE_CONTRACT.md)
- [Agent instructions](AGENTS.md)
- [First consumer: Sonic X-treme: Lost Adventure](https://github.com/celsowm/sonic-xtreme-saturn)

Only original or explicitly licensed fixtures belong in this repository. No commercial game assets, BIOS or ROM files.
