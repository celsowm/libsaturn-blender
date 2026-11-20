"""LibSaturn Toolkit — initial Blender authoring addon."""
bl_info = {
    "name": "LibSaturn Toolkit",
    "author": "LibSaturn contributors",
    "version": (0, 1, 0),
    "blender": (4, 0, 0),
    "location": "3D View > Sidebar > Saturn",
    "description": "Author and export Saturn scene metadata and greybox meshes",
    "category": "Import-Export",
}

def register():
    from . import addon
    addon.register()

def unregister():
    from . import addon
    addon.unregister()
