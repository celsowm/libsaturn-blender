"""Validate metadata contract v0 without Blender or third-party libraries."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from libsaturn_toolkit.contract import validate, KINDS

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
