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
from .faceutils import get_safe_custom_attribute


class FBRigMainPanel(bpy.types.Panel):
    bl_idname = 'FACEBUILDER_RIG_PT_main_panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = 'KT FaceRig v.0.2'
    # bl_context = 'objectmode'
    bl_category = 'KT FaceRig'

    # Panel appear only when Mesh or Armature selected
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and obj.type in ('MESH', 'ARMATURE')

    # Main Panel Draw
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.object

        col = layout.column()
        col.scale_y = 0.75
        col.label(text='1) Select FaceBuilder Head')
        col.label(text='2) DISABLE Mouth and Eyes')
        col.label(text='in FB Model settings')
        col.label(text='for proper skinning')

        op = layout.operator('keentools_facerig.actor_operator',
                             text='1. Generate Rig')
        op.action = 'generate_rig'

        op = layout.operator('keentools_facerig.actor_operator',
                             text='2. Skinning')
        op.action = 'skinning'

        box = layout.box()
        box.label(text='Selected: {}'.format(obj.name))

        attr = get_safe_custom_attribute(obj, 'fbmesh')
        if attr is not None:
            box = layout.box()
            box.label(text='Related mesh: {}'.format(attr))

        attr = get_safe_custom_attribute(obj, 'fbrig')
        if attr is not None:
            box = layout.box()
            box.label(text='Related rig: {}'.format(attr))

        box = layout.box()
        col = box.column()
        col.scale_y = 0.75
        col.label(text='1) Select Neutral Mesh')
        col.label(text='2) then select Animated Mesh')
        # col.label(text='to define neutral shape')
        col.label(text='(this step can be skipped')
        col.label(text='if animation starts from neutral)')
        op = box.operator('keentools_facerig.actor_operator',
                             text='3. Neutral mesh')
        op.action = 'animation_neutral'

        attr = get_safe_custom_attribute(obj, 'fbneutral')
        if attr is not None:
            box = layout.box()
            box.label(text='Neutral mesh: {}'.format(attr))

        attr = get_safe_custom_attribute(obj, 'fbanimation')
        if attr is not None:
            box = layout.box()
            box.label(text='Related anim: {}'.format(attr))

        box = layout.box()
        col = box.column()
        col.scale_y = 0.75
        col.label(text='1) Select Animated Mesh')
        col.label(text='2) then select generated FaceRig')
        col.label(text='(armature) to bake animation')
        op = box.operator('keentools_facerig.actor_operator',
                             text='4. Bake Animation')
        op.action = 'bake_animation'

        box = layout.box()
        col = box.column()
        col.scale_y = 0.75
        col.label(text='This button clears all')
        col.label(text='other objects from scene')
        col.label(text='before export')
        op = box.operator('keentools_facerig.actor_operator',
                             text='5. Clear Scene')
        op.action = 'clear_scene'

        box = layout.box()
        col = box.column()
        col.scale_y = 0.75
        col.label(text='Just Export to FBX')
        op = box.operator('keentools_facerig.actor_operator',
                             text='6. Export Scene')
        op.action = 'export_scene'
