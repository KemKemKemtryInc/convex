# ---------------------------------------------------------------------------------------------
#  Copyright (c) 2024 KemKemKemtryInc. All rights reserved.
#  Licensed under the MIT License. See License.md in the project root for license information.
# --------------------------------------------------------------------------------------------

import bpy
import importlib

from bpy.props import (
        FloatProperty,
        IntProperty,
        BoolProperty,
        EnumProperty,
        )


# from . import helper
from . import convex

bl_info = {
    "name": "convex",
    "author": "KemKemKemtry",
    "version": (1, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Add > Mesh > Add Convex",
    "description": "Add a convex surface.",
    "warning": "",
    "category": "Add Mesh"
}


def menu_func(self, context):
    layout = self.layout
    layout.separator()
    layout.operator_context = "INVOKE_DEFAULT"
    layout.operator(convex.MESH_OT_add_convex.bl_idname, text="Add Convex surface")

def register():    
    importlib.reload(convex)
    bpy.utils.register_class(convex.MESH_OT_add_convex)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(menu_func) 


def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(menu_func)
    bpy.utils.unregister_class(convex.MESH_OT_add_convex)
  
if __name__ == "__main__": 
    register()
