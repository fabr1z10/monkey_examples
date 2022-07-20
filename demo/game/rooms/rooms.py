import monkey
import numpy as np
import math

def w1_1():
    room = monkey.Room("test")
    a = monkey.RawModel(monkey.SHADER_COLOR, np.array([
        -64, -64, 0, 1, 0, 0, 1,
        64, -64, 0, 0, 1, 0, 1,
        0, 64, 0, 0, 0, 1, 1]), np.array([0, 1, 2]))
    root = room.root()

    cam_node = monkey.Node()
    cam_node.set_camera(monkey.camera_ortho(256, 240))
    root.add(cam_node)

    node = monkey.Node()
    node.set_model(a)
    #node.set_position(0,0,0)
    cam_node.add(node)
    return room


def w1_2():
    room = monkey.Room("test")
    a = monkey.RawModel(monkey.SHADER_TEXTURE, np.array([
        -64, -64, 0, 0, 1, 1, 1, 1, 1,
        64, -64, 0, 1, 1, 1, 1, 1, 1,
        0, 64, 0, 0.5, 0.0, 1, 1, 1, 1]), np.array([0, 1, 2]), tex='assets/wood.jpeg')
    root = room.root()

    cam_node = monkey.Node()
    cam_node.set_camera(monkey.camera_ortho(256, 240))
    root.add(cam_node)

    node = monkey.Node()
    node.set_model(a)
    #node.set_position(0,0,0)
    cam_node.add(node)
    return room


def text():
    room = monkey.Room("text")
    root = room.root()
    cam_node = monkey.Node()
    cam_node.set_camera(monkey.camera_ortho(256, 240))
    root.add(cam_node)
    node = monkey.Node()
    node.set_model(monkey.text(font='font1', text='CIAO\nBELO', size=8))
    cam_node.add(node)
    node.set_position(-128,120,0)

    node1 = monkey.Node()
    node1.set_model(monkey.get_sprite('sprites/mario'))
    cam_node.add(node1)
    return room


def w1_3():
    room = monkey.Room("test")
    b = monkey.RawModel(monkey.SHADER_COLOR, np.array([
        -64, -64, 0, 1, 0, 0, 1,
        64, -64, 0, 0, 1, 0, 1,
        0, 64, 0, 0, 0, 1, 1]), np.array([0, 1, 2]))
    a = monkey.RawModel(monkey.SHADER_TEXTURE, np.array([
        -64, -64, 0, 0, 1, 1, 1, 1, 1,
        64, -64, 0, 1, 1, 1, 1, 1, 1,
        0, 64, 0, 0.5, 0.0, 1, 1, 1, 1]), np.array([0, 1, 2]), tex='assets/wood.jpeg')

    root = room.root()

    cam_node = monkey.Node()
    cam_node.set_camera(monkey.camera_ortho(256, 240))
    root.add(cam_node)

    node1 = monkey.Node()
    node1.set_model(b)
    node1.set_position(64, 0, 0)
    cam_node.add(node1)
    node = monkey.Node()
    node.set_model(a)
    node.set_position(-64,0,0)
    cam_node.add(node)

    return room


def f(t):
    return 0, 0, 0, (math.pi*t) % (2*math.pi)



def composition():
    room = monkey.Room("collision")
    root = room.root()

    cam_node = monkey.Node()
    cam_node.set_camera(monkey.camera_ortho(256, 240))
    root.add(cam_node)

    node1 = monkey.Node()
    shape = monkey.rect(10, 10, ox=5, oy=5)
    node1.set_model(monkey.make_model(shape))
    node1.add_component(monkey.move(f))
    cam_node.add(node1)

    node2 = monkey.Node()
    shape2 = monkey.rect(2, 20, ox=1)
    node2.set_model(monkey.make_model(shape2))
    node2.set_position(0, 5, 0)
    node1.add(node2)
    return room

