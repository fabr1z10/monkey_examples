import monkey
from . import state
from . import factory
from . import util


def reset_invincibility():
    state.invincible = False


def mario_is_hit(player, foe):
    if state.invincible:
        return
    if state.mario_state == 0:
        player.set_state('dead')
        s = monkey.script()
        ii = s.add(monkey.delay(1))
        ii = s.add(monkey.move_accelerated(id=player.id,
                                           timeout=1,
                                           velocity=monkey.vec3(0, 100, 0),
                                           acceleration=monkey.vec3(0, -state.gravity, 0)), ii)
        s.add(monkey.callfunc(util.restart), ii)
        monkey.play(s)
    else:
        state.mario_state -= 1
        state.invincible = True
        st = state.mario_states[state.mario_state]
        player.set_model(monkey.get_sprite(st['model']))
        player.get_controller().set_size(st['size'], st['center'])
        s = monkey.script()
        ii = s.add(monkey.blink(id=player.id, duration=state.invincible_duration, period=0.2))
        s.add(monkey.callfunc(reset_invincibility), ii)
        monkey.play(s)


def jump_on_foe(player, foe, callback=None):
    a = player.get_dynamics()
    a.velocity.y = 200
    foe.set_state('dead')

def fire():
    player = monkey.engine().get_node(state.player_id)
    main = monkey.engine().get_node(state.cn)
    aa = factory.fireball(player.x, player.y+20, -1 if player.flip_x else 1)
    main.add(aa)


def make_coin(b):
    pos = b.position
    def f(comp, node):
        if node.position[1] < pos[1]:
            node.remove()
    node = monkey.Node()
    node.set_model(monkey.get_sprite('sprites/flying_coin'))
    node.set_position(pos[0], pos[1], 1)
    mm = monkey.move_dynamics(1.)
    mm.set_velocity(0, 250, 0)
    mm.set_constant_force(0, -state.gravity, 0)
    mm.set_callback(f)
    node.add_component(mm)
    state.coins += 1
    update_coin()
    main = monkey.engine().get_node(state.cn)
    main.add(node)


def make_powerup(id):
    def f(b):
        pos = b.get_parent().position
        node = factory.powerup(pos[0] + 8, pos[1], id)
        main = monkey.engine().get_node(state.cn)
        main.add(node)
    return f


def update_coin():
    monkey.engine().get_node(state.coin_label).set_text('{:02d}'.format(state.coins))


def hit_sensor(a, b, dist):
    pp = b.get_parent()
    v = a.get_dynamics().velocity
    if v.y < 0:
        return
    v.y = 0
    pp.get_collider().set_collision_flag(util.flags.platform)
    if pp.user_data['hits'] > 0:
        if pp.user_data['hits'] == 1:
            pp.set_animation('taken')
        print(pp.user_data['hits'])
        pp.user_data['hits']-=1
        ad = pp.get_move_dynamics()
        ad.set_velocity(0, 50, 0)
        pp.user_data['callback'](b)
    elif pp.user_data['hits'] == -1:
        if state.mario_state == 0:
            ad = pp.get_move_dynamics()
            ad.set_velocity(0, 50, 0)
        else:
            pp.remove()
            a.get_dynamics().velocity.y = 0
            main = monkey.engine().get_node(state.cn)
            pos = pp.position
            main.add(factory.brick_piece(0, pos[0], pos[1], -100, 150))
            main.add(factory.brick_piece(0, pos[0], pos[1], -50, 250))
            main.add(factory.brick_piece(0, pos[0], pos[1], 100, 150))
            main.add(factory.brick_piece(0, pos[0], pos[1], 50, 250))


def hit_powerup(player, b, dist):
    b.user_data['callback'](player)
    b.remove()


def hit_goomba(player, foe, dist):
    print(dist.x, dist.y, dist.z)
    print(player.id, " " , foe.id)
    if dist.y > 0:
        jump_on_foe(player, foe)
    else:
        mario_is_hit(player, foe)


def hit_koopa(player, foe, dist):
    if foe.state == 'dead':
        direction = 0
        if dist.x != 0:
            direction = -1 if dist.x > 0 else 1
        else:
            direction = -1 if player.x > foe.x else 1
        foe.set_state('fly', dir=direction)
    else:
        hit_goomba(player, foe, dist)


def hit_gk(goomba, koopa, dist):
    if koopa.state == 'fly':
        goomba.set_state('dead2')
        s = monkey.script()
        ii = s.add(monkey.move_accelerated(id=goomba.id,
                                           timeout=0.5,
                                           velocity=monkey.vec3(-50 if koopa.x > goomba.x else 50, 100, 0),
                                           acceleration=monkey.vec3(0, -state.gravity, 0)))
        s.add(monkey.remove(id=goomba.id), ii)
        monkey.play(s)


def hit_hotspot(player, hotspot, dist):
    on_start = hotspot.user_data.get('on_start')
    if on_start:
        on_start()
    rm = hotspot.user_data.get('remove', True)
    if rm:
        hotspot.remove()


def leave_hotspot(player, hotspot):
    on_end = hotspot.user_data.get('on_end')
    if on_end:
        on_end()