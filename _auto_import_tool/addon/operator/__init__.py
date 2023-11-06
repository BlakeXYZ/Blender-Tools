
###
### OPERATOR REGISTRATION / INIT
###

import bpy


from .main import MyProperties, ImportOperator, BXYZ_BATCH_IMPORTER_PT_MyUIPanel


###########################################################  
# REGISTRY

classes = [ MyProperties,
           ImportOperator,
           BXYZ_BATCH_IMPORTER_PT_MyUIPanel, ]


def register_operators():

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.BXYZ_BATCH_IMPORTER_properties = bpy.props.PointerProperty(type=MyProperties)


def unregister_operators():

    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.BXYZ_BATCH_IMPORTER_properties

