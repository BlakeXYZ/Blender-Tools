bl_info = {
    "name" : "Batch Asset Importer",
    "author" : "Blake XYZ",
    "description" : "Batch import 3d Assets + Textures and dynamically build Shader Graph per Asset using imported Textures.",
    "blender" : (3, 2, 0),
    "version" : (1, 0, 0),
    "location" : "",
    "warning" : "",
    "wiki" : "https://github.com/BlakeXYZ",
    "category" : "Tools"
}

###  
######      
###########################################################  
###### beginning of REGISTRY BRANCH
###


def register():
    from .addon.register import register_addon
    register_addon()

def unregister():
    from .addon.register import unregister_addon
    unregister_addon()
