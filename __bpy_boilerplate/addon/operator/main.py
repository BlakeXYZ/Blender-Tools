import os
import bpy



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
    bl_label = "Boilerplate Import Objects"
    
    def execute(self, context):
        props = context.scene.myaddon_properties

        selected_dir_path = props.my_dir_path
        toggle = props.my_toggle
        # print(f'Printing Boolean {toggle}')

        filePaths = os.listdir(selected_dir_path)   



    # Loops through DIR PATH and imports ALL .FBX files 
    # and RUNS function create_material()

        for filePath in filePaths:
            if filePath.endswith(".fbx"):

                my_asset_filePath = filePath
                my_asset_path = os.path.join(selected_dir_path, my_asset_filePath)

                # Import the FBX file
                bpy.ops.import_scene.fbx(filepath=my_asset_path)

                self.create_material()

        return {'FINISHED'}
    

    
#################################################################      
# CUSTOM FUNCTIONS

    def create_material(self):
        my_obj = bpy.context.selected_objects[0]
        my_obj_name = my_obj.name


    ###
    # CLEAN UP IMPORTED ASSET
        if my_obj.data.materials:
            # remove imported materials
            for material in my_obj.data.materials:
                bpy.data.materials.remove(material, do_unlink=True)
            # remove material slots
            my_obj.data.materials.clear()

        # Purge unused images without user interaction
        for img in bpy.data.images:
            if not img.users:
                bpy.data.images.remove(img)
    ###
            

        print(f'running create material - my_fbx_data  = {my_obj}')
        print(f'running create material - my_fbx  = {my_obj_name}')

        # Create a new material
        new_mat = bpy.data.materials.new(name="M_" + my_obj_name)

        # You can set various properties for the material
        new_mat.diffuse_color = (1, 0, 0, 1)  # Red color (R, G, B, Alpha)

        # Get object by its name AND append material
        my_obj.data.materials.append(new_mat)

    
    
#################################################################      
# UI PANELS

class MYADDON_PT_PanelInfo:
    bl_category = "Boiler Plate Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"  

class MYADDON_PT_MyUIPanel(MYADDON_PT_PanelInfo, bpy.types.Panel):
    bl_label = "My Boilerplate UI Panel"
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

 








    # # Iterate through the file groups and print configuration
        # for root_group, files in DICT_stored_tex_filePaths.items():
        #     print(f'=== Root Group: {root_group}')
        #     for file_info in files:
        #         print(f'abs_tex_filePath:          {file_info["abs_tex_filePath"]}')
        #         print(f'File Name:                  {file_info["fileName"]}')
        #         print(f'Suffix:                     {file_info["suffix"]}')
        #         print('-')