from . import factory
import monkey

def start():
    r = factory.ScummRoom(320)
    a = monkey.Node()
    a.add_component(monkey.walkarea(outline=[0, 0, 320, 0, 320, 128, 0, 128, 0, 100,200,100,200,32,0,32]))
    r.cam_node.add(a)
    r.add('dave', 20, 50, True, parent=a)
    #r, c, cam = factory.room(320)
    #c.add(factory.character(cam, 'dave', 0, 0))

    return r.r
