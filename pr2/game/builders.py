import yaml
import monkey
import monkey_toolkit
import monkey_toolkit.platformer
from . import settings
from . import actions
from . import factories
from . import facmap

collision_response = [
    monkey_toolkit.globals.CollisionResponse(monkey_toolkit.tags.player, settings.Tags.collectible_item,
        on_start=actions.enable_pickup, on_end=actions.disable_pickup),
    monkey_toolkit.globals.CollisionResponse(monkey_toolkit.tags.player_attack, settings.Tags.generic_foe,
        on_start=actions.foe_is_hit),
    monkey_toolkit.globals.CollisionResponse(monkey_toolkit.tags.player, settings.Tags.foe_platform_sensor,
        on_start=actions.enable_pickup_platform, on_end=actions.disable_pickup_platform),
    monkey_toolkit.globals.CollisionResponse(monkey_toolkit.tags.player, settings.Tags.ladder,
        on_start=actions.enable_stairs, on_end=actions.disable_stairs)

]


def world_1_1a():
    b = monkey_toolkit.platformer_toolkit(settings)
    room, cam, cam_node = b.platformer_room(3584, 256)

    cam_node.add(b.platform(69, 2, 0, 0, sheet='main', tile=(15, 7)))
    cam_node.add(b.player('mario', cam, 3, 3))
    print('sucalo2')
    return room





def smb2_world_1_1c():
    settings.on_restart = actions.on_restart
    monkey_toolkit.initialize(settings)
    room, cam, cam_node = monkey_toolkit.platformer_room(768, 480)
    cam_node.add(monkey_toolkit.tiled(0, 0, monkey_toolkit.tiled_model('smb2', 'W,20,R,340,14,4,E'), size=(20,17), z=0))
    cam_node.add(monkey_toolkit.tiled(24, 0, monkey_toolkit.tiled_model('smb2', 'W,24,R,48,14,4,E'), size=(24,2), z=0))
    cam_node.add(monkey_toolkit.tiled(24, 2, monkey_toolkit.tiled_model('smb2', 'W,3,R,9,14,4,E'), size=(3,3), z=0))
    cam_node.add(monkey_toolkit.tiled(37, 2, monkey_toolkit.tiled_model('smb2', 'W,11,R,110,14,4,E'), size=(11,10), z=0))
    cam_node.add(monkey_toolkit.tiled(25, 12, monkey_toolkit.tiled_model('smb2', 'W,23,R,115,14,4,E'), size=(23,5), z=0))
    start_pos = settings.start_positions[settings.room][settings.start_position]
    p0 = start_pos['pos']
    right = start_pos.get('right', True)
    player = factories.player(p0[0], p0[1])
    if not right:
        player.flip_x = True
    cam_node.add(player)
    return room

def prova_sprite():
    room = monkey.Room("mario")
    device_size = settings.device_size
    device_width = device_size[0]
    device_height = device_size[1]
    device_half_width = device_width // 2
    device_half_height = device_height // 2

    # setting the main cam
    cam_node = monkey.Node()
    #state.cn = cam_node.id
    cam = monkey.camera_ortho(device_width, device_height)
    cam.set_bounds(device_half_width, device_width - device_half_width, device_half_height, device_height - device_half_height, -100, 100)
    cam_node.set_camera(cam)
    room.set_main_cam(cam)
    root = room.root()
    root.add(cam_node)
    #state.main_cam = cam
    x=0
    y=0
    n = monkey.Node()
    n.set_model(monkey.get_sprite('sprites2/mario'))
    n.set_position(0,0,1)
    cam_node.add(n)
    for i in range(0, 2000):
        node = monkey.Node()
        node.set_model(monkey.get_sprite('sprites2/shyguy'))
        node.set_position(x, y, 0)
        x += 4
        if x > 320:
            x = 0
            y += 4
        cam_node.add(node)

    return room






