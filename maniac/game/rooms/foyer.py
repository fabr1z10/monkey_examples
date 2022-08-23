from . import factory
from . import state
from .items import items

def foyer():
    r = factory.ScummRoom('foyer', 640)
    r.add_walkarea(outline= [23,0,614,0,560,21,401,21,393,17,325,17,326,30,358,47,368,72,409,92,347,128,320,128,
                             324,92,323,72,300,47,273,17,220,17,218,23,148,23,145,17,73,17])
    r.add(factory.img('assets/foyer.png', 0, 0, -0.1))
    r.add(factory.sprite('gf_clock', 116, 31))

    # front door
    r.add(factory.hotspot(45, 111, 'front_door_in', 24, 3, sprite='front_door_in', anim=items['front_door']['anim']))

    # kitchen door
    r.add(factory.hotspot(39, 87, 'kitchen_door', 161, 24, sprite='kitchen_door', anim=items['kitchen_door']['anim'], z=-1))

    # door to sitting room
    r.add(factory.hotspot(19, 111, 'sitting_room_door', 591, 4, sprite='sitting_room_door', anim=items['sitting_room_door']['anim'], z=-1))


    r.add(factory.hotspot(26, 93, 'grandfather_clock', 109, 18))
    r.add(factory.hotspot(28, 45, 'vase_l', 222, 18))
    r.add(factory.hotspot(28, 45, 'vase_r', 374, 18))
    r.add_dynamic()

    return r.r
