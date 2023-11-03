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

#TODO: EXPAND on accepted suffixes
##          BC, ORM, N

    ########
    # CUSTOM SET VALUES
        LIST_accepted_suffixes = ['N', 'BC']  
        DICT_match_nodeInput_to_suffix = [
            {'Base Color':   'BC',  'Node Location':     '-500 , 300'},
            {'Normal':       'N',   'Node Location':     '-500 , -300'},
        ]
    #
    ########
   
        # Run custom func store_tex_filePaths and store in DICT
        self.DICT_stored_tex_filePaths = self.store_tex_filePaths(filePaths, selected_dir_path, LIST_accepted_suffixes)

#TODO: ACCEPT MULTIPLE 3D Asset Extensions

    # Loops through DIR PATH and imports ALL .FBX files 
    # and RUNS function create_material()

        for filePath in filePaths:
            if filePath.endswith(".fbx"):

                my_asset_filePath = filePath
                my_asset_path = os.path.join(selected_dir_path, my_asset_filePath)

                # Import the FBX file
                bpy.ops.import_scene.fbx(filepath=my_asset_path)

                self.create_material(self.DICT_stored_tex_filePaths, DICT_match_nodeInput_to_suffix, my_asset_filePath)

        return {'FINISHED'}
    

    
#################################################################      
# CUSTOM FUNCTIONS

    # Finding and Storing all files that end with _N and _BC
    def store_tex_filePaths(self, filePaths, selected_dir_path, LIST_accepted_suffixes):

        DICT_stored_tex_filePaths = {}
        accepted_fileExtensions = ['.bmp', '.png', '.jpg', '.jpeg', '.tga', '.exr', '.tif', '.tiff']

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
            if suffix not in LIST_accepted_suffixes:
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

        return DICT_stored_tex_filePaths


    def create_material(self, DICT_stored_tex_filePaths, DICT_match_nodeInput_to_suffix, my_asset_filePath):

        # 3d Asset Filepath Material is being created for
        print(f'my_asset_filePath - {my_asset_filePath}')

        # Create a new material
        my_obj = bpy.context.selected_objects[0]
        my_obj_name = my_obj.name

        # CLEAN UP IMPORTED ASSET
        if my_obj.data.materials:
            # remove imported materials
            for material in my_obj.data.materials:
                bpy.data.materials.remove(material, do_unlink=True)
            # remove material slots
            my_obj.data.materials.clear()
            
    
        new_mat = bpy.data.materials.new(name="M_" + my_obj_name)

    #########
    # IMPORT TEXTURES AND CONNECT TO MATERIAL

        # Setup connection to Node tree
        new_mat.use_nodes = True
        node_tree = new_mat.node_tree

        # Find the Principled BSDF shader node
        principled_bsdf = None
        for node in node_tree.nodes:
            if node.type == 'BSDF_PRINCIPLED':
                principled_bsdf = node
                break

        # Iterate through the file groups and print configuration
        for root_group, files in DICT_stored_tex_filePaths.items():
            for file_info in files:
                abs_tex_filePath = file_info["abs_tex_filePath"]
                tex_file_name  = file_info["fileName"]
                suffix = file_info["suffix"]

                # VALIDATE 3D ASSET has same 'ROOT' name as imported tex_filePath's root_group
                if not my_asset_filePath.startswith(root_group):
                    print(f'{my_asset_filePath} does not start with {root_group}')
                    continue

                # with selected SUFFIX, search through DICT and find matching nodeInput
                for item in DICT_match_nodeInput_to_suffix:
                    if suffix in item.values():
                        matching_nodeInput = next(key for key, value in item.items() if value == suffix)
                        node_location_str = item['Node Location']
                        node_location = tuple(map(int, node_location_str.split(',')))  # Parsing the values as integers
                        break

                # Create a texture node
                texture_node = node_tree.nodes.new(type='ShaderNodeTexImage')

                # Attach image to texture_node
                texture_node.image =  bpy.data.images.load(abs_tex_filePath)

                # Link the texture to the roughness input
                node_tree.links.new(texture_node.outputs['Color'], principled_bsdf.inputs[matching_nodeInput])

                # If NOT Base Color, change node color space to Non-Color
                if matching_nodeInput != 'Base Color':
                    texture_node.image.colorspace_settings.name = 'Non-Color'

                # INSERT Normal Map node between Normal Tex and Principled BSDF input 
                if matching_nodeInput == 'Normal':
                    # Build normal map node
                    normal_map_node = node_tree.nodes.new(type='ShaderNodeNormalMap')
                    normal_map_node.location = (-200 , -300)  # Adjust the location as needed
                    # reconnect links
                    node_tree.links.new(texture_node.outputs['Color'], normal_map_node.inputs['Color'])
                    node_tree.links.new(normal_map_node.outputs['Normal'], principled_bsdf.inputs['Normal'])

                # Adjust the texture's location and other properties if necessary
                texture_node.location = (node_location)  # Adjust the location as needed

        # Get object by its name AND append material
        my_obj.data.materials.append(new_mat)

    


    
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







    # # Iterate through the file groups and print configuration
        # for root_group, files in DICT_stored_tex_filePaths.items():
        #     print(f'=== Root Group: {root_group}')
        #     for file_info in files:
        #         print(f'abs_tex_filePath:          {file_info["abs_tex_filePath"]}')
        #         print(f'File Name:                  {file_info["fileName"]}')
        #         print(f'Suffix:                     {file_info["suffix"]}')
        #         print('-')