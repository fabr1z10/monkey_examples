import monkey
import math
from . import actions
from .. import settings
from . import func

cache = dict()

# TODO remove
# def tiled(x, y, model, z=-1):
#     node2 = monkey.Node()
#     node2.set_position(x*8, y*8, z)
#     node2.set_model(monkey.get_tiled(model))
#     return node2

def text(x, y, z, label, align, pal):
    t = monkey.Node()
    t.set_position(x * 8, y*8, z)
    t.set_model(monkey.models.text(font='font1', text=label, size=8, halign=align, palette='pal/'+str(pal)))
    return t

def ui_box(x, y, label, pal, tile='p1'):
    box = tiled(0, 0, 'tiles/'+tile)
    text = monkey.Node()

    text.set_model(monkey.models.text(font='font1', text=label, size=8, palette='pal/' + str(pal)))
    text.set_position(6, 12, 1)
    box.add(text)
    box.set_position(x, y, 0)
    return box

def container(x, y):
    pass

def rect(x, y, z, w, h, color):
    a1 = monkey.Node()
    a1.set_position(x, y, z)
    a1.set_model(monkey.models.rect(w, h, color, 1));
    return a1

def pixels(**kwargs):
    a = monkey.Node()
    a.set_model(monkey.models.pixels(**kwargs))
    return a


def rect(x, y, z, **kwargs):
    a = monkey.Node()
    a.set_position(x, y, z)
    a.set_model(monkey.models.rect(**kwargs))
    return a

def line(**kwargs):
    a = monkey.Node()
    a.set_model(monkey.models.line(**kwargs))
    return a
    # cam_node.add(ui_box(6, 204, 'PLAYER 1', 3, tile='p2'))
    # a = monkey.Node()
    # a.set_model(monkey.models.line(monkey.vec2(0,0), monkey.vec2(50, 50), monkey.vec4(1,0,0,1)))
    # cam_node.add(a)

def message(text,x, y):

    text_node = monkey.Node()
    text_node.set_position(x,y,1)
    model = monkey.models.text(font='font1', text=text, size=8, palette='pal/4', halign=monkey.HALIGN_CENTER)
    xx = model.size
    tiles_wide = math.ceil((xx.y - xx.x) / 8.0) + 2
    tiles_high = math.ceil((xx.w - xx.z) / 8.0)
    #yc = 120 + abs(xx.z)
    yc = 0
    #a.set_position(96, yc, 0.02)
    print(tiles_wide, tiles_high)
    rect_node = rect(xx.x - 8, yc + xx.z, -0.01, size=(tiles_wide*8, tiles_high*8), color=monkey.vec4(0, 0, 0, 255))
    #game_node.add(b)
    text_node.set_model(model)
    text_node.add(rect_node)
    #game_node.add(a)
    #game_node.add(
    border = monkey.Node()
    desc = '0,W,' + str(tiles_wide+2) + ',17,11,R,' + str(tiles_wide) + ',18,11,E,19,11,R,' + str(tiles_high) + ',17,10,R,' + str(tiles_wide)+',-1,E,19,10,E,17,9,R,'+ str(tiles_wide) + ',18,9,E,19,9'
    border.set_model(monkey.models.tiled(desc))
    border.set_position(xx.x - 16,xx.z-8,2)
    text_node.add(border)
    return text_node


def rect2(x, y, w, h, bg=monkey.vec4(0, 0, 0, 255)):
    a = rect(x, y, -0.9, size=(w, h), color=bg)
    a.add(rect(-1, 0, -0.01, size=(w+1, h+1), color=monkey.vec4(45, 45, 45, 255)))
    a.add(rect(0, -1, -0.01, size=(w+1, h+1), color=monkey.vec4(174, 174, 174, 255)))
    return a

def rect3(x, y, w, h, z = 0):
    a = rect(x, y, z, size=(w, h), color=monkey.vec4(174, 174, 174, 255))
    a.add(rect(-1, 1, -0.01, size=(w+2, h-2), color=monkey.vec4(174, 174, 174, 255)))
    a.add(rect(0, -1, -0.01, size=(w+2, h), color=monkey.vec4(0,0,0, 255)))
    a.add(rect(1, -2, -0.01, size=(w-1, h), color=monkey.vec4(0,0,0, 255)))
    a.add(rect(0, 1, -0.01, size=(w+3, h-3), color=monkey.vec4(0,0,0, 255)))
    return a

