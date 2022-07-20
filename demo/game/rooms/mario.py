import monkey
from .util import pippo

def mario():
    room = monkey.Room("collision")
    ce = monkey.collision_engine(80, 80)
    #ce.add_response(1, 2, on_start=make_red, on_end=make_white)
    room.add_runner(ce)

    root = room.root()
    kb = monkey.keyboard()
    kb.add(299, 1, 0, pippo)
    root.add_component(kb)

    cam_node = monkey.Node()
    cam = monkey.camera_ortho(256, 240)
    cam_node.set_camera(cam)
    root.add(cam_node)

    node1 = monkey.Node()
    shape = monkey.rect(10, 10, ox=-5, oy=0)
    node1.add_component(monkey.collider(shape, 1, 4, 1))
    node1.add_component(monkey.controller_2d(size=(10, 10, 0), center=(5, 0, 0)))
    node1.add_component(monkey.dynamics())
    node1.set_position(0, 20, 0)
    node1.set_model(monkey.make_model(shape))
    sm = monkey.state_machine()
    sm.add(monkey.walk_2d("pango", speed=50, gravity=150, jump_height=20, time_to_jump_apex=0.5))
    sm.set_initial_state("pango")
    node1.add_component(sm)
    node1.add_component(monkey.follow(cam, (0, 0, 5), (0, 1, 0)))
    cam_node.add(node1)

    node2 = monkey.Node()
    shape1 = monkey.rect(100, 20)
    node2.set_position(-50, -80, 0)
    node2.set_model(monkey.make_model(shape1))
    node2.add_component(monkey.collider(shape1, 2, 1, 2))
    cam_node.add(node2)


    return room