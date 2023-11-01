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

def register():

    from .main import register
    register()

def unregister(): 

    from .main import unregister
    unregister()

