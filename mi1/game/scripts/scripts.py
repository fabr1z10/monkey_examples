import monkey
import monkey_toolkit.scumm.actions as sa
import monkey_toolkit.scumm.scripts as ss
from .. import settings

# default actions
default_open = ss.player_say(1003)
default_close = ss.player_say(1004)
default_push = ss.player_say(1005)
default_pull = ss.player_say(1005)
default_pickup = ss.player_say(1006)
default_use = ss.player_say(1004)
default_turnon = ss.player_say(1004)
default_turnoff = ss.player_say(1004)
default_look = ss.player_say(1007)

walk_cliffside = ss.change_room('lookout', (247, 10), 'n')
walk_path_lookout_village = ss.change_room('village1', (8, 71), 'e')

open_door_village_scummbar = ss.open_door('door_village_scummbar')
close_door_village_scummbar = ss.close_door('door_village_scummbar')
walk_door_village_scummbar = ss.walk_door('door_village_scummbar', 'scummbar', (59, 20), 'e')

open_door_scummbar_village = ss.open_door('door_scummbar_village')
close_door_scummbar_village = ss.close_door('door_scummbar_village')
walk_door_scummbar_village = ss.walk_door('door_scummbar_village', 'village1', (715, 13), 's')

open_door_scummbar_kitchen = ss.open_door('door_scummbar_kitchen')
close_door_scummbar_kitchen = ss.close_door('door_scummbar_kitchen')
walk_door_scummbar_kitchen = ss.walk_door('door_scummbar_kitchen', 'kitchen', (46, 13), 'e')

open_door_kitchen_scummbar = ss.open_door('door_kitchen_scummbar')
close_door_kitchen_scummbar = ss.close_door('door_kitchen_scummbar')
walk_door_kitchen_scummbar = ss.walk_door('door_kitchen_scummbar', 'scummbar', (595, 13), 'w')

pickup_meat = ss.pickup('meat')
pickup_pot = ss.pickup('pot')
def pickup_fish(s):
    gulls = monkey.get_nodes('gull')
    if gulls and next(iter(gulls)).anim == 'eat':
        ss.player_say(1000)(s)
    else:
        settings.objects['collider_seagull']['active']=False
        ss.pickup('fish')(s)


def open_door_kitchen_pier(s):
    #monkey.get_node(settings.ids.walk_areas[0]).set_wall(0, False)
    ss.open_door('door_kitchen_pier')(s)
    settings.rooms['rooms']['kitchen']['walk_areas'][0]['desc']['walls'][0]['active'] = False
    s.add(sa.set_wall(0, 0, False))
def close_door_kitchen_pier(s):
    #monkey.get_node(settings.ids.walk_areas[0]).set_wall(0, True)
    settings.rooms['rooms']['kitchen']['walk_areas'][0]['desc']['walls'][0]['active'] = True
    ss.close_door('door_kitchen_pier')(s)
    s.add(sa.set_wall(0, 0, True))




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
look_fireplace = ss.player_say(1147)
look_mancomb =ss.change_room('mancomb')
look_estevan = ss.change_room('estevan')
look_cobb = ss.change_room('cobb')
look_pieces_of_eight = ss.player_say(1008)
look_scummbar_pirate1 = ss.player_say(1174)
talk_scummbar_pirate1 = ss.player_say(1175, 1174)
look_scummbar_pirate4 = ss.player_say(1176)
look_scummbar_pirate5 = ss.player_say(1177)

def talk_important_looking_pirates(s):
    s.add(sa.say(tag='scummbar_important_pirate2', line=1182))
    s.add(sa.start_dialogue(dialogue='ilp', set=1))

def pippo():
    print('stupendo')