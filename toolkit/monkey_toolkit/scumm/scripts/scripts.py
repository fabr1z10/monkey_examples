import monkey
from .. import actions
from .. import scumm

def player_say(*lines):
    def f(s):
        for l in lines:
            s.add(monkey.actions.say(tag='player', text=scumm.cippo.strings[l]))
    return f


def change_room(room, pos, dir):
    def f(s: monkey.script):
        s.add(actions.change_room(room=room, pos=pos, dir=dir))
    return f

def open_door(object_id):
    def f(s: monkey.script):
        obj = scumm.cippo.objects[object_id]
        if obj['anim'] == 'open':
            return
        else:
            obj['anim'] = 'open'
        for door in obj.get('connected_doors', []):
            scumm.cippo.objects[door]['anim'] = 'open'
        s.add(monkey.actions.animate(tag=object_id, anim='open'))
    return f

def close_door(object_id):
    def f(s: monkey.script):
        obj = scumm.cippo.objects[object_id]
        if obj['anim'] == 'closed':
            return
        else:
            obj['anim'] = 'closed'
        for door in obj.get('connected_doors', []):
            scumm.cippo.objects[door]['anim'] = 'open'
        s.add(monkey.actions.animate(tag='door_village_scummbar', anim='closed'))
    return f


def walk_door(object_id, room, pos, dir):
    def f(s: monkey.script):
        obj = scumm.cippo.objects[object_id]
        if obj['anim'] == 'open':
            change_room(room, pos, dir)(s)
    return f

