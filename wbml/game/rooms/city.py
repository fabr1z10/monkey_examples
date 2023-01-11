################## city of wonderland

import monkey
from .. import settings
from . import actions
from .factory import *
from . import gamestate
import math

def create_hand():
    game_node = monkey.get_node(settings.ids.game_node)
    r = monkey.root()
    kb = r.get_keyboard()
    kb.add(263, 1, 0, func.move_hand_left)
    kb.add(262, 1, 0, func.move_hand_right)
    kb.add(settings.button_1, 1, 0, func.select)
    hand = sprite(10.5,15.5,1.1,'sprites/hand')
    settings.ids.hand = hand.id
    game_node.add(hand)

def f2():
    gamestate.player_position = (81.5, 6)
    gamestate.shop.exit_room = 'city'
    gamestate.shop.l_item_text = ['Jump at fence,\n\nget time.']
    gamestate.shop.r_item_text = ['DEATH god has the\n\nkey to neighbor.']
    msg = [message('What ?', 96, 120+16)]
    s = monkey.script()
    ii = -1
    for m in msg:
        ii =s.add(monkey.actions.add(id=settings.ids.game_node, node=m), ii)
        ii= s.add(monkey.actions.reveal_text(id=m.id, interval=0.1), ii)
        ii= s.add(monkey.actions.wait_for_key(65), ii)
        ii= s.add(monkey.actions.remove(id=m.id), ii)
    ii = s.add(monkey.actions.callfunc(create_hand),ii)
    monkey.play(s)

def f():
    gamestate.player_position = (45.5, 4)
    gamestate.city_door1 = 'barred'
    msg = [
        message('Oh!fighter\n\nListen!↓', 96, 120+16),
        message('Our country\n\ndepends on you . ↓', 96, 120+16),
        message("Defeat DRAGON, and\n\nLet's regain peace. ↓", 96, 120 + 16),
        message('Get this sword and\n\npill.', 96, 120 + 16),
    ]

    s = monkey.script()
    ii = -1
    for m in msg:
        ii =s.add(monkey.actions.add(id=settings.ids.game_node, node=m), ii)
        ii= s.add(monkey.actions.reveal_text(id=m.id, interval=0.01), ii)
        ii= s.add(monkey.actions.wait_for_key(65), ii)
        ii= s.add(monkey.actions.remove(id=m.id), ii)
    ii =s.add(actions.change_room('city'), ii)
    #ii =s.add(monkey.actions.add(id=settings.ids.game_node, node=msg2), ii)
    #ii= s.add(monkey.actions.reveal_text(id=msg2.id, interval=0.1), ii)
    #ii= s.add(monkey.actions.wait_for_key(65), ii)
    #ii= s.add(monkey.actions.remove(id=msg2.id), ii)
    monkey.play(s)

def ctyhous1():
    room, game_node = common_room(192, 192)
    game_node.add(tiled2(model='tiles/room1', z=0))
    game_node.add(sprite(8.5,6.5,0.1,'sprites/creature1'))
    game_node.add(rect4(8,19,7,4,z=1))
    game_node.add(sprite(9,20,1.1,'sprites/sword'))
    room.set_on_start(f)
    return room

def ctyhous2():
    gamestate.hand_pos = 0
    room, game_node = common_room(192, 192)
    #kb = room.root().get_keyboard()

    game_node.add(tiled(0,0,'tiles/room2',z=0))
    game_node.add(rect4(2,20,6,3,z=1))
    game_node.add(rect4(9,19,6,3,z=1))
    game_node.add(rect4(16,20,6,3,z=1))
    game_node.add(sprite(3.25,20.6,1.1,'sprites/cocktail'))
    game_node.add(sprite(17.5,20.6,1.1,'sprites/beermug'))
    game_node.add(sprite(9.4,20,1.1,'sprites/exit'))
    game_node.add(sprite(8,6.0,0.1,'sprites/creature2'))
    game_node.add(text(7,18,1,'8',monkey.HALIGN_RIGHT, 4))
    game_node.add(text(22,18,1,'5',monkey.HALIGN_RIGHT, 4))
    room.set_on_start(f2)

    return room