def rect4(x, y, w, h, z = 0):
    a = monkey.Node()
    desc='0,W,' + str(w) + ',24,15,R,' + str(w-2) + ',25,15,E,26,15,R,' + str(h-2) +',24,14,R,'+str(w-2)+',25,14,E,26,14,E,24,13,R,'+str(w-2)+',25,13,E,26,13'
    print(desc)
    #desc='0,W,2,0,0'
    model = monkey.models.tiled(desc)
    a.set_model(model)
    a.set_position(x*8,y*8,z)
    return a

def moving_platform(**kwargs):
    # moving platform
    node = monkey.Node()
    w = kwargs['w']
    x0 = kwargs.get('x0', 0)
    y0 = kwargs.get('y0', 0)
    shape1 = monkey.segment(0, 0, w * 8, 0)
    node.add_component(monkey.platform())
    node.add_component(monkey.collider(shape1, settings.flags.platform_passthrough, 0, settings.tags.platform))
    points = kwargs['points']
    pts = dict()
    for i in range(0, len(points), 3):
        pts[points[i]] = monkey.vec2(points[i+1] * 8, points[i+2] * 8)
        print(pts)
    node.add_component(monkey.move_translate(points=pts))
    desc = kwargs.get('desc')
    model = kwargs.get('model')
    # if desc is provided build a model
    if desc:
        if desc not in cache:
            cache[desc] = monkey.models.tiled(desc=desc, x=x0,y=y0)
        node.set_model(cache[desc])
    elif model:
        node.set_model(monkey.get_tiled(model))
    return node


# unified
def tiled2(**kwargs):
    node = monkey.Node()

    # if width is provided --> a rectangular platform is added
    w = kwargs.get('w')
    h = kwargs.get('h')
    if w:
        if h is None:
            print('called tiled2 with width but no height!')
            exit(1)
        shape1 = monkey.rect(8 * w, 8 * h)
        node.add_component(monkey.collider(shape1, settings.flags.platform, 0, settings.tags.platform))
    pos = kwargs.get('pos', (0, 0))
    z = kwargs.get('z', 0)
    desc = kwargs.get('desc')
    model = kwargs.get('model')
    # if desc is provided build a model
    if desc:
        if desc not in cache:
            cache[desc] = monkey.models.tiled(desc=desc)
        node.set_model(cache[desc])
    elif model:
        node.set_model(monkey.get_tiled(model))
    node.set_position(pos[0] * 8, pos[1] * 8, z)
    return node

# TODO remove
# def platform(desc, **kwargs):
#     node = monkey.Node()
#     if desc:
#         if desc not in cache:
#             cache[desc] = monkey.models.tiled(desc)
#         node.set_model(cache[desc])
#     w = kwargs.get('w')
#     h = kwargs.get('h')
#     pos = kwargs.get('pos', (0, 0))
#     if w:
#         shape1 = monkey.rect(8 * w, 8 * h)
#         node.add_component(monkey.collider(shape1, settings.flags.platform, 0, settings.tags.platform))
#     node.set_position(pos[0] * 8, pos[1] * 8, 1)
#     return node

def line_platform(x, y, length, passthrough=True):
    node = monkey.Node()
    shape1 = monkey.segment(0,0,length*8,0)
    node.set_position(x*8,y*8,0)
    node.add_component(monkey.collider(shape1, settings.flags.platform_passthrough if passthrough else settings.flags.platform, 0, settings.tags.platform))
    return node



def change_state(id, state):
    def f():
        if settings.mario_state > 0:
            monkey.get_node(id).set_state(state)
    return f


def check_door():
    if settings.current_door:
        monkey.get_node(settings.ids.player).set_state('knock')
        s = monkey.script()
        door_id = settings.current_door[0]
        door = monkey.get_node(door_id)
        ii = s.add(monkey.actions.animate(id=settings.ids.player, anim='knock', sync=True))
        ii = s.add(monkey.actions.animate(id=settings.current_door[0], anim='open'), ii)
        ii = s.add(actions.change_room(door.user_data["world"]), ii)
        settings.current_door = None
        monkey.play(s)



