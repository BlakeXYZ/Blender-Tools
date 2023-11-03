
###
### OPERATOR REGISTRATION / INIT
###

import bpy


from .main import MyProperties, PrintPathOperator, ImportOperator, MYADDON_PT_MyUIPanel


###########################################################  
# REGISTRY

classes = [MyProperties,
           PrintPathOperator, 
           ImportOperator,
           MYADDON_PT_MyUIPanel, ]  

def register_operators():

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.myaddon_properties = bpy.props.PointerProperty(type=MyProperties)


def unregister_operators():

    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.myaddon_properties

