import monkey_toolkit
import monkey
from . import settings
#from rooms.chars import get_character




from .actions import *


platform_types = {
    'line': monkey_toolkit.platformer.PlatformType.LINE,
    'solid': monkey_toolkit.platformer.PlatformType.SOLID,
    'none': monkey_toolkit.platformer.PlatformType.NONE
}

def trunk_hor(**kwargs):
    w = kwargs['width']
    ts = settings.tile_size[0]
    z = kwargs.get('z', 0)
    pal =kwargs.get('pal', 0)
    node = monkey.Node()
    b = monkey.models.quad(settings.main_batch, frames=[
        {
            'quads': [
                {'size': (ts, ts), 'tex_coords': [144,32,16,16], 'repeat': [1, 1], 'palette': pal},
                {'size': ((w-2)*ts, ts), 'tex_coords': [160, 32, 16, 16], 'repeat': [w-2, 1], 'palette': pal, 'pos': [ts, 0]},
                {'size': (ts, ts), 'tex_coords': [176, 32, 16, 16], 'repeat': [1, 1], 'palette': pal, 'pos': [(w-1)*ts, 0]}
            ]
        }])
    node.set_model(b)
    pos = kwargs['pos']
    node.set_position(pos[0]*ts, pos[1]*ts, z)
    shape = monkey.rect(w * ts, ts)
    node.add_component(monkey.collider(shape, 2, 0, 2))
    return node


def trunk_vert(**kwargs):
    h = kwargs['height']
    ts = settings.tile_size[0]
    z = kwargs.get('z', 0)
    pal =kwargs.get('pal', 0)
    node = monkey.Node()
    b = monkey.models.quad(settings.main_batch, frames=[
        {
            'quads': [
                {
                    'size': (ts, (h - 1) * ts),
                    'tex_coords': [128, 48, 16, 16],
                    'repeat': (1, h-1),
                    'palette': pal
                },
                {
                    'size': (ts, ts),
                    'tex_coords': [128, 32, 16, 16],
                    'repeat': (1, 1),
                    'palette': pal,
                    'pos': [0, (h-1)*ts]
                }
            ]
        }])
    node.set_model(b)
    pos = kwargs['pos']
    node.set_position(pos[0]*ts, pos[1]*ts, z)
    shape = monkey.rect(ts, h * ts)
    node.add_component(monkey.collider(shape, 2, 0, 2))
    return node


def wfalls_frame(w, h, pal, tbody0, tbody1, ttop0, ttop1):
    return {
        'ticks': 10,
        'quads': [
            {
                'size': [w * 8, (h-1) * 8],
                'tex_coords': [tbody0, tbody1, 8, 8],
                'repeat': [w, h-1],
                'palette': pal,
            },
            {
                'size': [w * 8, 8],
                'tex_coords': [ttop0, ttop1, 8, 8],
                'repeat': [w, 1],
                'palette': pal,
                'pos': [0, (h-1) * 8]
            }
        ]
    }


def wfalls(**kwargs):
    node = monkey.Node()
    size = kwargs['size']
    w = size[0]
    h = size[1]
    z = kwargs.get('z', 0)
    pos = kwargs['pos']
    pal = 0
    tpf = 10
    ts = settings.tile_size[0]
    b = monkey.models.quad(settings.main_batch, frames=[
        wfalls_frame(w, h, pal, 0, 120, 0, 112),
        wfalls_frame(w, h, pal, 8, 120, 8, 112),
        wfalls_frame(w, h, pal, 16, 120, 16, 112),
        wfalls_frame(w, h, pal, 24, 120, 24, 112),
        wfalls_frame(w, h, pal, 0, 120, 0, 128),
        wfalls_frame(w, h, pal, 8, 120, 8, 128),
        wfalls_frame(w, h, pal, 16, 120, 16, 128),
        wfalls_frame(w, h, pal, 24, 120, 16, 128)
    ])

    #     {
    #         'ticks': tpf,
    #         'quads': [
    #             {
    #                 'size': (w * 8, (h-1) * 8),
    #                 'tex_coords': [0, 120, 8, 8],
    #                 'repeat': (w, h-1),
    #                 'palette': pal,
    #             }
    #         ]
    #     },
    #     {
    #         'ticks': tpf,
    #         'quads': [
    #             {
    #                 'size': (w * 8, (h-1) * 8),
    #                 'tex_coords': [8, 120, 8, 8],
    #                 'repeat': (w, h - 1),
    #                 'palette': pal,
    #
    #             }
    #         ]
    #     },
    #     {
    #         'ticks': tpf,
    #         'quads': [
    #             {
    #                 'size': (w * 8, (h - 1) * 8),
    #                 'tex_coords': [16, 120, 8, 8],
    #                 'repeat': (w, h - 1),
    #                 'palette': pal,
    #
    #             }
    #         ]
    #     },
    #     {
    #         'ticks': tpf,
    #         'quads': [
    #             {
    #                 'size': (w * 8, (h - 1) * 8),
    #                 'tex_coords': [24, 120, 8, 8],
    #                 'repeat': (w, h - 1),
    #                 'palette': pal,
    #
    #             }
    #         ]
    #     },
    #
    # ])
    node.set_position(pos[0] * ts, pos[1] * ts, z)
    node.set_model(b)
    return node

