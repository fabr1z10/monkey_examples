import monkey
from . import settings
from . import scumm


def sh(s, c):
    b = monkey.Node()
    b.set_model(monkey.models.from_shape(s, c))
    return b

import random








def hello_world(r):
    scumm.room_loader(r, settings.room_id)
