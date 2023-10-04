from game.scripts.helper import _dl
import monkey_toolkit.scumm.actions as sa
import monkey
from .. import settings

def on_start_mancomb():
    s = monkey.script()
    s.add(sa.start_dialogue(dialogue='mancomb', set=1))
    monkey.play(s)

def dial_mancomb_1_10(s):
    s.add(_dl(1100, 0)) #monkey.actions.msg(text=settings.strings[1100], pos=(240, 128), id=settings.ids.root, remove=1))
    s.add(_dl(1122, 1)) #monkey.actions.msg(text=settings.strings[1122], pos=(80, 128), id=settings.ids.root, remove=1, pal=11))
    s.add(monkey.actions.animate(tag='mancomb', anim='laugh'))
    s.add(_dl(1123, 1))
    s.add(_dl(1124, 1))
def dial_mancomb_1_20(s):
    s.add(_dl(1101, 0)) #monkey.actions.msg(text=settings.strings[1100], pos=(240, 128), id=settings.ids.root, remove=1))
    s.add(_dl(1126, 1)) #monkey.actions.msg(text=settings.strings[1122], pos=(80, 128), id=settings.ids.root, remove=1, pal=11))
    s.add(_dl(1127, 1))
    s.add(monkey.actions.animate(tag='mancomb', anim='blink'))
    s.add(_dl(1128, 1))
    s.add(_dl(1129, 1))
    s.add(monkey.actions.animate(tag='mancomb', anim='blink'))
    s.add(_dl(1130, 1))
    s.add(monkey.actions.animate(tag='mancomb', anim='blink'))

def dial_mancomb_1_21(s):
    s.add(_dl(1112, 0))
    s.add(_dl(1131, 1))
    s.add(_dl(1132, 1))
    s.add(monkey.actions.animate(tag='mancomb', anim='blink'))
    s.add(_dl(1133, 1))

def dial_mancomb_1_30(s):
    s.add(_dl(1102, 0))
    s.add(_dl(1142, 1))
    s.add(_dl(1143, 1))
    s.add(monkey.actions.animate(tag='mancomb', anim='blink'))

def dial_mancomb_1_40(s):
    s.add(_dl(1103, 0))
    s.add(_dl(1103, 1))
    s.add(_dl(1141, 1))
    s.add(monkey.actions.animate(tag='mancomb', anim='blink'))
    s.add(sa.change_room(room='scummbar', pos=settings.objects['mancomb']['walkto'], dir=settings.objects['mancomb']['turn']))
def dial_mancomb_2_10(s):
    s.add(_dl(1104, 0))
    s.add(monkey.actions.animate(tag='mancomb', anim='neutral'))
    s.add(_dl(1125, 1))

def dial_mancomb_2_20(s):
    s.add(_dl(1105, 0))
    s.add(monkey.actions.animate(tag='mancomb', anim='neutral'))
    s.add(_dl(1146, 1))
    s.add(_dl(1000, 1))
    s.add(monkey.actions.animate(tag='mancomb', anim='blink'))



def dial_mancomb_5_10(s):
    s.add(_dl(1116, 0))
    s.add(_dl(1134, 1))
    s.add(_dl(1135, 1))
    s.add(monkey.actions.animate(tag='mancomb', anim='neutral'))

def dial_mancomb_5_20(s):
    s.add(_dl(1117, 0))
    s.add(_dl(1144, 1))
    s.add(_dl(1145, 1))
    s.add(monkey.actions.animate(tag='mancomb', anim='blink'))


def dial_mancomb_6_10(s):
    s.add(_dl(1119, 0))
    s.add(_dl(1136, 1))
    s.add(_dl(1137, 1))
    s.add(monkey.actions.animate(tag='mancomb', anim='blink'))
    s.add(_dl(1138, 1))
    s.add(_dl(1139, 1))
    s.add(monkey.actions.animate(tag='mancomb', anim='laugh'))
    s.add(_dl(1140, 1))
    s.add(monkey.actions.animate(tag='mancomb', anim='neutral'))

def dial_mancomb_4_10(s):
    s.add(_dl(1113, 0))
    s.add(_dl(1128, 1))
    s.add(_dl(1129, 1))
    s.add(monkey.actions.animate(tag='mancomb', anim='blink'))
    s.add(_dl(1130, 1))
