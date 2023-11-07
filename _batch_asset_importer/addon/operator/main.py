import os
import bpy



#################################################################      
# SCENE PROPERTIES


class MyProperties(bpy.types.PropertyGroup):

    my_dir_path: bpy.props.StringProperty(
        name="Asset Path",
        description="Select Asset Directory Path",
        subtype='DIR_PATH'
    )

    my_dir_tex_path: bpy.props.StringProperty(
        name="Texture Path",
        description="Select Texture Directory Path",
        subtype='DIR_PATH'
    )

    my_tex_diff_path_toggle: bpy.props.BoolProperty(
        name="Toggle - Texture Directory Path",
        description="Are your Textures located in a different Folder? If so, TOGGLE ON",
        default=False,

    )


#################################################################      
# OPERATORS

class ImportOperator(bpy.types.Operator):
    bl_idname = "bxyz_batch_importer.import_asset" # naming convention - must be lowercase
    bl_label = "Batch Import Assets"
    bl_options = {'UNDO'} # solves crash - "EXCEPTION_ACCESS_VIOLATION" error when trying to undo
    
    def execute(self, context):
        props = context.scene.BXYZ_BATCH_IMPORTER_properties

        selected_dir_path = props.my_dir_path
        selected_fileNames = os.listdir(selected_dir_path)   

    ####
    # CUSTOM SET VALUES
        DICT_accepted_asset_fileExtensions_config = {
            '.fbx' : bpy.ops.import_scene.fbx, 
            '.stl' : bpy.ops.import_mesh.stl, 
            '.obj' : bpy.ops.import_scene.obj,}

        LIST_accepted_tex_fileExtensions_config = ['.bmp', '.png', '.jpg', '.jpeg', '.tga', '.exr', '.tif', '.tiff']

        DICT_tex_suffix_nodeInput_config = [
            {'Suffix': 'BC',    'Node Input': 'Base Color',            'Node Location':     '-700 ,    300'},
            {'Suffix': 'ORM',   'Node Input': 'ORM',                   'Node Location':     '-700 ,    000'},
            {'Suffix': 'N',     'Node Input': 'Normal',                'Node Location':     '-700 ,    -300'},
        ]
   ####

        # TOGGLE LOGIC, if Textures are in different path
        if  props.my_tex_diff_path_toggle is True:
            selected_tex_dir_path = props.my_dir_tex_path
            selected_tex_fileNames = os.listdir(selected_tex_dir_path)  
            print(f'selected_tex_dir_path {selected_tex_dir_path}')
 
        # If TEXTURE FILES are not in Diff Path, set selected_tex info to same as 3d Object selected_ info
        else:
            print(f'toggle is False')
            selected_tex_dir_path = selected_dir_path
            selected_tex_fileNames = selected_fileNames

        # Run custom func store_tex_filePaths and store in DICT
        self.DICT_stored_tex_filePaths = self.store_tex_filePaths(selected_tex_fileNames, selected_tex_dir_path, LIST_accepted_tex_fileExtensions_config, DICT_tex_suffix_nodeInput_config)

    ####
    # Loops through DIR PATH and imports ALL assets that match DICT_accepted_asset_fileExtensions_config (ex: myasset.fbx or .stl)
    # and uses matching value pair (import operator) to import asset. 
    # and RUNS function create_material()
        for fileName in selected_fileNames:

            _, fileExtension = os.path.splitext(fileName)
            if fileExtension in DICT_accepted_asset_fileExtensions_config.keys():

                my_asset_fileName = fileName
                my_asset_absPath = os.path.join(selected_dir_path, my_asset_fileName)

                import_operator = DICT_accepted_asset_fileExtensions_config[fileExtension]    # inside custom DICT: Get Import Operator that matches current fileExtension 
                import_operator(filepath = my_asset_absPath)

                # Import Textures and Set up NODE GRAPH for each Asset
                self.create_material(my_asset_fileName, self.DICT_stored_tex_filePaths, DICT_tex_suffix_nodeInput_config)

        return {'FINISHED'}
    

    
