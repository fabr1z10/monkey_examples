title='New game'

window_size=[320, 200]
device_size=window_size
enable_framebuffer = True
enable_mouse = True
debug_collision = True

string_file='strings.yaml'

room='hello_world'
room_id='mancomb'

player_script_id = '_player'
dialogue_font='main/large'
dialogue_batch='sprites'
dialogue_margin = (10,5)
dialogue_offset = 60
dialogue_timeout = 2

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
}

class ids:
    current_action = None


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