"""Blender-dependent world-space authoring export. No hardware baking here."""
import math
import re
from pathlib import Path
from .contract import canonical_bytes

def _number(value):
    if not math.isfinite(value) or abs(value) > 1e9:
        raise ValueError("non-finite or out-of-range coordinate")
    result = round(float(value), 6)
    return 0.0 if result == 0 else result

def _point(vec, scale):
    return [_number(value * scale) for value in vec]

def collect(context):
    scene = context.scene
    scale = float(scene.unit_settings.scale_length)
    if not math.isfinite(scale) or scale <= 0:
        raise ValueError("invalid scene unit scale")
    depsgraph = context.evaluated_depsgraph_get()
    entities = []
    mesh_rows = []
    for obj in sorted(scene.objects, key=lambda value: value.name):
        kind = obj.get("saturn_kind")
        ident = obj.get("saturn_id")
        role = obj.get("saturn_mesh")
        if kind is None and ident is not None:
            raise ValueError(f"{obj.name}: ID without entity kind")
        if kind is not None:
            evaluated = obj.evaluated_get(depsgraph)
            entities.append({"id": ident, "kind": kind, "position": _point(evaluated.matrix_world.translation, scale)})
        if role is not None:
            if role not in ("render", "collision"):
                raise ValueError(f"{obj.name}: unknown mesh role")
            if obj.type != "MESH":
                raise ValueError(f"{obj.name}: mesh role requires mesh")
            evaluated = obj.evaluated_get(depsgraph)
            matrix = evaluated.matrix_world
            det = matrix.to_3x3().determinant()
            if not math.isfinite(det) or abs(det) < 1e-12:
                raise ValueError(f"{obj.name}: singular transform")
            mesh = evaluated.to_mesh()
            try:
                vertices = [_point(matrix @ vertex.co, scale) for vertex in mesh.vertices]
                faces = []
                for polygon in mesh.polygons:
                    face = list(polygon.vertices)
                    if len(face) not in (3, 4) or len(set(face)) != len(face):
                        raise ValueError(f"{obj.name}: greybox faces must be triangles or quads")
                    if det < 0:
                        face.reverse()
                    faces.append(face)
                mesh_rows.append((role, obj.name, vertices, faces))
            finally:
                evaluated.to_mesh_clear()
    return canonical_bytes(entities), mesh_rows

def obj_bytes(mesh_rows, role):
    lines = ["# LibSaturn Toolkit greybox; RH Z-up metres; no materials or UVs"]
    offset = 1
    for i, (mesh_role, name, vertices, faces) in enumerate(mesh_rows):
        if mesh_role != role:
            continue
        safe = re.sub(r"[^a-zA-Z0-9_-]", "_", name)
        lines.append(f"o mesh_{i:04d}_{safe}")
        lines.extend("v " + " ".join(f"{v:.6f}" for v in vertex) for vertex in vertices)
        lines.extend("f " + " ".join(str(v + offset) for v in face) for face in faces)
        offset += len(vertices)
    return ("\n".join(lines) + "\n").encode("utf-8")

def export_bundle(context, path):
    """Validate all data before touching output; keep render and collision separate."""
    metadata, meshes = collect(context)
    path = Path(path)
    if path.suffix.lower() != ".json":
        raise ValueError("metadata output requires .json")
    outputs = {
        path: metadata,
        path.with_suffix(".render.obj"): obj_bytes(meshes, "render"),
        path.with_suffix(".collision.obj"): obj_bytes(meshes, "collision"),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    for target, content in outputs.items():
        target.write_bytes(content)
    return tuple(outputs)
