import monkey
import game.settings as settings
import monkey_toolkit

def restart_room():
    monkey.close_room()


def common(room, world_width, world_height):
    room.add_runner(monkey.collision_engine(64, 64, 0))

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
    root.add(monkey_toolkit.platformer.tiled(88,200, settings.models['coin_counter'], batch='ui'))

    # root.add(monkey_toolkit.platformer.text(104, 112, 'mario', '©1985 NINTENDO', pal=1))
    # root.add(monkey_toolkit.platformer.text(96, 48, 'mario', 'TOP- ' + str(settings.top_score).zfill(6)))
    # root.add(monkey_toolkit.platformer.text(88, 88, 'mario', '1 PLAYER GAME'))
    # root.add(monkey_toolkit.platformer.text(88, 72, 'mario', '2 PLAYER GAME'))

    kb = monkey.keyboard()
    kb.add(settings.keys.restart, 1, 0, restart_room)
    root.add_component(kb)


def world1_1(r):
    common(r, 3584, 224)
    root = r.root()
    root.add(monkey_toolkit.platformer.platform(0, -1, 138, 4, tile=(224, 8, 16, 16)))
    root.add(monkey_toolkit.platformer.platform(-1, -1, 1, 32))
    root.add(monkey_toolkit.platformer.player2d(64, 128, 10, 10, 100, 32, 0.2))
    root.add(monkey_toolkit.platformer.tiled(17, 20, settings.models['cloud1']))
    root.add(monkey_toolkit.platformer.tiled(23, 3, settings.models['bush3']))
    root.add(monkey_toolkit.platformer.tiled(47, 3, settings.models['bush1']))
    root.add(monkey_toolkit.platformer.tiled(0, 3, settings.models['hill_large']))

    root.add(monkey_toolkit.platformer.foe2d(128, 128, 'mario/goomba'))


