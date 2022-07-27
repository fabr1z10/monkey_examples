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