title='New game'

window_size=[320, 200]
device_size=window_size
enable_framebuffer = True
enable_mouse = True
debug_collision = True
game_is_active = True


string_file='strings.yaml'

room='hello_world'
room_id='scummbar'

player_script_id = '_player'
dialogue_font='main/large'
dialogue_batch='sprites'
dialogue_margin = (10,5)
dialogue_offset = 75
dialogue_timeout = 222
dialogue_width = 148
msg_parent_node = 0


class palettes:
    inventory_unselected_palette = 5
    inventory_selected_palette = 6
    dialogue_unselected_palette = 9
    dialogue_selected_palette = 10

speed = 300

x=0
x1=0
main_node=0

spritesheets = {
    'main': '../assets/spritesheet/mi1/main',
    'lookout': '../assets/spritesheet/mi1/lookout',
    'village1': '../assets/spritesheet/mi1/village1',
    'scummbar': '../assets/spritesheet/mi1/scummbar',
    'mancomb': '../assets/spritesheet/mi1/mancomb',
    'estevan': '../assets/spritesheet/mi1/estevan',
    'cobb': '../assets/spritesheet/mi1/cobb',
    'kitchen': '../assets/spritesheet/mi1/kitchen',
}

class ids:
    current_action = None
    root = None
    ui_main = None


player = 'guybrush'

objects = dict()
objects_in_room = dict()
current_action = []
strings = None
default_verb = None
verbs = {
    'open': {
        'text': 0,
        'pos': [2, 40]
    },
    'close': {
        'text': 1,
        'pos': [2, 31]
    },
    'push': {
        'text': 2,
        'pos': [2, 22]
    },
    'pull': {
        'text': 3,
        'pos': [2, 13]
    },
    'walk': {
        'text': 4,
        'pos': [48, 40],
        'default': True
    },
    'pickup': {
        'text': 5,
        'pos': [48, 31]
    },
    'talk': {
        'text': 6,
        'pos': [48, 22]
    },
    'give': {
        'text': 7,
        'pos': [48, 13],
        'double': True
    },
    'use': {
        'text': 8,
        'pos': [100, 40],
        'double': True
    },
    'look': {
        'text': 9,
        'pos': [100, 31]
    },
    'turnon': {
        'text': 10,
        'pos': [100, 22]
    },
    'turnoff': {
        'text': 11,
        'pos': [100, 13]
    },

}

inventory={
    'pieces_of_eight': 203
}

actors = {
    0: {'pos': [240, 128], 'pal': 0},           # guybrush rhs
    1: {'pos': [80, 128], 'pal': 11},           # mancomb seepgood
    2: {'pos': [240, 128], 'pal': 12},          # estevan
    3: {'pos': [80, 128], 'pal': 0},            # guybrush lhs
    4: {'pos': [184, 114], 'pal': 13}           # cobb
}

class Variables:
    talked_to_estevan = 0
    seagull_state = 0