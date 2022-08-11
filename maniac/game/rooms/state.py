import monkey
from . import data


verb_color_selected = (1.0, 1.0, 85.0/255.0, 1.0)
verb_color_unselected = (0.0, 170.0/255.0, 0, 1.0)
current_verb_color = (1.0, 85.0/255.0, 1.0, 1.0)
dave_text = (85.0/255.0, 85.0/255.0, 1.0, 1.0)

player_id = None

current_verb = None
current_item = None
current_item2 = None

ids = dict()

items = {
    'sign': {'text': data.text[100], 'walk_to': monkey.vec2(25, 6), 'dir': 's'}
}

def get(id):
    return monkey.engine().get_node(ids[id])


