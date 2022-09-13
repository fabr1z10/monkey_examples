import monkey
from .util import *
from .. import settings
from . import functions
from . import state

cache = dict()

def text(what, x, y):
    n1 = monkey.Node()
    n1.set_model(monkey.text(font='font1', text=what, size=8))
    n1.set_position(-128 + x, 120 - y, 2)
    return n1

def cino():
    state.time -= 1
    monkey.get_node(state.time_label).set_text('{:03d}'.format(state.time))



def pane():
    s = monkey.script()
    i =s.add(monkey.repeat(cino, 1))
    monkey.play(s)


def room(world_width):
    state.room_details= dict()
    room = monkey.Room("mario")
    room.set_on_start(pane)

    ce = monkey.collision_engine(80, 80)
    ce.add_response(tags.player, tags.sensor, on_start=functions.hit_sensor)
    ce.add_response(tags.player, tags.powerup, on_start=functions.hit_powerup)
    ce.add_response(tags.player, tags.goomba, on_start=functions.hit_goomba)
    ce.add_response(tags.player, tags.koopa, on_start=functions.hit_koopa)
    ce.add_response(tags.player, tags.hotspot, on_start=functions.hit_hotspot, on_end=functions.leave_hotspot)
    ce.add_response(tags.goomba, tags.koopa, on_start=functions.hit_gk)
    ce.add_response(tags.goomba, tags.fire, on_start=functions.fire_hit_foe)
    room.add_runner(ce)
    room.add_runner(monkey.scheduler())
    root = room.root()
    kb = monkey.keyboard()
    kb.add(299, 1, 0, restart)
    kb.add(264, 1, 0, check_warp)
    kb.add(341, 1, 0, functions.fire)
    root.add_component(kb)

    # create camera
    device_size = settings.device_size
    device_width = device_size[0]
    device_height = device_size[1]
    device_half_width = device_width // 2
    device_half_height = device_height // 2
    cam_node = monkey.Node()
    state.cn = cam_node.id
    cam = monkey.camera_ortho(device_width, device_height)
    cam.set_bounds(device_half_width, world_width - device_half_width, device_half_height, device_half_height, -100, 100)
    cam_node.set_camera(cam)
    root.add(cam_node)
    state.main_cam = cam

    score_node = monkey.Node()
    score_cam = monkey.camera_ortho(device_width, device_height)
    score_node.set_camera(score_cam)
    score_node.add(text('MARIO', 24, 8))
    score_node.add(text('{:06d}'.format(state.score), 24, 16))
    score_node.add(text('*', 96, 16))
    coin_counter = text('{:02d}'.format(state.coins), 104, 16)
    state.coin_label = coin_counter.id
    score_node.add(coin_counter)
    score_node.add(text('WORLD', 144, 8))
    score_node.add(text(state.world_name, 152, 16))
    score_node.add(text('TIME', 200, 8))
    time_label = text('{:03d}'.format(state.time), 208, 16)
    score_node.add(time_label)
    state.time_label = time_label.id
    score_node.add(sprite(-2.8, 6.5, 'sprites/coin_counter'))
    root.add(score_node)

    return room, cam, cam_node


def mario(cam, x, y):
    node = monkey.Node()
    node.add_component(monkey.sprite_collider(flags.player, flags.foe, tags.player))
    sta = state.mario_states[state.mario_state]
    node.add_component(monkey.controller_2d(size=sta['size'], center=sta['center']))
    node.add_component(monkey.dynamics())
    node.set_position(x, y, 0)
    node.set_model(monkey.get_sprite(sta['model']))
    sm = monkey.state_machine()
    sm.add(monkey.walk_2d_player("pango", speed=state.mario_speed, gravity=state.gravity, jump_height=80, time_to_jump_apex=0.5))
    sm.add(monkey.walk_2d_auto("auto", speed=state.mario_speed, gravity=state.gravity, jump_height=80, time_to_jump_apex=0.5))
    sm.add(monkey.idle("dead", "dead"))
    sm.add(monkey.idle("warp", "idle"))
    sm.set_initial_state("pango")
    node.add_component(sm)
    node.add_component(monkey.follow(cam, (0, 0, 5), (0, 1, 0)))
    return node


