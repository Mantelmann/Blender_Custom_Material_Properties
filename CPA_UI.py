import bpy
import sys
import os

from bpy.props import (StringProperty,
                       IntProperty,
                       FloatProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)
    #print(sys.path)

import CPA_functions

import importlib
importlib.reload(CPA_functions)


class nbProperties(PropertyGroup):
    
        property_name: bpy.props.StringProperty(
        name = "Property Name",
        description = "Name of selected Property"
    )
    
        material_name: bpy.props.StringProperty(
        name = "Material Name",
        description = "Wil select all objects with this material"
    )






class setupProperties(Operator):
    bl_label = "Setup Custom Property for this Object"
    bl_description = "Prepare Custom Property for Material use"
    bl_info = "Create UV-map, Driver, Modifier for Custom Property"
    bl_idname = "wm.setup_properties"

    def execute(self, context):
        scene = context.scene
        cpa = scene.cpa
                
        obj = bpy.context.active_object

        propname = cpa.property_name

        CPA_functions.setupProperty(obj, propname)

        return {'FINISHED'}
    
class removeProperties(Operator):
    bl_label = "Remove Custom Property for this Object"
    bl_description = "Remove Custom Property"
    bl_info = "Remove UV-map, Driver, Modifier for Custom Property"
    bl_idname = "wm.remove_properties"

    def execute(self, context):
        scene = context.scene
        cpa = scene.cpa
                
        obj = bpy.context.active_object

        propname = cpa.property_name

        CPA_functions.removeProperty(obj, propname)

        return {'FINISHED'}
    
class setupPropertiesForMaterial(Operator):
    bl_label = "Property For Every Object of Material"
    bl_description = "Prepare Custom Property for every Object with Material"
    bl_info = "Create UV-map, Driver, Modifier for Custom Property for every object with given Material"
    bl_idname = "wm.setup_properties_material"

    def execute(self, context):
        scene = context.scene
        cpa = scene.cpa
        
        material = cpa.material_name
        propname = cpa.property_name

        
        objects = [o for o in scene.objects if material in o.material_slots]
        
        if len(objects) == 0:
            raise Exception("No Materials found with name " + material)
        
        for obj in objects:    
            CPA_functions.setupProperty(obj, propname)

        return {'FINISHED'}
    
class removePropertiesForMaterial(Operator):
    bl_label = "Remove Property For Material"
    bl_description = "Remove Custom Property for every Object with Material"
    bl_info = "Remove UV-map, Driver, Modifier for Custom Property for every object with given Material"
    bl_idname = "wm.remove_properties_material"

    def execute(self, context):
        scene = context.scene
        cpa = scene.cpa
        
        material = cpa.material_name
        propname = cpa.property_name

        
        objects = [o for o in scene.objects if material in o.material_slots]
        
        if len(objects) == 0:
            raise Exception("No Materials found with name " + material)
        
        for obj in objects:    
            CPA_functions.removeProperty(obj, propname)

        return {'FINISHED'}



class OBJECT_PT_CPA(Panel):
    bl_label = "Custom Properties for Materials"
    bl_idname = "OBJECT_PT_CPA"
    bl_space_type = "PROPERTIES"   
    bl_region_type = "WINDOW"
    bl_context = "object"

    @classmethod
    def poll(self,context):
        return True

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.separator()
        layout.prop(scene.cpa, "property_name")
        layout.operator("wm.setup_properties")
        layout.operator("wm.remove_properties")
        layout.separator()
        layout.prop(scene.cpa, "material_name")
        layout.operator("wm.setup_properties_material")
        layout.operator("wm.remove_properties_material")
        



classes = (
    nbProperties,
    setupProperties,
    removeProperties,
    setupPropertiesForMaterial,
    removePropertiesForMaterial,
    OBJECT_PT_CPA
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.cpa = PointerProperty(type=nbProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.cpa


if __name__ == "__main__":
    register()