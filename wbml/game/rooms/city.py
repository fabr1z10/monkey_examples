import monkey
from .. import settings
from . import actions
from .factory import *
import math

def f():

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
    ii =s.add(actions.change_room('r1'), ii)
    #ii =s.add(monkey.actions.add(id=settings.ids.game_node, node=msg2), ii)
    #ii= s.add(monkey.actions.reveal_text(id=msg2.id, interval=0.1), ii)
    #ii= s.add(monkey.actions.wait_for_key(65), ii)
    #ii= s.add(monkey.actions.remove(id=msg2.id), ii)
    monkey.play(s)

def r0():
    room, game_node = common_room(192, 192)
    game_node.add(tiled(0,0,'tiles/room1',z=0))
    game_node.add(sprite(8.5,6.5,0.1,'sprites/creature1'))
    game_node.add(rect4(8,19,7,4,z=1))
    game_node.add(sprite(9,20,1.1,'sprites/sword'))


    room.set_on_start(f)


    #    platform(desc='1,W,27,R,27,1,3,E,R,27,1,2,E', w=54, h=4))
    return room


def r1():
    room, game_node = common_room(1024, 256)
    p = player(game_node.get_camera(), 10, 50)
    game_node.add(p)
    settings.ids.player = p.id
    #game_node.add(platform(desc='0,W,54,R,27,10,53,9,53,E,R,27,10,52,9,52,E,R,27,10,51,9,51,E,R,27,10,50,9,50,E', w=54, h=4))
    game_node.add(
        platform(desc='1,W,27,R,27,1,3,E,R,27,1,2,E', w=54, h=4))
    game_node.add(platform(desc='1,W,12,R,2,R,12,1,3,E,E,R,4,0,3,R,10,1,3,E,6,6,E,0,2,R,10,1,2,E,6,5', w=24,h=14,pos=(54,0)))
    game_node.add(platform(desc='1,W,6,R,2,R,6,1,3,E,E,R,5,1,2,E,2,3', w=12,h=6,pos=(78,0)))
    game_node.add(platform(desc='1,W,10,R,10,1,3,E,R,10,1,2,E', w=20,h=4,pos=(90,0)))

    # trees
    for i in [(0,4), (24, 4), (30, 4), (64, 14), (70, 14)]:
        game_node.add(tiled(i[0], i[1], model='tiles/tree', z=-0.1))
    # arrow
    for i in [(12,4), (56, 14), (90, 4)]:
        game_node.add(tiled(i[0], i[1], model='tiles/arrow', z=-0.1))
    #game_node.add(tiled(0,4,model='tiles/tree',z=0))
    #game_node.add(tiled(24, 4, model='tiles/tree', z=0))
    #game_node.add(tiled(30, 4, model='tiles/tree', z=0))
    #game_node.add(tiled(12,4,model='tiles/arrow',z=0.1))
    #game_node.add(tiled(56, 14, model='tiles/arrow', z=0.1))
    game_node.add(tiled(16,4,model='tiles/sign',z=0))
    game_node.add(tiled(40,4,model='tiles/trunk',z=0))
    game_node.add(door(44,4,'ciao'))
    game_node.add(tiled(76,6,model='tiles/trunk2',z=0))
    game_node.add(door(80,6,'bar',anim='bar'))

    game_node.add(line_platform(42,12,8))
    game_node.add(line_platform(78,14,8))
    #game_node.add(foe(6,4,'sprites/snake', True, settings.tags.snake, 0))
    game_node.add(snake(10, 4))
    #game_node.add(coin(8,5))

    return room
    room = monkey.Room("mario")
    root = room.root()
    world_width = 256
    # create camera
    device_size = settings.device_size
    device_width = device_size[0]
    device_height = device_size[1]
    device_half_width = device_width // 2
    device_half_height = device_height // 2
    cam_node = monkey.Node()
    cam = monkey.camera_ortho(device_width, device_height)
    cam.set_bounds(device_half_width, world_width - device_half_width, device_half_height, device_half_height, -100, 100)
    cam_node.set_camera(cam)
    root.add(cam_node)


    # life_box = tiled(0, 0, 'tiles/p1')
    # life_text = monkey.Node()
    # life_text.set_model(monkey.text(font='font1', text='LIFE', size=8, palette='pal/1'))
    # cam_node.add(life_box)
    # life_text.set_position(6, 12, 1)
    # life_box.add(life_text)
    # life_box.set_position(6,180,0)

    cam_node.add(ui_box(6, 180, 'LIFE', 1))
    # cam_node.add(ui_box(6, 148, 'GOLD', 2))
    #cam_node.add(rect(0,0,-2,256,240,monkey.vec4(112,112,112,255)))
    #rect2(cam_node, 8, 120, 40, 24)
    # rect2(cam_node, 1, 1, 0, 0)
    # rect2(cam_node, 1, 1, 0, 119)
    # rect2(cam_node, 1, 1, 0, 120)
    #rect2(cam_node, 8, 24, 40, 32)
    cam_node.add(pixels(points=[6, 184]))
    cam_node.add(line(a=(0,0), b=(100,100)))
    cam_node.add(rect(0, 0, -1, size=(256, 224), color=monkey.vec4(112, 112, 112, 255)))
    cam_node.add(rect2(8, 120, 40, 24))
    cam_node.add(rect2(8, 24, 40, 32))
    cam_node.add(rect2(56, 8, 192, 192))

    # cam_node.add(ui_box(6, 204, 'PLAYER 1', 3, tile='p2'))
    # a = monkey.Node()
    # a.set_model(monkey.models.line(monkey.vec2(0,0), monkey.vec2(50, 50), monkey.vec4(1,0,0,1)))
    # cam_node.add(a)

    #a1 = monkey.Node()
    #a1.set_position(120,60,0)
    #a1.set_model(monkey.models.rect(30, 10, monkey.vec4(1,0,0,1), 0))
    #cam_node.add(rect(0, 0, -1, 256, 240, monkey.vec4(112, 112, 112, 255)))

    # gold_box = tiled(0, 0, 'tiles/p1')
    # gold_text = monkey.Node()
    # gold_text.set_model(monkey.text(font='font1', text='GOLD', size=8, palette='pal/2'))
    # cam_node.add(gold_box)
    # gold_text.set_position(6, 12, 1)
    # gold_box.add(gold_text)
    # gold_box.set_position(6,148,0)

    return room