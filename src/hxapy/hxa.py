import ctypes
from enum import *

MAGIC_NUMBER = "HxA\0"
HXA_VERSION_API = "0.3"
LATEST_VERSION = 3

class File():
    def __init__(self, header, nodes):
        self.header = header
        self.nodes = nodes

class Header():
    def __init__(self, magic_number, version, node_count):
        self.magic_number = magic_number
        self.version = version
        self.node_count = node_count

class Meta():
    def __init__(self, name, data_type, data):
        self.name = name
        self.data_type = data_type
        self.data = data

class Node():
    def __init__(self, meta_stack, node_type, content):
        self.node_type = node_type
        self.meta_stack = meta_stack
        self.content = content

class Node_Geomety():
    def __init__(self, vertex_count, vertex_stack, edge_corner_count, corner_stack, edge_stack, face_count, face_stack):
        self.vertex_count = vertex_count
        self.vertex_stack = vertex_stack

        self.edge_corner_count = edge_corner_count
        self.corner_stack = corner_stack
        self.edge_stack = edge_stack

        self.face_count = face_count
        self.face_stack = face_stack

class Node_Image():
    def __init__(self, image_type, resolution, image_stack):
        self.image_type = image_type
        self.resolution = resolution
        self.image_stack = image_stack

class Layer():
    def __init__(self, name, components, data_type, data):
        self.name = name
        self.components = components
        self.data_type = data_type
        self.data = data

class Node_Type(IntEnum):
    Meta_Only = 0
    Geometry = 1
    Image = 2

class Layer_Data_Type(IntEnum):
    Uint8 = 0
    Int32 = 1
    Float = 2
    Double = 3

class Image_Type(IntEnum):
    Image_Cube = 0
    Image_1D = 1
    Image_2D = 2
    Image_3D = 3

class Meta_Type(IntEnum):
    Int64  = 0
    Double = 1
    Node   = 2
    Text   = 3
    Binary = 4
    Meta   = 5

CONVENTION_HARD_BASE_VERTEX_LAYER_NAME       = "vertex"
CONVENTION_HARD_BASE_VERTEX_LAYER_ID         = 0
CONVENTION_HARD_BASE_VERTEX_LAYER_COMPONENTS = 3
CONVENTION_HARD_BASE_CORNER_LAYER_NAME       = "reference"
CONVENTION_HARD_BASE_CORNER_LAYER_ID         = 0
CONVENTION_HARD_BASE_CORNER_LAYER_COMPONENTS = 1
CONVENTION_HARD_BASE_CORNER_LAYER_TYPE       = Layer_Data_Type.Int32
CONVENTION_HARD_EDGE_NEIGHBOUR_LAYER_NAME    = "neighbour"
CONVENTION_HARD_EDGE_NEIGHBOUR_LAYER_TYPE    = Layer_Data_Type.Int32

CONVENTION_SOFT_LAYER_SEQUENCE       = "sequence"
CONVENTION_SOFT_LAYER_NAME_UV        = "uv"
CONVENTION_SOFT_LAYER_NORMALS        = "normal"
CONVENTION_SOFT_LAYER_BINORMAL       = "binormal"
CONVENTION_SOFT_LAYER_TANGENT        = "tangent"
CONVENTION_SOFT_LAYER_COLOR          = "color"
CONVENTION_SOFT_LAYER_CREASES        = "creases"
CONVENTION_SOFT_LAYER_SELECTION      = "select"
CONVENTION_SOFT_LAYER_SKIN_WEIGHT    = "skining_weight"
CONVENTION_SOFT_LAYER_SKIN_REFERENCE = "skining_reference"
CONVENTION_SOFT_LAYER_BLENDSHAPE     = "blendshape"
CONVENTION_SOFT_LAYER_ADD_BLENDSHAPE = "addblendshape"
CONVENTION_SOFT_LAYER_MATERIAL_ID    = "material"

CONVENTION_SOFT_ALBEDO            = "albedo"
CONVENTION_SOFT_LIGHT             = "light"
CONVENTION_SOFT_DISPLACEMENT      = "displacement"
CONVENTION_SOFT_DISTORTION        = "distortion"
CONVENTION_SOFT_AMBIENT_OCCLUSION = "ambient_occlusion"

CONVENTION_SOFT_NAME      = "name"
CONVENTION_SOFT_TRANSFORM = "transform"

def write_to_file (filepath, hxa_file):
    os_file = open(filepath, 'wb')
    write_header(os_file, hxa_file.header)
    for node in hxa_file.nodes:
        write_node(os_file, node)

def write_header(os_file, header):
    print("writing header")
    os_file.write(bytes(header.magic_number, 'utf-8'))
    os_file.write(ctypes.c_uint32(header.version))
    os_file.write(ctypes.c_uint32(header.node_count))
    

def write_node(os_file, node):
    os_file.write(ctypes.c_uint8(node.node_type))

    os_file.write(ctypes.c_uint32(len(node.meta_stack)))
    for meta in node.meta_stack:
        write_meta(os_file, meta)

    if(node.node_type == Node_Type.Geometry):
        write_geometry_node(os_file, node.content)
    elif(node.node_type == Node_Type.Image):
        write_image_node(os_file, node.content)

