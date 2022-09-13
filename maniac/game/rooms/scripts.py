import monkey
from . import state
from .items import items, update_item, get, geu
from . import factory
from . import func


def ws(item_id):
    s = monkey.script(id='cane')
    ii = -1
    for id, s1 in state.before_action_script.items():
        ii = s1(s)
    if item_id not in state.inventory:
        item = items[item_id]
        w = geu(item, 'walk_to')
        ii = s.add(monkey.walk(id=state.player_id, pos=monkey.vec2(w[0], w[1]), dir=get(item, 'dir', None), speed=100))
    return s, ii

def h1(*lines):
    def f():
        s, ii = ws(state.current_item)
        s.add(factory.say(list(lines)), ii)
        monkey.play(s)
    return f

def _pickup(id):
    def f():
        if id not in state.inventory:
            s, ii = ws(id)
            ii = s.add(monkey.remove(id=items[id]['id']), ii)
            ii = s.add(monkey.callfunc(func.add_to_inventory(id)), ii)
            monkey.play(s)
    return f


def read_sign():
    s, ii = ws('sign')
    s.add(factory.say([1000, 1001]), ii)
    monkey.play(s)


def _walk_path(room_to, pos, dir):
    def f():
        s, ii = ws(state.current_item)
        s.add(monkey.callfunc(func.change_room(room_to, pos, dir)), ii)
        monkey.play(s)
    return f

def walkto_path_start_frontdoor():
    s, ii = ws('path_start_frontdoor')
    s.add(monkey.callfunc(func.change_room('front_door', monkey.vec2(950, 4), 'w')), ii)
    monkey.play(s)

def turnoff_basement_light_switch():
    s, ii = ws(state.current_item)
    s.add(monkey.callfunc(func.darken), ii)
    monkey.play(s)

def turnon_basement_light_switch():
    s, ii = ws(state.current_item)
    s.add(monkey.callfunc(func.brighten), ii)
    monkey.play(s)

walkto_stairs = _walk_path('foyer', monkey.vec2(459, 22), 's')

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
read_grandfather_clock = h1(1008)
read_furnace = h1(1010)
read_nuclear_reactor = h1(1011)


def change_state(id, state):
    def f():
        item = items[id]
        if item['state'] == state:
            return
        new_state = item['states'][state]
        item['state'] = state
        node = monkey.get_node(item['id'])
        hotspot = node.get_hotspot()
        if 'size' in new_state:
            size = new_state['size']
            offset = new_state.get('offset', (0, 0))
            s = monkey.aabb(offset[0], offset[0] + size[0], offset[1], offset[1] + size[1])
            hotspot.set_shape(s)
        if 'priority' in new_state:
            hotspot.priority = new_state['priority']
        if 'anim' in new_state:
            node.set_animation(new_state['anim'])
    return f

def update_hotspot(id, width=0, height=0, x=0, y=0, prio=-1):
    def f():
        node = monkey.get_node(id)
        hotspot = node.get_hotspot()
        if width != 0 and height != 0:
            node.clear_children()
            s = monkey.aabb(x, x+width, y, y+height)
            hotspot.set_shape(s)
            b = monkey.Node()
            b.set_model(monkey.make_model(s, color=(1,0,0,1)))
            node.add(b)
        if prio != -1:
            hotspot.priority = prio
    return f


def pull_doormat():
    s, ii = ws('doormat')
    ii = s.add(monkey.callfunc(change_state('doormat', 1)))
    monkey.play(s)


def push_doormat():
    s, ii = ws('doormat')
    ii = s.add(monkey.callfunc(change_state('doormat', 0)))
    monkey.play(s)


def pickup_key():
    if 'key' not in state.inventory:
        s, ii = ws('key')
        ii = s.add(monkey.remove(id=items['key']['id']), ii)
        ii = s.add(monkey.callfunc(func.add_to_inventory('key')), ii)
        monkey.play(s)

pickup_silver_key = _pickup('silver_key')

