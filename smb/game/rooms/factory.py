import monkey
from .util import *
from .. import settings
from . import functions
from . import state

cache = dict()

def text(what, x, y):
    n1 = monkey.Node()
    n1.set_model(monkey.models.text(font='font1', text=what, size=8))
    n1.set_position(-128 + x, 120 - y, 2)
    return n1

def cino():
    state.time -= 1
    monkey.get_node(state.time_label).set_text('{:03d}'.format(state.time))



def pane():
    s = monkey.script()
    i =s.add(monkey.actions.repeat(cino, 1))
    monkey.play(s)


def room(world_width, world_height):
    state.room_details= dict()
    room = monkey.Room("mario")


    ce = monkey.collision_engine(80, 80, 0)
    ce.add_response(tags.player, tags.sensor, on_start=functions.hit_sensor)
    ce.add_response(tags.player, tags.powerup, on_start=functions.hit_powerup)
    ce.add_response(tags.player, tags.goomba, on_start=functions.hit_goomba)
    ce.add_response(tags.player, tags.koopa, on_start=functions.hit_koopa)
    ce.add_response(tags.player, tags.hotspot, on_start=functions.hit_hotspot, on_end=functions.leave_hotspot)
    ce.add_response(tags.player_attack, tags.foe, on_start = functions.bomba)
    ce.add_response(tags.goomba, tags.koopa, on_start=functions.hit_gk)
    ce.add_response(tags.goomba, tags.fire, on_start=functions.fire_hit_foe)
    # only for smb2
    ce.add_response(tags.player, tags.door, on_start=functions.enable_door, on_end=functions.disable_door)
    ce.add_response(tags.player, tags.pickup_sensor, on_start=functions.enable_pickup, on_end=functions.disable_pickup)
    ce.add_response(tags.player, tags.pickup_sensor_platform, on_start=functions.enable_pickup_platform, on_end=functions.disable_pickup_platform)
    ce.add_response(tags.player, tags.stairs, on_start=functions.enable_stairs, on_end=functions.disable_stairs)
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
    cam.set_bounds(device_half_width, world_width - device_half_width, device_half_height, world_height - device_half_height, -100, 100)
    cam_node.set_camera(cam)
    root.add(cam_node)
    state.main_cam = cam

    # score_node = monkey.Node()
    # score_cam = monkey.camera_ortho(device_width, device_height)
    # score_node.set_camera(score_cam)
    # score_node.add(text('MARIO', 24, 8))
    # score_node.add(text('{:06d}'.format(state.score), 24, 16))
    # score_node.add(text('*', 96, 16))
    # coin_counter = text('{:02d}'.format(state.coins), 104, 16)
    # state.coin_label = coin_counter.id
    # score_node.add(coin_counter)
    # score_node.add(text('WORLD', 144, 8))
    # score_node.add(text(state.world_name, 152, 16))
    # score_node.add(text('TIME', 200, 8))
    # time_label = text('{:03d}'.format(state.time), 208, 16)
    # score_node.add(time_label)
    # state.time_label = time_label.id
    # score_node.add(sprite(-2.8, 6.5, 'sprites/coin_counter'))
    # root.add(score_node)
    # room.set_on_start(pane)
    return room, cam, cam_node

def door(x, y, world_to):
    node = monkey.Node()
    node.set_model(monkey.get_sprite('sprites2/door'))
    node.set_position(x*16, y*16, 0.5)
    node.add_component(monkey.collider(monkey.aabb(0,16,0,2), flags.foe, flags.player, tags.door))
    node.user_data = {'world_to': world_to}
    return node

def stairs(x, y, height):
    node = monkey.Node()
    shape = monkey.aabb(0, 16, 0, height*16)
    node.add_component(monkey.collider(shape, flags.foe, flags.player, tags.stairs))
    node.set_position(x*16,y*16,0)
    return node

def veggie(x, y):
    node = monkey.Node()
    node.set_model(monkey.get_sprite('sprites2/veggie'))
    node.add_component(monkey.sprite_collider(flags.foe, flags.player, tags.pickup_sensor))
    node.set_position(x*16,y*16,0)
    sm = monkey.state_machine()
    sm.add(monkey.walk_2d_foe("pango", speed=0, gravity=state.gravity, jump_height=80, time_to_jump_apex=0.5,
                                 walk_anim='idle', jump_anim='idle'))
    sm.add(monkey.idle("lifted", "up"))
    sm.add(monkey.bounce("bounce", gravity=state.gravity, check_walls=False, bounce_velocity=150,
                         collision_mask = flags.foe, collision_flag=flags.player_hit, collision_tag=tags.player_attack))

    sm.set_initial_state("pango")
    node.add_component(sm)
    node.add_component(monkey.controller_2d(size=monkey.vec3(10, 14, 0), center=monkey.vec3(5,0,0)))
    node.add_component(monkey.dynamics())
    return node


