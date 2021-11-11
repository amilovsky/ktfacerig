import enum


class TopologyVersion(enum.Enum):
    undefined = enum.auto()
    v1 = enum.auto()
    v2 = enum.auto()
    v3 = enum.auto()


def _get_topology_data1():
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
    return template_pairs, internal_bones


def _get_topology_data2():
    template_pairs = {'nose':(3895, 5674), 'nose.001':(5674, 5723),
                      'nose.002':(5723, 5381), 'nose.003':(5381, 5257),
                      'nose.004':(5257, 8770), 'lip.T.L':(9314, 9114),
                      'lip.T.L.001':(9114, 9649), 'lip.B.L':(9177, 8659),
                      'lip.B.L.001':(8659, 9649), 'jaw':(9861, 9317),
                      'chin':(9317, 8673), 'chin.001':(8673, 8769),
                      'ear.L':(10741, 11832), 'ear.L.001':(11832, 11695),
                      'ear.L.002':(11695, 11174), 'ear.L.003':(11174, 11182),
                      'ear.L.004':(11182, 10741), 'ear.R':(10652, 11898),
                      'ear.R.001':(11898, 10526), 'ear.R.002':(10526, 11128),
                      'ear.R.003':(11128, 11390), 'ear.R.004':(11390, 10652),
                      'lip.T.R':(9314, 6704), 'lip.T.R.001':(6704, 6606),
                      'lip.B.R':(9177, 7550), 'lip.B.R.001':(7550, 6606),
                      'brow.B.L':(2388, 2099), 'brow.B.L.001':(2099, 3441),
                      'brow.B.L.002':(3441, 2531), 'brow.B.L.003':(2531, 4325),
                      'lid.T.L':(2978, 2200), 'lid.T.L.001':(2200, 3182),
                      'lid.T.L.002':(3182, 946), 'lid.T.L.003':(946, 1143),
                      'lid.B.L':(1143, 651), 'lid.B.L.001':(651, 1219),
                      'lid.B.L.002':(1219, 4147), 'lid.B.L.003':(4147, 2978),
                      'brow.B.R':(125, 3733), 'brow.B.R.001':(3733, 4135),
                      'brow.B.R.002':(4135, 932), 'brow.B.R.003':(932, 4322),
                      'lid.T.R':(2971, 293), 'lid.T.R.001':(293, 3730),
                      'lid.T.R.002':(3730, 3651), 'lid.T.R.003':(3651, 1635),
                      'lid.B.R':(1635, 1647), 'lid.B.R.001':(1647, 652),
                      'lid.B.R.002':(652, 2818), 'lid.B.R.003':(2818, 2971),
                      'forehead.L':(2549, 2547),
                      'forehead.L.001':(13388, 2720),
                      'forehead.L.002':(14789, 2386),
                      'temple.L':(13407, 821), 'jaw.L':(821, 9207),
                      'jaw.L.001':(9207, 9134), 'chin.L':(9134, 9649),
                      'cheek.B.L':(9649, 4253),
                      'cheek.B.L.001':(4253, 2068), 'brow.T.L':(2068, 2386),
                      'brow.T.L.001':(2386, 2720), 'brow.T.L.002':(2720, 2547),
                      'brow.T.L.003':(2547, 3895), 'forehead.R':(892, 3189),
                      'forehead.R.001':(14492, 463),
                      'forehead.R.002':(13110, 138), 'temple.R':(14203, 4015),
                      'jaw.R':(4015, 5803), 'jaw.R.001':(5803, 7539),
                      'chin.R':(7539, 6606), 'cheek.B.R':(6606, 4246),
                      'cheek.B.R.001':(4246, 434), 'brow.T.R':(434, 138),
                      'brow.T.R.001':(138, 463), 'brow.T.R.002':(463, 3189),
                      'brow.T.R.003':(3189, 2141), 'cheek.T.L':(2068, 0),
                      'cheek.T.L.001':(0, 3695), 'nose.L':(3695, 5214),
                      'nose.L.001':(5214, 5723), 'cheek.T.R':(434, 1),
                      'cheek.T.R.001':(1, 1478), 'nose.R':(1478, 5167),
                      'nose.R.001':(5167, 5723)}
    internal_bones = {'spine.006': ((15876, 15788), (14983, 13600))}
    return template_pairs, internal_bones


def version_by_vertices_count(vertices_count):
    if vertices_count == 17200:
        return TopologyVersion.v1
    elif vertices_count == 17838:
        return TopologyVersion.v2
    return TopologyVersion.undefined


def version_by_object(obj):
    if obj is None or obj.type != 'MESH':
        return TopologyVersion.undefined
    return version_by_vertices_count(len(obj.data.vertices))


def get_topology_data(ver=TopologyVersion.v1):
    if ver == TopologyVersion.v1:
        return _get_topology_data1()
    elif ver == TopologyVersion.v2:
        return _get_topology_data2()
    return {}, {}


def _convert_to_points(template_pairs):
    points = {}
    for name in template_pairs:
        index = template_pairs[name][0]
        if index not in points.keys():
            points[index] = 'point-' + name

    for name in template_pairs:
        index = template_pairs[name][1]
        if index not in points.keys():
            points[index] = 'tip-' + name
    return points


def get_points_data(ver=TopologyVersion.v1):
    if ver == TopologyVersion.v1:
        template_pairs, _ = _get_topology_data1()
        return _convert_to_points(template_pairs)
    elif ver == TopologyVersion.v2:
        template_pairs, _ = _get_topology_data2()
        return _convert_to_points(template_pairs)
    return {}
