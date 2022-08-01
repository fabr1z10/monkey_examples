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






def hit_powerup(player, b, dist):
    b.user_data['callback'](player)
    b.remove()


def jump_on_foe(player, foe, callback=None):
    a = player.get_dynamics()
    a.velocity.y = 200
    foe.set_state('dead')
    #if callback:
    #    callback(foe)

def reset_invincibility():
    state.invincible = False

def mario_is_hit(player, foe):
    if state.invincible:
        return
    if state.mario_state == 0:
        player.set_state('dead')
        s = monkey.script()
        ii = s.add(monkey.delay(1))
        ii = s.add(monkey.move_accelerated(id=player.id,
                                           timeout=1,
                                           velocity=monkey.vec3(0, 100, 0),
                                           acceleration=monkey.vec3(0, -state.gravity, 0)), ii)
        # s.add(monkey.remove(id=player.id), ii)
        s.add(monkey.callfunc(pippo), ii)
        monkey.play(s)
    else:
        state.mario_state -= 1
        state.invincible = True
        st = state.mario_states[state.mario_state]
        player.set_model(monkey.get_sprite(st['model']))
        player.get_controller().set_size(st['size'], st['center'])
        s = monkey.script()
        ii = s.add(monkey.blink(id=player.id, duration=state.invincible_duration, period=0.2))
        s.add(monkey.callfunc(reset_invincibility), ii)
        monkey.play(s)



def hit_goomba(player, foe, dist):
    print(dist.x, dist.y, dist.z)
    print(player.id, " " , foe.id)
    if dist.y > 0:
        jump_on_foe(player, foe)
    else:
        mario_is_hit(player, foe)

def hit_gk(goomba, koopa, dist):
    if koopa.state == 'fly':
        goomba.set_state('dead2')
        s = monkey.script()
        ii = s.add(monkey.move_accelerated(id=goomba.id,
                                           timeout=0.5,
                                           velocity=monkey.vec3(-50 if koopa.x > goomba.x else 50, 100, 0),
                                           acceleration=monkey.vec3(0, -state.gravity, 0)))
        s.add(monkey.remove(id=goomba.id), ii)
        monkey.play(s)


def hit_koopa(player, foe, dist):
    if foe.state == 'dead':
        direction = 0
        if dist.x != 0:
            direction = -1 if dist.x > 0 else 1
        else:
            direction = -1 if player.x > foe.x else 1
        foe.set_state('fly', dir=direction)
    else:
        hit_goomba(player, foe, dist)


def hit_hotspot(player, hotspot, dist):
    on_start = hotspot.user_data.get('on_start')
    if on_start:
        on_start()
    rm = hotspot.user_data.get('remove', True)
    if rm:
        hotspot.remove()


def leave_hotspot(player, hotspot):
    on_end= hotspot.user_data.get('on_end')
    if on_end:
        on_end()


def hit_sensor(a, b, dist):
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
            a.get_dynamics().velocity.y = 0


            main = monkey.engine().get_node(cn)
            pos = pp.position
            main.add(brick_piece(0, pos[0], pos[1], -100, 150))
            main.add(brick_piece(0, pos[0], pos[1], -50, 250))
            main.add(brick_piece(0, pos[0], pos[1], 100, 150))
            main.add(brick_piece(0, pos[0], pos[1], 50, 250))



def w11():
    global cn
    world_width = 3584
    room = monkey.Room("collision")
    ce = monkey.collision_engine(80, 80)
    ce.add_response(tags.player, tags.sensor, on_start=hit_sensor)
    ce.add_response(tags.player, tags.powerup, on_start=hit_powerup)
    ce.add_response(tags.player, tags.goomba, on_start=hit_goomba)
    ce.add_response(tags.player, tags.koopa, on_start=hit_koopa)
    ce.add_response(tags.player, tags.hotspot, on_start=hit_hotspot, on_end=leave_hotspot)
    ce.add_response(tags.goomba, tags.koopa, on_start=hit_gk)
    room.add_runner(ce)
    room.add_runner(monkey.scheduler())

    root = room.root()
    kb = monkey.keyboard()
    kb.add(299, 1, 0, pippo)
    kb.add(264, 1, 0, check_warp)
    root.add_component(kb)

    cam_node = monkey.Node()
    cn = cam_node.id
    state.cn = cam_node.id
    cam = monkey.camera_ortho(256, 240)
    cam.set_bounds(128, world_width-128, 120, 120, -100, 100)
    cam_node.set_camera(cam)
    root.add(cam_node)

    # draw lines
    #draw_lines(cam_node)

    player = mario(cam, 32, 32)
    state.player_id = player.id
    cam_node.add(player)



    cam_node.add(goomba(352, 32))
    cam_node.add(goomba(654, 32))
    cam_node.add(goomba(816, 32))
    cam_node.add(goomba(840, 32))
    #cam_node.add(koopa(160, 32))
    cam_node.add(spawn(1136, 32, [(goomba, 1280, 160), (goomba, 1312, 160)]))
    cam_node.add(warp_down(58*16, 6*16, 'w11'))
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

    a = (16, 5, 23, 5, 22, 9, 94, 9, 106, 5, 109, 5, 112, 5, 129, 9, 130, 9, 170, 5)
    for i in range(0, len(a), 2):
        cam_node.add(brick(a[i], a[i+1], 'sprites/bonusbrick', 1, make_coin))
    b = (20, 5, 22, 5, 24, 5, 77, 5, 79, 5, 80, 9, 81, 9, 82, 9, 83, 9, 84, 9, 85, 9, 86, 9, 87, 9,
         91, 9, 92, 9, 93, 9, 100, 5, 118, 5, 121, 9, 122, 9, 123, 9, 128, 9, 129, 5, 130, 5, 131, 9,
         168, 5, 169, 5, 171, 5)
    for i in range(0, len(b), 2):
        cam_node.add(brick(b[i], b[i+1], 'sprites/brick', -1, None))
    c = (21, 5, 78, 5, 109, 9)
    for i in range(0, len(c), 2):
        cam_node.add(brick(c[i], c[i + 1], 'sprites/bonusbrick', 1, make_powerup))
    d = (94, 5)
    for i in range(0, len(d), 2):
        cam_node.add(brick(d[i], d[i+1], 'sprites/brick', 5, make_coin))
    e = (101, 5)
    for i in range(0, len(e), 2):
        cam_node.add(brick(e[i], e[i + 1], 'sprites/brick', 1, make_powerup)) # this must be star

    return room