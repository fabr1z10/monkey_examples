import monkey
from ... import settings


def change_room(room_id):
    def f():
        settings.room = room_id
        monkey.close_room()
    return monkey.actions.callfunc(f)
