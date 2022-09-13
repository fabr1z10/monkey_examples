import monkey
from . import data
from . import factory
from .. import settings

room_init = {
    'foyer': {'pos': monkey.vec2(50, 6), 'dir': 'e'},
    'front_door': {'pos': monkey.vec2(391, 3), 'dir': 's'},
    'basement': {'pos': monkey.vec2(572, 115), 'dir': 's'},
    'start': {'pos': monkey.vec2(20, 10), 'dir': 's'},
}

verb_color_selected = monkey.vec4(1.0, 1.0, 85.0/255.0, 1.0)
verb_color_unselected = monkey.vec4(0.0, 170.0/255.0, 0, 1.0)
current_verb_color = monkey.vec4(1.0, 85.0/255.0, 1.0, 1.0)
inventory_color_unselected = monkey.vec4(1.0, 85.0/255.0, 1.0, 1.0)
inventory_color_selected = monkey.vec4(1.0, 1.0, 85.0/255.0, 1.0)
character_dark_color = monkey.vec4(85./255., 85./255., 85./255., 1.)
dave_text = monkey.vec4(85.0/255.0, 85.0/255.0, 1.0, 1.0)
bernard_text = monkey.vec4(1.0)

def setup():
    from .items import items, update_item
    rinit = room_init[settings.room]
    print(rinit)
    items[current_player]['room'] = settings.room
    items[current_player]['pos'] = rinit['pos']
    items[current_player]['dir'] = rinit['dir']

player_id = None

current_verb = None
current_item = None
current_item2 = None
current_player = 'dave'
players = ['dave','bernard','razor']

before_action_script = dict()


inventory = {
    #'key': ['dave', 1]
}

ids = dict()

front_door_unlocked = True


def get(id):
    return monkey.get_node(ids[id])


