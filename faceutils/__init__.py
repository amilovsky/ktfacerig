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

import logging

import bpy
import mathutils
from mathutils import Vector
from .topology_data import (TopologyVersion,
                            version_by_object,
                            get_topology_data,
                            get_points_data)


_logger = logging.getLogger(__name__)
_log = lambda: None
_log.logger = _logger
_log.output = _logger.debug
_log.error = _logger.error


def create_empty(name, size=0.5, display_type='ARROWS'):  # 'PLAIN_AXES'
    em = bpy.data.objects.new( "empty", None )
    bpy.context.scene.collection.objects.link(em)
    em.empty_display_size = size
    em.empty_display_type = display_type
    em.name = name
    return em


def create_empties_from_bones(armature, bones):
    for bone in bones:
        em = create_empty(bone.name)
        em.matrix_world = armature.matrix_world @ bone.matrix


def all_empties_list():
    return [obj for obj in bpy.context.scene.objects if obj.type == 'EMPTY']


def get_bones_with_prefix_list(bones, name_prefix):
    return [bone for bone in bones if bone.name[:len(name_prefix)] == name_prefix]


def get_deform_bones_list(arm_obj):
    return [bone for bone in arm_obj.pose.bones if bone.bone.use_deform]


def get_edit_bones_list(arm_obj):
    return [bone for bone in arm_obj.data.edit_bones]


def get_pose_bones_list(arm_obj):
    return [bone for bone in arm_obj.pose.bones]


def selected_pose_bones_list():
    return [bone for bone in bpy.context.selected_pose_bones]


def select_object(obj):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(state=True)
    bpy.context.view_layer.objects.active = obj


def to_edit_mode():
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)


def to_object_mode():
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)


def to_pose_mode():
    bpy.ops.object.mode_set(mode='POSE', toggle=False)


def get_kd_from_mesh(obj):
    mesh = obj.data
    # create a kd-tree from a mesh
    size = len(mesh.vertices)
    kd = mathutils.kdtree.KDTree(size)
    for i, v in enumerate(mesh.vertices):
        kd.insert(v.co, i)
        print(v.co)
    kd.balance()
    return kd


def create_armature(name='our_armature'):
    arm = bpy.data.armatures.new('armature')
    arm_obj = bpy.data.objects.new(name, arm)
    bpy.context.scene.collection.objects.link(arm_obj)
    return arm_obj


def add_bone(armature, name, loc=(0.0, 0.0, 0.0), vec=(0.0, 0.0, 0.2)):
    b = armature.data.edit_bones.new(name)
    b.head = loc
    b.tail = Vector(loc) + Vector(vec)
    return b


def add_root(armature, root_name):
    bones = get_edit_bones_list(armature)
    root = add_bone(armature, root_name, loc=(0, 0, 0))
    for bone in bones:
        bone.parent = root
    return root


def create_bones_from_empties(armature, empties):
    select_object(armature)
    to_edit_mode()
    for em in empties:
        add_bone(armature, em.name, em.location)
    to_object_mode()


def create_bones_at_points(armature, mesh, points):
    for name in points:
        vert = mesh.vertices[points[name]]
        add_bone(armature, name, vert.co, (0.0, 0.2, 0.0))


def get_object_modifier(obj, mod_type='MESH_SEQUENCE_CACHE'):
    for m in obj.modifiers:
        if m.type == mod_type:
            return m
    return None


def get_evaluated_mesh(obj):
    dg = bpy.context.evaluated_depsgraph_get()
    ev = obj.evaluated_get(dg)
    return ev.to_mesh()


# Functions for Custom Attributes perform
def has_custom_attribute(obj, attr_name):
    return attr_name in obj.keys()


def get_custom_attribute(obj, attr_name):
    return obj[attr_name]


def get_safe_custom_attribute(obj, attr_name):
    if has_custom_attribute(obj, attr_name):
        return obj[attr_name]
    else:
        return None


def set_custom_attribute(obj, attr_name, val):
    obj[attr_name] = val


