import monkey
from . import state
from .. import pippo


class flags:
    player = 1
    platform = 2
    foe = 4
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



def pippo():
    state.invincible = False
    monkey.engine().close_room()

def change_room(room):
    def f():
        pippo.room = room
        pippo()
    return f


def check_warp():
    if state.warp != 0:
        print('CICCIOBELLO', state.player_id)
        s = monkey.script()
        ii = s.add(monkey.set_state(id=state.player_id, state='warp'))
        ii = s.add(monkey.move_by(id=state.player_id, y=-64, t=1), ii)
        s.add(monkey.callfunc(change_room(state.warp)), ii)
        monkey.play(s)
