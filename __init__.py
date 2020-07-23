# ##### BEGIN GPL LICENSE BLOCK #####
# KTFaceRig add-on for Blender is an unofficial Face Rig add-on
# working with KeenTools FaceBuilder model.
# Copyright (C) 2020 Alexander Milovsky

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ##### END GPL LICENSE BLOCK #####


bl_info = {
    "name": "KT FaceRig for KeenTools FaceBuilder",
    "author": "Alexander Milovsky",
    "blender": (2, 80, 0),
    "location": "View3D > UI",
    "description": "Unofficial FaceRig & Animation transfer",
    "wiki_url": "https://github.com/amilovsky/ktfacerig",
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
