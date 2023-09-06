import monkey
from . import settings

def player_say(*lines):
    def f(s):
        for l in lines:
            s.add(monkey.actions.say(tag='player', text=settings.strings[l]))
    return f

# default actions
_open = player_say(1003)
_close = player_say(1004)
_push = player_say(1005)
_pull = player_say(1005)
_pickup = player_say(1006)
_use = player_say(1004)
_turnon = player_say(1004)
_turnoff = player_say(1004)
_look = player_say(1007)

def open_prova(s: monkey.script):
    s.add(monkey.actions.say(tag='player', text='Look at that fabulous ship out there!'))



#close_prova = player_say('Re-elect Governor Marley.')
#close_prova = player_say("So what brings you to\nMêlée Island™ anyway?")
close_prova = player_say("I've come seeking my\nfortune.")
look_poster = player_say(1001, 1002)
