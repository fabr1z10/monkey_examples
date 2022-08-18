import monkey
from . import data
from . import factory

verb_color_selected = (1.0, 1.0, 85.0/255.0, 1.0)
verb_color_unselected = (0.0, 170.0/255.0, 0, 1.0)
current_verb_color = (1.0, 85.0/255.0, 1.0, 1.0)
inventory_color_unselected = (1.0, 85.0/255.0, 1.0, 1.0)
inventory_color_selected = (1.0, 1.0, 85.0/255.0, 1.0)
dave_text = (85.0/255.0, 85.0/255.0, 1.0, 1.0)

player_id = None

current_verb = None
current_item = None
current_item2 = None
current_player = 'dave'


inventory = {
    #'key': ['dave', 1]
}

ids = dict()

front_door_unlocked = True




def get(id):
    return monkey.engine().get_node(ids[id])


