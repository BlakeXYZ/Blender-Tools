
###
### LOCAL REGISTRATION / INIT
###

import bpy


from .add_lights import BK_01_OP_Add_Lights

classes = (
    BK_01_OP_Add_Lights,
)



def register_operators():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister_operators():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

