from . import settings
import monkey_toolkit
import monkey


def platform(**kwargs):
    tile = kwargs.get('tile')
    # if tile is not None:
    #     tile = settings.tiles[tile]
    return monkey_toolkit.platformer.platform(settings.main_batch, **dict(kwargs, tile=tile))# pos[0], pos[1], size[0], size[1], tile, z)


def player(**kwargs):
    aa = monkey_toolkit.multi_sprite(settings.main_batch, 'sprites', 'wonderboy')
    aa.add("legs", monkey.get_sprite(settings.main_batch, "sprites/boots_legend"))
    aa.add("body", monkey.get_sprite(settings.main_batch, "sprites/body_no"))
    #aa.add("sword", monkey.get_sprite(settings.main_batch, "sprites/gradius"))

    print(type(aa))

    model = [
        {
            'key': 'legs',
            'sprite': 'sprites/legs_no_no'
        },
        {
            'key': 'body',
            'sprite': 'sprites/body',
            'parent': 'legs',
            'joint': 0
        }
    ]
    player = monkey_toolkit.character(settings.main_batch, **dict(kwargs, size=[10,14], speed=50, player=True, controller_mask_down=monkey_toolkit.flags.platform |
        monkey_toolkit.flags.platform_passthrough, climb=True, model=aa, walk_keys=[], collision_shape = monkey.aabb(0, 10, 0, 10)))
    sm = player.get_state_machine()
    #sm.add(monkey.attack("attack1", anims=['attack1'], speed=settings.mario_speed, gravity=settings.gravity, exit_state='walk'))

    #sm.add(monkey.idle("lift", "lift", exit_on_complete=True, exit_state='walk_item'))
    #sm.add(monkey.idle("enter_door", "idle"))
    # walk + carry
    #sm.add(monkey.walk_2d_player("walk_item", speed=kwargs['speed'], gravity=settings.gravity, jump_height=80, time_to_jump_apex=0.5,
    #   walk_anim='walk_item', idle_anim='idle_item', keys={68: pickup_shoot}))
    #sm.add(monkey.idle("dead", "dead"))
    return player