def moving_platform(**kwargs):
    quads0 = []
    quads1 = []
    w = kwargs['width']
    pal = kwargs.get('pal', 0)
    ts = settings.tile_size[0]
    if w == 1:
        quads0.append({'size': (ts, ts), 'tex_coords': kwargs.get('mid'), 'repeat': (1, 1), 'palette': pal})
        quads1.append({'size': (ts, ts), 'tex_coords': kwargs.get('mid'), 'repeat': (1, 1), 'palette': pal, 'flipv': True})
    else:
        if w > 1:
            quads0.append({'size': (ts, ts), 'tex_coords': kwargs.get('left'), 'repeat': (1, 1), 'palette': pal})
            quads0.append({'size': (ts, ts), 'tex_coords': kwargs.get('right'), 'repeat': (1, 1), 'palette': pal, 'pos': ((w-1)*ts, 0)})
            quads1.append({'size': (ts, ts), 'tex_coords': kwargs.get('left'), 'repeat': (1, 1), 'palette': pal,'flipv': True})
            quads1.append({'size': (ts, ts), 'tex_coords': kwargs.get('right'), 'repeat': (1, 1), 'palette': pal,'flipv': True, 'pos': ((w - 1) * ts, 0)})
        if w > 2:
            quads0.append({'size': ((w-2)*ts, ts), 'tex_coords': kwargs.get('mid'), 'repeat': (w-2, 1), 'palette': pal})
            quads1.append({'size': ((w - 2) * ts, ts), 'tex_coords': kwargs.get('mid'), 'repeat': (w - 2, 1), 'palette': pal, 'flipv': True})

    model = monkey.models.quad(settings.main_batch, frames=[
        {'quads': quads0, 'ticks': 10},
        {'quads': quads1, 'ticks': 10}
    ])
    return monkey_toolkit.platformer.moving_platform(settings.main_batch, **dict(kwargs, model=model))


def platform(**kwargs):
    #pos = kwargs['pos']
    #size = kwargs['size']
    tile = kwargs.get('tile')
    if tile is not None:
        tile = settings.tiles[tile]
    #pal = kwargs.get('pal', 0)
    #z = kwargs.get('z', 0)
    return monkey_toolkit.platformer.platform(settings.main_batch, **dict(kwargs, tile=tile))# pos[0], pos[1], size[0], size[1], tile, z)


def platform_border(**kwargs):
    pos = kwargs['pos']
    size = kwargs['size']
    tile = settings.multi_tiles[kwargs['multi_tile']]
    pal = kwargs.get('pal', 0)
    z = kwargs.get('z', 0)
    print(tile)

    platform_type = platform_types[kwargs['platform']]
    return monkey_toolkit.platformer.platform_border(settings.main_batch, pos[0], pos[1], size[0], size[1], tile, pal=pal, z=z, platform_type=platform_type)


def _column(**kwargs):
    height = kwargs.get('height')
    pos = kwargs.get('pos')
    ts = settings.tile_size[0]
    z = kwargs.get('z', 0)
    b = monkey.models.quad(settings.main_batch, frames=[
        {
            'quads': [
                {
                    'size': (ts, (height - 1) * ts),
                    'tex_coords': kwargs['tile_0'],
                    'repeat': (1, height - 1),
                    'palette': 0
                },
                {
                    'size': (ts, ts),
                    'tex_coords': kwargs['tile_1'],
                    'repeat': (1, 1),
                    'palette': 0,
                    'pos': [0, (height - 1) * ts]
                }
            ]
        }
    ])
    node = monkey.Node()
    node.set_model(b)
    node.set_position(pos[0] * ts, pos[1] * ts, z)
    return node


def tree(**kwargs):
    return _column(**dict(kwargs, tile_0=[80, 48, 16, 16], tile_1=[80,32, 16, 16], z=-0.05))







