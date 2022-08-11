import monkey

from . import func
from . import state
from . import data

def update_action():
    v = verbs[state.current_verb]
    node = state.get('current_verb')
    a = v[0]
    if state.current_item:
        a += ' ' + state.items[state.current_item]['text']
    if state.current_item2:
        a += ' in ' + state.items[state.current_item2]['text']
    node.set_text(a)


def on_click_verb(verb):
    def f(a, b):
        state.current_verb = verb
        state.current_item = None
        state.current_item2 = None
        update_action()
    return f


verbs = {
    'push': [data.text[0], on_click_verb('push')],
    'pull': [data.text[1], on_click_verb('pull')],
    'give': [data.text[2], on_click_verb('give')],
    'open': [data.text[3], on_click_verb('open')],
    'close': [data.text[4], on_click_verb('close')],
    'read': [data.text[5], on_click_verb('read')],
    'walkto': [data.text[6], on_click_verb('walkto')],
    'pickup': [data.text[7], on_click_verb('pickup')],
    'whatis': [data.text[8], on_click_verb('whatis')],
    'unlock': [data.text[9], on_click_verb('unlock')],
    'newkid': [data.text[10], on_click_verb('newkid')],
    'use': [data.text[11], on_click_verb('use')],
    'turnon': [data.text[12], on_click_verb('turnon')],
    'turnoff': [data.text[13], on_click_verb('turnoff')],
    'fix': [data.text[14], on_click_verb('fix')],

}


class ScummRoom:
    def __init__(self, width):
        self.r = monkey.Room("mario")
        self.r.add_runner(monkey.scheduler())
        self.walkareas = []
        root = self.r.root()
        kb = monkey.keyboard()
        kb.add(299, 1, 0, func.restart)
        root.add_component(kb)

        # create camera
        device_width = 320
        device_height = 128
        device_half_width = device_width // 2
        device_half_height = device_height // 2
        cam_node = monkey.Node()
        cam = monkey.camera_ortho(device_width, device_height, viewport=[0, 56, device_width, device_height])
        cam.set_bounds(device_half_width, width - device_half_width, device_half_height, device_half_height, -100, 100)
        cam_node.set_camera(cam)
        cam_node.add_component(monkey.hot_spot_manager())
        cam_node.add(main_hotspot(width, 128))
        root.add(cam_node)

        self.cam_node = cam_node
        self.cam = cam

        ui = monkey.Node()
        ui_cam = monkey.camera_ortho(device_width, 200)
        ui.add_component(monkey.hot_spot_manager())
        ui.set_camera(ui_cam)

        ui.add(verb('push', 0, 40, state.verb_color_unselected))
        ui.add(verb('pull', 0, 32, state.verb_color_unselected))
        ui.add(verb('give', 0, 24, state.verb_color_unselected))

        ui.add(verb('open', 56, 40, state.verb_color_unselected))
        ui.add(verb('close', 56, 32, state.verb_color_unselected))
        ui.add(verb('read', 56, 24, state.verb_color_unselected))

        ui.add(verb('walkto', 120, 40, state.verb_color_unselected))
        ui.add(verb('pickup', 120, 32, state.verb_color_unselected))
        ui.add(verb('whatis', 120, 24, state.verb_color_unselected))

        ui.add(verb('unlock', 192, 40, state.verb_color_unselected))
        ui.add(verb('newkid', 192, 32, state.verb_color_unselected))
        ui.add(verb('use', 192, 24, state.verb_color_unselected))

        ui.add(verb('turnon', 256, 40, state.verb_color_unselected))
        ui.add(verb('turnoff', 256, 32, state.verb_color_unselected))
        ui.add(verb('fix', 256, 24, state.verb_color_unselected))

        state.current_verb='walkto'
        cv = text(verbs[state.current_verb][0], 0, 48, state.current_verb_color)[0]
        state.ids['current_verb'] = cv.id
        ui.add(cv)

        # score_node.add(text('MARIO', 24, 8))
        # score_node.add(text('{:06d}'.format(state.score), 24, 16))
        # score_node.add(text('*', 96, 16))
        # coin_counter = text('{:02d}'.format(state.coins), 104, 16)
        # state.coin_label = coin_counter.id
        # score_node.add(coin_counter)
        # score_node.add(text('WORLD', 144, 8))
        ##score_node.add(text(state.world_name, 152, 16))
        ##score_node.add(text('TIME', 200, 8))
        # score_node.add(text('{:03d}'.format(state.time), 208, 16))
        # score_node.add(sprite(-2.8, 6, 'sprites/coin_counter'))
        root.add(ui)

    def add(self, node, parent=None):
        if parent is None:
            parent = self.cam_node
        else:
            parent = self.walkareas[parent]
        parent.add(node)



    def add_walkarea(self, **kwargs):
        a = monkey.Node()
        a.add_component(monkey.walkarea(**kwargs))
        self.cam_node.add(a)
        self.walkareas.append(a)


