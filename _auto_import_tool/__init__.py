bl_info = {
    "name" : "Batch Asset Importer",
    "author" : "Blake XYZ",
    "version" : (1, 0),
    "blender" : (3, 2),
    "location" : "View 3D > N Panel",
    "warning" : "",
    "wiki" : "https://github.com/BlakeXYZ",
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
