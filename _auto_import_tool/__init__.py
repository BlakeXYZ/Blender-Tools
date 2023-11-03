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
