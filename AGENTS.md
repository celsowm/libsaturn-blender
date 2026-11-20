# Agent instructions

- Read docs/ROADMAP.md and docs/SCENE_CONTRACT.md first.
- Inspect the pinned LibSaturn public headers, tools and examples before adding adapters. Do not invent SDK APIs.
- Keep Blender-dependent code separate from Python-only validation and conversion. MCP is an optional authoring interface, not a build dependency.
- Never run arbitrary third-party scripts or import untrusted .blend files with auto-execution enabled.
- Use original synthetic fixtures. Track provenance and licenses; do not commit commercial game assets.
- Deterministic exports, stable IDs, explicit units, bounded memory, test malformed inputs.
- Report host, Blender, emulator and real hardware evidence separately. Never claim 30 FPS from a design target.
- Run python -m unittest discover -s tests before commits. Record commands, tool versions and hashes.
