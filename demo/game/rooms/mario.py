import monkey

from . import state
from .util import *
from .collider import draw_lines
from .factory import *


cn = None
gravity = 500


def on_collect_mushroom(player):
    state.mario_state += 1
    state.mario_state = min(state.mario_state, len(state.mario_states) - 1)
    st = state.mario_states[state.mario_state]
    player.set_model(monkey.get_sprite(st['model']))
    player.get_controller().set_size(st['size'], st['center'])


def make_powerup(b):
    pos = b.get_parent().position
    node = monkey.Node()
    node.set_model(monkey.get_sprite('sprites/mushroom'))
    node.set_position(pos[0] + 8, pos[1], 1)
    sm = monkey.state_machine()
    sm.add(monkey.idle("idle", 'idle'))
    sm.add(monkey.walk_2d_foe("pango", speed=20, gravity=state.gravity, jump_height=80, time_to_jump_apex=0.5, jump_anim='idle'))
    sm.set_initial_state('idle')
    node.add_component(sm)
    node.add_component(monkey.sprite_collider(flags.foe, flags.player, tags.powerup))
    node.add_component(monkey.controller_2d(size=(10, 10, 0), center=(5, 0, 0)))
    node.add_component(monkey.dynamics())
    node.user_data = {'callback': on_collect_mushroom}

    s = monkey.script()
    ii = s.add(monkey.move_by(node=node, y=16, t=1))
    s.add(monkey.set_state(node=node, state='pango'), ii)
    monkey.play(s)
    main = monkey.engine().get_node(cn)
    main.add(node)


def make_coin(b):
    pos = b.position
    def f(comp, node):
        if node.position[1] < pos[1]:
            node.remove()

    node = monkey.Node()
    node.set_model(monkey.get_sprite('sprites/flying_coin'))

    node.set_position(pos[0], pos[1], 1)
    mm = monkey.move_dynamics(1.)
    mm.set_velocity(0, 250, 0)
    mm.set_constant_force(0, -gravity, 0)
    mm.set_callback(f)
    node.add_component(mm)
    main = monkey.engine().get_node(cn)
    main.add(node)







def hit_powerup(player, b):
    b.user_data['callback'](player)
    b.remove()


def hit_sensor(a, b):
    pp = b.get_parent()
    if pp.user_data['hits'] > 0:
        if pp.user_data['hits'] == 1:
            pp.set_animation('taken')
        print(pp.user_data['hits'])
        pp.user_data['hits']-=1
        ad = pp.get_move_dynamics()
        ad.set_velocity(0, 50, 0)
        pp.user_data['callback'](b)
    elif pp.user_data['hits'] == -1:
        if state.mario_state == 0:
            ad = pp.get_move_dynamics()
            ad.set_velocity(0, 50, 0)
        else:
            pp.remove()
            main = monkey.engine().get_node(cn)
            pos = pp.position
            main.add(brick_piece(0, pos[0], pos[1], -100, 150))
            main.add(brick_piece(0, pos[0], pos[1], -50, 250))
            main.add(brick_piece(0, pos[0], pos[1], 100, 150))
            main.add(brick_piece(0, pos[0], pos[1], 50, 250))



def w11():
    global cn
    room = monkey.Room("collision")
    ce = monkey.collision_engine(80, 80)
    ce.add_response(tags.player, tags.sensor, on_start=hit_sensor)
    ce.add_response(tags.player, tags.powerup, on_start=hit_powerup)
    room.add_runner(ce)
    room.add_runner(monkey.scheduler())

    root = room.root()
    kb = monkey.keyboard()
    kb.add(299, 1, 0, pippo)
    root.add_component(kb)

    cam_node = monkey.Node()
    cn = cam_node.id
    state.cn = cam_node.id
    cam = monkey.camera_ortho(256, 240)
    cam_node.set_camera(cam)
    root.add(cam_node)

    # draw lines
    #draw_lines(cam_node)

    cam_node.add(mario(cam, 32, 32))

    cam_node.add(platform(69, 2, 15, 7, 0, 0))
    cam_node.add(platform(15, 2, 15, 7, 71, 0))
    cam_node.add(platform(64, 2, 15, 7, 89, 0))
    cam_node.add(platform(69, 2, 15, 7, 155, 0))
    cam_node.add(platform(4, 1, 15, 8, 134, 2))
    cam_node.add(platform(3, 1, 15, 8, 135, 3))
    cam_node.add(platform(2, 1, 15, 8, 136, 4))
    cam_node.add(platform(1, 1, 15, 8, 137, 5))
    cam_node.add(platform(4, 1, 15, 8, 140, 2))
    cam_node.add(platform(3, 1, 15, 8, 140, 3))
    cam_node.add(platform(2, 1, 15, 8, 140, 4))
    cam_node.add(platform(1, 1, 15, 8, 140, 5))
    cam_node.add(platform(5, 1, 15, 8, 148, 2))
    cam_node.add(platform(4, 1, 15, 8, 149, 3))
    cam_node.add(platform(3, 1, 15, 8, 150, 4))
    cam_node.add(platform(2, 1, 15, 8, 151, 5))
    cam_node.add(platform(1, 1, 15, 8, 152, 5))
    cam_node.add(platform(4, 1, 15, 8, 155, 2))
    cam_node.add(platform(3, 1, 15, 8, 155, 3))
    cam_node.add(platform(2, 1, 15, 8, 155, 4))
    cam_node.add(platform(1, 1, 15, 8, 155, 5))
    cam_node.add(platform(9, 1, 15, 8, 181, 2))
    cam_node.add(platform(8, 1, 15, 8, 182, 3))
    cam_node.add(platform(7, 1, 15, 8, 183, 4))
    cam_node.add(platform(6, 1, 15, 8, 184, 5))
    cam_node.add(platform(5, 1, 15, 8, 185, 6))
    cam_node.add(platform(4, 1, 15, 8, 186, 7))
    cam_node.add(platform(3, 1, 15, 8, 187, 8))
    cam_node.add(platform(2, 1, 15, 8, 188, 9))
    cam_node.add(platform_model(2, 2, 28, 2, 'tiles/pipe2'))
    cam_node.add(platform_model(2, 3, 38, 2, 'tiles/pipe3'))
    cam_node.add(platform_model(2, 4, 46, 2, 'tiles/pipe4'))
    cam_node.add(platform_model(2, 4, 57, 2, 'tiles/pipe4'))
    cam_node.add(platform_model(2, 2, 163, 2, 'tiles/pipe2'))
    cam_node.add(platform_model(2, 2, 179, 2, 'tiles/pipe2'))

    a = (16, 5, 23, 5, 22, 9)
    for i in range(0, len(a), 2):
        cam_node.add(brick(a[i], a[i+1], 'sprites/bonusbrick', 1, make_coin))
    b = (20, 5, 22, 5, 24, 5)
    for i in range(0, len(b), 2):
        cam_node.add(brick(b[i], b[i+1], 'sprites/brick', -1, None))
    c = (21, 5)
    for i in range(0, len(c), 2):
        cam_node.add(brick(c[i], c[i + 1], 'sprites/bonusbrick', 1, make_powerup))
    return room