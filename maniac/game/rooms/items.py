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
    'front_door': {'text': data.text[103], 'walk_to': monkey.vec2(401, 48), 'dir': 'n', 'anim': 'closed'},
    'key': {'text': data.text[102], 'walk_to': monkey.vec2(380, 47), 'dir': 's'}
}


def update_item(item, key, value):
    def f():
        items[item][key] = value
    return f
