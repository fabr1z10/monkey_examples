import monkey

from .util import *
from . import factory
from . import functions
from . import state
import numpy as np


def rise():
    s = monkey.script()
    ii = s.add(monkey.set_state(id=state.player_id, state='warp'))
    ii = s.add(monkey.move_by(id=state.player_id, y=64, t=1), ii)
    s.add(monkey.set_state(id=state.player_id, state='pango'), ii)
    monkey.play(s)

def w11():
    room, cam, cam_node = factory.room(3584)

    start_positions = [ (32, 32, None), (2624, 0, rise)]
    sp = start_positions[state.start_position]
    if sp[2]:
        room.set_on_start(sp[2])
    player = factory.mario(cam, sp[0], sp[1])
    state.player_id = player.id
    cam_node.add(player)

    cam_node.add(factory.goomba(352, 32))
    # cam_node.add(factory.goomba(654, 32))
    # cam_node.add(factory.goomba(816, 32))
    # cam_node.add(factory.goomba(840, 32))
    # cam_node.add(factory.spawn(1136, 32, [(factory.goomba, 1280, 160), (factory.goomba, 1312, 160)]))
    # cam_node.add(factory.warp_down(58*16, 6*16, 'w11b', 0))
    cam_node.add(factory.platform(69, 2, 15, 7, 0, 0))
    cam_node.add(factory.platform(15, 2, 15, 7, 71, 0))
    cam_node.add(factory.platform(64, 2, 15, 7, 89, 0))
    cam_node.add(factory.platform(69, 2, 15, 7, 155, 0))
    cam_node.add(factory.platform(4, 1, 15, 8, 134, 2))
    cam_node.add(factory.platform(3, 1, 15, 8, 135, 3))
    cam_node.add(factory.platform(2, 1, 15, 8, 136, 4))
    cam_node.add(factory.platform(1, 1, 15, 8, 137, 5))
    cam_node.add(factory.platform(4, 1, 15, 8, 140, 2))
    cam_node.add(factory.platform(3, 1, 15, 8, 140, 3))
    cam_node.add(factory.platform(2, 1, 15, 8, 140, 4))
    cam_node.add(factory.platform(1, 1, 15, 8, 140, 5))
    cam_node.add(factory.platform(5, 1, 15, 8, 148, 2))
    cam_node.add(factory.platform(4, 1, 15, 8, 149, 3))
    cam_node.add(factory.platform(3, 1, 15, 8, 150, 4))
    cam_node.add(factory.platform(2, 1, 15, 8, 151, 5))
    cam_node.add(factory.platform(1, 1, 15, 8, 152, 5))
    cam_node.add(factory.platform(4, 1, 15, 8, 155, 2))
    cam_node.add(factory.platform(3, 1, 15, 8, 155, 3))
    cam_node.add(factory.platform(2, 1, 15, 8, 155, 4))
    cam_node.add(factory.platform(1, 1, 15, 8, 155, 5))
    cam_node.add(factory.platform(9, 1, 15, 8, 181, 2))
    cam_node.add(factory.platform(8, 1, 15, 8, 182, 3))
    cam_node.add(factory.platform(7, 1, 15, 8, 183, 4))
    cam_node.add(factory.platform(6, 1, 15, 8, 184, 5))
    cam_node.add(factory.platform(5, 1, 15, 8, 185, 6))
    cam_node.add(factory.platform(4, 1, 15, 8, 186, 7))
    cam_node.add(factory.platform(3, 1, 15, 8, 187, 8))
    cam_node.add(factory.platform(2, 1, 15, 8, 188, 9))
    cam_node.add(factory.platform(1, 1, 15, 8, 198, 2))
    cam_node.add(factory.platform_model(2, 2, 28, 2, 'tiles/pipe2'))
    cam_node.add(factory.platform_model(2, 3, 38, 2, 'tiles/pipe3'))
    cam_node.add(factory.platform_model(2, 4, 46, 2, 'tiles/pipe4'))
    cam_node.add(factory.platform_model(2, 4, 57, 2, 'tiles/pipe4'))
    cam_node.add(factory.platform_model(2, 2, 163, 2, 'tiles/pipe2'))
    cam_node.add(factory.platform_model(2, 2, 179, 2, 'tiles/pipe2'))
    # cam_node.add(factory.tiled(198, 3, 'tiles/flagpole'))
    # flag = factory.sprite(197.5, 11, 'sprites/flag')
    # state.room_details['flag'] = flag.id
    # cam_node.add(flag)
    # cam_node.add(factory.tiled(202, 2, 'tiles/castle', z=-0.5))
    #
    # [cam_node.add(factory.tiled(x, 2, 'tiles/hill')) for x in 48 * np.array(range(0,5))]
    # [cam_node.add(factory.tiled(x, 2, 'tiles/hillsmall')) for x in 16 + 48 * np.array(range(0, 5))]
    # [cam_node.add(factory.tiled(x, 2, 'tiles/bush3')) for x in 11 + 48 * np.array(range(0, 5))]
    # [cam_node.add(factory.tiled(x, 2, 'tiles/bush2')) for x in 41 + 48 * np.array(range(0, 5))]
    # [cam_node.add(factory.tiled(x, 2, 'tiles/bush1')) for x in 71 + 48 * np.array(range(0, 5))]
    # [cam_node.add(factory.tiled(x, 10, 'tiles/cloud1')) for x in 8 + 48 * np.array(range(0, 5))]
    # [cam_node.add(factory.tiled(x, 11, 'tiles/cloud1')) for x in 19 + 48 * np.array(range(0, 5))]
    # [cam_node.add(factory.tiled(x, 10, 'tiles/cloud3')) for x in 27 + 48 * np.array(range(0, 5))]
    # [cam_node.add(factory.tiled(x, 11, 'tiles/cloud2')) for x in 36 + 48 * np.array(range(0, 5))]
    #
    # cam_node.add(factory.end_level(198, 3))
    # cam_node.add(factory.next_level(205, 2))
    # a = (16, 5, 23, 5, 22, 9, 94, 9, 106, 5, 109, 5, 112, 5, 129, 9, 130, 9, 170, 5)
    # for i in range(0, len(a), 2):
    #     cam_node.add(factory.brick(a[i], a[i+1], 'sprites/bonusbrick', 1, functions.make_coin))
    # b = (20, 5, 22, 5, 24, 5, 77, 5, 79, 5, 80, 9, 81, 9, 82, 9, 83, 9, 84, 9, 85, 9, 86, 9, 87, 9,
    #      91, 9, 92, 9, 93, 9, 100, 5, 118, 5, 121, 9, 122, 9, 123, 9, 128, 9, 129, 5, 130, 5, 131, 9,
    #      168, 5, 169, 5, 171, 5)
    # for i in range(0, len(b), 2):
    #     cam_node.add(factory.brick(b[i], b[i+1], 'sprites/brick', -1, None))
    # c = (21, 5, 78, 5, 109, 9)
    # for i in range(0, len(c), 2):
    #     cam_node.add(factory.brick(c[i], c[i + 1], 'sprites/bonusbrick', 1, functions.make_powerup(0)))
    # d = (94, 5)
    # for i in range(0, len(d), 2):
    #     cam_node.add(factory.brick(d[i], d[i+1], 'sprites/brick', 5, functions.make_coin))
    # e = (101, 5)
    # for i in range(0, len(e), 2):
    #     cam_node.add(factory.brick(e[i], e[i + 1], 'sprites/brick', 1, functions.make_powerup)) # this must be star
    #
    # cam_node.add(factory.brick(64, 6, 'sprites/hidden_brick', 1, functions.make_coin, True)) # this must be star

    return room


def w11b():
    room, cam, cam_node = factory.room(256)
    player = factory.mario(cam, 32, 32)
    state.player_id = player.id
    cam_node.add(player)
    cam_node.add(factory.platform(16, 2, 15, 9, 0, 0))
    cam_node.add(factory.platform(1, 11, 10, 3, 0, 2))
    cam_node.add(factory.platform(7, 3, 10, 3, 4, 2))
    cam_node.add(factory.platform(7, 1, 10, 3, 4, 12))
    cam_node.add(factory.platform_model(0, 0, 13, 2, 'tiles/pipeh'))
    cam_node.add(factory.rect(1, 11, 15, 2))
    cam_node.add(factory.line(3, 13, 4))
    coins = [
        4, 5, 5, 5, 6, 5, 7, 5, 8, 5, 9, 5, 10, 5,
        4, 7, 5, 7, 6, 7, 7, 7, 8, 7, 9, 7, 10, 7,
        5, 9, 6, 9, 7, 9, 8, 9, 9, 9
    ]
    for i in range(0, len(coins), 2):
        cam_node.add(factory.coin(coins[i], coins[i+1]))
    cam_node.add(factory.warp_right(13*16, 2*16, 'w11', 1))
    return room