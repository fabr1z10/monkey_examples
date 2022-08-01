import monkey
from .util import *
from ..pippo import *

from . import state

cache = dict()

def mario(cam, x, y):
    node = monkey.Node()
    node.add_component(monkey.sprite_collider(flags.player, flags.foe, tags.player))
    sta = state.mario_states[state.mario_state]
    node.add_component(monkey.controller_2d(size=sta['size'], center=sta['center']))
    node.add_component(monkey.dynamics())
    node.set_position(x, y, 0)
    node.set_model(monkey.get_sprite(sta['model']))
    sm = monkey.state_machine()
    sm.add(monkey.walk_2d_player("pango", speed=200, gravity=state.gravity, jump_height=80, time_to_jump_apex=0.5))
    sm.add(monkey.idle("dead", "dead"))
    sm.add(monkey.idle("warp", "idle"))
    sm.set_initial_state("pango")
    node.add_component(sm)
    node.add_component(monkey.follow(cam, (0, 0, 5), (0, 1, 0)))
    return node


def platform(w, h, tx, ty, x, y):
    node2 = monkey.Node()
    shape1 = monkey.rect(16*w, 16*h)
    node2.set_position(x*16, y*16, 0)
    model_desc = '0,W,' + str(w) + ',R,' + str(w*h) + ',' + str(tx) + ',' + str(ty) + ',E'
    if model_desc not in cache:
        cache[model_desc] = monkey.tiled(model_desc)
    node2.set_model(cache[model_desc])
    node2.add_component(monkey.collider(shape1, flags.platform, 0, tags.platform))
    return node2


def platform_model(w, h, x, y, model):
    node2 = monkey.Node()
    shape1 = monkey.rect(16*w, 16*h)
    node2.set_position(x*16, y*16, 0)
    node2.set_model(monkey.get_tiled(model))
    node2.add_component(monkey.collider(shape1, flags.platform,0, tags.platform))
    return node2


def brick(x, y, sprite, hits, callback):
    node2 = monkey.Node()
    shape1 = monkey.rect(16, 16)
    node2.set_position(x*16, y*16, 0)
    node2.set_model(monkey.get_sprite(sprite))
    node2.add_component(monkey.collider(shape1, flags.platform, 0, flags.platform))
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
    node.add_component(monkey.controller_2d(size=(10, 10, 0), center=(5, 0, 0)))
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

def enter_warp(warp_to):
    def f():
        state.warp = warp_to
    return f


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

def warp_down(x, y, warp_to):
    node = hotspot(x - 8, y, 16, 2)
    node.user_data = {'remove': False, 'on_start': enter_warp(warp_to), 'on_end': leave_warp}
    #node.user_data = {'callback': make_nodes(l)}
    return node
