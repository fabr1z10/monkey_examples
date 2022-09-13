from . import factory


def start():
    r = factory.ScummRoom('start', 320)
    r.add_walkarea(outline= [0, 2, 320, 2, 320, 12, 0, 12])
    r.add(factory.img('assets/start.png', 0, 0))
    r.add(factory.img('assets/start1.png', 0, 0, 1))
    r.add_dynamic()
    r.add_item('sign', x=9, y=24)
    r.add_item('path_start_frontdoor',x=0, y=0)
    return r.r