def generate_rig_from_mesh(obj, arm_name='FaceBuilderRig', ver=TopologyVersion.v1):
    template_pairs, internal_bones = get_topology_data(ver)

    points = {}
    for name in template_pairs:
        index = template_pairs[name][0]
        if index not in points.keys():
            points[index] = 'point-' + name

    for name in template_pairs:
        index = template_pairs[name][1]
        if index not in points.keys():
            points[index] = 'tip-' + name

    # print(points)

    to_object_mode()
    mesh = obj.data

    arm_obj = create_armature(arm_name)
    select_object(arm_obj)
    to_edit_mode()
    for name in points:
        v1 = mesh.vertices[name]
        bone = add_bone(arm_obj, points[name], obj.matrix_world @ v1.co,
                           (0.0, -0.2, 0.0))
        bone.use_deform = False

    for name in template_pairs:
        v1 = mesh.vertices[template_pairs[name][0]]
        v2 = mesh.vertices[template_pairs[name][1]]
        bone = add_bone(arm_obj, 'DEF-' + name, obj.matrix_world @ v1.co)
        bone.tail = obj.matrix_world @ v2.co

    root = add_root(arm_obj, 'root')
    name = 'spine.006'
    v1 = mesh.vertices[internal_bones[name][0][0]]
    v2 = mesh.vertices[internal_bones[name][0][1]]
    root.head = obj.matrix_world @ (0.5 * v1.co + 0.5 * v2.co)
    v1 = mesh.vertices[internal_bones[name][1][0]]
    v2 = mesh.vertices[internal_bones[name][1][1]]
    root.tail = obj.matrix_world @ (0.5 * v1.co + 0.5 * v2.co)

    to_pose_mode()
    for name in template_pairs:
        bone = arm_obj.pose.bones['DEF-' + name]
        ind1 = template_pairs[name][0]
        ind2 = template_pairs[name][1]
        copy_loc = bone.constraints.new('COPY_LOCATION')
        stretch_to = bone.constraints.new('STRETCH_TO')
        copy_loc.target = arm_obj
        copy_loc.subtarget = points[ind1]
        stretch_to.target = arm_obj
        stretch_to.subtarget = points[ind2]

    to_object_mode()
    return arm_obj


def get_point_locations(obj, points):
    res = {}
    mesh = get_evaluated_mesh(obj)

    if len(mesh.vertices) < len(points):
        return None
    for num in points:
        res[num] = mesh.vertices[num].co.copy()
    return res


def get_delta_point_locations(current, neutral):
    if current is None or neutral is None:
        return None
    delta = {}
    for num in current:
        delta[num] = current[num] - neutral[num]
    return delta


def bake_animation_to_rig(animated, arm_obj, neutral_mesh=None):
    ver = version_by_object(animated)
    points = get_points_data(ver)
    _log.output(f'bake_animation_to_rig points:\n{points}')

    to_object_mode()

    mod = get_object_modifier(animated, 'MESH_SEQUENCE_CACHE')
    _log.output(f'mod: {mod}')
    if mod is not None:
        mod.show_viewport = False

    _log.output(f'neutral_mesh: {neutral_mesh}')
    if neutral_mesh is not None:
        neutral = get_point_locations(neutral_mesh, points)
    else:
        neutral = get_point_locations(animated, points)

    if mod is not None:
        mod.show_viewport = True
    current = get_point_locations(animated, points)
    delta = get_delta_point_locations(current, neutral)
    _log.output(f'bake_animation_to_rig delta:\n{delta}')

    select_object(arm_obj)
    to_pose_mode()
    if delta is not None:
        for num in delta:
            bone = arm_obj.pose.bones[points[num]]
            reposition_bone(bone, delta[num])

    scene = bpy.context.scene
    current_frame = scene.frame_current
    for i in range(scene.frame_start, scene.frame_end + 1):
        scene.frame_set(i)
        current = get_point_locations(animated, points)
        delta = get_delta_point_locations(current, neutral)
        if delta is not None:
            for num in delta:
                bone = arm_obj.pose.bones[points[num]]
                reposition_bone(bone, delta[num])
                bone.keyframe_insert(data_path='location', frame=i)

    to_object_mode()
    scene.frame_current = current_frame


def reposition_bone(bone, delta):
    # loc = bone.bone.matrix_local @ bone.location.copy() + delta[num]
    loc = bone.bone.matrix_local @ Vector((0, 0, 0)) + delta
    bone.location = bone.bone.matrix_local.inverted() @ loc
