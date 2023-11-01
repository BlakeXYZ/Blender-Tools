import bpy

class QWIK_OP_reset_origin(bpy.types.Operator):
    bl_idname = "qwik.reset_origin"
    bl_label = "Reset Origin"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self,context):
 
        # Get the scene
        scene = bpy.context.scene
        # Set the 3D cursor location to the origin point
        scene.cursor.location = (0, 0, 0)
        # Set the active object to the origin point
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

        print("1")
        return {'FINISHED'}


# ----------------------- REGISTER ---------------------

classes = (
    QWIK_OP_reset_origin,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)



def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)










