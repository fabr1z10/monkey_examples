import monkey
from . import state
from .. import settings



class flags:
    player = 1
    platform = 2
    foe = 4
    player_hit = 8
    platform_passthrough = 32

class tags:
    player = 1
    platform = 2
    powerup = 3
    sensor = 4
    foe = 5
    goomba = 6
    koopa = 7
    hotspot = 8
    coin = 9
    fire = 10
    pickup_sensor =11
    player_attack = 12
    pickup_sensor_platform = 13





def restart():
    state.invincible = False
    state.held_item = None
    state.pickup_item = None
    state.pickup_platform_item = None
    monkey.close_room()

def change_room(room, pos):
    def f():
        settings.room = room
        state.start_position = pos
        restart()
    return f


def check_warp():
    if state.warp != 0:
        print('CICCIOBELLO', state.player_id)
        s = monkey.script()
        ii = s.add(monkey.set_state(id=state.player_id, state='warp'))
        ii = s.add(monkey.move_by(id=state.player_id, y=-64, t=1), ii)
        s.add(monkey.callfunc(change_room(state.warp[0], state.warp[1])), ii)
        monkey.play(s)
