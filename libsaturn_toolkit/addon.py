"""Optional interactive Blender UI. Headless scripts use exporter directly."""
import uuid
import bpy
from bpy.props import EnumProperty, StringProperty
from bpy_extras.io_utils import ExportHelper
from .contract import KINDS
from .exporter import export_bundle

class SATURN_OT_mark_entity(bpy.types.Operator):
    bl_idname = "saturn.mark_entity"
    bl_label = "Mark entity"
    bl_options = {"UNDO"}
    kind: EnumProperty(items=[(kind, kind.replace("_", " ").title(), "") for kind in KINDS])
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    def execute(self, context):
        obj = context.active_object
        if not obj.get("saturn_id"):
            obj["saturn_id"] = uuid.uuid4().hex
        obj["saturn_kind"] = self.kind
        return {"FINISHED"}
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class SATURN_OT_mark_mesh(bpy.types.Operator):
    bl_idname = "saturn.mark_mesh"
    bl_label = "Mark mesh role"
    bl_options = {"UNDO"}
    role: EnumProperty(items=[("render", "Render", ""), ("collision", "Collision", ""), ("none", "Clear", "")])
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == "MESH"
    def execute(self, context):
        obj = context.active_object
        if self.role == "none":
            if "saturn_mesh" in obj:
                del obj["saturn_mesh"]
        else:
            obj["saturn_mesh"] = self.role
        return {"FINISHED"}
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class SATURN_OT_regenerate_id(bpy.types.Operator):
    bl_idname = "saturn.regenerate_id"
    bl_label = "Assign new entity ID"
    bl_options = {"UNDO"}
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.get("saturn_kind") is not None
    def execute(self, context):
        context.active_object["saturn_id"] = uuid.uuid4().hex
        return {"FINISHED"}

class SATURN_OT_clear_entity(bpy.types.Operator):
    bl_idname = "saturn.clear_entity"
    bl_label = "Clear entity"
    bl_options = {"UNDO"}
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    def execute(self, context):
        for key in ("saturn_kind", "saturn_id"):
            if key in context.active_object:
                del context.active_object[key]
        return {"FINISHED"}

class SATURN_OT_export(bpy.types.Operator, ExportHelper):
    bl_idname = "saturn.export_scene"
    bl_label = "Export Saturn scene"
    filename_ext = ".json"
    filter_glob: StringProperty(default="*.json", options={"HIDDEN"})
    def execute(self, context):
        try:
            paths = export_bundle(context, self.filepath)
        except (ValueError, OSError, RuntimeError) as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        self.report({"INFO"}, f"Exported {len(paths)} authoring files")
        return {"FINISHED"}

class SATURN_PT_tools(bpy.types.Panel):
    bl_label = "LibSaturn Toolkit"
    bl_idname = "SATURN_PT_tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Saturn"
    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        if obj:
            layout.label(text=f"Entity: {obj.get('saturn_kind', 'unmarked')}")
            layout.label(text=f"Mesh: {obj.get('saturn_mesh', 'unmarked')}")
            layout.operator("saturn.mark_entity")
            layout.operator("saturn.regenerate_id")
            layout.operator("saturn.clear_entity")
            layout.operator("saturn.mark_mesh")
        layout.operator("saturn.export_scene")

CLASSES = (SATURN_OT_mark_entity, SATURN_OT_mark_mesh, SATURN_OT_regenerate_id, SATURN_OT_clear_entity, SATURN_OT_export, SATURN_PT_tools)
def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)
def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
