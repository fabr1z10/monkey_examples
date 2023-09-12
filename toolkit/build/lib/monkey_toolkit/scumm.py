import monkey

cippo = None


def move_object(obj_id, room, pos):
    o = cippo.objects[obj_id]
    if 'room' in o and o['room']:
        cippo.objects_in_room[o['room']].remove(obj_id)
    if room:
        cippo.objects_in_room[room].append(obj_id)
    o['pos'] = [pos[0], pos[1], 0]

def change_room(**kwargs):
    def f():
        cippo.room_id = kwargs['room']
        pos = kwargs['pos']
        move_object(cippo.player, cippo.room_id, pos)
        player = cippo.objects[cippo.player]
        player['walkarea'] = kwargs.get('walkarea', 0)
        player['anim'] = 'idle_' + kwargs['dir']
        monkey.close_room()

    s = monkey.actions.callfunc(f)
    return s