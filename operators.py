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


import bpy
from .faceutils import generate_rig_from_mesh, bake_animation_to_rig,\
    select_object, set_custom_attribute, has_custom_attribute, \
    get_safe_custom_attribute


def find_marked_object(ftype='ARMATURE', fattr='fbmesh'):
    for obj in bpy.context.scene.objects:
        if obj.type == ftype:
            if has_custom_attribute(obj, fattr):
                return obj
    return None


def selected_pair():
    selected = bpy.context.selected_objects
    if len(selected) != 2:
        return None, None
    if selected[0] is bpy.context.active_object:
        return selected[0], selected[1]
    else:
        return selected[1], selected[0]


class FBRigActor(bpy.types.Operator):
    bl_idname = 'keentools_facerig.actor_operator'
    bl_label = 'Main Action Operator'
    bl_options = {'REGISTER', 'UNDO'}

    action: bpy.props.StringProperty(name="Action string", default="Just text")
    num: bpy.props.IntProperty(name="Numeric parameter", default=0)

    def execute(self, context):
        scene = context.scene
        obj = context.object
        self.report({'INFO'}, "Action: {0}".format(self.action))

        if self.action == 'generate_rig':
            arm_obj = generate_rig_from_mesh(obj, 'FBRig')
            select_object(arm_obj)
            obj.select_set(state=True)

            set_custom_attribute(arm_obj, 'fbmesh', obj.name)
            set_custom_attribute(obj, 'fbrig', arm_obj.name)

        elif self.action == 'skinning':
            obj1, obj2 = selected_pair()
            if obj1 is None:
                return {'CANCELLED'}
            if obj1.type != 'ARMATURE' or obj2.type != 'MESH':
                return {'CANCELLED'}
            bpy.ops.object.parent_set(type='ARMATURE_AUTO')

        elif self.action == 'animation_source':
            obj1, obj2 = selected_pair()
            if obj1 is None:
                return {'CANCELLED'}
            if obj1.type != 'ARMATURE' or obj2.type != 'MESH':
                return {'CANCELLED'}
            # arm_obj = find_marked_object()
            # if arm_obj is None:
            #     return {'CANCELLED'}
            set_custom_attribute(obj1, 'fbanimation', obj2.name)
            select_object(obj1)

        elif self.action == 'animation_neutral':
            obj1, obj2 = selected_pair()
            if obj1 is None:
                return {'CANCELLED'}
            set_custom_attribute(obj1, 'fbneutral', obj2.name)

        elif self.action == 'bake_animation':
            obj1, obj2 = selected_pair()
            if obj1 is None:
                return {'CANCELLED'}
            if obj1.type != 'ARMATURE' or obj2.type != 'MESH':
                return {'CANCELLED'}
            neutral = get_safe_custom_attribute(obj2, 'fbneutral')
            neutral_obj = None if neutral is None else bpy.context.scene.objects[neutral]

            bake_animation_to_rig(obj2, obj1, neutral_obj)

        elif self.action == 'clear_scene':
            arm_obj = find_marked_object('ARMATURE', 'fbmesh')
            obj = find_marked_object('MESH', 'fbrig')
            select_object(arm_obj)
            obj.select_set(state=True)
            bpy.ops.object.select_all(action='INVERT')
            bpy.ops.object.delete(use_global=False, confirm=False)
            select_object(arm_obj)
            obj.select_set(state=True)

        elif self.action == 'export_scene':
            bpy.ops.export_scene.fbx('INVOKE_DEFAULT',
                                     use_armature_deform_only=True,
                                     add_leaf_bones=False)

        print(self.action)
        return {'FINISHED'}

    # Operator Panel Draw
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.object

        layout.label(text="Simple text label", icon="INFO")
        layout.label(text="Action: {}".format(self.action))
        # layout.prop(self, 'action', text="String value")
        # layout.prop(self, 'num', text="Number")