def update_door(id, open: bool):
    def f():
        anim = 'open' if open else 'closed'
        s, ii = ws(id)
        ii = s.add(monkey.animate(id=items[id]['id'], anim=anim), ii)
        master = items[id].get('master', id)
        print('master is ',master)
        ii = s.add(monkey.callfunc(update_item(master, 'anim', anim)))
        monkey.play(s)
    return f

def walk_door(id):
    def f():
        s, ii = ws(id)
        item = items[id]
        master = item.get('master', id)
        if items[master]['anim'] == 'open':
            s.add(monkey.callfunc(func.change_room(item['room_id'], item['room_pos'], item['room_dir'])), ii)
        monkey.play(s)
    return f


def open_front_door():
    if not state.front_door_unlocked:
        h1(1007)()
    else:
        update_door('front_door', True)()

def open_basement_door():
    s, ii = ws('basement_door')
    if items['basement_door']['anim'] == 'closed':
        s.add(factory.say([1009]), ii)
    monkey.play(s)

open_front_door_in = update_door('front_door_in', True)
close_front_door_in = update_door('front_door_in', False)
walkto_front_door_in = walk_door('front_door_in')

def open_fuse_box():
    s, ii = ws('fuse_box')
    ii = s.add(monkey.animate(id=items['fuse_box']['id'], anim='open'), ii)
    ii = s.add(monkey.callfunc(update_item('fuse_box', 'anim', 'open')))
    ii = s.add(monkey.callfunc(update_hotspot(items['fuse_box']['id'], 49,33,-16,0)), ii)
    ii = s.add(monkey.callfunc(update_hotspot(items['circuit_breakers']['id'], 0, 0, 0, 0, 3)), ii)
    monkey.play(s)

def close_fuse_box():
    s, ii = ws('fuse_box')
    ii = s.add(monkey.animate(id=items['fuse_box']['id'], anim='closed'), ii)
    ii = s.add(monkey.callfunc(update_item('fuse_box', 'anim', 'closed')))
    ii = s.add(monkey.callfunc(update_hotspot(items['fuse_box']['id'], 33,33,0,0)), ii)
    ii = s.add(monkey.callfunc(update_hotspot(items['circuit_breakers']['id'], 0, 0, 0, 0, 1)), ii)
    monkey.play(s)

open_kitchen_door = update_door('kitchen_door', True)
close_kitchen_door = update_door('kitchen_door', False)
walkto_kitchen_door = walk_door('kitchen_door')

open_sitting_room_door = update_door('sitting_room_door', True)
close_sitting_room_door = update_door('sitting_room_door', False)
walkto_sitting_room_door = walk_door('sitting_room_door')
walkto_basement_door = walk_door('basement_door')

def rm_before_action_script(id):
    def f():
        del state.before_action_script[id]
    return f

def push_gargoyle_r():
    def b(id):
        def f(s):
            print('current player = ',state.current_player, ' ', id)
            if state.current_player == id:
                bd = items['basement_door']
                bd['anim'] = 'closed'
                ii = s.add(monkey.animate(id=bd['id'], anim='closed'))
                master = bd.get('master', 'basement_door')
                ii = s.add(monkey.callfunc(update_item(master, 'anim', 'closed')), ii)
                ii = s.add(monkey.callfunc(rm_before_action_script('gargoyle')), ii)
                return ii
            else:
                return -1
        return f
    def a():
        state.before_action_script['gargoyle'] = b(state.current_player)
    s, ii = ws(state.current_item)
    bd = items['basement_door']
    ii = s.add(monkey.animate(id=bd['id'], anim='open'), ii)
    master = bd.get('master', 'basement_door')
    ii = s.add(monkey.callfunc(update_item(master, 'anim', 'open')), ii)
    ii = s.add(monkey.callfunc(a), ii)
    monkey.play(s)

close_front_door = update_door('front_door', False)
walkto_front_door = walk_door('front_door')

