from . import globals
import monkey


def restart():
    if globals.on_restart:
        globals.on_restart()
    monkey.close_room()


def enter_nogo_area(player, area, dist):
    player.active = False
    s = monkey.script()
    s.add(monkey.actions.delay(1))
    s.add(monkey.actions.callfunc(restart))
    monkey.play(s)


def enter_warp(player, area, dist):
    globals.state.room = area.user_data['room']
    globals.state.start_position = area.user_data['pos']
    restart()



def enter_door(player, door, dist):
    print('entering door')
    globals.state.current_door = door.id

def leave_door(player, door):
    print('leaving door')
    globals.state.current_door = None





