bl_info = {
    "name" : "BlakeXYZ Qwik Scripts",
    "description" : "Scripts built to help myself work faster. I hope you find them useful. Cheers!",
    "author" : "Blake XYZ",
    "version" : (1, 0),
    "blender" : (3, 0),
    "location" : "View 3D > Tool, Object Context Menu",
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
    from .addon.menu import register
    register()

    from .addon.reset_origin import register
    register()

def unregister():
    from .addon.menu import unregister
    unregister()

    from .addon.reset_origin import unregister
    unregister()

