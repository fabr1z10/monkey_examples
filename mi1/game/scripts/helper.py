import monkey
from .. import settings

def _dl(line, actor):
    return monkey.actions.msg(text=settings.strings[line], pos=settings.actors[actor]['pos'], pal=settings.actors[actor]['pal'], id=settings.ids.root, remove=1)