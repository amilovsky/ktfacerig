import bpy
import mathutils
from mathutils import Vector


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


def generate_rig_from_mesh(obj, arm_name='FaceBuilderRig'):
    template_pairs = {'nose': (8863, 14038), 'nose.001': (14038, 13816),
                      'nose.002': (13816, 13821), 'nose.003': (13821, 6661),
                      'nose.004': (6661, 5946), 'lip.T.L': (7900, 4704),
                      'lip.T.L.001': (4704, 5458), 'lip.B.L': (14473, 1461),
                      'lip.B.L.001': (1461, 5458), 'jaw': (12087, 9902),
                      'chin': (9902, 7983), 'chin.001': (7983, 13680),
                      'ear.L': (5235, 12977), 'ear.L.001': (12977, 914),
                      'ear.L.002': (914, 5717), 'ear.L.003': (5717, 922),
                      'ear.L.004': (922, 5235), 'ear.R': (5809, 15542),
                      'ear.R.001': (15542, 2270), 'ear.R.002': (2270, 9404),
                      'ear.R.003': (9404, 2278), 'ear.R.004': (2278, 5809),
                      'lip.T.R': (7900, 6723), 'lip.T.R.001': (6723, 14609),
                      'lip.B.R': (14473, 2837), 'lip.B.R.001': (2837, 14609),
                      'brow.B.L': (13584, 13461), 'brow.B.L.001': (13461, 7909),
                      'brow.B.L.002': (7909, 825), 'brow.B.L.003': (825, 7859),
                      'lid.T.L': (1387, 8116), 'lid.T.L.001': (8116, 570),
                      'lid.T.L.002': (570, 9878), 'lid.T.L.003': (9878, 6500),
                      'lid.B.L': (6500, 7138), 'lid.B.L.001': (7138, 13788),
                      'lid.B.L.002': (13788, 7297), 'lid.B.L.003': (7297, 1387),
                      'brow.B.R': (14967, 14848), 'brow.B.R.001': (14848, 5091),
                      'brow.B.R.002': (5091, 2181),
                      'brow.B.R.003': (2181, 8256), 'lid.T.R': (15178, 1928),
                      'lid.T.R.001': (1928, 1926), 'lid.T.R.002': (1926, 6577),
                      'lid.T.R.003': (6577, 2696), 'lid.B.R': (2696, 8773),
                      'lid.B.R.001': (8773, 15163),
                      'lid.B.R.002': (15163, 5511),
                      'lid.B.R.003': (5511, 15178), 'forehead.L': (14024, 6790),
                      'forehead.L.001': (10669, 13435),
                      'forehead.L.002': (3121, 13580),
                      'temple.L': (12573, 8869), 'jaw.L': (8869, 6883),
                      'jaw.L.001': (6883, 5961), 'chin.L': (5961, 5458),
                      'cheek.B.L': (5458, 373), 'cheek.B.L.001': (373, 250),
                      'brow.T.L': (250, 13580), 'brow.T.L.001': (13580, 13435),
                      'brow.T.L.002': (13435, 6790),
                      'brow.T.L.003': (6790, 8863), 'forehead.R': (15395, 6418),
                      'forehead.R.001': (11434, 14827),
                      'forehead.R.002': (3745, 14963),
                      'temple.R': (12070, 6443), 'jaw.R': (6443, 9237),
                      'jaw.R.001': (9237, 9758), 'chin.R': (9758, 14609),
                      'cheek.B.R': (14609, 1729), 'cheek.B.R.001': (1729, 1606),
                      'brow.T.R': (1606, 14963), 'brow.T.R.001': (14963, 14827),
                      'brow.T.R.002': (14827, 6418),
                      'brow.T.R.003': (6418, 8863), 'cheek.T.L': (250, 13118),
                      'cheek.T.L.001': (13118, 8631), 'nose.L': (8631, 5773),
                      'nose.L.001': (5773, 13816), 'cheek.T.R': (1606, 14516),
                      'cheek.T.R.001': (14516, 5005), 'nose.R': (5005, 6637),
                      'nose.R.001': (6637, 13816)}
    internal_bones = {'spine.006': ((16438, 17068), (11136, 12234))}

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
    points = {8863: 'point-nose', 14038: 'point-nose.001',
              13816: 'point-nose.002', 13821: 'point-nose.003',
              6661: 'point-nose.004', 7900: 'point-lip.T.L',
              4704: 'point-lip.T.L.001', 14473: 'point-lip.B.L',
              1461: 'point-lip.B.L.001', 12087: 'point-jaw',
              9902: 'point-chin', 7983: 'point-chin.001', 5235: 'point-ear.L',
              12977: 'point-ear.L.001', 914: 'point-ear.L.002',
              5717: 'point-ear.L.003', 922: 'point-ear.L.004',
              5809: 'point-ear.R', 15542: 'point-ear.R.001',
              2270: 'point-ear.R.002', 9404: 'point-ear.R.003',
              2278: 'point-ear.R.004', 6723: 'point-lip.T.R.001',
              2837: 'point-lip.B.R.001', 13584: 'point-brow.B.L',
              13461: 'point-brow.B.L.001', 7909: 'point-brow.B.L.002',
              825: 'point-brow.B.L.003', 1387: 'point-lid.T.L',
              8116: 'point-lid.T.L.001', 570: 'point-lid.T.L.002',
              9878: 'point-lid.T.L.003', 6500: 'point-lid.B.L',
              7138: 'point-lid.B.L.001', 13788: 'point-lid.B.L.002',
              7297: 'point-lid.B.L.003', 14967: 'point-brow.B.R',
              14848: 'point-brow.B.R.001', 5091: 'point-brow.B.R.002',
              2181: 'point-brow.B.R.003', 15178: 'point-lid.T.R',
              1928: 'point-lid.T.R.001', 1926: 'point-lid.T.R.002',
              6577: 'point-lid.T.R.003', 2696: 'point-lid.B.R',
              8773: 'point-lid.B.R.001', 15163: 'point-lid.B.R.002',
              5511: 'point-lid.B.R.003', 14024: 'point-forehead.L',
              10669: 'point-forehead.L.001', 3121: 'point-forehead.L.002',
              12573: 'point-temple.L', 8869: 'point-jaw.L',
              6883: 'point-jaw.L.001', 5961: 'point-chin.L',
              5458: 'point-cheek.B.L', 373: 'point-cheek.B.L.001',
              250: 'point-brow.T.L', 13580: 'point-brow.T.L.001',
              13435: 'point-brow.T.L.002', 6790: 'point-brow.T.L.003',
              15395: 'point-forehead.R', 11434: 'point-forehead.R.001',
              3745: 'point-forehead.R.002', 12070: 'point-temple.R',
              6443: 'point-jaw.R', 9237: 'point-jaw.R.001',
              9758: 'point-chin.R', 14609: 'point-cheek.B.R',
              1729: 'point-cheek.B.R.001', 1606: 'point-brow.T.R',
              14963: 'point-brow.T.R.001', 14827: 'point-brow.T.R.002',
              6418: 'point-brow.T.R.003', 13118: 'point-cheek.T.L.001',
              8631: 'point-nose.L', 5773: 'point-nose.L.001',
              14516: 'point-cheek.T.R.001', 5005: 'point-nose.R',
              6637: 'point-nose.R.001', 5946: 'tip-nose.004',
              13680: 'tip-chin.001', 7859: 'tip-brow.B.L.003',
              8256: 'tip-brow.B.R.003'}

    to_object_mode()

    mod = get_object_modifier(animated, 'MESH_SEQUENCE_CACHE')
    mod.show_viewport = False

    if neutral_mesh is not None:
        neutral = get_point_locations(neutral_mesh, points)
    else:
        neutral = get_point_locations(animated, points)

    mod.show_viewport = True
    current = get_point_locations(animated, points)
    delta = get_delta_point_locations(current, neutral)
    # print(delta)
    # print(neutral_mesh)

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
