import monkey
from . import state


def read_sign():
    s = monkey.script(id='cane')
    item = state.items['sign']
    ii = s.add(monkey.walk(id=state.player_id, pos=item['walk_to'], dir=item.get('dir',None), speed=100))
    s.add(monkey.say(id=state.player_id, lines=['a','b']), ii)
    monkey.play(s)
