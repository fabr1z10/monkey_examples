import monkey_toolkit
import monkey
from . import settings
from . import actions
from . import facmap
from . import factories
import yaml

collision_response = [
    # monkey_toolkit.globals.CollisionResponse(monkey_toolkit.tags.player, settings.Tags.collectible_item,
    #     on_start=actions.enable_pickup, on_end=actions.disable_pickup),
    # monkey_toolkit.globals.CollisionResponse(monkey_toolkit.tags.player_attack, settings.Tags.generic_foe,
    #     on_start=actions.foe_is_hit),
    # monkey_toolkit.globals.CollisionResponse(monkey_toolkit.tags.player, settings.Tags.foe_platform_sensor,
    #     on_start=actions.enable_pickup_platform, on_end=actions.disable_pickup_platform),
    # monkey_toolkit.globals.CollisionResponse(monkey_toolkit.tags.player, settings.Tags.ladder,
    #     on_start=actions.enable_stairs, on_end=actions.disable_stairs),
    # monkey_toolkit.globals.CollisionResponse(monkey_toolkit.tags.player, settings.Tags.door,
    #     on_start=actions.enter_door, on_end=actions.leave_door)
]



def generic_room_loader(room_id):
    cx = settings.device_size[0] * 0.5
    cy = settings.device_size[1] * 0.5
    with open("game/worlds/" + room_id + ".yaml", "r") as stream:
        monkey_toolkit.globals.tile_size = (16, 16)
        monkey_toolkit.globals.device_size = settings.device_size
        monkey_toolkit.globals.gravity = settings.gravity
        monkey_toolkit.globals.reference_cam = settings.main_cam
        monkey_toolkit.globals.on_restart = actions.on_restart
        try:
            data = yaml.safe_load(stream)
            world = data['world']
            world_size = world['size']
            settings.main_cam.set_bounds(cx, world_size[0] - cx, cy, world_size[1]-cy, -10, 10)
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
            return room
        except yaml.YAMLError as exc:
            print(exc)


def prova():
    return generic_room_loader('1')

    monkey_toolkit.globals.tile_size = (16, 16)
    monkey_toolkit.globals.device_size = settings.device_size
    monkey_toolkit.globals.gravity = settings.gravity
    monkey_toolkit.globals.reference_cam = settings.main_cam
    #monkey_toolkit.globals.on_restart = actions.on_restart

    room = monkey_toolkit.platformer_room(256, 224)
    room.set_main_cam(settings.main_cam)
    root = room.root()
    n = monkey.Node()

    m = monkey.models.multi_sprite(settings.main_batch)
    m.add("main", monkey.get_sprite(settings.main_batch, "sprites/pippo"), "", 0)
    m.add("body", monkey.get_sprite(settings.main_batch, "sprites/body"), "main", 0)
    n.set_model(m)
    root.add(n)
    return room