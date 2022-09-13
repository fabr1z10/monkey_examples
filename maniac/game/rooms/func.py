import monkey
from . import state
from . import factory
from . import scripts
from .. import settings
from . import items


def restart():
    monkey.engine().close_room()


def darken():
    for n in monkey.get_node(state.ids['bg']).get_children():
        n.set_mult_color(monkey.vec4(0, 0, 0, 1.))
    pl = monkey.get_node(state.player_id)
    pl.set_mult_color(monkey.vec4(0.))
    pl.set_add_color(state.character_dark_color)


def brighten():
    for n in monkey.get_node(state.ids['bg']).get_children():
        n.set_mult_color(monkey.vec4(1.))



def z(y):
    return 1. - y / 144.


def change_room(room, pos, dir):
    def f():
        settings.room = room
        i = items.items[state.current_player]
        i['room'] = room
        i['walkarea'] = 0
        i['pos'] = pos
        i['dir'] = dir
        print(i)
        #state.start_position = pos
        restart()
    return f


def enter_item(item):
    def f(n):
        state.current_item = item
        factory.update_action()
    return f


def leave_item(n):
    state.current_item = None
    factory.update_action()


def run_action(n,p):
    if not state.current_item:
        return
    act = state.current_verb + '_' + state.current_item
    if state.current_item2:
        act += '_' + state.current_item2
    print('checking action: ' + act)
    if hasattr(scripts, act):
        getattr(scripts, act)()
    else:
        actd = state.current_verb + '_'
        if hasattr(scripts, actd):
            print('found default script for verb: ', actd)
            getattr(scripts, actd)()
    state.current_verb = 'walkto'
    state.current_item = None
    state.current_item2 = None
    factory.update_action()


def add_to_inventory(item_id):
    def f():
        state.inventory[item_id]= [state.current_player, 1]
        inv = monkey.get_node(state.ids['inventory'])
        factory.update_inventory(inv)
    return f