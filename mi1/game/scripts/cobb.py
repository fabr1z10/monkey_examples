from game.scripts.helper import _dl
import monkey_toolkit.scumm.actions as sa
import monkey
from .. import settings


def on_start_cobb():
    s = monkey.script()
    s.add(_dl(1169, 4)) #monkey.actions.msg(text=settings.strings[1100], pos=(240, 128), id=settings.ids.root, remove=1))
    s.add(sa.start_dialogue(dialogue='cobb', set=1))
    monkey.play(s)

def dial_cobb_1_10(s):
    s.add(_dl(1170, 3))
    s.add(_dl(1169, 4))

def dial_cobb_1_20(s):
    s.add(_dl(1171, 3))
    s.add(_dl(1169, 4))