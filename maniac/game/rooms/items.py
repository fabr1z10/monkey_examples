from . import factory
from . import data
from . import state
import monkey


def geu(item, key):
    if 'states' in item:
        state = item['states'][item['state']]
        if key in state:
            return state[key]
    if key in item:
        return item[key]
    exit(1)

def get(item, key, default_value):
    if 'states' in item:
        state = item['states'][item['state']]
        if key in state:
            return state[key]
    if key in item:
        return item[key]
    return default_value


items = {
    'dave': {'type': 'character', 'id': None,
             'text_color': state.dave_text, 'room': 'foyer',
             'pos': monkey.vec2(410, 10),
             'walkarea': 0,
             'text': data.text[108],
             'model': 'dave',
             'dir': 'w'},
    'bernard': {'type': 'character', 'id': None,
             'text_color': state.bernard_text, 'room': 'front_door',
             'pos': monkey.vec2(360, 10),
             'text': data.text[109],
             'walkarea': 0,
             'model': 'bernard',
             'dir': 'w'},
    'razor': {'text': data.text[110]},
    'sign': {'type': 'hot_spot', 'size': (31, 22), 'text': data.text[100], 'walk_to': (25, 6), 'dir': 's'},
    'path_start_frontdoor': {'type': 'hot_spot', 'size': (8, 128), 'text': '', 'walk_to': (1, 6),
                             'dir': 'w'},

    'furnace': {'text': data.text[114], 'walk_to': monkey.vec2(452, 5), 'dir': 'n'},
    'nuclear_reactor': {'text': data.text[115], 'walk_to': monkey.vec2(487, 5), 'dir': 'n'},
    'fuse_box': {'text': data.text[116], 'walk_to': monkey.vec2(80, 20), 'dir': 'n', 'anim': 'closed'},
    'circuit_breakers': {'text': data.text[117], 'walk_to': monkey.vec2(80, 20), 'dir': 'n'},
    'stairs': {'text': data.text[111], 'walk_to': monkey.vec2(574, 121), 'dir': 'n'},
    'doormat': {'type': 'hot_spot', 'text': data.text[101], 'walk_to': (380, 47), 'dir': 's', 'sprite': 'doormat',
                'states': [
                    {'size': (90, 5), 'anim': 'closed'},
                    {'size': (48, 5), 'anim': 'open'}
                ], 'state': 0},
    'front_door': {'text': data.text[103], 'walk_to': monkey.vec2(401, 48), 'dir': 'n', 'anim': 'closed',
                    'room_id': 'foyer', 'room_dir': 'e', 'room_pos': monkey.vec2(50, 6)},
    'front_door_in': {'text': data.text[103], 'walk_to': monkey.vec2(50, 6), 'dir': 'w', 'master': 'front_door',
                    'room_id': 'front_door', 'room_dir': 's', 'room_pos': monkey.vec2(401, 48)},
    'kitchen_door': {'text': data.text[106], 'walk_to': monkey.vec2(180, 22), 'dir': 'n', 'anim': 'closed',
                   'room_id': 'kitchen', 'room_dir': 'e', 'room_pos': monkey.vec2(50, 6)},
    'sitting_room_door': {'text': data.text[106], 'walk_to': monkey.vec2(590, 6), 'dir': 'e', 'anim': 'closed',
                     'room_id': 'sitting_room', 'room_dir': 'e', 'room_pos': monkey.vec2(50, 6)},
    'basement_door': {'text': data.text[106], 'walk_to': monkey.vec2(459, 22), 'dir': 'n', 'anim': 'closed',
                          'room_id': 'basement', 'room_dir': 's', 'room_pos': monkey.vec2(572, 115)},

    'key': {'text': data.text[102], 'walk_to': monkey.vec2(380, 47), 'dir': 's'},
    'silver_key': {'text': data.text[113], 'walk_to': monkey.vec2(102, 21), 'dir': 'n'},
    'grandfather_clock': {'text': data.text[104], 'walk_to': monkey.vec2(120, 16), 'dir': 'n'},
    'vase_l': {'text': data.text[105], 'walk_to': monkey.vec2(232, 15), 'dir': 'n' },
    'vase_r': {'text': data.text[105], 'walk_to': monkey.vec2(384, 15), 'dir': 'n'},
    'gargoyle_r': {'text': data.text[107], 'walk_to': monkey.vec2(340, 15), 'dir': 'n'},
    'basement_light_switch': {'text': data.text[112], 'walk_to': monkey.vec2(547, 21), 'dir': 'n'}
}


def update_item(item, key, value):
    def f():
        items[item][key] = value
    return f
