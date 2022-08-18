import monkey
from . import state
from . import factory
from . import scripts
from .. import pippo
from . import items

def restart():
    monkey.engine().close_room()


def change_room(room, pos, dir):
    def f():
        pippo.room = room
        i = items.items[state.current_player]
        i['room'] = room
        i['walkarea'] = 0
        i['pos'] = pos
        i['dir'] = dir
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
        inv = monkey.engine().get_node(state.ids['inventory'])
        factory.update_inventory(inv)
    return f