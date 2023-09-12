import monkey

from .. import scumm

def move_object(obj_id, room, pos):
    o = scumm.cippo.objects[obj_id]
    print(scumm.cippo.objects_in_room)
    print('caled with ', obj_id, room)
    if 'room' in o and o['room']:
        scumm.cippo.objects_in_room[o['room']].remove(obj_id)
    if room:
        scumm.cippo.objects_in_room[room].append(obj_id)
    o['room'] = room
    o['pos'] = [pos[0], pos[1], 0]

def change_room(**kwargs):
    def f():
        scumm.cippo.room_id = kwargs['room']
        pos = kwargs['pos']
        move_object(scumm.cippo.player, scumm.cippo.room_id, pos)
        player = scumm.cippo.objects[scumm.cippo.player]
        player['walkarea'] = kwargs.get('walkarea', 0)
        player['anim'] = 'idle_' + kwargs['dir']
        monkey.close_room()

    s = monkey.actions.callfunc(f)
    return s