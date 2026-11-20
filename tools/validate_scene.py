"""Validate metadata contract v0 without Blender or third-party libraries."""
import json
import math
import sys
from pathlib import Path

KINDS = {"player_spawn", "ring", "spring", "checkpoint", "enemy", "goal", "camera_anchor", "prop"}

def validate(scene):
    if not isinstance(scene, dict) or set(scene) != {"version", "units", "axes", "entities"}:
        raise ValueError("invalid scene keys")
    if type(scene["version"]) is not int or scene["version"] != 0:
        raise ValueError("unsupported version")
    if scene["units"] != "m" or scene["axes"] != "RH_Z_UP":
        raise ValueError("unsupported coordinate convention")
    if not isinstance(scene["entities"], list):
        raise ValueError("entities must be an array")
    seen = set()
    for entity in scene["entities"]:
        if not isinstance(entity, dict) or set(entity) != {"id", "kind", "position"}:
            raise ValueError("invalid entity keys")
        ident = entity["id"]
        if not isinstance(ident, str) or not ident.strip() or ident in seen:
            raise ValueError("invalid or duplicate entity id")
        seen.add(ident)
        kind = entity["kind"]
        if not isinstance(kind, str) or kind not in KINDS:
            raise ValueError("unknown entity kind")
        pos = entity["position"]
        if not isinstance(pos, list) or len(pos) != 3 or any(type(v) not in (int, float) or abs(v) > 1e9 or not math.isfinite(v) for v in pos):
            raise ValueError("invalid position")
    return len(seen)

def main():
    if len(sys.argv) != 2:
        print("usage: validate_scene.py SCENE.json", file=sys.stderr)
        return 2
    try:
        count = validate(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"valid scene metadata: {count} entities")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
