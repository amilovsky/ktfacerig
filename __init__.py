bl_info = {
    "name": "KT FaceRig for KeenTools FaceBuilder",
    "author": "Alexander Milovsky",
    "blender": (2, 80, 0),
    "location": "View3D > UI",
    "description": "Unofficial FaceRig & Animation transfer",
    "wiki_url": "https://keentools.io/",
    "warning": "",
    "category": "Rigging"
}


import bpy
from . operators import (FBRigActor,)
from . panels import (FBRigMainPanel,)

classes = (
    FBRigActor,
    FBRigMainPanel
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
