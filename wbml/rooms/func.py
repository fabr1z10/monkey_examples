import monkey
from ... import settings
from . import gamestate
from . import actions
from . import factory

hand_pos_x = [4, 10.5, 18.5]
hand_pos_y = 15.5

def restart():
    monkey.close_room()

def hit_snake(player, snake, dist):
    energy = snake.user_data['energy']
    energy -= 1
    print('energy is ',energy)
    if energy <= 0:
        snake.set_state('dead', dir=snake.x>=player.x)
    else:
        snake.set_state('hit',dir=snake.x>=player.x)
    snake.user_data['energy'] = energy

def collect(player, coin, dist):
    print('SUCAMI')
    coin.remove()

def on_enter_door(player, door, dist):
    print('entering door')
    settings.current_door = (door.id, door.user_data['world'])
    print('current door: ', settings.current_door)

def on_enter_gate(player, gate, dist):
    if gamestate.gate == 1:
        player.set_state('enter')
        s = monkey.script()
        ii = s.add(monkey.actions.move_by(id=gate.id, y=32,t=1))
        ii = s.add(actions.change_room(gate.user_data['world']), ii)

        monkey.play(s)


def on_leave_door(player, door):
    print('leaving door')
    settings.current_door = None

def move_hand_right():
    if gamestate.hand_pos == 1:
        return
    gamestate.hand_pos += 1
    monkey.get_node(settings.ids.hand).set_position(hand_pos_x[gamestate.hand_pos + 1] * 8, hand_pos_y * 8, 1)

def move_hand_left():
    if gamestate.hand_pos == -1:
        return
    gamestate.hand_pos -= 1
    monkey.get_node(settings.ids.hand).set_position(hand_pos_x[gamestate.hand_pos + 1] * 8, hand_pos_y * 8, 1)

def select():
    monkey.get_node(settings.ids.hand).active=False
    if gamestate.hand_pos == -1:
        s, ii = build_text(gamestate.shop.l_item_text)
        s.add(actions.change_room(gamestate.shop.exit_room), ii)
        monkey.play(s)
    elif gamestate.hand_pos == 1:
        s, ii = build_text(gamestate.shop.r_item_text)
        s.add(actions.change_room(gamestate.shop.exit_room), ii)
        monkey.play(s)
    else:
        s = monkey.script()
        s.add(actions.change_room(gamestate.shop.exit_room))
        monkey.play(s)


def build_text(msg):
    s = monkey.script()
    ii = -1
    for me in msg:
        m = factory.message(me, 96, 120 + 16)
        ii =s.add(monkey.actions.add(id=settings.ids.game_node, node=m), ii)
        ii= s.add(monkey.actions.reveal_text(id=m.id, interval=0.1), ii)
        ii= s.add(monkey.actions.wait_for_key(65), ii)
        ii= s.add(monkey.actions.remove(id=m.id), ii)
    return s, ii