def ciao():
    with open("game/worlds/1_1.yaml", "r") as stream:
        monkey_toolkit.globals.tile_size = (16, 16)
        monkey_toolkit.globals.device_size = settings.device_size
        monkey_toolkit.globals.gravity = settings.gravity
        monkey_toolkit.globals.reference_cam = settings.main_cam
        settings.on_restart = actions.on_restart
        try:
            data = yaml.safe_load(stream)
            world = data['world']
            world_size = world['size']
            room = monkey_toolkit.platformer_room(world_size[0], world_size[1], collision=collision_response)
            room.set_main_cam(settings.main_cam)
            root = room.root()
            for d in world['desc']:
                cl = d['class']
                factory = facmap.factory_map[cl]
                for item in d['items']:
                    clones = len(item['pos']) // 2
                    for i in range(0, clones):
                        #** dict(kwargs,
                        root.add(factory(**dict(item, pos=[item['pos'][2*i], item['pos'][2*i+1]])))
            # add player (only if start is present)
            start_positions = world.get('start')
            print(start_positions)
            if start_positions:
                start_pos = start_positions[settings.start_position]
                p0 = start_pos['pos']
                right = start_pos.get('right', True)
                player = factories.player(pos=p0)
                settings.player_id = player.id
                if not right:
                    player.flip_x = True
                root.add(player)
        #
            #for i in range(0, 500):
            #    cam_node.add(monkey_toolkit.sprite(settings.main_batch, 3+i*0.1, 2, 'sprites2/shyguy'))
        #
        #     #cam_node.add(waterfalls(56, 0, 22, 12))
        #     #cam_node.add(factories.wfalls(size=[22,12], pos=[5,2], z=-0.1))
            return room
        #
        #
        #
        except yaml.YAMLError as exc:
            print(exc)

    # #monkey_toolkit.initialize(settings)
    # #b = monkey_toolkit.platformer_toolkit(settings, on_restart=on_restart)
    # monkey_toolkit.tags.shyguy = 100
    # #monkey_toolkit.flags.platform = 2
    # desc = {'sheet': 'smb2', 'left': (0, 3), 'bottom': (1, 3), 'right': (2, 3), 'top_left': (0, 2), 'top': (1, 2), 'top_right': (2, 2)}
    # start_pos = settings.start_positions[settings.room][settings.start_position]
    #
    #
    # qq = {
    #     'top_left': (0, 32, 16, 16),
    #     'top': (16, 32, 16, 16),
    #     'top_right': (32, 32, 16, 16),
    #     'left': (0, 48, 16, 16),
    #     'center': (16, 48, 16, 16),
    #     'right': (32, 48, 16, 16)
    # }
    # cam_node.add(monkey_toolkit.platformer.platform(0, 0, 54, 1, (96, 32, 16, 16), 0))
    # cam_node.add(monkey_toolkit.platformer.platform(0, 1, 54, 1, (64, 48, 16, 16), 0))
    # cam_node.add(monkey_toolkit.platformer.platform_border(0, 2, 3, 5, qq, 0, platform_type=monkey_toolkit.platformer.PlatformType.LINE,z=-0.1))
    # cam_node.add(monkey_toolkit.platformer.platform_border(26, 2, 6, 7, qq, 0,
    #                                                        platform_type=monkey_toolkit.platformer.PlatformType.LINE))
    # # a = monkey.Node()
    # # b = monkey.models.quad(batch=0, frames=[{'quads':[
    # #      {'size': (54 * 16, 16), 'tex_coords': (96, 32, 16, 16), 'repeat': (54, 1), 'palette': 0}
    # # ]}])
    # # shape = monkey.rect(54*16,16)
    # # a.add_component(monkey.collider(shape, 2, 0, 2))
    # # a.set_model(b)
    # # cam_node.add(a)
    #
    # a2 = monkey.Node()
    # b2 = monkey.models.quad(batch=0, frames=[{'quads':[
    #      {'size': (60 * 16, 16), 'tex_coords': (96, 32, 16, 16), 'repeat': (60, 1), 'palette': 0}
    # ]}])
    # shape2 = monkey.rect(60*16,16)
    # a2.set_position(-3*16,-16, 0)
    # a2.add_component(monkey.collider(shape2, 2, 0, 2))
    # a2.set_model(b2)
    # cam_node.add(a2)
    #
    #
    #
    # a1 = monkey.Node()
    # b1 = monkey.models.lines(batch=1, points=[0,0,0,64,64,64,64,0,16,0,16,48,48,48,48,16,32,16,32,32], color=[255,1,1,1])
    # #a1.set_position(0,16,0)
    # a1.set_model(b1)
    # cam_node.add(a1)
    #
    # veg1 = [(5, 2), (19, 2), (102, 2)]
    # #veg2 = [(8, 2), (15, 2), (27, 9), (28, 9), (29, 9)]
    # #cherries = [(36, 7), (48, 6), (95, 9), (102, 5), (106, 5)]
    # #for p in veg1:
    # #    cam_node.add(make_character(p[0] + 0.5, p[1], 'veggie', shoot_item='veg1'))
    # #for p in veg2:
    # #    cam_node.add(make_character(p[0] + 0.5, p[1], 'veggie', shoot_item='veg2'))
    #
    # return room