def img(file, x, y, z = 0, size=None):
    n = monkey.Node()
    n.set_model(monkey.image(file, size=size))
    n.set_position(x, y, z)
    return n


def text(what, x, y, color):
    n1 = monkey.Node()
    t = monkey.text(font='font', text=what, size=8)
    n1.set_model(t)
    n1.set_position(x-160, y-100+8, 0)
    n1.set_mult_color(*color)
    return n1, t.size

def on_enter(a):
    def f(m):
        m.set_mult_color(*state.verb_color_selected)
    return f

def on_exit(a):
    def f(m):
        m.set_mult_color(*state.verb_color_unselected)
    return f

def pino(m):
    print('ciao')

def gigi(m):
    print('gigi')

def pane(node, pos):
    s = monkey.script(id='cane')
    s.add(monkey.walk(id=state.player_id, pos=pos, speed=100))
    monkey.play(s)





def verb(id, x, y, color):
    v = verbs[id]
    verb, size = text(v[0], x, y, color)
    s = monkey.aabb(0, size.x, -8, -8+size.y)
    verb.add_component(monkey.hotspot(s, on_enter=on_enter(id), on_leave=on_exit(id), on_click=v[1]))
    r = monkey.Node()
    #r.set_position(0, -8, 0)
    r.set_model(monkey.make_model(s))
    verb.add(r)
    return verb


def main_hotspot(width, height):
    n = monkey.Node()
    s = monkey.aabb(0, width, 0, height)
    n.add_component(monkey.hotspot(s, on_enter=pino, on_leave=gigi, on_click=pane))
    n.set_model(monkey.make_model(s))

    return n


# def room(world_width):
#     r = monkey.Room("mario")
#     r.add_runner(monkey.scheduler())
#     root = r.root()
#     kb = monkey.keyboard()
#     kb.add(299, 1, 0, func.restart)
#     root.add_component(kb)
#
#     # create camera
#     device_width = 320
#     device_height = 128
#     device_half_width = device_width // 2
#     device_half_height = device_height // 2
#     cam_node = monkey.Node()
#     cam = monkey.camera_ortho(device_width, device_height, viewport=[0, 56, device_width, device_height])
#     cam.set_bounds(device_half_width, world_width - device_half_width, device_half_height, device_half_height, -100, 100)
#     cam_node.set_camera(cam)
#     cam_node.add_component(monkey.hot_spot_manager())
#     cam_node.add(main_hotspot(50, 100))
#     root.add(cam_node)
#
#     ui = monkey.Node()
#     ui_cam = monkey.camera_ortho(device_width, 200)
#     ui.add_component(monkey.hot_spot_manager())
#     ui.set_camera(ui_cam)
#
#     ui.add(verb('Push', 0, 40, state.verb_color_unselected))
#     ui.add(verb('Pull', 0, 32, state.verb_color_unselected))
#     ui.add(verb('Give', 0, 24, state.verb_color_unselected))
#
#     ui.add(verb('Open', 56, 40, state.verb_color_unselected))
#     ui.add(verb('Close', 56, 32, state.verb_color_unselected))
#     ui.add(verb('Read', 56, 24, state.verb_color_unselected))
#
#     ui.add(verb('Walk to', 120, 40, state.verb_color_unselected))
#     ui.add(verb('Pick up', 120, 32, state.verb_color_unselected))
#     ui.add(verb('What is', 120, 24, state.verb_color_unselected))
#
#     ui.add(verb('Unlock', 192, 40, state.verb_color_unselected))
#     ui.add(verb('New kid', 192, 32, state.verb_color_unselected))
#     ui.add(verb('Use', 192, 24, state.verb_color_unselected))
#
#     ui.add(verb('Turn on', 256, 40, state.verb_color_unselected))
#     ui.add(verb('Turn off', 256, 32, state.verb_color_unselected))
#     ui.add(verb('Fix', 256, 24, state.verb_color_unselected))
#
#     #score_node.add(text('MARIO', 24, 8))
#     #score_node.add(text('{:06d}'.format(state.score), 24, 16))
#     #score_node.add(text('*', 96, 16))
#     #coin_counter = text('{:02d}'.format(state.coins), 104, 16)
#     #state.coin_label = coin_counter.id
#     #score_node.add(coin_counter)
#     #score_node.add(text('WORLD', 144, 8))
#     ##score_node.add(text(state.world_name, 152, 16))
#     ##score_node.add(text('TIME', 200, 8))
#     #score_node.add(text('{:03d}'.format(state.time), 208, 16))
#     #score_node.add(sprite(-2.8, 6, 'sprites/coin_counter'))
#     root.add(ui)
#
#     return r, cam_node, cam


def character(cam, model, x, y, is_player):
    node = monkey.Node()
    node.set_position(x, y, 0)
    node.set_model(monkey.get_sprite('sprites/'+model))
    node.add_component(monkey.follow(cam, (0, 0, 5), (0, 1, 0)))
    if is_player:
        state.player_id = node.id
    return node