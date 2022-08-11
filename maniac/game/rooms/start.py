from . import factory
from . import state
from . import scripts
import monkey

def enter_item(item):
    def f(n):
        print('sica0')
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
    state.current_verb = 'walkto'
    state.current_item = None
    state.current_item2 = None
    factory.update_action()

def start():
    r = factory.ScummRoom(320)
    #r.add_walkarea(outline=[0, 0, 320, 0, 320, 128, 0, 128, 0, 100,200,100,200,32,0,32])
    r.add_walkarea(outline= [0, 2, 320, 2, 320, 12, 0, 12])
    #a = monkey.Node()
    #a.add_component(monkey.walkarea())
    #r.cam_node.add(a)
    r.add(factory.img('assets/start.png', 0, 0))
    r.add(factory.img('assets/start1.png', 0, 0, 1))
    r.add(factory.character(r.cam, 'dave', 20, 50, True), parent=0)

    a = monkey.Node()
    s = monkey.aabb(0, 31, 0, 22)
    a.add_component(monkey.hotspot(s,
                                   on_enter=enter_item('sign'),
                                   on_leave=leave_item,
                                   on_click=run_action,
                                   priority=1))
    a.set_model(monkey.make_model(s))
    a.set_position(9,24,0)
    r.add(a)
    #r, c, cam = factory.room(320)
    #c.add(factory.character(cam, 'dave', 0, 0))

    return r.r