def player(cam, x, y):
    node = monkey.Node()
    node.add_component(monkey.sprite_collider(settings.flags.player, settings.flags.foe, settings.tags.player,
                                              cast_mask=settings.flags.foe, cast_tag=settings.tags.player_attack))
    sta = settings.mario_states[settings.mario_state]
    node.add_component(monkey.controller_2d(size=sta['size'], center=sta['center']))
    node.add_component(monkey.dynamics())
    node.set_position(x * 8, y * 8, 0)
    node.set_model(monkey.get_sprite(sta['model']))
    sm = monkey.state_machine()
    sm.add(monkey.walk_2d_player("pango",
                                 speed=settings.mario_speed,
                                 gravity=settings.gravity,
                                 jump_height=80,
                                 time_to_jump_apex=0.5,
                                 keys={
                                     65: change_state(node.id, 'attack1'),
                                     264: check_door
                                 }))
    sm.add(monkey.attack("attack1", anims=['attack1'], speed=settings.mario_speed, gravity=settings.gravity, exit_state='pango'))
    sm.add(monkey.walk_2d_auto("auto", speed=settings.mario_speed, gravity=settings.gravity, jump_height=80, time_to_jump_apex=0.5))
    sm.add(monkey.idle("dead", "dead"))
    sm.add(monkey.idle("knock", "knock"))
    sm.add(monkey.idle("enter", "enter"))
    sm.set_initial_state("pango")
    node.add_component(sm)
    node.add_component(monkey.follow(cam, (0, 0, 5), (0, 1, 0)))
    return node


def on_collect(id):
    monkey.get_node(id).remove()

def on_hit(id):
    c = monkey.get_node(id)
    s = monkey.script()
    ii = s.add(monkey.actions.delay(1))
    ii = s.add(monkey.actions.remove(id=id), ii)
    ii = s.add(monkey.actions.add(node=coin(c.x/8.0, c.y/8.0 + 1), id=settings.ids.game_node), ii)
    sid =  monkey.play(s)
    return sid

def sprite(x, y, z, model):
    node = monkey.Node()
    node.set_model(monkey.get_sprite(model))
    node.set_position(x * 8, y * 8, z)
    return node


def door(**kwargs):
    pos = kwargs.get('pos', (0, 0))
    model = kwargs.get('model', 'sprites/door')
    anim = kwargs.get('anim')
    world = kwargs.get('world')
    tag = kwargs.get('tag', settings.tags.door)
    #x, y, world, anim='closed'):
    node = monkey.Node()
    node.set_model(monkey.get_sprite(model))
    node.set_position(pos[0] * 8, pos[1] * 8, -0.08)
    if anim != 'barred':
        shape = monkey.rect(8, 16, ox=12)
        node.add_component(monkey.collider(shape, settings.flags.foe, settings.flags.player, tag))
        node.user_data = {'world': world}
    node.set_animation(anim)
    return node

def foe(**kwargs):  #x, y, model, flip, tag, speed):
    x = kwargs.get('x', 0)
    y = kwargs.get('y', 0)
    speed = kwargs.get('speed', 0)
    model = kwargs['model']         # required
    energy = kwargs.get('energy', 1)
    jump_anim = kwargs.get('jump_anim', 'jump')
    walk_anim = kwargs.get('walk_anim', 'walk')
    idle_anim = kwargs.get('idle_anim', 'idle')
    velocity = kwargs.get('velocity', monkey.vec3(0.0))
    dead = kwargs.get('dead', True)
    hflip = kwargs.get('hflip', True)
    script = kwargs.get('script', None)
    dir = kwargs.get('dir', -1)
    collision_tag =kwargs['tag']
    edge_flip = kwargs.get('flip_on_edge', False)
    node = monkey.Node()
    node.set_model(monkey.get_sprite(model))
    node.set_position(x * 8, y * 8, 0)
    sm = monkey.state_machine()
    sm.add(monkey.walk_2d_foe("walk", speed=speed, gravity=settings.gravity, jump_height=80, time_to_jump_apex=0.5,
                              jump_anim=jump_anim, idle_anim=idle_anim, flip=hflip, dir=dir, flip_on_edge=edge_flip))
    #if dead:
    sm.add(monkey.hit("hit", velocity=monkey.vec2(100,0), anim='hit', timeout=0.5, exit_state='walk'))
    sm.add(monkey.walk_2d_foe("dead", speed=0, gravity=settings.gravity, jump_height=80, time_to_jump_apex=0.5,
                             jump_anim='dead', walk_anim='dead', idle_anim='dead', flip=hflip, script=script))
    sm.set_initial_state('walk')
    node.add_component(sm)
    node.add_component(monkey.sprite_collider(settings.flags.foe, settings.flags.player, collision_tag))
    node.add_component(monkey.controller_2d(size=(10, 10, 0), center=(5, 0, 0)))
    node.add_component(monkey.dynamics(velocity=velocity))
    node.user_data= {'energy': energy}
    return node

def snake(x, y):
    return foe(x=x, y=y, model='sprites/snake', tag=settings.tags.snake, script=on_hit, jump_anim='walk', idle_anim='walk')

