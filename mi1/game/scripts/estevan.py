from game.scripts.helper import _dl
import monkey_toolkit.scumm.actions as sa
import monkey
from .. import settings


def on_start_estevan():
    s = monkey.script()
    line = 1152 if settings.Variables.talked_to_estevan == 0 else 1168
    s.add(_dl(line, 2)) #monkey.actions.msg(text=settings.strings[1100], pos=(240, 128), id=settings.ids.root, remove=1))
    settings.Variables.talked_to_estevan = 1
    s.add(sa.start_dialogue(dialogue='estevan', set=1))
    monkey.play(s)

def dial_estevan_1_10(s):
    s.add(_dl(1148, 3)) #monkey.actions.msg(text=settings.strings[1100], pos=(240, 128), id=settings.ids.root, remove=1))
    s.add(_dl(1153, 2)) #monkey.actions.msg(text=settings.strings[1122], pos=(80, 128), id=settings.ids.root, remove=1, pal=11))

def dial_estevan_1_20(s):
    s.add(_dl(1149, 3)) #monkey.actions.msg(text=settings.strings[1100], pos=(240, 128), id=settings.ids.root, remove=1))
    s.add(_dl(1155, 2)) #monkey.actions.msg(text=settings.strings[1122], pos=(80, 128), id=settings.ids.root, remove=1, pal=11))
    s.add(_dl(1156, 2)) #monkey.actions.msg(text=settings.strings[1122], pos=(80, 128), id=settings.ids.root, remove=1, pal=11))
    s.add(monkey.actions.animate(tag='estevan', anim='blink'))
    s.add(_dl(1157, 2)) #monkey.actions.msg(text=settings.strings[1122], pos=(80, 128), id=settings.ids.root, remove=1, pal=11))
    s.add(_dl(1158, 2)) #monkey.actions.msg(text=settings.strings[1122], pos=(80, 128), id=settings.ids.root, remove=1, pal=11))
    s.add(monkey.actions.animate(tag='estevan', anim='blink'))

def dial_estevan_1_30(s):
    s.add(_dl(1150, 3))
    s.add(_dl(1159, 2))
    s.add(_dl(1160, 2))
    s.add(monkey.actions.animate(tag='estevan', anim='blink'))
    s.add(_dl(1161, 2))
    s.add(_dl(1162, 2))
    s.add(monkey.actions.animate(tag='estevan', anim='blink'))
    s.add(_dl(1163, 2))

def dial_estevan_1_35(s):
    s.add(_dl(1154, 3))
    s.add(_dl(1164, 2))
    s.add(_dl(1165, 2))
    s.add(monkey.actions.animate(tag='estevan', anim='blink'))
    s.add(_dl(1166, 2))

def dial_estevan_1_40(s):
    s.add(_dl(1151, 3))
    s.add(_dl(1167, 2))
    s.add(sa.change_room(room='scummbar', pos=settings.objects['estevan']['walkto'], dir=settings.objects['estevan']['turn']))