def rect(w, h, x, y):
    node = monkey.Node()
    shape1 = monkey.rect(16*w, 16*h)
    node.set_position(x*16, y*16, 0)
    node.add_component(monkey.collider(shape1, flags.platform, 0, tags.platform))
    return node


def line(w, x, y):
    node = monkey.Node()
    shape1 = monkey.segment(0, 0, w*16, 0)
    node.set_position(x*16, y*16, 0)
    node.add_component(monkey.collider(shape1, flags.platform_passthrough, 0, tags.platform))
    return node



def platform(w, h, tx, ty, x, y):
    node2 = monkey.Node()
    shape1 = monkey.rect(16*w, 16*h)
    node2.set_position(x*16, y*16, 1)
    model_desc = '0,W,' + str(w) + ',R,' + str(w*h) + ',' + str(tx) + ',' + str(ty) + ',E'
    if model_desc not in cache:
        cache[model_desc] = monkey.tiled(model_desc)
    node2.set_model(cache[model_desc])
    node2.add_component(monkey.collider(shape1, flags.platform, 0, tags.platform))
    return node2


def tiled(x, y, model, z=-1):
    node2 = monkey.Node()
    node2.set_position(x*16, y*16, z)
    node2.set_model(monkey.get_tiled(model))
    return node2


def sprite(x, y, model):
    node2 = monkey.Node()
    node2.set_position(x*16, y*16, 0)
    node2.set_model(monkey.get_sprite(model))
    return node2



def platform_model(w, h, x, y, model):
    node2 = monkey.Node()
    node2.set_position(x*16, y*16, 1)
    node2.set_model(monkey.get_tiled(model))
    if w != 0 and h != 0:
        shape1 = monkey.rect(16*w, 16*h)
        node2.add_component(monkey.collider(shape1, flags.platform,0, tags.platform))
    return node2


def brick(x, y, sprite, hits, callback, hidden=False):
    node2 = monkey.Node()
    shape1 = monkey.rect(16, 16)
    node2.set_position(x*16, y*16, 0)
    node2.set_model(monkey.get_sprite(sprite))
    brick_flag = 0 if hidden else flags.platform
    node2.add_component(monkey.collider(shape1, brick_flag, 0, flags.platform))
    md = monkey.move_dynamics(1.)
    md.add_elastic_force(x*16, y*16, 0, 50)
    node2.user_data = {'hits': hits, 'callback': callback}
    #md.set_velocity(0, 10, 0)
    md.set_min_y(16*y)
    node2.add_component(monkey.platform())
    node2.add_component(md)
    sensor = monkey.Node()
    shape2 = monkey.rect(12, 4)
    sensor.add_component(monkey.collider(shape2, flags.foe, flags.player, tags.sensor))
    sensor.set_position(2, -2, 0)
    node2.add(sensor)
    return node2


def brick_piece(y0, x, y, vx, vy):
    def f(comp, node):
        if node.position[1] < y0:
            node.remove()
    node = monkey.Node()
    node.set_model(monkey.get_sprite('sprites/brickpiece'))
    node.set_position(x, y, 1)
    mm = monkey.move_dynamics(1.)
    mm.set_velocity(vx, vy, 0)
    mm.set_constant_force(0, -state.gravity, 0)
    mm.set_callback(f)
    node.add_component(mm)
    return node


def foe(x, y, model, walk, dead, flip, tag):
    node = monkey.Node()
    node.set_model(monkey.get_sprite(model))
    node.set_position(x, y, 0)
    sm = monkey.state_machine()
    #sm.add(monkey.idle("idle", 'idle'))
    sm.add(monkey.walk_2d_foe("pango", speed=20, gravity=state.gravity, jump_height=80, time_to_jump_apex=0.5, jump_anim=walk, flip=flip))
    sm.add(monkey.walk_2d_foe("dead", speed=0, gravity=state.gravity, jump_height=80, time_to_jump_apex=0.5, jump_anim=dead,
                              walk_anim=dead, idle_anim=dead, flip=flip))
    sm.set_initial_state('pango')
    node.add_component(sm)
    node.add_component(monkey.sprite_collider(flags.foe, flags.player, tag))
    node.add_component(monkey.controller_2d(size=(10, 10, 0), center=(5, 0, 0)))
    node.add_component(monkey.dynamics())
    return node


