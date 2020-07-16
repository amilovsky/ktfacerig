import bpy
from .faceutils import get_safe_custom_attribute


class FBRigMainPanel(bpy.types.Panel):
    bl_idname = "FACEBUILDER_RIG_PT_main_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "KT FaceRig v.0.1"
    # bl_context = "objectmode"
    bl_category = "KT FaceRig"

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
        col.label(text='1) Select FaceBuilder')
        col.label(text='2) Disable Mouth and Eyes')
        col.label(text='in model settings')

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

        col = layout.column()
        col.scale_y = 0.75
        col.label(text='1) Select Neutral Animated Mesh')
        col.label(text='2) then select Target Mesh')
        col.label(text='to define neutral shape')
        op = layout.operator('keentools_facerig.actor_operator',
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

        col = layout.column()
        col.scale_y = 0.75
        col.label(text='1) Select Animated Mesh')
        col.label(text='2) then select Rig')
        col.label(text='to bake animation')
        op = layout.operator('keentools_facerig.actor_operator',
                             text='4. Bake Animation')
        op.action = 'bake_animation'


        col = layout.column()
        col.scale_y = 0.75
        col.label(text='This button clear all')
        col.label(text='other objects from scene')
        col.label(text='before export')
        op = layout.operator('keentools_facerig.actor_operator',
                             text='5. Clear Scene')
        op.action = 'clear_scene'

        col = layout.column()
        col.scale_y = 0.75
        col.label(text='Just Export to FBX')
        op = layout.operator('keentools_facerig.actor_operator',
                             text='6. Export Scene')
        op.action = 'export_scene'
