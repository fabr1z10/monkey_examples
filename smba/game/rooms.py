import monkey
import game.settings as settings
import monkey_toolkit
import game.builder as build
from inspect import signature



def restart_room():
    monkey.close_room()


def kolpo(room):
    # load the current room data
    print (settings.rooms)
    room_data = settings.rooms.get(settings.world, None)
    assert room_data, settings.world + ' is not a valid room!'
    settings.world_name = room_data['id']
    size = room_data['size']
    common(room, size[0], size[1])
    root = room.root()
    for key, v in room_data['desc'].items():
        for value in v:
            builder = getattr(build, key, None)
            assert builder, "builder: <" + key + "> not found!"
            f = builder(**value)
            param_number = len(signature(f).parameters)
            for i in range(0, len(value['items']), param_number):
                print(value['items'][i:i+param_number])
                root.add(f(*value['items'][i:i+param_number]))
                #f(*value['items'][i:i+param_number])
    player = room_data.get('player', 0)
    if player == 1:
        start_pos = room_data.get('start_position')[0]
        root.add(monkey_toolkit.platformer.player2d(start_pos[0], start_pos[1], 10, 10, 'mario/mario', speed=200, jump_height=80,
                                                    time_to_jump_apex=0.4, acc_time = 0.2))
    root.add(monkey_toolkit.platformer.foe2d(10, 5, 10, 10, 'mario/goomba', speed=10, jump_height=64, time_to_jump_apex=0.2, flip_on_edge=True))

def pino(a, b, pos):
    b.remove()

def common(room, world_width, world_height):
    ce = monkey.collision_engine(64, 64, 0)
    ce.add_response(0, 1, on_start=pino)
    room.add_runner(ce)

    ds = settings.device_size
    dshw = ds[0] // 2
    dshh = ds[1] // 2
    cam = monkey.camera_ortho(ds[0], ds[1],
                              viewport=(0, 0, ds[0], ds[1]),
                              bounds_x=(dshw, world_width - dshw), bounds_y=(dshh, world_height - dshh))
    room.add_camera(cam)
    ui_cam = monkey.camera_ortho(ds[0], ds[1],
                              viewport=(0, 0, ds[0], ds[1]),
                              bounds_x=(dshw, dshw), bounds_y=(dshh, dshh))
    room.add_camera(ui_cam)
    room.set_clear_color(92,148,252)
    room.add_batch('main', monkey.sprite_batch(max_elements=10000, cam=0, sheet='mario'))
    room.add_batch('ui', monkey.sprite_batch(max_elements=10000, cam=1, sheet='mario'))
    room.add_batch('line', monkey.line_batch(max_elements=1000, cam=0))
    root = room.root()
    root.add(monkey_toolkit.platformer.text(24, 216, 'mario', 'MARIO', batch='ui'))
    root.add(monkey_toolkit.platformer.text(24, 208, 'mario', str(settings.score).zfill(6), batch='ui'))
    root.add(monkey_toolkit.platformer.text(144, 216, 'mario', 'WORLD', batch='ui'))
    root.add(monkey_toolkit.platformer.text(152, 208, 'mario', settings.world_name, batch='ui'))
    root.add(monkey_toolkit.platformer.text(200, 216, 'mario', 'TIME', batch='ui'))
    root.add(monkey_toolkit.platformer.text(96, 208, 'mario', '*', batch='ui'))
    root.add(monkey_toolkit.platformer.text(104, 208, 'mario', str(settings.coins).zfill(2), batch='ui'))
    root.add(monkey_toolkit.platformer.tiled(11, 25, settings.models['coin_counter'], batch='ui'))

    # root.add(monkey_toolkit.platformer.text(104, 112, 'mario', '©1985 NINTENDO', pal=1))
    # root.add(monkey_toolkit.platformer.text(96, 48, 'mario', 'TOP- ' + str(settings.top_score).zfill(6)))
    # root.add(monkey_toolkit.platformer.text(88, 88, 'mario', '1 PLAYER GAME'))
    # root.add(monkey_toolkit.platformer.text(88, 72, 'mario', '2 PLAYER GAME'))

    kb = monkey.keyboard()
    kb.add(settings.keys.restart, 1, 0, restart_room)
    root.add_component(kb)


def pipe(x, y, height, pal):
    assert (height > 2)
    model = {
        'sheet': 'mario',
        'size': [4, height],
        'animations': {
            'main': {
                'frames': [
                    { 'data': [0x50000+pal, 0x10000 + (height-2), 38, 39, 134, 40, 0x20000, 166, 167, 168, 169, 102, 103, 104, 105]}
                ]
            }
        }
    }
    return monkey_toolkit.platformer.tiled(x, y, model, platform=1)

def world1_1(r):
    common(r, 3584, 224)
    root = r.root()
    root.add(monkey_toolkit.platformer.platform(0, -1, 138, 4, tile=(224, 8, 16, 16)))
    root.add(monkey_toolkit.platformer.platform(142, -1, 30, 4, tile=(224, 8, 16, 16)))
    root.add(monkey_toolkit.platformer.platform(178, -1, 128, 4, tile=(224, 8, 16, 16)))
    root.add(monkey_toolkit.platformer.platform(310, -1, 138, 4, tile=(224, 8, 16, 16)))
    root.add(monkey_toolkit.platformer.platform(-1, -1, 1, 32))
    root.add(monkey_toolkit.platformer.player2d(64, 128, 10, 10, 200, 32, 0.2))
    root.add(monkey_toolkit.platformer.tiled(17, 20, settings.models['cloud1']))
    root.add(monkey_toolkit.platformer.tiled(23, 3, settings.models['bush3']))
    root.add(monkey_toolkit.platformer.tiled(47, 3, settings.models['bush1']))
    root.add(monkey_toolkit.platformer.tiled(0, 3, settings.models['hill_large']))
    root.add(monkey_toolkit.platformer.foe2d(128, 128, 'mario/goomba'))
    #root.add(monkey_toolkit.platformer.tiled(0, 9, settings.models['coin_counter'], batch='ui'))

    root.add(pipe(56, 3, 4, 0))
    root.add(pipe(76, 3, 6, 0))
    root.add(pipe(92, 3, 8, 0))
    root.add(pipe(114, 3, 8, 0))
    root.add(pipe(326, 3, 4, 0))
    root.add(pipe(358, 3, 4, 0))


