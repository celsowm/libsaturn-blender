"""Run inside Blender background mode."""
import json
import sys
import tempfile
from pathlib import Path
import bpy
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import libsaturn_toolkit
from libsaturn_toolkit.exporter import export_bundle

bpy.ops.wm.read_factory_settings(use_empty=True)
libsaturn_toolkit.register()
try:
    bpy.context.scene.unit_settings.scale_length = 2
    bpy.ops.mesh.primitive_plane_add(size=2)
    obj = bpy.context.object
    obj.location = (1, 2, 3)
    obj.scale.x = -1
    obj["saturn_mesh"] = "render"
    obj["saturn_kind"] = "player_spawn"
    obj["saturn_id"] = "spawn"
    bpy.context.view_layer.update()
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "scene.json"
        outputs = export_bundle(bpy.context, path)
        first = [p.read_bytes() for p in outputs]
        assert json.loads(first[0])["entities"][0]["position"] == [2, 4, 6]
        assert b"f 4 3 2 1" in first[1] or any(line.startswith(b"f ") for line in first[1].splitlines())
        assert b"\nv " not in first[2]
        assert first == [p.read_bytes() for p in export_bundle(bpy.context, path)]
        other = obj.copy()
        bpy.context.collection.objects.link(other)
        bpy.context.view_layer.update()
        try:
            export_bundle(bpy.context, path)
        except ValueError:
            pass
        else:
            raise AssertionError("duplicate IDs accepted")
        assert first == [p.read_bytes() for p in outputs]
finally:
    libsaturn_toolkit.unregister()
print("Blender smoke passed")
