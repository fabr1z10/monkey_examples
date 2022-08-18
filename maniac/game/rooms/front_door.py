from . import factory
from . import state
from . import scripts
from .items import items
import monkey


def front_door():
    r = factory.ScummRoom('front_door', 960)
    r.add_walkarea(outline= [0, 2, 960, 2, 960, 14, 483, 14, 480, 3, 448, 3, 423, 38, 423, 48, 335, 48,
                             335, 38, 304, 3, 277, 3, 277, 14, 0, 14])
    r.add(factory.img('assets/frontdoor.png', 0, 0, -0.1))
    r.add(factory.img('assets/frontdoor1.png', 815, 0, 1))

    # door mat
    doormat_open = items['doormat']['open']
    doormat_width = 48 if doormat_open else 90
    r.add(factory.hotspot(doormat_width, 5, 'doormat', 336, 41, sprite='doormat',
                          anim='open' if doormat_open else 'closed', priority=2, z=0.1))

    # key
    if 'key' not in state.inventory:
        r.add(factory.hotspot(11, 4, 'key', 412, 42, sprite='key'))

    # front door
    r.add(factory.hotspot(43, 78, 'front_door', 381, 50, sprite='front_door', anim=items['front_door']['anim']))
    r.add_dynamic()
    return r.r
