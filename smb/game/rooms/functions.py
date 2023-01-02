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
        ii = s.add(monkey.actions.delay(1))
        ii = s.add(monkey.actions.move_accelerated(id=player.id,
                                           timeout=1,
                                           velocity=monkey.vec3(0, 100, 0),
                                           acceleration=monkey.vec3(0, -state.gravity, 0)), ii)
        s.add(monkey.actions.callfunc(util.restart), ii)
        monkey.play(s)
    else:
        state.mario_state -= 1
        state.invincible = True
        st = state.mario_states[state.mario_state]
        player.set_model(monkey.get_sprite(st['model']))
        player.get_controller().set_size(st['size'], st['center'])
        s = monkey.script()
        ii = s.add(monkey.actions.blink(id=player.id, duration=state.invincible_duration, period=0.2))
        s.add(monkey.actions.callfunc(reset_invincibility), ii)
        monkey.play(s)


def jump_on_foe(player, foe, callback=None):
    a = player.get_dynamics()
    a.velocity.y = 200
    foe.set_state('dead')

def fire():
    if state.mario_state == 2:
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
        foe_killed(goomba, -50 if koopa.x > goomba.x else 50)


def foe_killed(foe, vx):
    foe.set_state('dead2')
    s = monkey.script()
    ii = s.add(monkey.move_accelerated(id=foe.id,
                                       timeout=0.5,
                                       velocity=monkey.vec3(vx, 100, 0),
                                       acceleration=monkey.vec3(0, -state.gravity, 0)))
    s.add(monkey.remove(id=foe.id), ii)
    monkey.play(s)


def fire_hit_foe(foe, fire, dist):
    fire.remove()
    foe_killed(foe, -50 if fire.x > foe.x else 50)

def enable_pickup(player, foe, dist):
    state.pickup_item = foe.id

def enable_pickup_platform(player, foe, dist):
    state.pickup_item = foe.get_parent().get_parent().id
    state.pickup_platform_item[state.pickup_item] = foe.get_parent().id


def disable_pickup(player, foe):
    state.pickup_item = None

def disable_pickup_platform(player, foe):
    state.pickup_item = None
    #state.pickup_platform_item = None


def bounce(item, n):
    print('bounce=',n)
    if n == 2:
        item.get_dynamics().velocity = monkey.vec3(0,0,0)
        item.set_state('pango')
        if item.id in state.pickup_platform_item:
            monkey.get_node(state.pickup_platform_item[item.id]).active = True#()# = False
            del state.pickup_platform_item[item.id]


def pickup():
    # this function throws the item
    if state.held_item:
        player = monkey.get_node(state.player_id)
        item = monkey.get_node(state.held_item)  # .remove()
        player.get_parent().move_to(item)
        item.set_position(player.x, player.y + 22, 0.1)
        #item.remove()
        player.set_state('pango')
        item.set_state('bounce', velocity=monkey.vec2(-state.shoot_speed if player.flip_x else state.shoot_speed, 0))
        state.held_item = None


    elif state.pickup_item:
        if state.pickup_item in state.pickup_platform_item:
            monkey.get_node(state.pickup_platform_item[state.pickup_item]).active = False#()# = False
        item = monkey.get_node(state.pickup_item)#.remove()
        state.held_item = state.pickup_item
        state.pickup_item = None
        player = monkey.get_node(state.player_id)
        player.set_state('lift')
        item.set_state('lifted')

        player.move_to(item)
        item.set_position(0,22,0.1)

        #a = monkey.Node()
        #a.set_model(monkey.get_sprite('sprites2/veggie_item'))
        #a.set_position(0, 22, 0.1)
        #player.add(a)


def bomba(player, foe, dist):
    foe.set_state('dead', velocity = monkey.vec2(0, 100))

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