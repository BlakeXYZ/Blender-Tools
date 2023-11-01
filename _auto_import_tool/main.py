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
    bl_label = "Import Object"
    
    def execute(self, context):
        props = context.scene.myaddon_properties

        selected_dir_path = props.my_dir_path
        toggle = props.my_toggle

        # print(f'Printing Boolean {toggle}')

        filePaths = os.listdir(selected_dir_path)

        print(filePaths)
        

        DICT_stored_tex_filePaths = self.store_tex_filePaths(filePaths, selected_dir_path)


    # # Loops through DIR PATH and imports ALL .FBX files 
    # # and RUNS function create_material()
    #     for filePath in filePaths:
    #         if filePath.endswith(".fbx"):
    #             print(f"Found an FBX file: {filePath}")

    #             my_fbx_file = filePath
    #             my_fbx_path = os.path.join(selected_dir_path, my_fbx_file)

    #             print(my_fbx_path)

    #             # Import the FBX file
    #             bpy.ops.import_scene.fbx(filepath=my_fbx_path)

    #             self.create_material(DICT_stored_tex_filePaths)

    #             break # DEBUGGING This will exit the loop after the first iteration
        


        return {'FINISHED'}
    

    # Finding and Storing all files that end with _N and _BC
    def store_tex_filePaths(self, filePaths, selected_dir_path):

        DICT_stored_tex_filePaths = {}
        accepted_fileExtensions = ['.bmp', '.png', '.jpg', '.jpeg', '.tga', '.exr', '.tif', '.tiff']
        accepted_suffixes = ['N', 'BC']

        for filePath in filePaths:

            # SPLIT filePath extension
            fileNameWithoutExtension, fileExtension = os.path.splitext(filePath)

            # SPLIT fileName from the RIGHT by "_" and get last part as suffix
            split_file_name = fileNameWithoutExtension.rsplit("_", 1) # split only once from the right

            try:
                root, suffix = split_file_name
            except:
                # VALIDATE if filePath contains any SUFFIX
                print(f'SKIPPING - Selected Texture File: "{fileNameWithoutExtension}" DOES NOT CONTAIN A SUFFIX. Full file path: {filePath}')
                continue

            # FILTER Folders and unaccepted File Extensions
            if fileExtension not in accepted_fileExtensions:
                # print(f'SKIPPING File: "{filePath}" with FileExtension: "{fileExtension}" DOES NOT MATCH accepted_fileExtensions')
                continue

            # FILTER unaccepted suffixes
            if suffix not in accepted_suffixes:
                # print(f'SKIPPING File: "{filePath}" with Suffix: "{suffix}" DOES NOT MATCH accepted_suffixes')
                continue

            # Add new root list
            if root not in DICT_stored_tex_filePaths: 
                DICT_stored_tex_filePaths[root] = []

            # GET FULL Texture Path
            abs_tex_filePath = os.path.join(selected_dir_path, filePath)

            # Create a dictionary entry for the current filepath root
            DICT_stored_tex_filePaths[root].append({
                'abs_tex_filePath': abs_tex_filePath,
                'fileName': fileNameWithoutExtension,
                'suffix': suffix
            })

        # # Iterate through the file groups and print configuration
        # for root_group, files in DICT_stored_tex_filePaths.items():
        #     print(f'=== Root Group: {root_group}')
        #     for file_info in files:
        #         print(f'abs_tex_filePath:          {file_info["abs_tex_filePath"]}')
        #         print(f'File Name:                  {file_info["fileName"]}')
        #         print(f'Suffix:                     {file_info["suffix"]}')
        #         print('-')

        return DICT_stored_tex_filePaths

    def create_material(self, DICT_stored_tex_filePaths):
        my_fbx_data = bpy.context.selected_objects[0]
        my_fbx_name = my_fbx_data.name

        print(f'running create material - my_fbx_data  = {my_fbx_data}')
        print(f'running create material - my_fbx  = {my_fbx_name}')

        # Create a new material
        new_mat = bpy.data.materials.new(name="M_" + my_fbx_name)

        # You can set various properties for the material
        new_mat.diffuse_color = (1, 0, 0, 1)  # Red color (R, G, B, Alpha)
#####
# TODO: IMPORT TEXTURES AND CONNECT TO MATERIAL

        # Create a new texture and load an image file
        texture = bpy.data.textures.new(name="MyTexture", type='IMAGE')
        image_path = "/path/to/your/texture/image.png"  # Replace with the path to your texture image

        # Load the image into the texture
        texture.image = bpy.data.images.load(image_path)
#
#####
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

