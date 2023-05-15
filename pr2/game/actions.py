from . import settings
import monkey
import monkey_toolkit
#from rooms.chars import get_character, get_shoot_item

offset = [16,22]


def on_restart():
    print('current pickup item=',settings.pickup_item)
    settings.invincible = False
    settings.current_door =None
    settings.held_item = None
    settings.pickup_item = None
    settings.pickup_platform_item = dict()
    settings.active_door=None


# this is called when player enters a foe platform sensor or a collectible hotspot
def enable_pickup(player, foe, dist):
    settings.pickup_item = foe.id
    print('pickup item is now', settings.pickup_item)


# this is called when player leaves a foe platform sensor or a collectible hotspot
def disable_pickup(player, foe):
    settings.pickup_item = None
    print('pickup item cleared')


def enable_pickup_platform(player, foe, dist):
    settings.pickup_item = foe.get_parent().get_parent().id
    settings.pickup_platform_item[settings.pickup_item] = foe.get_parent().id


def disable_pickup_platform(player, foe):
    settings.pickup_item = None
    #state.pickup_platform_item = None


def create_shoot_item(x, y, z, id):
    #sitem =get_shoot_item(id)
    node = monkey.Node()
    pal = id.get('pal', 0)
    node.set_model(monkey.get_sprite(settings.main_batch, id['model']), pal=pal)
    #if pal:
    #    node.set_palette(pal)
    node.set_position(x, y, z)
    node.add_component(monkey.sprite_collider(monkey_toolkit.flags.player_hit, monkey_toolkit.flags.foe, monkey_toolkit.tags.player_attack))
    node.add_component(monkey.controller_2d(size=(10, 14, 0)))
    node.add_component(monkey.dynamics())
    sm = monkey.state_machine()
    sm.add(monkey.idle("idle", "idle"))

    sm.add(monkey.bounce("bounce", gravity=settings.gravity, check_walls=id['bounce_on_walls'], on_bounce_y=id.get('bounce_callback', None), bounce_velocity=[150], speed=200,
                         collision_mask = monkey_toolkit.flags.foe, collision_flag= monkey_toolkit.flags.player_hit, collision_tag=monkey_toolkit.tags.player_attack))
    node.add_component(sm)
    return node

# this is called when fire button is pressed
def pickup_shoot():
    # this function throws the item
    player = monkey.get_node(monkey_toolkit.globals.internal.player_id)
    if settings.held_item:
        player = monkey.get_node(settings.player_id)#  globals.internal.player_id)
        item = monkey.get_node(settings.held_item)  # .remove()
        # make player's parent the item's parent
        # before: parent -> player -> item
        # after: parent -> item
        player.get_parent().move_to(item)
        item.set_position(player.x, player.y + offset[settings.mario_state], 0.1)
        player.set_state('walk')
        item.set_state('bounce', left=player.flip_x) #velocity=(-settings.shoot_speed if player.flip_x else settings.shoot_speed, 0))
        settings.held_item = None
    elif settings.pickup_item:
        #if settings.pickup_item in settings.pickup_platform_item:
        #    monkey.get_node(settings.pickup_platform_item[settings.pickup_item]).active = False#()# = False
        #item = monkey.get_node(settings.pickup_item).remove()
        pitem = monkey.get_node(settings.pickup_item)
        settings.pickup_item = None
        aa = pitem.user_data['shoot_item']
        fi = pitem.user_data.get('foe_item')
        #bounce = pitem.user_data['bounce']
        pitem.remove()
        n = create_shoot_item(0, 0, 1, aa)
        n.user_data = {'foe_item': fi}
        player.add(n)
        player.set_state('lift')
        s = monkey.script()
        s.add(monkey.actions.move(id=n.id, frames={
            0: [0, -10, 0.1],
            6: [0, -8, 0.1],
            12: [0, 4, 0.1],
            16: [0, -2, 0.1],
            17: [0, 6, 0.1],
            18: [0, 7, 0.1],
            21: [0, 12, 0.1],
            23: [0, 22, 0.1]
        }))
        monkey.play(s)
        settings.held_item = n.id

        return

        player = monkey.get_node(globals.internal.player_id)
        item.set_state('lifted')
        # now player is item's parent
        player.move_to(item)
        item.set_position(0, offset[settings.mario_state], 0.1)


def pow_bounce(item, n):
    if n==1:
        node = monkey.Node()
        node.set_model(monkey.get_sprite('sprites2/explosion'))
        node.set_position(item.x, item.y, 1)
        item.get_parent().add(node)
        s = monkey.script()
        s.add(monkey.actions.animate(id=node.id, anim='idle', sync=True))
        s.add(monkey.actions.remove(id=node.id))
        monkey.play(s)
        item.remove()

def cippo(item, n):
    if n == 1:
        item.remove()


def bounce(item, n):
    print('bounce=',n)
    if n == 2:
        id = item.user_data.get('foe_item')
        print('foe item is ', id)
        #from rooms.factories import make_character
        par = item.get_parent()
        item.active = False
        item.remove()

        new_pos = [item.x/16, item.y/16]
        id[1].update(pos=new_pos, z=item.z)
        node = id[0](**id[1])
        par.add(node)
        #if id:
        #    node = make_character(item.x / 16, item.y /16, id)
        #    par.add(node)

        # item.get_dynamics().set_velocity(0, 0, 0)
        # item.set_state('walk')
        # if item.id in settings.pickup_platform_item:
        #     monkey.get_node(settings.pickup_platform_item[item.id]).active = True#()# = False
        #     del settings.pickup_platform_item[item.id]


def reset_invincibility():
    settings.invincible = False

def foe_is_hit(player_attack, foe, dist):
    foe.set_state('dead')
    s = monkey.script()
    v0 = [100, 100, 0]
    if player_attack.x > foe.x:
        v0[0] = -100
    if foe.flip_x:
        v0[0] *= -1
    s.add(monkey.actions.move_accelerated(id=foe.id, velocity=v0, acceleration=(0, -settings.gravity, 0), timeout=1))
    monkey.play(s)
    #foe.remove()

def collect(player, item, dist):
    item.remove()


def collision_player_foe(player, foe, dist):
    if settings.invincible:
        return
    if settings.mario_state == 0:
        player.set_state('dead')
        # put back scheduler + scripts
        s = monkey.script()
        s.add(monkey.actions.delay(1))
        s.add(monkey.actions.move_accelerated(id=player.id, timeout=1,
            velocity=(0, 100, 0), acceleration=(0, -settings.gravity, 0)))
        s.add(monkey.actions.callfunc(monkey_toolkit.restart))
        monkey.play(s)
    else:
        settings.mario_state -= 1
        settings.invincible = True
        id = settings.mario_states[settings.mario_state]
        char_info = get_character(id)['args']
        player.set_model(monkey.get_sprite(char_info['model']))
        #player.get_controller().set_size(char_info['size'])
        s = monkey.script()
        s.add(monkey.actions.blink(id=player.id, duration=settings.invincible_duration, period=0.2))
        s.add(monkey.actions.callfunc(reset_invincibility))
        monkey.play(s)