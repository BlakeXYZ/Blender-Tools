import bpy, math
from bpy.props import IntProperty, FloatProperty

class BK_01_OP_Add_Lights(bpy.types.Operator):

    """ Add lights to scene """

    bl_idname = "bk.add_lights"
    bl_label = "Add My Lights"
    bl_options = {'REGISTER', 'UNDO'}

    radius: FloatProperty(name="Radius", description="Radius of Circle", default=1, min=1, max=100)
    count: IntProperty(name="Light Count", description="Amount of Lights", default=5, min=3, max=50)
    height: FloatProperty(name="Height", description="Height of Lights", default=6, min=-50, max=50)
    brightness: IntProperty(name="Light Brightness", default=500, min=0, max=2000)




    def draw(self, context):

        layout = self.layout
        layout.prop(self, 'radius')
        layout.prop(self, 'count')
        layout.prop(self, 'height')
        layout.prop(self, 'brightness')


    def execute(self, context):
        objs = []

        for i in range(self.count):
            myLight = bpy.data.lights.new('My Point Light', 'POINT')
            obj = bpy.data.objects.new("LightObj", myLight)
            objs.append(obj)
            context.collection.objects.link(obj)

            angle = i * math.pi * 2 / self.count

            loc = (
                math.cos(angle) * self.radius,      # X Pos
                math.sin(angle) * self.radius,      # Y Pos
                self.height                         # Z Pos
            )

            ### Set obj props           
            obj.location = loc                      # Equivalent to: light = C.active_object in Blender Console
            obj.data.energy = self.brightness

        empty = bpy.data.objects.new('LightEmpty', None)
        empty.location = (0,0,0)
        context.collection.objects.link(empty)
        for obj in objs:
            obj.parent = empty


        # print("HERE  Yay")
        return {'FINISHED'}
