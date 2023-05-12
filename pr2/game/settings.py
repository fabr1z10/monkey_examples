import monkey

from enum import Enum


class Keys:
    FIRE = 68
    UP = 265




window_size = (256, 240)
device_size = (256, 240)
title = 'ciao belo!'
room = 'ciao'
start_position = 0
tile_size = (16, 16)
gravity = 500
debug_collision = False
#clear_color = (0.2, 0., 0., 1.)
shaders = [monkey.SHADER_BATCH]
cam = monkey.camera_ortho(256, 240, viewport=(0,0,256,240))

tilesets = {
    'main': {'img': 'smb1.png', 'tile_size': (16, 16)},
    'smb2': {'img': 'smb2i.png', 'tile_size': (16, 16)},
    'wfalls': {'img': 'wfalls.png', 'tile_size': (8, 8)}
}

class Flags:
    foe_platform = 1 << 9

class Tags:
    shyguy = 100
    foe_platform_sensor = 101
    collectible_item = 102
    generic_foe = 200
    generic_collectible = 201

start_positions = {
    'smb2_world_1_1b': [
        {'pos': (3, 3), 'right': True}
    ],
    'smb2_world_1_1c': [
        {'pos': (34, 2), 'right': False}
    ],
    'ciao': [
        {'pos': (0,3), 'right': True}
    ]

}

current_door =None
on_stairs = False
held_item = None
pickup_item = None
pickup_platform_item = dict()
shoot_speed = 200
invincible = True
invincible_duration = 5
mario_state = 1
mario_states = ['mario', 'supermario']

tiles = dict()
multi_tiles= dict()
main_batch = None