#################################################################      
# CUSTOM FUNCTIONS

    # Finding and Storing all files that end with _N and _BC
    def store_tex_filePaths(self, selected_tex_fileNames, selected_tex_dir_path, LIST_accepted_tex_fileExtensions_config, DICT_tex_suffix_nodeInput_config):

        DICT_stored_tex_filePaths = {}

        for fileName in selected_tex_fileNames:

            # SPLIT filePath extension
            fileNameWithoutExtension, fileExtension = os.path.splitext(fileName)

            # SPLIT fileName from the RIGHT by "_" and get last part as suffix
            split_file_name = fileNameWithoutExtension.rsplit("_", 1) # split only once from the right

            try:
                root, suffix = split_file_name
            except:
                # VALIDATE if filePath contains any SUFFIX
                print(f'SKIPPING - Selected Texture File: "{fileNameWithoutExtension}" DOES NOT CONTAIN A SUFFIX. Full file path: {fileName}')
                continue

            # FILTER Folders and unaccepted File Extensions
            if fileExtension not in LIST_accepted_tex_fileExtensions_config:
                # print(f'SKIPPING File: "{filePath}" with FileExtension: "{fileExtension}" DOES NOT MATCH accepted_fileExtensions')
                continue

            # FILTER unaccepted suffixes
            # Check if suffix matches any 'Suffix' value in the configuration
            if not any(config['Suffix'] == suffix for config in DICT_tex_suffix_nodeInput_config):
                print(f"{fileName}'s suffix '_{suffix}' does not match any config Suffixes")
                continue

            # Add new root list
            if root not in DICT_stored_tex_filePaths: 
                DICT_stored_tex_filePaths[root] = []

            # GET FULL Texture Path
            abs_tex_filePath = os.path.join(selected_tex_dir_path, fileName)

            # Create a dictionary entry for the current filepath root
            DICT_stored_tex_filePaths[root].append({
                'abs_tex_filePath': abs_tex_filePath,
                'fileName': fileNameWithoutExtension,
                'suffix': suffix
            })

        return DICT_stored_tex_filePaths


    def create_material(self, my_asset_filePath, DICT_stored_tex_filePaths, DICT_tex_suffix_nodeInput_config):

        # 3d Asset Filepath Material is being created for
        print(f'my_asset_filePath - {my_asset_filePath}')

        # Create a new material
        my_asset = bpy.context.selected_objects[0]
        my_asset_name = my_asset.name

    ####
    # CLEAN UP IMPORTED ASSET
        if my_asset.data.materials:
            # remove imported materials
            for material in my_asset.data.materials:
                bpy.data.materials.remove(material, do_unlink=True)
            # remove material slots
            my_asset.data.materials.clear()

        # Purge unused images without user interaction
        for img in bpy.data.images:
            if not img.users:
                bpy.data.images.remove(img)
    ####
        
        # Build New Material for current Asset
        new_mat = bpy.data.materials.new(name="M_" + my_asset_name) 

    ####
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


        ####
        # BATCH IMPORT TEXTURES AND BUILD NODE GRAPH

        # Build NODE String Names
        BC_AO_Mix_Node_Name = 'BC_AO_Multiply'


        for root_group, files in DICT_stored_tex_filePaths.items():
            for file_info in files:
                abs_tex_filePath = file_info["abs_tex_filePath"]
                tex_file_name  = file_info["fileName"]
                current_suffix = file_info["suffix"]

                # VALIDATE 3D ASSET has same 'ROOT' name as imported tex_filePath's root_group
                if not my_asset_filePath.startswith(root_group):
                    # print(f'{tex_file_name} root does not match {my_asset_filePath} root')
                    continue
                    
                # Loop through the config to find matching DICT info for current current suffix
                for config in DICT_tex_suffix_nodeInput_config:
                    if config['Suffix'] == current_suffix:
                        matching_nodeInput = config['Node Input']
                        node_location_str = config['Node Location']
                        node_location = tuple(map(int, node_location_str.split(',')))  # Parsing the values as integers
                        break

                # Create a texture node
                current_texture_node = node_tree.nodes.new(type='ShaderNodeTexImage')
                # Attach image to texture_node
                current_texture_node.image =  bpy.data.images.load(abs_tex_filePath)

                # node_tree.links.new(texture_node.outputs['Color'], principled_bsdf.inputs[matching_nodeInput])

            #######
            ####
            # BUILD NODE GRAPH && CONNECT NODES
                if matching_nodeInput == 'Base Color':
                    # Build MIX RGB Node
                    BC_AO_mix_rgb_node = node_tree.nodes.new(type='ShaderNodeMixRGB')
                    BC_AO_mix_rgb_node.location = (-200 , 250)  # Adjust the location as needed
                    BC_AO_mix_rgb_node.blend_type = 'MULTIPLY'
                    BC_AO_mix_rgb_node.inputs['Fac'].default_value = 0.2
                    BC_AO_mix_rgb_node.inputs['Color2'].default_value = (1,1,1,1)
                    BC_AO_mix_rgb_node.name =     BC_AO_Mix_Node_Name     # Critical, for selection later (ex. mix_rgb_node = node_tree.nodes.get(BC_AO_Mix_Node_Name)
                    BC_AO_mix_rgb_node.label =    BC_AO_Mix_Node_Name     # Non critical, easy to read graph

                    # Connect BC Tex to MIX RGB, and MIX RGB to principled bsdf input
                    node_tree.links.new(current_texture_node.outputs['Color'], BC_AO_mix_rgb_node.inputs['Color1'])
                    node_tree.links.new(BC_AO_mix_rgb_node.outputs['Color'], principled_bsdf.inputs['Base Color'])

                # If NOT Base Color, change node color space to Non-Color
                if matching_nodeInput != 'Base Color':
                    current_texture_node.image.colorspace_settings.name = 'Non-Color'

                # INSERT Normal Map node between Normal Tex and Principled BSDF input 
                if matching_nodeInput == 'Normal':
                    # Build normal map node
                    normal_map_node = node_tree.nodes.new(type='ShaderNodeNormalMap')
                    normal_map_node.location = (-200 , -300)  # Adjust the location as needed

                    # reconnect links
                    node_tree.links.new(current_texture_node.outputs['Color'], normal_map_node.inputs['Color'])
                    node_tree.links.new(normal_map_node.outputs['Normal'], principled_bsdf.inputs['Normal'])

                if matching_nodeInput == 'ORM':
                    # Build SEPARATE RGB
                    sep_rgb_node = node_tree.nodes.new(type='ShaderNodeSeparateRGB')
                    sep_rgb_node.location = (-400 , 000)  # Adjust the location as needed

                    # Connect ORM Color to SEPARATE RGB
                    node_tree.links.new(current_texture_node.outputs['Color'], sep_rgb_node.inputs['Image'])

                    # SEPARATE RGB - Red to Multiply Mix RGB - BC_AO_Mix_Node
                    BC_AO_mix_rgb_node = node_tree.nodes.get(BC_AO_Mix_Node_Name)
                    node_tree.links.new(sep_rgb_node.outputs['R'], BC_AO_mix_rgb_node.inputs['Color2'])
                    # SEPARATE RGB - Green to principled_bsdf.inputs['Roughness']
                    node_tree.links.new(sep_rgb_node.outputs['G'], principled_bsdf.inputs['Roughness'])
                    # SEPARATE RGB - Red to principled_bsdf.inputs['Metallic']
                    node_tree.links.new(sep_rgb_node.outputs['B'], principled_bsdf.inputs['Metallic'])
                ####
                #######

                # Adjust the texture's location and other properties if necessary
                current_texture_node.location = (node_location)  # Adjust the location as needed

        # Get object by its name AND append material
        my_asset.data.materials.append(new_mat)

    
    
#################################################################      
# UI PANELS

class BXYZ_BATCH_IMPORTER_PT_PanelInfo:
    bl_category = "Batch Asset Importer"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"  

class BXYZ_BATCH_IMPORTER_PT_MyUIPanel(BXYZ_BATCH_IMPORTER_PT_PanelInfo, bpy.types.Panel):
    bl_label = "Batch Asset Importer"
    bl_idname = "MYADDON_PT_MyUIPanel"
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.BXYZ_BATCH_IMPORTER_properties
        
        layout.prop(props, "my_dir_path")

        # Create a boolean property
        layout.prop(props, "my_tex_diff_path_toggle", text="Are Texture Files in Different Path?")

        # IF Texture Files are in Different Path, prompt user to select "my_dir_tex_path"
        if props.my_tex_diff_path_toggle:
            layout.prop(props, "my_dir_tex_path")

        layout.operator("bxyz_batch_importer.import_asset")


