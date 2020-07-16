bl_info = {
    "name": "Unofficial FaceRig for KeenTools FaceBuilder",
    "author": "Alexander Milovsky",
    "blender": (2, 80, 0),
    "location": "View3D > UI",
    "description": "Add-on generates Face bone rig to transfer shape animation "
                   "into bone-based animation suitable for game-engines."
                   "Now works only with KeenTools FaceBuilder Head model."
                   "You can install FaceBuilder addon from "
                   "https://keentools.io/",
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