def cobra(x, y):
    return foe(x=x, y=y, model='sprites/snake2', tag=settings.tags.snake, script=on_hit, jump_anim='walk', speed=50,
               idle_anim='walk', flip_on_edge=True, energy=3)

def coin(x, y):
    return foe(x=x, y=y, model='sprites/coin', tag=settings.tags.coin, jump_anim='default', walk_anim='default',
               idle_anim='fall', velocity=monkey.vec3(0, 200, 0))



def common_room(world_width, world_height):
    room = monkey.Room("wbml")
    ce = monkey.collision_engine(80, 80)
    ce.add_response(settings.tags.player_attack, settings.tags.snake, on_start=func.hit_snake)
    ce.add_response(settings.tags.player, settings.tags.coin, on_start=func.collect)
    ce.add_response(settings.tags.player, settings.tags.door, on_start=func.on_enter_door, on_end=func.on_leave_door)
    ce.add_response(settings.tags.player, settings.tags.gate, on_start=func.on_enter_gate)
    # ce.add_response(tags.player, tags.powerup, on_start=functions.hit_powerup)
    # ce.add_response(tags.player, tags.goomba, on_start=functions.hit_goomba)
    # ce.add_response(tags.player, tags.koopa, on_start=functions.hit_koopa)
    # ce.add_response(tags.player, tags.hotspot, on_start=functions.hit_hotspot, on_end=functions.leave_hotspot)
    # ce.add_response(tags.goomba, tags.koopa, on_start=functions.hit_gk)
    # ce.add_response(tags.goomba, tags.fire, on_start=functions.fire_hit_foe)
    room.add_runner(ce)
    room.add_runner(monkey.scheduler())

    root = room.root()
    kb = monkey.keyboard()
    kb.add(299, 1, 0, func.restart)
    root.add_component(kb)


    # create camera
    device_size = settings.device_size
    device_width = device_size[0]
    device_height = device_size[1]
    device_half_width = device_width // 2
    device_half_height = device_height // 2

    # ui stuff
    ui_node = monkey.Node()
    ui_cam = monkey.camera_ortho(device_width, device_height, viewport=[0, 0, 256, 224])
    ui_cam.set_bounds(device_half_width, device_half_width, device_half_height, device_half_height, -100, 100)
    ui_node.set_camera(ui_cam)
    root.add(ui_node)

    #cam_node.add(ui_box(6, 180, 'LIFE', 1))
    #    ui_node.add(pixels(points=[6, 184]))
    #cam_node.add(line(a=(0,0), b=(100,100)))
    ui_node.add(rect(0, 0, -1, size=(256, 224), color=monkey.vec4(112, 112, 112, 255)))
    ui_node.add(rect2(8, 120, 40, 24))
    ui_node.add(rect2(8, 24, 40, 32))
    ui_node.add(rect2(56, 8, 192, 192))
    ui_node.add(rect2(17, 97, 14, 14, bg=monkey.vec4(81,81,81,255)))
    ui_node.add(rect2(33, 97, 14, 14, bg=monkey.vec4(81,81,81,255)))
    ui_node.add(rect2(17, 81, 14, 14, bg=monkey.vec4(81,81,81,255)))
    ui_node.add(rect2(33, 81, 14, 14, bg=monkey.vec4(81,81,81,255)))
    ui_node.add(rect2(17, 65, 14, 14, bg=monkey.vec4(81,81,81,255)))
    ui_node.add(rect2(33, 65, 14, 14, bg=monkey.vec4(81,81,81,255)))

    ui_node.add(rect3(7, 150, 42, 20))
    ui_node.add(rect3(7, 182, 42, 20))
    ui_node.add(rect3(7, 206, 66, 20))
    ui_node.add(rect3(95, 206, 66, 20))
    ui_node.add(rect3(6, 6, 42, 12))

    ui_node.add(text(1.5,24,1,'LIFE',monkey.HALIGN_LEFT,1))
    ui_node.add(text(1.5,20,1,'GOLD',monkey.HALIGN_LEFT,2))
    ui_node.add(text(6,19,1,str(settings.gold),monkey.HALIGN_RIGHT,5))
    # main stuff
    game_node = monkey.Node()
    game_cam = monkey.camera_ortho(192, 192, viewport=[56, 8, 192, 192])
    game_cam.set_bounds(192 // 2, world_width - 192 // 2, 192 // 2, world_height - 192 // 2, -100, 100)
    game_node.set_camera(game_cam)
    root.add(game_node)
    settings.ids.game_node = game_node.id
    return room, game_node