def stairs(**kwargs):
    pos = kwargs.get('pos')
    h = kwargs.get('height')
    z = kwargs.get('z', 0)
    ts = settings.tile_size[0]
    b = monkey.models.quad(settings.main_batch, frames=[
        {
            'ticks': 5,
            'quads': [
                {

                    'size': (ts, (h - 1) * ts),
                    'tex_coords': [96, 48, 16, 16],
                    'repeat': (1, h-1),
                    'palette': 0
                },
                {

                    'size': (ts, ts),
                    'tex_coords': [80, 32, 16, 16],
                    'repeat': (1, 1),
                    'palette': 0,
                    'pos': [0, (h-1) * ts]
                }
            ]
        },
        {
            'ticks': 5,
            'quads': [
                {
                    'size': (ts, (h - 1) * ts),
                    'tex_coords': [112, 48, 16, 16],
                    'repeat': (1, h - 1),
                    'palette': 0
                },
                {
                    'size': (ts, ts),
                    'tex_coords': [80, 32, 16, 16],
                    'repeat': (1, 1),
                    'palette': 0,
                    'pos': [0, (h - 1) * ts]
                }
            ]
        },

    ])
    node = monkey.Node()
    node.set_model(b)
    shape = monkey.aabb(0, ts, 0, h * ts)
    node.add_component(monkey.collider(shape, settings.Flags.foe, settings.Flags.player, settings.Tags.ladder))
    node.set_position(pos[0] * ts, pos[1] * ts, z)

    ls = monkey.Node()
    shape2 = monkey.segment(0, (h-1) * ts, ts, (h-1)*ts)
    ls.add_component(monkey.collider(shape2, 1 << 6, settings.Flags.player, 0))
    node.add(ls)
    return node



def vine(x, y, h, pal=None, z=-1):
    t = 10
    desc = [
        ('W,1,R,' + str(h) + ',6,3,E,5,2', t),
        ('W,1,R,' + str(h) + ',7,3,E,5,2', t),
    ]
    model = monkey_toolkit.anim_tiled_model('smb2', desc, pal)

    return monkey_toolkit.stairs(x, y, 1, h, model=model)

    #return monkey_toolkit.tiled(x, y, monkey_toolkit.anim_tiled_model('smb2', desc, pal), z=z)


def make_character(x, y, id, **kwargs):
    char_info = get_character(id)
    args = char_info['args']
    func = char_info['factory']
    return func(x, y, args, **kwargs)


def player(**kwargs):
    id = settings.mario_states[settings.mario_state]
    wkeys = [
        (settings.Keys.FIRE, pickup_shoot),
        (settings.Keys.UP, on_key_up)]
        #(settings.Keys.UP, monkey_toolkit.Action.enter_door)]
    return smb2(**dict(kwargs, model='sprites2/supermario', size=(10, 14, 0), speed=300, walk_keys=wkeys, pal=0, jump_height=80))
    #return make_character(x, y, id, walk_keys=wkeys, climb=True, player=True)



def smb2(**kwargs):
    player = monkey_toolkit.character(settings.main_batch, **dict(kwargs, player=True, controller_mask_down=monkey_toolkit.flags.platform |
        monkey_toolkit.flags.platform_passthrough | settings.Flags.foe_platform, climb=True)) # walk_keys=wkeys, climb=True)
    sm = player.get_state_machine()
    sm.add(monkey.idle("lift", "lift", exit_on_complete=True, exit_state='walk_item'))
    sm.add(monkey.idle("enter_door", "idle"))
    # walk + carry
    sm.add(monkey.walk_2d_player("walk_item", speed=kwargs['speed'], gravity=settings.gravity, jump_height=80, time_to_jump_apex=0.5,
        walk_anim='walk_item', idle_anim='idle_item', keys={68: pickup_shoot}))
    sm.add(monkey.idle("dead", "dead"))
    return player


def smb2_item(**kwargs):
    foe = monkey_toolkit.character(settings.main_batch, **kwargs)  # 5, 2, 'shyguy')
    foe.user_data = {'shoot_item': kwargs['shoot_item'], 'bounce': False}
    #sm = foe.get_state_machine()
    #sm.add(monkey.idle("lifted", "up"))
    #sm.add(monkey.bounce("bounce", gravity=settings.gravity, check_walls=False, on_bounce_y=bounce, bounce_velocity=[150], speed=200,
    #                     collision_mask = monkey_toolkit.flags.foe, collision_flag= monkey_toolkit.flags.player_hit, collision_tag=monkey_toolkit.tags.player_attack))
    return foe

# makes a generic foe from x, y, and id
#def make_foe(x, y, id):


def bonus(**kwargs):
    node = monkey_toolkit.sprite(settings.main_batch, **kwargs)
    return node


