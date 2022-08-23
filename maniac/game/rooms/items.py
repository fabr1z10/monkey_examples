from . import factory
from . import data
from . import state
import monkey


items = {
    'dave': {'type': 'character', 'id': None,
             'text_color': state.dave_text, 'room': 'front_door',
             'pos': monkey.vec2(410, 10),
             'walkarea': 0,
             'model': 'dave',
             'dir': 'w'},
    'sign': {'text': data.text[100], 'walk_to': monkey.vec2(25, 6), 'dir': 's'},
    'path_start_frontdoor': {'text': '', 'walk_to': monkey.vec2(1, 6), 'dir': 'w'},
    'doormat': {'text': data.text[101], 'walk_to': monkey.vec2(380, 47), 'dir': 's', 'open': True},
    'front_door': {'text': data.text[103], 'walk_to': monkey.vec2(401, 48), 'dir': 'n', 'anim': 'closed',
                    'room_id': 'foyer', 'room_dir': 'e', 'room_pos': monkey.vec2(50, 6)},
    'front_door_in': {'text': data.text[103], 'walk_to': monkey.vec2(50, 6), 'dir': 'w', 'master': 'front_door',
                    'room_id': 'front_door', 'room_dir': 's', 'room_pos': monkey.vec2(401, 48)},
    'kitchen_door': {'text': data.text[106], 'walk_to': monkey.vec2(180, 22), 'dir': 'n', 'anim': 'closed',
                   'room_id': 'kitchen', 'room_dir': 'e', 'room_pos': monkey.vec2(50, 6)},
    'sitting_room_door': {'text': data.text[106], 'walk_to': monkey.vec2(590, 6), 'dir': 'e', 'anim': 'closed',
                     'room_id': 'sitting_room', 'room_dir': 'e', 'room_pos': monkey.vec2(50, 6)},

    'key': {'text': data.text[102], 'walk_to': monkey.vec2(380, 47), 'dir': 's'},
    'grandfather_clock': {'text': data.text[104], 'walk_to': monkey.vec2(120, 16), 'dir': 'n'},
    'vase_l': {'text': data.text[105], 'walk_to': monkey.vec2(232, 15), 'dir': 'n' },
    'vase_r': {'text': data.text[105], 'walk_to': monkey.vec2(384, 15), 'dir': 'n'},
}


def update_item(item, key, value):
    def f():
        items[item][key] = value
    return f
