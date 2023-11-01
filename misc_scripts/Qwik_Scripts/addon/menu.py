import bpy

#----------------------------------- UI --------------------------

class QWIK_MT_menu(bpy.types.Menu):
    bl_idname = "QWIK_MT_menu"
    bl_label = "Qwik Menu"
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self, context):
        layout = self.layout
        layout.operator("qwik.reset_origin") #pull in IDname from reset_origin class
        
#----------------------------------- FUNCTIONS --------------------------

def draw_menu(self, context):
    self.layout.menu("QWIK_MT_menu", text="BlakeXYZ Qwik Scripts")

# ----------------------- REGISTER ---------------------

classes = (
    QWIK_MT_menu,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.VIEW3D_MT_object_context_menu.prepend(draw_menu)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_menu)










