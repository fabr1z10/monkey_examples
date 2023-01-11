from .factory import *
from . import gamestate


def round2():
    room, game_node = common_room(1280, 192)

    p = player(game_node.get_camera(), gamestate.player_position[0], gamestate.player_position[1])
    game_node.add(p)
    settings.ids.player = p.id

    game_node.add(tiled2(w=1, h=20, pos=(-1, -1)))              # left boundary
    game_node.add(tiled2(w=1, h=40, pos=(160, -1)))
    game_node.add(tiled2(desc='1,W,23,R,23,20,11,E,R,23,20,10,E', w=46, h=4, pos=(0, 0)))
    game_node.add(tiled2(desc='1,W,1,20,11,20,11,20,10', w=2, h=6, pos=(46, 0)))
    game_node.add(tiled2(desc='1,W,24,R,3,R,24,20,11,E,E,R,24,20,10,E', w=48, h=8, pos=(48, 0)))
    game_node.add(tiled2(model='tiles/tower2',pos=(0,4),z=-0.1))
    game_node.add(tiled2(model='tiles/big_house_1',pos=(16,4),z=-0.1))

    # trees
    for i in [(10, 4)]:
        game_node.add(tiled2(pos=(i[0], i[1]), model='tiles/tree', z=-0.1))
    return room
