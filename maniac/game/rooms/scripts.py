import monkey
from . import state
from .items import items, update_item
from . import factory
from . import func


def ws(item_id):
    s = monkey.script(id='cane')
    ii = -1
    if item_id not in state.inventory:
        item = items[item_id]
        ii = s.add(monkey.walk(id=state.player_id, pos=item['walk_to'], dir=item.get('dir',None), speed=100))
    return s, ii

def h1(*lines):
    def f():
        s, ii = ws(state.current_item)
        s.add(factory.say(list(lines)), ii)
        monkey.play(s)
    return f

def read_sign():
    s, ii = ws('sign')
    s.add(factory.say([1000, 1001]), ii)
    monkey.play(s)


def walkto_path_start_frontdoor():
    s, ii = ws('path_start_frontdoor')
    s.add(monkey.callfunc(func.change_room('front_door', monkey.vec2(950, 4), 'w')), ii)
    monkey.play(s)



def walkto_():
    s, _ = ws(state.current_item)
    monkey.play(s)


push_ = h1(1002)
pull_ = push_
open_ = h1(1003)
close_ = h1(1004)
pickup_ = h1(1005)
turnon_ = h1(1004)
turnoff_ = h1(1004)
read_ = h1(1006)

def update_hotspot(id, width, height):
    def f():
        node = monkey.engine().get_node(id)
        node.clear_children()
        s = monkey.aabb(0, width, 0, height)
        node.get_hotspot().set_shape(s)
        b = monkey.Node()
        b.set_model(monkey.make_model(s, color=(1,0,0,1)))
        node.add(b)
    return f


def pull_doormat():
    s, ii = ws('doormat')
    if not items['doormat']['open']:
        ii = s.add(monkey.animate(id=items['doormat']['id'], anim='open'), ii)
        ii = s.add(monkey.callfunc(update_hotspot(items['doormat']['id'], 48, 5)), ii)
        s.add(monkey.callfunc(update_item('doormat', 'open', True)), ii)
    monkey.play(s)


def push_doormat():
    s, ii = ws('doormat')
    if items['doormat']['open']:
        ii = s.add(monkey.animate(id=items['doormat']['id'], anim='closed'), ii)
        ii = s.add(monkey.callfunc(update_hotspot(items['doormat']['id'], 90, 5)), ii)
        s.add(monkey.callfunc(update_item('doormat', 'open', False)), ii)
    monkey.play(s)


def pickup_key():
    if 'key' not in state.inventory:
        s, ii = ws('key')
        ii = s.add(monkey.remove(id=items['key']['id']), ii)
        ii = s.add(monkey.callfunc(func.add_to_inventory('key')), ii)
        monkey.play(s)


def update_door(id, open: bool):
    def f():
        anim = 'open' if open else 'closed'
        s, ii = ws(id)
        ii = s.add(monkey.animate(id=items[id]['id'], anim=anim), ii)
        ii = s.add(monkey.callfunc(update_item('front_door', 'anim', anim)))
        monkey.play(s)
    return f


def open_front_door():
    if not state.front_door_unlocked:
        h1(1007)()
    else:
        update_door('front_door', True)()

close_front_door = update_door('front_door', False)