def boulder(**kwargs):
    ts = settings.tile_size
    node = monkey_toolkit.sprite(settings.main_batch, **kwargs)
    shape = monkey.rect(ts[0], ts[1], ox=-ts[0]*0.5)
    node.add_component(monkey.collider(shape, settings.Flags.platform, 0, 0))

    sensor = monkey.Node()
    sensor.set_position(2, 15, 0)
    sh = monkey.aabb(-6, 6, 0, 2)
    sensor.add_component(monkey.collider(sh, monkey_toolkit.flags.foe, monkey_toolkit.flags.player, settings.Tags.foe_platform_sensor))
    node2 = monkey.Node()
    node2.add(sensor)
    node.add(node2)
    node.user_data = {
        'shoot_item': {
            'model': kwargs.get('model'),
            'bounce_on_walls': True,
            'bounce_callback': cippo,
            'pal': kwargs.get('pal', 0)
        },
        'bounce': True,

    }
    return node


def tweeter(**kwargs):
    left = kwargs.get('left', True)
    size = kwargs.get('size', [10, 14, 0])
    node = monkey_toolkit.sprite(settings.main_batch, **kwargs)
    node.user_data = {
        'shoot_item': {
            'model': kwargs.get('model') + '_item',
            'bounce_on_walls': True,
            'bounce_callback': bounce,
            'pal': kwargs.get('pal', 0)
        },
        'bounce': True,
        'foe_item': [tweeter, dict(**kwargs)]
    }
    sm = monkey.state_machine()
    flip = kwargs.get('flip', True)
    flip_on_edge = kwargs.get('flip_on_edge', True)
    sm.add(monkey.bounce("walk", gravity=settings.gravity, check_walls=True, bounce_velocity=[50, 50, 50, 100], left=left,
        speed=kwargs['speed'], flip=flip, flip_on_edge=flip_on_edge))
    sm.add(monkey.idle("dead", "dead"))
    sm.set_initial_state('walk')#, velocity=(50, 0, 0))
    node.add_component(sm)
    node.add_component(monkey.sprite_collider(monkey_toolkit.flags.foe, monkey_toolkit.flags.player, kwargs['tag']))
    node.add_component(monkey.controller_2d(size=size, center=kwargs.get('center', None)))
    node.add_component(monkey.dynamics())
    add_platform_to_foe(node)

    # platform = monkey.Node()
    # shape1 = monkey.segment(-8, 16, 8, 16)
    # platform.add_component(monkey.collider(shape1, monkey_toolkit.flags.platform_passthrough, 0, monkey_toolkit.tags.platform))
    # platform.add_component(monkey.platform())
    # psensor = monkey.Node()
    # psensor.set_position(0, 16, 0)
    # sh =  monkey.aabb(0, 2, 0, 16)
    # psensor.add_component(monkey.collider(sh, monkey_toolkit.flags.foe, monkey_toolkit.flags.player, settings.Tags.foe_platform_sensor))
    # platform.add(psensor)
    # node.add(platform)
    return node

def add_platform_to_foe(foe):
    platform = monkey.Node()
    shape1 = monkey.segment(-8, 16, 8, 16)
    platform.add_component(monkey.collider(shape1, settings.Flags.foe_platform, 0, monkey_toolkit.tags.platform))
    platform.add_component(monkey.platform())
    psensor = monkey.Node()
    psensor.set_position(0, 16, 0)
    sh =  monkey.aabb(0, 2, 0, 16)
    psensor.add_component(monkey.collider(sh, monkey_toolkit.flags.foe, monkey_toolkit.flags.player, settings.Tags.foe_platform_sensor))
    platform.add(psensor)
    foe.add(platform)


def hoopster(x, y, args, **kwargs):
    node = monkey_toolkit.sprite(x, y, 'sprites2/hoopster')
    sp = monkey.script_player()
    script = monkey.script()
    script.add(monkey.actions.move_by(id=node.id, y=32, t=1), loop=True)
    script.add(monkey.actions.animate(id=node.id, anim='down'))
    script.add(monkey.actions.move_by(id=node.id, y=-32, t=1))
    script.add(monkey.actions.animate(id=node.id, anim='up'))
    sp.play(script)
    node.add_component(sp)
    node.add_component(monkey.sprite_collider(monkey_toolkit.flags.foe, monkey_toolkit.flags.player, settings.Tags.generic_foe))

    return node


