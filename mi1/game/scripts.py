import monkey
import monkey_toolkit.scumm.actions as sa
import monkey_toolkit.scumm.scripts as ss
from . import settings

# default actions
_open = ss.player_say(1003)
_close = ss.player_say(1004)
_push = ss.player_say(1005)
_pull = ss.player_say(1005)
_pickup = ss.player_say(1006)
_use = ss.player_say(1004)
_turnon = ss.player_say(1004)
_turnoff = ss.player_say(1004)
_look = ss.player_say(1007)

walk_cliffside = ss.change_room('lookout', (247, 10), 'n')
walk_path_lookout_village = ss.change_room('village1', (8, 71), 'e')

open_door_village_scummbar = ss.open_door('door_village_scummbar')
close_door_village_scummbar = ss.close_door('door_village_scummbar')
walk_door_village_scummbar = ss.walk_door('door_village_scummbar', 'lookout', (247, 10), 'n')
# def open_door_village_scummbar(s: monkey.script):
#     obj = settings.objects['door_village_scummbar']
#     if obj['anim'] == 'open':
#         return
#     else:
#         obj['anim'] = 'open'
#         for door in obj.get('connected_doors', []):
#             settings.objects[door]['anim'] = 'open'
#         s.add(monkey.actions.animate(tag='door_village_scummbar', anim='open'))
#
# def close_door_village_scummbar(s: monkey.script):
#     obj = settings.objects['door_village_scummbar']
#     if obj['anim'] == 'closed':
#         return
#     else:
#         obj['anim'] = 'closed'
#         for door in obj.get('connected_doors', []):
#             settings.objects[door]['anim'] = 'open'
#         s.add(monkey.actions.animate(tag='door_village_scummbar', anim='closed'))
#
# def walk_door_village_scummbar(s):
#     obj = settings.objects['door_village_scummbar']
#     if obj['anim'] == 'open':
#         ss.change_room('lookout', (247, 10), 'n')(s)
#def walk_cliffside(s: monkey.script):
#     s.add(sa.change_room(room='lookout', pos=(247, 10), dir='n'))
#
# def walk_path_lookout_village(s: monkey.script):
#     s.add(sa.change_room(room='village1', pos=(8, 71), dir='e'))


def open_prova(s: monkey.script):
    s.add(monkey.actions.say(tag='player', text='Look at that fabulous ship out there!'))



#close_prova = player_say('Re-elect Governor Marley.')
#close_prova = player_say("So what brings you to\nMêlée Island™ anyway?")
close_prova = ss.player_say("I've come seeking my\nfortune.")
look_poster = ss.player_say(1001, 1002)