def on_jump_goomba(goomba_id):
    s = monkey.script()
    ii = s.add(monkey.delay(1))
    sid = s.add(monkey.remove(id=goomba_id), ii)
    monkey.play(s)
    return sid

def on_jump_koopa(koopa_id):
    s = monkey.script()
    ii = s.add(monkey.delay(1))
    ii = s.add(monkey.blink(id=koopa_id, duration=10, period=0.2), ii)
    ii = s.add(monkey.set_state(id=koopa_id, state='pango'), ii)
    sid =  monkey.play(s)
    return sid


def coin(x, y):
    def f(player):
        state.coins += 1
        functions.update_coin()
    node = monkey.Node()
    node.set_model(monkey.get_sprite('sprites/coin'))
    node.set_position(16*x, 16*y, 0)
    node.add_component(monkey.sprite_collider(flags.foe, flags.player, tags.powerup))
    node.user_data = {'callback': f}
    return node


def fireball(x, y, dir):
    node = monkey.Node()
    node.set_model(monkey.get_sprite('sprites/fire'))
    node.set_position(x, y, 1)
    sm = monkey.state_machine()
    sm.add(monkey.walk_2d_foe("pango", speed=200, gravity=state.gravity, jump_height=16, time_to_jump_apex=0.5, acc_time=0.0001,
                              jump_anim='default', idle_anim='default', walk_anim='default', flip=False, up=True))
    sm.set_initial_state('pango', dir=dir)
    node.add_component(sm)
    node.add_component(monkey.sprite_collider(flags.player_hit, flags.foe, tags.fire))
    node.add_component(monkey.controller_2d(size=(4, 4, 0), center=(0,0, 0)))
    node.add_component(monkey.dynamics())
    node.add_component(monkey.self_destroy(timeout=1))
    return node


def goomba(x, y):
    node = monkey.Node()
    node.set_model(monkey.get_sprite('sprites/goomba'))
    node.set_position(x, y, 0)
    sm = monkey.state_machine()
    sm.add(monkey.walk_2d_foe("pango", speed=20, gravity=state.gravity, jump_height=80, time_to_jump_apex=0.5,
                              jump_anim='walk', flip=False))
    sm.add(monkey.walk_2d_foe("dead", speed=0, gravity=state.gravity, jump_height=80, time_to_jump_apex=0.5, jump_anim='dead',
                              walk_anim='dead', idle_anim='dead', flip=False, script=on_jump_goomba))
    sm.add(monkey.idle("dead2", "dead2"))
    sm.set_initial_state('pango')
    node.add_component(sm)
    node.add_component(monkey.sprite_collider(flags.foe, flags.player, tags.goomba))
    node.add_component(monkey.controller_2d(size=monkey.vec3(10, 10, 0), center=monkey.vec3(5, 0, 0)))
    node.add_component(monkey.dynamics())
    return node

def koopa(x, y):
    node = monkey.Node()
    node.set_model(monkey.get_sprite('sprites/koopa'))
    node.set_position(x, y, 0)
    sm = monkey.state_machine()
    sm.add(monkey.walk_2d_foe("pango", speed=20, gravity=state.gravity, jump_height=80, time_to_jump_apex=0.5,
                              jump_anim='walk', flip=True))
    sm.add(monkey.walk_2d_foe("dead", speed=0, gravity=state.gravity, jump_height=80, time_to_jump_apex=0.5, jump_anim='hide',
                              walk_anim='hide', idle_anim='hide', flip=True, script=on_jump_koopa))
    sm.add(monkey.walk_2d_foe("fly", speed=80, gravity=state.gravity, jump_height=80, time_to_jump_apex=0.5, jump_anim='hide',
                              walk_anim='hide', idle_anim='hide', flip=True))
    sm.set_initial_state('pango')
    node.add_component(sm)
    node.add_component(monkey.sprite_collider(flags.foe, flags.player | flags.foe, tags.koopa))
    node.add_component(monkey.controller_2d(size=(10, 10, 0), center=(5, 0, 0)))
    node.add_component(monkey.dynamics())
    return node


