import monkey

window_size = (256, 224)
device_size = (256, 224)
title = 'Wonderboy in Monsterland'
room = 'round2'
shaders = (monkey.SHADER_COLOR, monkey.SHADER_TEXTURE, monkey.SHADER_TEXTURE_PALETTE)
debug_collision = True
mario_state = 1
gravity = 500
mario_speed = 200
button_1 = 65
gold = 450

current_door = None

tilesets = {
    0: {'img': 'assets/wbml2.png', 'tile_size': (8, 8)},
    1: {'img': 'assets/wbml2.png', 'tile_size': (16, 16)}
}

class flags:
    player = 1
    platform = 2
    foe = 4
    player_hit = 8
    platform_passthrough = 32

class tags:
    player = 1
    platform = 2
    powerup = 3
    sensor = 4
    foe = 5
    goomba = 6
    koopa = 7
    hotspot = 8
    coin = 9
    fire = 10
    player_attack = 11
    snake = 12
    door = 13
    gate = 14


# mario_states = [
#     {'model': 'sprites/wb0', 'size': monkey.vec3(10, 14, 0), 'center': monkey.vec3(5, 0, 0)},
#     {'model': 'sprites/wb1', 'size': monkey.vec3(10, 30, 0), 'center': monkey.vec3(5, 0, 0)},
#     {'model': 'sprites/fierymario', 'size': monkey.vec3(10, 30, 0), 'center': monkey.vec3(5, 0, 0)}
# ]

class ids:
    game_node = None
    player = None
    hand = None

class shop_info:
    def __init__(self):
        self.exit_room = ''
        self.l_item = None
        self.l_item_text = None
        self.r_item = None
        self.r_item_text = None