def smb2_world_1_1b():
    settings.on_restart = on_restart
    monkey_toolkit.initialize(settings)
    #b = monkey_toolkit.platformer_toolkit(settings, on_restart=on_restart)
    monkey_toolkit.tags.shyguy = 100
    #monkey_toolkit.flags.platform = 2
    desc = {'sheet': 'smb2', 'left': (0, 3), 'bottom': (1, 3), 'right': (2, 3), 'top_left': (0, 2), 'top': (1, 2), 'top_right': (2, 2)}
    room, cam, cam_node = monkey_toolkit.platformer_room(2560, 240)
    settings.collision_engine.add_response(monkey_toolkit.tags.player, settings.Tags.foe_platform_sensor,
                                           on_start=enable_pickup_platform, on_end=disable_pickup_platform)
    settings.collision_engine.add_response(monkey_toolkit.tags.player, settings.Tags.veggie,
                                           on_start=enable_pickup, on_end=disable_pickup)
    settings.collision_engine.add_response(monkey_toolkit.tags.player, settings.Tags.generic_foe, on_start=collision_player_foe)
    settings.collision_engine.add_response(monkey_toolkit.tags.player_attack, settings.Tags.generic_foe, on_start=foe_is_hit)
    settings.collision_engine.add_response(monkey_toolkit.tags.player, settings.Tags.generic_collectible,
                                           on_start=collect)
    cam_node.add(monkey_toolkit.tiled(7, 2, monkey_toolkit.tiled_model('smb2', 'W,1,R,4,5,3,E,5,2'), z=-0.1))
    cam_node.add(monkey_toolkit.tiled(9, 2, monkey_toolkit.tiled_model('smb2', 'W,1,R,5,5,3,E,5,2'), z=-0.1))
    cam_node.add(monkey_toolkit.tiled(0, 0, monkey_toolkit.tiled_model('smb2', 'W,54,R,54,6,2,E,R,54,4,3,E'), size=(54, 2), z=1))
    cam_node.add(monkey_toolkit.tiled(55, 9, monkey_toolkit.tiled_model('smb2', 'W,13,9,2,R,11,10,2,E,11,2'), size=(13, 1)))
    cam_node.add(monkey_toolkit.tiled(87, 0, monkey_toolkit.tiled_model('smb2', 'W,31,R,31,6,2,E,R,31,4,3,E'), size=(31,2)))
    cam_node.add(monkey_toolkit.tiled(122, 0, monkey_toolkit.tiled_model('smb2', 'W,53,R,53,6,2,E,R,53,4,3,E'), size=(53,2)))
    cam_node.add(monkey_toolkit.tiled(36, 2, monkey_toolkit.tiled_model('smb2', 'W,1,8,3,8,2'), size=(1, 2)))
    cam_node.add(monkey_toolkit.tiled(41, 2, monkey_toolkit.tiled_model('smb2', 'W,1,8,2'), size=(1, 1)))
    cam_node.add(monkey_toolkit.tiled(46, 2, monkey_toolkit.tiled_model('smb2', 'W,1,8,3,8,3,8,2'), size=(1, 3)))
    cam_node.add(monkey_toolkit.tiled(113,8, monkey_toolkit.tiled_model('smb2', 'W,5,R,4,0,3,R,4,1,3,E,E,0,2,R,4,1,2,E'), z=-2))
    cam_node.add(monkey_toolkit.tiled(122,8, monkey_toolkit.tiled_model('smb2', 'W,7,R,4,R,6,1,3,E,2,3,E,R,6,1,2,E,2,2'), z = -2))
    cam_node.add(monkey_toolkit.tiled(117, 2, monkey_toolkit.tiled_model('smb2', 'W,6,9,2,R,4,10,2,E,11,2'), size=(6, 1)))
    cam_node.add(monkey_toolkit.platform(-1, 0, 1, 16))
    cam_node.add(monkey_toolkit.platform(160, 0, 1, 16))
    # cam_node.add(b.platform(113, 13, 5, 0))
    # cam_node.add(b.platform(122, 13, 7, 0))
    #
    # # #cam_node.add(b.platform(54, 2, 0, 0))
    cam_node.add(monkey_toolkit.rounded_platform(desc, 0, 2, 3, 5, z=-0.1))
    cam_node.add(monkey_toolkit.rounded_platform(desc, 51, 2, 3, 5, z=-0.2))
    cam_node.add(monkey_toolkit.rounded_platform(desc, 53, 0, 4, 5, z=-0.1))
    cam_node.add(monkey_toolkit.rounded_platform(desc, x=53, y=2, w=3, h=7, z=-0.3))
    cam_node.add(monkey_toolkit.rounded_platform(desc, 26, 2, 6, 7, z=-0.3))
    cam_node.add(monkey_toolkit.rounded_platform(desc, 67, 0, 3, 9, z=-0.3))
    cam_node.add(monkey_toolkit.rounded_platform(desc, 79, 0, 7, 2, z=-0.3))
    cam_node.add(monkey_toolkit.rounded_platform(desc, 80, 2, 3, 7, z=-0.3))
    cam_node.add(monkey_toolkit.rounded_platform(desc, 81, 2, 4, 2, z=-0.2))
    cam_node.add(monkey_toolkit.rounded_platform(desc, 87, 2, 7, 3, z=-0.1))
    cam_node.add(monkey_toolkit.rounded_platform(desc, 87, 2, 6, 6, z=-0.2))
    cam_node.add(monkey_toolkit.rounded_platform(desc, 87, 2, 4, 9, z=-0.3))
    cam_node.add(monkey_toolkit.rounded_platform(desc, 99, 2, 2, 4, z=-0.1))
    cam_node.add(monkey_toolkit.rounded_platform(desc, 109, 2, 9, 7, z=-0.1))
    cam_node.add(monkey_toolkit.rounded_platform(desc, 122, 2, 16, 7, z=-0.1))
    cam_node.add(monkey_toolkit.rounded_platform(desc, 129, 2, 12, 11, z=-0.2))
    cam_node.add(monkey_toolkit.rounded_platform(desc, 138, 2, 14, 7, z=-0.1))
    cam_node.add(monkey_toolkit.rounded_platform(desc, 152, 2, 7, 7, z=-0.1))
    cam_node.add(monkey_toolkit.rounded_platform(desc, 159, 2, 16, 13, z=-0.1))
    cam_node.add(monkey_toolkit.rounded_platform(desc, 159, 15, 5, 5, z=-0.1))
    cam_node.add(monkey_toolkit.rounded_platform(desc, 166, 15, 4, 8, z=-0.1))
    cam_node.add(monkey_toolkit.rounded_platform(desc, 160, 15, 9, 11, z=-0.2))
    # #cam_node.add(b.rounded_platform(desc, 113, 2, 16, 11, z=-0.2))
    cam_node.add(waterfalls(56, 0, 22, 12))
    cam_node.add(waterfalls(70, 0, 20, 16))
    cam_node.add(waterfalls(118, 0, 8, 26, z=-0.1))
    #cam_node.add(vine(32, 2, 10))
    # # cam_node.add(waterfalls(b, 5, 5, 11, 5, pal='pal/1'))
    #
    # #player = b.player('mario', cam, 3, 3, walk_keys=wkeys, climb=True)
    # # add custom states
    #
    #
    start_pos = settings.start_positions[settings.room][settings.start_position]
    p0 = start_pos['pos']
    right = start_pos.get('right', True)
    player = make_player(p0[0], p0[1])
    if not right:
        player.flip_x = True
    cam_node.add(player)


    # *** foes
    foes_id = ['shyguy_red', 'shyguy', 'tweeter', 'hoopster']
    foes = [(14, 2, 0), (17, 2, 0), (38, 2, 0), (40, 3, 2), (44, 2, 0), (61, 10, 0), (64, 10, 0), (30, 9, 1), (55, 5, 1), (21, 3, 2),
            (67, 10, 2), (92, 8, 1), (90, 5, 1), (91, 2, 1), (105, 2, 0), (114, 2, 0), (116, 2, 2), (110, 9, 1), (129, 2, 0), (132, 2, 2),
            (132, 9, 1), (153, 9, 0), (157.5, 10, 3)]
    for foe in foes:
        cam_node.add(make_character(foe[0], foe[1], foes_id[foe[2]]))




    #cam_node.add(make_character(10, 3, 'ninji'))
    cam_node.add(make_character(41.5, 3, 'pow'))
    cam_node.add(monkey_toolkit.door(1, 2, 1, 2, 'smb2_world_1_1b', model='sprites2/door_black', z=-0.05))
    cam_node.add(monkey_toolkit.door(126, 2, 1, 2, 'smb2_world_1_1c', desc=monkey_toolkit.tiled_model('smb2', 'W,1,R,2,14,6,E'), z=-0.05))
    #
    #
    #
    cam_node.add(monkey_toolkit.moving_platform(2, loop=0,
        desc=monkey_toolkit.anim_tiled_model('smb2', [
            ('W,2,9,2,11,2', 5), ('W,2,V,9,2,V,11,2', 5)]), points=[
                {'pos': (72, 7), 't': 0 },
                {'pos': (72, 7.75), 't': 1, 'z': -1.2},
                {'pos': (72, -1), 't': 5, 'z': 1}]))
    # cam_node.add(b.moving_platform(2, loop=1, desc=monkey_toolkit.tiled_model('smb2', 'W,2,9,2,11,2'), points=[{'pos': (10, 2), 't': 0}, {'pos': (10, 15), 't': 10}]))
    cam_node.add(vine(32, 2, 9))
    cam_node.add(vine(157, 9, 10))
    # cam_node.add(vine(b, 32, 2, 10))
    # cam_node.add(b.stairs(157, 9, 1, 10))


    veg1 = [(5, 2), (19, 2), (102, 2)]
    veg2 = [(8, 2), (15, 2), (27, 9), (28, 9), (29, 9)]
    cherries = [(36, 7), (48, 6), (95, 9), (102, 5), (106, 5)]
    for p in veg1:
        cam_node.add(make_character(p[0] + 0.5, p[1], 'veggie', shoot_item='veg1'))
    for p in veg2:
        cam_node.add(make_character(p[0] + 0.5, p[1], 'veggie', shoot_item='veg2'))
    for p  in cherries:
        cam_node.add(make_character(p[0] + 0.5, p[1], 'cherry'))

    # nogo-areas
    cam_node.add(monkey_toolkit.nogo_area(53, -1, 33, 1))
    cam_node.add(monkey_toolkit.warp(4, 2, 1, 1, room='smb2_world_1_1c', pos=0))
    return room