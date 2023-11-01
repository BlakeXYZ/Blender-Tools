import os
import bpy

bl_info = {
    "name" : "Auto Import Tool",
    "author" : "Blake Kostroun",
    "version" : (1, 0),
    "blender" : (3, 2),
    "location" : "View 3D > Tool",
    "warning" : "",
    "wiki" : "https://www.artstation.com/blakekostroun",
    "category" : "New Addon",
}


#################################################################      
# SCENE PROPERTIES


class MyProperties(bpy.types.PropertyGroup):

    my_dir_path: bpy.props.StringProperty(
        name="Object Path",
        description="Select Directory Path",
        subtype='DIR_PATH'
    )

    my_dir_tex_path: bpy.props.StringProperty(
        name="Texture Path",
        description="Select Texture Path",
        subtype='DIR_PATH'
    )

    my_toggle: bpy.props.BoolProperty(
        name="Toggle",
        description="Toggle On Off",
        default=False,

    )


#################################################################      
# OPERATORS

class PrintPathOperator(bpy.types.Operator):
    bl_idname = "myaddon.print_path"
    bl_label = "Print My Path"
    
    def execute(self, context):
        # Your file path handling logic here
        selected_dir_path = context.scene.myaddon_properties.my_dir_path
        # You can use the selected_file_path for further operations
        print("Selected File Path:", selected_dir_path)

        print(os.listdir(selected_dir_path))

        return {'FINISHED'}
    

class ImportOperator(bpy.types.Operator):
    bl_idname = "myaddon.import"
    bl_label = "Import Object"
    
    def execute(self, context):
        props = context.scene.myaddon_properties

        selected_dir_path = props.my_dir_path
        toggle = props.my_toggle


        # print(f'Printing Boolean {toggle}')

        dir_path_files = os.listdir(selected_dir_path)
####
######
    # Finding and Storing all files that end with _N and _BC
    # TODO: Have DICT built inside EACH .FBX found 

    # TODO: FOCUS ON MINIMAL VIABLE PRODUCT
    # Can ramp up later to facilitate for numerous fbx files/texture files and edge cases
######
####
    
        DICT_tex_files = {}

        for current_file in dir_path_files:
            current_file_basename = current_file.split(".")[0]

            if current_file_basename.endswith("_N"):
                DICT_tex_files['Normal'] = current_file
            elif current_file_basename.endswith("_BC"):
                DICT_tex_files['Base_Color'] = current_file

        print(DICT_tex_files)

    # # Loops through DIR PATH and imports ALL .FBX files 
    # # and RUNS function create_material()
        # for current_file in dir_path_files:
        #     if current_file.endswith(".fbx"):
        #         print(f"Found an FBX file: {current_file}")

        #         my_fbx_file = current_file
        #         my_fbx_path = os.path.join(selected_dir_path, my_fbx_file)

        #         print(my_fbx_path)

        #         # Import the FBX file
        #         bpy.ops.import_scene.fbx(filepath=my_fbx_path)

        #         self.create_material()

        #         break # DEBUGGING This will exit the loop after the first iteration
        


        return {'FINISHED'}
    
    def create_material(self):
        my_fbx_data = bpy.context.selected_objects[0]
        my_fbx_name = my_fbx_data.name

        print(f'running create material - my_fbx_data  = {my_fbx_data}')
        print(f'running create material - my_fbx  = {my_fbx_name}')

        # Create a new material
        new_mat = bpy.data.materials.new(name="M_" + my_fbx_name)

        # You can set various properties for the material
        new_mat.diffuse_color = (1, 0, 0, 1)  # Red color (R, G, B, Alpha)

        # Get object by its name AND append material
        my_fbx_data.data.materials.append(new_mat)

    


    
#################################################################      
# UI PANELS

class MYADDON_PT_PanelInfo:
    bl_category = "Auto Import Tool"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"  

class MYADDON_PT_MyUIPanel(MYADDON_PT_PanelInfo, bpy.types.Panel):
    bl_label = "My UI Panel"
    bl_idname = "MYADDON_PT_MyUIPanel"
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.myaddon_properties
        
        layout.prop(props, "my_dir_path")

        # Create a boolean property
        layout.prop(props, "my_toggle", text="Are Texture Files in Different Path?")

        # IF Texture Files are in Different Path, prompt user to select "my_dir_tex_path"
        if props.my_toggle:
            layout.prop(props, "my_dir_tex_path")

        layout.operator("myaddon.print_path")
        layout.operator("myaddon.import")

 

###########################################################  
# REGISTRY

classes = [MyProperties,
           PrintPathOperator, 
           ImportOperator,
           MYADDON_PT_MyUIPanel, ]  

def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.myaddon_properties = bpy.props.PointerProperty(type=MyProperties)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.myaddon_properties