def ninji(x, y, args, **kwargs):
    ts = settings.tile_size
    node = monkey.Node()
    node.set_model(monkey.get_sprite('sprites2/ninji'))
    z = kwargs.get('z', 0)
    node.set_position(ts[0] * x, ts[1] * y, z)
    coll_flag = monkey_toolkit.flags.foe
    coll_mask = monkey_toolkit.flags.player
    coll_tag = settings.Tags.generic_foe
    node.add_component(monkey.sprite_collider(coll_flag, coll_mask, coll_tag))
    node.add_component(monkey.controller_2d(size=args['size'], center=args.get('center', None)))
    node.add_component(monkey.dynamics())
    sp = monkey.script_player()
    script = monkey.script()
    script.add(monkey.actions.move_dynamics(id=node.id, velocity=(0, 200, 0), acceleration=(0, -settings.gravity, 0)), loop=True)
    script.add(monkey.actions.animate(id=node.id, anim='idle'))
    script.add(monkey.actions.delay(0.1))
    script.add(monkey.actions.animate(id=node.id, anim='jump'))
    sp.play(script)
    node.add_component(sp)
    add_platform_to_foe(node)
    node.user_data = {'shoot_item': args['shoot_item'], 'bounce': True, 'foe_item': args.get('foe_item')}
    return node


def veg(**kwargs):
    return smb2_item(**dict(kwargs, tag=settings.Tags.collectible_item, speed=0, size=[8,8,0], walk_anim='idle',
                                            jump_anim='idle', flip=False))


def smb2_foe(**kwargs):
    foe = monkey_toolkit.character(settings.main_batch, **kwargs)
    foe.user_data = {
        'shoot_item': {
            'model': kwargs.get('model') + '_item',
            'bounce_on_walls': True,
            'bounce_callback': bounce,
            'pal': kwargs.get('pal', 0)
        },
        'bounce': True,
        'foe_item': [smb2_foe, dict(**kwargs)]
    }

    #collider = foe.get_sprite_collider()
    #collider.set_override('up', 0, 0, 0)
    sm = foe.get_state_machine()
    sm.add(monkey.idle("dead", "dead"))
    # sm.add(monkey.bounce("bounce", gravity=settings.gravity, check_walls=True, on_bounce_y=bounce, bounce_velocity=[150], speed=200,
    #                      collision_mask = monkey_toolkit.flags.foe, collision_flag= monkey_toolkit.flags.player_hit, collision_tag=monkey_toolkit.tags.player_attack))
    # platform = monkey.Node()
    # shape1 = monkey.segment(-8, 16, 8, 16)
    # platform.add_component(monkey.collider(shape1, monkey_toolkit.flags.platform_passthrough, 0, monkey_toolkit.tags.platform))
    # platform.add_component(monkey.platform())
    # psensor = monkey.Node()
    # psensor.set_position(0, 16, 0)
    # sh =  monkey.aabb(0, 2, 0, 16)
    # psensor.add_component(monkey.collider(sh, monkey_toolkit.flags.foe, monkey_toolkit.flags.player, settings.Tags.foe_platform_sensor))
    # platform.add(psensor)
    # foe.add(platform)
    # ADD BACK!!!
    add_platform_to_foe(foe)
    return foe


# def waterfalls(x, y, w, h, pal=None, z=-1):
#     t = 5
#     fmt = "W," + str(w) + ",R," + str(w*(h-1)) + ",{0},1,E,R," + str(w) +",{1},{2},E"
#     desc = [
#         (fmt.format(0, 0, 0), t),
#         (fmt.format(1, 1, 0), t),
#         (fmt.format(2, 2, 0), t),
#         (fmt.format(3, 3, 0), t),
#         (fmt.format(0, 0, 2), t),
#         (fmt.format(1, 1, 2), t),
#         (fmt.format(2, 2, 2), t),
#         (fmt.format(3, 2, 2), t)
#     ]
#     return monkey_toolkit.tiled(x, y, monkey_toolkit.anim_tiled_model('wfalls', desc, pal), z=z)


def door(**kwargs): #x, y, width, height, world, **kwargs):
    pos = kwargs['pos']
    # destination world
    world = kwargs['world']
    start_pos = kwargs['start_position']
    # door might have a model
    model = kwargs.get('model', None)
    z = kwargs.get('z', 0)
    ts = settings.tile_size[0]
    node = monkey.Node()
    shape = monkey.aabb(0, ts, 0, 2 * ts)
    node.add_component(monkey.collider(shape, settings.Flags.foe, settings.Flags.player, settings.Tags.door))
    node.set_position(pos[0] * ts, pos[1] * ts, z)
    node.user_data = {'world': world, 'start_position': start_pos, 'has_sprite': model is not None}
    if model:
        m = monkey.get_sprite(settings.main_batch, model)
        node.set_model(m)
    return node