def write_meta(os_file, meta):
    print("writing metadata" + meta.name)
    write_name(os_file, meta.name)
    os_file.write(ctypes.c_uint8(meta.data_type))

    if (meta.data_type == Meta_Type.Int64):
        os_file.write(ctypes.c_uint32(len(meta.data)))
        for value in data:
            os_file.write(ctypes.c_int64(value))

    elif (meta.data_type == Meta_Type.Double):
        os_file.write(ctypes.c_uint32(len(meta.data)))
        for value in data:
            os_file.write(ctypes.c_double(value))

    elif (meta.data_type == Meta_Type.Node):
        os_file.write(ctypes.c_uint32(len(meta.data)))
        for value in data:
            write_node(os_file, node)

    elif (meta.data_type == Meta_Type.Text):
        write_string(os_file, meta.data)

    elif (meta.data_type == Meta_Type.Binary):
        os_file.write(ctypes.c_uint32(len(meta.data)))
        for value in data:
            os_file.write(ctypes.c_uint8(value))

    elif (meta.data_type == Meta_Type.Meta):
        os_file.write(ctypes.c_uint32(len(meta.data)))
        for value in data:
            write_meta(os_file, value)

def write_geometry_node(os_file, content):
    print("writing geometry node")
    os_file.write(ctypes.c_uint32(content.vertex_count))
    write_layer_stack(os_file, content.vertex_stack)

    os_file.write(ctypes.c_uint32(content.edge_corner_count))
    write_layer_stack(os_file, content.corner_stack)
    write_layer_stack(os_file, content.edge_stack)


    os_file.write(ctypes.c_uint32(content.face_count))
    write_layer_stack(os_file, content.face_stack)


def write_image_node(os_file, content):
    print("writing image node")
    os_file.write(ctypes.c_uint8(content.image_type))

    for dim in content.resolution:
        os_file.write(ctypes.c_uint32(dim))

    write_layer_stack(os_file, content.image_stack)

def write_layer_stack(os_file, stack):
    print("writing layer stack")
    os_file.write(ctypes.c_uint32(len(stack)))
    for layer in stack:
        write_layer(os_file, layer)


def write_layer(os_file, layer):
    print("writing layer: " + layer.name)
    write_name(os_file, layer.name)
    os_file.write(ctypes.c_uint8(layer.components))
    os_file.write(ctypes.c_uint8(layer.data_type))

    if (layer.data_type == Layer_Data_Type.Uint8):
        for value in layer.data:
            os_file.write(ctypes.c_uint8(value))
    elif(layer.data_type == Layer_Data_Type.Int32):
        for value in layer.data:
            os_file.write(ctypes.c_int32(value))
    elif(layer.data_type == Layer_Data_Type.Float):
        for value in layer.data:
            os_file.write(ctypes.c_float(value))
    elif(layer.data_type == Layer_Data_Type.Double):
         for value in layer.data:
            os_file.write(ctypes.c_double(value))

def write_name(os_file, name):
    print("writing name: " + name)
    os_file.write(ctypes.c_uint8(len(name)))
    os_file.write(bytes(name, 'utf-8'))

def write_string(os_file, string):
    print("writing string: " + string)
    os_file.write(ctypes.c_uint32(len(string)))
    os_file.write(bytes(string, 'utf-8'))

def triangle():
    vertex_count = 3
    vertex_position_data = [-1.0, 0.0, 0.0, 0.0, 0.0, 2.0, 1.0, 0.0, 0.0]
    vertex_position_layer = Layer(CONVENTION_HARD_BASE_VERTEX_LAYER_NAME, CONVENTION_HARD_BASE_VERTEX_LAYER_COMPONENTS, Layer_Data_Type.Float, vertex_position_data)
    vertex_uv_data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    vertex_uv_layer = Layer(CONVENTION_SOFT_LAYER_NAME_UV, 2, Layer_Data_Type.Float, vertex_uv_data)
    vertex_normal_data = [0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0]
    vertex_normal_layer = Layer(CONVENTION_SOFT_LAYER_NORMALS, 3, Layer_Data_Type.Float, vertex_normal_data)
    vertex_stack = [vertex_position_layer, vertex_uv_layer, vertex_normal_layer]


    corner_data = [0, 1, -3]
    corner_stack = [Layer(CONVENTION_HARD_BASE_CORNER_LAYER_NAME, CONVENTION_HARD_BASE_CORNER_LAYER_COMPONENTS, CONVENTION_HARD_BASE_CORNER_LAYER_TYPE, corner_data)]
    

    edge_data = [0, 1, 1, 2, 2, 0]
    edge_stack = [Layer(CONVENTION_HARD_EDGE_NEIGHBOUR_LAYER_NAME, 2, CONVENTION_HARD_EDGE_NEIGHBOUR_LAYER_TYPE, edge_data)]
    edge_corner_count = 3

    face_data = [0]
    face_layer = Layer("faces", 1, Layer_Data_Type.Int32, face_data)
    face_stack = [face_layer]
    face_count = 1
  
    content = Node_Geomety(vertex_count, vertex_stack, edge_corner_count, corner_stack, edge_stack, face_count, face_stack)

    meta_name = "test quad"
    meta_data = "test meta text"
    meta_stack = [Meta(meta_name, Meta_Type.Text, meta_data)]

    node_type = Node_Type.Geometry
    
    nodes = [Node(meta_stack, node_type, content)]
    header = Header(MAGIC_NUMBER, LATEST_VERSION, len(nodes))
    hxa_file = File(header, nodes)

    return hxa_file