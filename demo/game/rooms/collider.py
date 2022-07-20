import monkey
import numpy as np
import math

def make_red(a, b):
    b.set_mult_color(1,0,0,1)


def make_white(a, b):
    b.set_mult_color(1,1,1,1)

def draw_lines(parent):
    # draw lines
    for i in range(-2, 2):
        cn = monkey.Node()
        cn.set_model(monkey.RawModel(monkey.SHADER_COLOR, np.array([-160, 80 * i, 0, 1, 1, 1, 1, 160, 80 * i, 0, 1, 1, 1, 1]), np.array([0, 1]), prim=monkey.LINES))
        parent.add(cn)
    for i in range(-2, 2):
        cn = monkey.Node()
        cn.set_model(monkey.RawModel(monkey.SHADER_COLOR, np.array([80*i, -160, 0, 1, 1, 1, 1, 80*i,160, 0, 1, 1, 1, 1]), np.array([0, 1]), prim=monkey.LINES))
        parent.add(cn)


def make_node(shape, x, y):
    node = monkey.Node()
    node.set_position(x, y, 0)
    node.set_model(monkey.make_model(shape, points=100))
    node.add_component(monkey.collider(shape, 2, 1, 2))
    return node


def collider3():
    room = monkey.Room("collision")
    ce = monkey.collision_engine(80, 80)
    ce.add_response(1, 2, on_start=make_red, on_end=make_white)
    room.add_runner(ce)

    root = room.root()

    cam_node = monkey.Node()
    cam = monkey.camera_perspective(far =1000)
    cam_node.set_camera(cam)
    root.add(cam_node)

    draw_lines(cam_node)

    node1 = monkey.Node()
    shape = monkey.rect(10, 10, ox=-5, oy=-5)
    node1.add_component(monkey.collider(shape, 1, 1|2, 1))
    node1.add_component(monkey.controller())
    node1.add_component(monkey.dynamics())
    node1.add_component(monkey.follow(cam, (0, -80, 30), (0, 0, 1)))
    node1.set_model(monkey.make_model(shape))

    sm = monkey.state_machine()
    sm.add(monkey.car_2d("pango", speed=50, rotation_speed=1.))
    sm.set_initial_state("pango")
    node1.add_component(sm)

    cam_node.add(node1)

    # objects
    cam_node.add(make_node(monkey.rect(100, 20), -50, -80))
    cam_node.add(make_node(monkey.circle(20), 0, 50))
    cam_node.add(make_node(monkey.convex_poly(np.array([0,0,20,0,30,10,15,10])), 40, 50))

    n1 = monkey.Node()
    n1.set_position(-50, -30, 0)
    cs = monkey.compound_shape()
    cs.add_shape(monkey.rect(50, 20))
    cs.add_shape(monkey.rect(20, 50, ox=50))
    cs.add_shape(monkey.circle(10, oy=10))
    n1.set_model(monkey.make_model(cs, points=100))
    n1.add_component(monkey.collider(cs, 2, 1, 2))

    cam_node.add(n1)
    return room

def collider2():
    room = monkey.Room("collision")
    ce = monkey.collision_engine(80, 80)
    ce.add_response(1, 2, on_start=make_red, on_end=make_white)
    room.add_runner(ce)

    root = room.root()

    cam_node = monkey.Node()
    cam_node.set_camera(monkey.camera_ortho(256, 240))
    root.add(cam_node)

    draw_lines(cam_node)

    node1 = monkey.Node()
    shape = monkey.rect(10, 10, ox=-5, oy=-5)
    node1.add_component(monkey.collider(shape, 1, 1|2, 1))
    node1.add_component(monkey.controller())
    node1.add_component(monkey.dynamics())
    node1.set_model(monkey.make_model(shape))

    sm = monkey.state_machine()
    sm.add(monkey.car_2d("pango", speed=50, rotation_speed=1.))
    sm.set_initial_state("pango")
    node1.add_component(sm)

    cam_node.add(node1)

    node2 = monkey.Node()
    shape1 = monkey.rect(100, 20)
    node2.set_position(-50, -80, 0)
    node2.set_model(monkey.make_model(shape1))
    node2.add_component(monkey.collider(shape1, 2, 1, 2))
    cam_node.add(node2)

    return room

def pippo():
    monkey.engine().close_room()


def make_ramp(width, height, up, x, y):
    node3 = monkey.Node()
    shape2 = monkey.convex_poly(np.array([0, 0, width, 0, width if up else 0, height]))
    node3.set_position(x, y, 0)
    node3.set_model(monkey.make_model(shape2))
    node3.add_component(monkey.collider(shape2, 2, 1, 2))
    return node3

def make_moving_platform(width, func):
    node = monkey.Node()
    shape = monkey.segment(0, 0, width, 0)
    node.set_model(monkey.make_model(shape))
    node.add_component(monkey.collider(shape, 32, 1, 2))
    node.add_component(monkey.move(func))
    node.add_component(monkey.platform())
    pos = func(0)
    node.set_position(pos[0], pos[1], pos[2])
    return node


def g(t):
    a = t/2.
    return -10 + 2 * 10 * abs(a - math.floor(a + 0.5)), -30, 0, 0

def h(t):
    a = t/5.
    return 120, -70 + 2 * 140 * abs(a - math.floor(a + 0.5)), -30, 0, 0


def collider():
    room = monkey.Room("collision")
    ce = monkey.collision_engine(80, 80)
    ce.add_response(1, 2, on_start=make_red, on_end=make_white)
    room.add_runner(ce)

    root = room.root()
    kb = monkey.keyboard()
    kb.add(299, 1, 0, pippo)
    root.add_component(kb)


    cam_node = monkey.Node()
    cam = monkey.camera_ortho(256, 240)
    cam_node.set_camera(cam)
    root.add(cam_node)

    # draw lines
    draw_lines(cam_node)

    node1 = monkey.Node()
    shape = monkey.rect(10, 10, ox=-5, oy=0)
    node1.add_component(monkey.collider(shape, 1, 4, 1))
    node1.add_component(monkey.controller_2d(size=(10, 10, 0), center=(5, 0, 0)))
    node1.add_component(monkey.dynamics())
    node1.set_position(130, 20, 0)
    node1.set_model(monkey.make_model(shape))

    sm = monkey.state_machine()
    sm.add(monkey.walk_2d("pango", speed=50, gravity=150, jump_height=20, time_to_jump_apex=0.5))
    sm.set_initial_state("pango")
    node1.add_component(sm)
    node1.add_component(monkey.follow(cam, (0, 0, 5), (0, 1, 0)))

    node2 = monkey.Node()
    shape1 = monkey.rect(100, 20)
    node2.set_position(-50, -80, 0)
    node2.set_model(monkey.make_model(shape1))
    node2.add_component(monkey.collider(shape1, 2, 1, 2))

    node3 = monkey.Node()
    shape2 = monkey.convex_poly(np.array([0,0,50,0, 50, 10]))
    node3.set_position(6, -60, 0)
    node3.set_model(monkey.make_model(shape2))
    node3.add_component(monkey.collider(shape2, 2, 1, 2))

    cam_node.add(node2)
    cam_node.add(node3)
    cam_node.add(make_ramp(50, 50, True, 70, -60))
    cam_node.add(make_ramp(50, 50, False, -120, -70))

    # add moving platform
    cam_node.add(make_moving_platform(50, g))
    cam_node.add(make_moving_platform(50, h))
    cam_node.add(node1)


    return room