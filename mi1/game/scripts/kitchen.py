from game.scripts.helper import _dl
import monkey_toolkit.scumm.actions as sa
import monkey
from .. import settings




def kitchen_create_seagull():
    a = monkey.Node()
    a.tag='gull'
    a.set_position(0,0,1)
    a.set_model(monkey.get_sprite('kitchen/seagull'),batch='bg')
    root = monkey.get_node(settings.ids.root)
    root.add(a)

def plank(node, pos, btn, act):

    if btn==0 and act==1:
        s = monkey.script(id=settings.player_script_id)
        s.add(monkey.actions.walk(target=[291,11], tag='player'))
        s.add(monkey.actions.turn(tag='player', dir='s'))
        s.add(monkey.actions.animate(tag='plank', anim='up'))
        gull = monkey.get_nodes("gull")
        if gull:
            g = next(iter(gull))
            if g.anim == 'eat':
                anim = 'jump1' if settings.Variables.seagull_state == 0 else 'jump2'
                settings.Variables.seagull_state = (settings.Variables.seagull_state + 1) % 2
                s.add(monkey.actions.animate(tag='gull', anim=anim))
        monkey.play(s)