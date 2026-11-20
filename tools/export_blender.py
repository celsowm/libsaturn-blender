"""Usage: blender -b SCENE.blend --python-exit-code 1 --python tools/export_blender.py -- out/scene.json"""
import sys
from pathlib import Path
import bpy
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from libsaturn_toolkit.exporter import export_bundle

if __name__ == "__main__":
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if len(args) != 1:
        raise SystemExit("expected one output JSON path after --")
    for path in export_bundle(bpy.context, args[0]):
        print(path)