def mario2(cam, x, y):
    node = monkey.Node()
    character_info = state.characters[state.player_character]
    node.set_model(monkey.get_sprite(character_info['model']))
    node.add_component(monkey.sprite_collider(flags.player, flags.foe, tags.player))
    node.add_component(monkey.controller_2d(size=character_info['size'], center=character_info['center']))
    node.add_component(monkey.dynamics())
    sm = monkey.state_machine()
    sm.add(monkey.walk_2d_player("pango", speed=state.mario_speed, gravity=state.gravity, jump_height=80, time_to_jump_apex=0.5,
                                 keys={settings.fire_button: functions.pickup, settings.door_button: functions.enter_door}))
    sm.add(monkey.walk_2d_player("walk_item", speed=state.mario_speed, gravity=state.gravity, jump_height=80, time_to_jump_apex=0.5,
                                 walk_anim='walk_item', idle_anim='idle_item', keys={68: functions.pickup}))
    sm.add(monkey.climb("climb", speed=state.climb_speed, anim='climb', anim_idle='climb_idle'))
    sm.add(monkey.idle("lift", "lift", exit_on_complete=True, exit_state='walk_item'))

    sm.set_initial_state("pango")
    node.add_component(sm)
    node.add_component(monkey.follow(cam, (0, 0, 5), (0, 1, 0)))
    node.set_position(x * 16, y * 16, 1)
    return node

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
        cache[model_desc] = monkey.models.tiled(desc=model_desc)
    node2.set_model(cache[model_desc])
    node2.add_component(monkey.collider(shape1, flags.platform, 0, tags.platform))
    return node2

def rounded_platform(x, y, w, h, pal=None, z=0):
    if w > 2:
        dstring = 'W,' + str(w) + ',R,' + str(h-1)+ ',0,3,R,' + str(w-2) + ',1,3,E,2,3,E,0,2,R,' + str(w-2) + ',1,2,E,2,2'
    else:
        dstring = 'W,' + str(w) + ',R,' + str(h-1) + ',0,3,2,3,E,0,2,2,2'
    a = tiled1(x, y, 2, dstring, pal=pal, z=z)
    shape1 = monkey.segment(0, h*16, w*16, h*16)
    #node.set_position(x*16, y*16, 0)
    a.add_component(monkey.collider(shape1, flags.platform_passthrough, 0, tags.platform))
    return a



def animtiled(x, y, sheet, frames, pal=None, z=0):
    node = monkey.Node()
    node.set_model(monkey.models.tiled_animated(sheet=sheet, frames=frames, palette=pal))#'pal/0'))
    node.set_position(x * 16, y * 16, z)
    return node


def tiled1(x, y, sheet, model_desc, pal=None, z = 0):
    node = monkey.Node()
    #model_desc = '1,W,1,0,0'
    node.set_model(monkey.models.tiled(sheet=sheet, desc=model_desc, palette=pal))#'pal/0'))
    node.set_position(x * 16, y * 16, z)
    return node


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
    node.set_position(x, y, 1)
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

def foe2(x, y, model, speed, tag):
    node = monkey.Node()
    node.set_model(monkey.get_sprite(model))
    node.set_position(16* x, 16* y, 1)
    sm = monkey.state_machine()
    sm.add(monkey.walk_2d_foe("pango", speed=speed, flip=True, flip_on_edge=True, gravity=state.gravity, jump_height=80, time_to_jump_apex=0.5, jump_anim='walk', idle_anim='walk'))
    sm.add(monkey.bounce("dead", gravity=state.gravity, check_walls=False, animation='dead'))
    sm.add(monkey.idle("lifted", "up"))
    sm.add(monkey.bounce("bounce", gravity=state.gravity, check_walls=True, on_bounce_y=functions.bounce, bounce_velocity=150,
                         collision_mask = flags.foe, collision_flag=flags.player_hit, collision_tag=tags.player_attack))
    sm.set_initial_state('pango')
    node.add_component(sm)
    node.add_component(monkey.sprite_collider(flags.foe, flags.player, tag))
    node.add_component(monkey.controller_2d(size=monkey.vec3(10, 10, 0), center=monkey.vec3(5, 0, 0)))
    node.add_component(monkey.dynamics())
    platform = monkey.Node()
    shape1 = monkey.segment(-8, 16, 8, 16)
    #node.set_position(0, 0, 0)
    platform.add_component(monkey.collider(shape1, flags.platform_passthrough, 0, tags.platform))
    #pl = line(1,-0.5,1.2)
    platform.add_component(monkey.platform())
    psensor = monkey.Node()
    psensor.set_position(0, 16, 0)
    sh =  monkey.aabb(0, 2, 0, 16)
    psensor.add_component(monkey.collider(sh, flags.foe, flags.player, tags.pickup_sensor_platform))
    platform.add(psensor)
    node.add(platform)
    return node



def on_jump_goomba(goomba_id):
    print('goomba id: ' ,goomba_id)
    s = monkey.script()
    ii = s.add(monkey.actions.delay(1))
    sid = s.add(monkey.actions.remove(id=goomba_id), ii)
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


def bigshoe(x, y):
    node = monkey.Node()
    node.set_model(monkey.image('assets/shoe1.png', anchor = monkey.vec2(273, 47)))
    node.add_component(monkey.movequat(
        z =2,
        key_frames = [
            {'t': 0, 'angle': 20, 'pos': monkey.vec2(100, 160), 'dir': monkey.vec2(0, 1)},
            {'t': 2, 'angle': 0, 'pos': monkey.vec2(160, 0), 'dir': monkey.vec2(0, 1)},
            {'t': 4, 'angle': 0, 'pos': monkey.vec2(160, 0), 'dir': monkey.vec2(0, 1)},
            {'t': 6, 'angle': -20, 'pos': monkey.vec2(220, 160), 'dir': monkey.vec2(0, 1)}
        ]
    ))
    return node

def p1(x, y):
    node = monkey.Node()
    node.set_model(monkey.get_mesh('grl3/torso'))
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
    s.add(monkey.actions.move_by(id=flag_id, y=48-flag.y, speed=50))
    ii = s.add(monkey.actions.move_by(id=state.player_id, y=48-node.y, speed=50))
    s.add(monkey.actions.set_state(id=state.player_id, state='auto', events=[{'t': 0, 'right': True}]), ii)
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