def make_nodes(l):
    def f():
        main = monkey.engine().get_node(state.cn)
        for a in l:
            main.add(a[0](*a[1:]))
    return f

def enter_warp(warp_to, pos):
    def f():
        state.warp = (warp_to, pos)
    return f

def enter_warp_h(room, pos):
    def f():
        node = monkey.engine().get_node(state.player_id)
        node.set_state('auto', events=[
            {'t': 0, 'right': True},
            {'t': 1, 'callback': change_room(room, pos)}])

    return f

def hit_end_level():
    node = monkey.engine().get_node(state.player_id)
    node.get_dynamics().velocity.y = 0
    flag_id = state.room_details['flag']
    flag = monkey.engine().get_node(flag_id)
    node.set_state('warp', anim='slide')
    s = monkey.script()
    s.add(monkey.move_by(id=flag_id, y=48-flag.y, speed=50))
    ii = s.add(monkey.move_by(id=state.player_id, y=48-node.y, speed=50))
    s.add(monkey.set_state(id=state.player_id, state='auto', events=[{'t': 0, 'right': True}]), ii)
    monkey.play(s)

def go_to_next():
    node = monkey.engine().get_node(state.player_id)
    node.remove()


def leave_warp():
    state.warp = 0


def hotspot(x, y, w, h):
    node = monkey.Node()
    shape1 = monkey.rect(w, h)
    node.set_position(x, y, 0)
    node.add_component(monkey.collider(shape1, flags.foe, flags.player, tags.hotspot))

    return node

def spawn(x, y, l):
    node = hotspot(x, y, 2, 256)
    node.user_data = {'on_start': make_nodes(l)}
    return node

def warp_down(x, y, room, pos):
    node = hotspot(x - 8, y, 16, 2)
    node.user_data = {'remove': False, 'on_start': enter_warp(room, pos), 'on_end': leave_warp}
    #node.user_data = {'callback': make_nodes(l)}
    return node

def warp_right(x, y, room, pos):
    node = hotspot(x - 8, y, 16, 2)
    node.user_data = {'remove': False, 'on_start': enter_warp_h(room, pos), 'on_end': leave_warp}
    return node

def end_level(x, y):
    node = hotspot(x*16 + 7, y*16, 2, 160)
    node.user_data = {'remove': True, 'on_start': hit_end_level}
    return node

def next_level(x, y):
    node = hotspot(x*16, y*16, 2, 160)
    node.user_data = {'remove': True, 'on_start': go_to_next}
    return node

def on_collect_mushroom(player):
    state.mario_state += 1
    state.mario_state = min(state.mario_state, len(state.mario_states) - 1)
    st = state.mario_states[state.mario_state]
    player.set_model(monkey.get_sprite(st['model']))
    player.get_controller().set_size(st['size'], st['center'])

def on_collect_1up(player):
    pass


power_ups = [
    lambda: (on_collect_mushroom, 'sprites/mushroom', False) if state.mario_state == 0 else (on_collect_mushroom, 'sprites/starman', True),
    lambda: (on_collect_1up, 'sprites/mushroom_1up', False)
]


def powerup(x, y, id):
    pup = power_ups[id]()
    print(pup)
    node = monkey.Node()
    node.set_model(monkey.get_sprite(pup[1]))
    node.set_position(x, y, 1)
    sm = monkey.state_machine()
    sm.add(monkey.idle("idle", 'idle'))
    sm.add(monkey.walk_2d_foe("pango", speed=20, gravity=state.gravity, jump_height=80, time_to_jump_apex=0.5, jump_anim='idle', up=pup[2]))
    sm.set_initial_state('idle')
    node.add_component(sm)
    node.add_component(monkey.sprite_collider(flags.foe, flags.player, tags.powerup))
    node.add_component(monkey.controller_2d(size=(10, 10, 0), center=(5, 0, 0)))
    node.add_component(monkey.dynamics())
    node.user_data = {'callback': pup[0]}
    s = monkey.script()
    ii = s.add(monkey.move_by(node=node, y=16, t=1))
    s.add(monkey.set_state(node=node, state='pango'), ii)
    monkey.play(s)
    return node