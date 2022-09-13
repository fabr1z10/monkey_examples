from . import factory
from . import func
from .items import items
import monkey
from . import state

def basement():
    r = factory.ScummRoom('basement', 656)
    r.add_walkarea(outline= [0,0,656,0,620,20,600,20,586,122,564,122,564,20,494,20,494,7,102,7,102,16,327,16,327,20,56,20,0,3])

    bg = monkey.Node()
    bg.add(factory.img('assets/basement.png', 0, 0, -0.1))
    bg.add(factory.img('assets/basement1.png', 512, 24, func.z(24)))
    bg.add(factory.img('assets/basement2.png', 112, 8, func.z(8)))
    r.add(bg)
    state.ids['bg'] = bg.id
    r.add(factory.hotspot(48, 8, 'stairs', 561, 120))
    r.add(factory.hotspot(7, 8, 'basement_light_switch', 545, 56))

    # key
    if 'silver_key' not in state.inventory:
        r.add(factory.hotspot(7, 12, 'silver_key', 98, 61, sprite='silver_key'))
    r.add(factory.hotspot(61, 33, 'furnace', 425, 10))
    r.add(factory.hotspot(55, 49, 'nuclear_reactor', 448, 42))

    fbox = items['fuse_box']['anim']
    r.add(factory.hotspot(33, 33, 'fuse_box', 64, 47, sprite='fuse_box', anim=fbox, z=-0.05, priority=2))
    r.add(factory.hotspot(22, 23, 'circuit_breakers', 70, 52, priority=1))

    r.add_dynamic()
    return r.r