def ctyhous3():
    room, game_node = common_room(192, 192)
    game_node.add(tiled2(model='tiles/room3',z=-0.1))
    p = player(game_node.get_camera(), 2, 14)
    game_node.add(tiled2(w=24,h=4))
    game_node.add(tiled2(w=1,h=24,pos=(-1, 0)))
    game_node.add(tiled2(w=1, h=24,pos=(24,0)))
    game_node.add(p)
    return room



def city():
    room, game_node = common_room(1280, 192)

    p = player(game_node.get_camera(), gamestate.player_position[0], gamestate.player_position[1])
    game_node.add(p)
    settings.ids.player = p.id

    game_node.add(tiled2(w=1, h=20, pos=(-1, -1)))              # left boundary
    game_node.add(tiled2(w=1, h=40, pos=(160, -1)))
    game_node.add(tiled2(desc='1,W,27,R,27,1,3,E,R,27,1,2,E', w=54, h=4, pos=(0, 0)))
    game_node.add(tiled2(desc='1,W,12,R,2,R,12,1,3,E,E,R,4,0,3,R,10,1,3,E,6,6,E,0,2,R,10,1,2,E,6,5', w=24, h=14, pos=(54,0)))
    game_node.add(tiled2(desc='1,W,6,R,2,R,6,1,3,E,E,R,5,1,2,E,2,3', w=12,h=6,pos=(78,0)))
    game_node.add(tiled2(desc='1,W,10,R,10,1,3,E,R,10,1,2,E', w=20, h=4, pos=(90,0)))
    game_node.add(tiled2(desc='1,W,2,R,4,1,3,E,0,2,1,2', w=4, h=6, pos=(110, 0)))
    game_node.add(tiled2(desc='1,W,2,R,6,1,3,E,0,2,1,2', w=4, h=8, pos=(114, 0)))
    game_node.add(tiled2(desc='1,W,41,R,164,1,3,E,0,2,R,40,1,2,E', w=82, h=10, pos=(118, 0)))

    # trees
    for i in [(0,4), (24, 4), (30, 4), (64, 14), (70, 14), (134,10), (140,10), (146,10)]:
        game_node.add(tiled2(pos=(i[0], i[1]), model='tiles/tree', z=-0.1))

    # arrow
    for i in [(12,4), (56, 14), (90, 4)]:
        game_node.add(tiled2(pos=(i[0], i[1]), model='tiles/arrow', z=-0.1))

    game_node.add(tiled2(model='tiles/tower', pos=(154,10), z=-0.1))
    # fence
    game_node.add(tiled2(desc='1,W,6,R,6,16,9,E,R,6,16,8,E,R,6,16,7,E', pos=(122,10), z=-0.1))
    game_node.add(tiled2(model='tiles/house1', pos=(134,10), z=-0.1))
    game_node.add(tiled2(pos=(16, 4),model='tiles/sign',z=-0.1))
    game_node.add(tiled2(pos=(40, 4), model='tiles/trunk',z=-0.1))
    game_node.add(door(pos=(44, 4), world='ctyhous1', anim=gamestate.city_door1))
    game_node.add(tiled2(pos=(76, 6),model='tiles/trunk2',z=-0.1))
    game_node.add(door(pos=(80, 6), world='ctyhous2', anim=gamestate.city_door2))
    game_node.add(door(pos=(136, 10), world='ctyhous3', anim=gamestate.city_door1))
    game_node.add(door(pos=(156, 10), world='l2', model='sprites/portcullis', anim='default', tag=settings.tags.gate))


    game_node.add(moving_platform(w=2,points=[0,52,6,2,52,14,4,52,6], desc='1,W,1,19,7', y0=-1))

    game_node.add(line_platform(42,12,8))
    game_node.add(line_platform(78,14,8))
    game_node.add(line_platform(134,18,8))

    game_node.add(snake(62, 14))
    game_node.add(snake(82, 14))
    game_node.add(snake(119, 10))
    game_node.add(cobra(100, 4))
    game_node.add(cobra(130, 10))

    return room
