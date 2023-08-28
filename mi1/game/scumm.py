import monkey
from . import settings
import yaml

def main_click(node, pos, btn, act):
    # walk on left button CLICK
    if btn == 0 and act == 1:
        a = monkey.script(id=settings.player_script_id)
        a.add(monkey.actions.walk(target=pos, tag='player'))
        monkey.play(a)

def make_ui():
    ui = monkey.Node()
    keys = [
        ('Open', 2, 40),
        ('Close', 2, 31),
        ('Push', 2, 22),
        ('Pull', 2, 13),
        ('Walk to', 48, 40),
        ('Pick up', 48, 31),
        ('Talk to', 48, 22),
        ('Give', 48, 13),
        ('Use', 100, 40),
        ('Look at', 100, 31),
        ('Turn on', 100, 22),
        ('Turn off', 100, 13)
    ]

    for key in keys:
        k = monkey.Node()
        k.set_model(monkey.models.text(text=key[0],
            font='main/small'), batch='ui')
        hs = monkey.text_hotspot(batch='ui_line')
        hs.set_on_enter(on_enter_verb)
        hs.set_on_leave(on_leave_verb)
        hs.set_on_click(on_click_verb)
        k.add_component(hs)
        k.set_position(key[1], key[2] + 9, 0)
        k.set_palette(1)
        ui.add(k)

    lbl_current_action = monkey.Node()
    lbl_current_action.set_model(monkey.models.text(text='sucamisucamisucamisucami', font='main/small',
                                                    halign=monkey.ALIGN_CENTER), batch='ui')
    lbl_current_action.set_position(160, 58, 0)
    lbl_current_action.set_palette(3)
    settings.ids.current_action = lbl_current_action.id
    ui.add(lbl_current_action)
    return ui

def room_loader(room, id):
    with open("assets/rooms.yaml", "r") as stream:
        try:

            data = yaml.safe_load(stream)
            world = data['rooms'][id]
            room.add_runner(monkey.hotspot_manager())
            room.add_runner(monkey.scheduler())
            # r.add_spritesheet('main')
            size = world['size']
            cam = monkey.camera_ortho(320, 144,
                viewport=(0, 56, 320, 144),
                bounds_x=(160, size[0]-160), bounds_y=(72, size[1]-72))
            room.add_camera(cam)
            ui_cam = monkey.camera_ortho(320, 56,
                viewport=(0, 0, 320, 56),
                bounds_x=(160, 160),
                bounds_y=(28, 28))
            room.add_camera(ui_cam)
            room.add_batch('sprites', monkey.sprite_batch(max_elements=10000, cam=0, sheet='main'))
            room.add_batch('line', monkey.line_batch(max_elements=1000, cam=0))
            room.add_batch('ui', monkey.sprite_batch(max_elements=1000, cam=1, sheet='main'))
            room.add_batch('ui_line', monkey.line_batch(max_elements=1000, cam=1))
            root = room.root()

            playableArea = monkey.Node()
            hs = monkey.hotspot(monkey.aabb(0, size[0], 0, size[1]), batch='line')
            hs.set_on_click(main_click)
            playableArea.add_component(hs)
            root.add(playableArea)
            for wa in world['walk_areas']:
                walkArea = monkey.walkarea(poly=wa, batch='line')
                root.add(walkArea)
            # add player
            player = monkey.get_multi('main/guybrush', 'sprites')
            player.add_component(monkey.scumm_char(speed=settings.speed))
            player.set_animation('idle_e')
            player.set_position(20, 10, 0)  # random.randint(-160, 160), random.randint(-72,72), 0)
            player.add_component(monkey.follow(cam=0, pos=(0,0,5)))
            player.tag = 'player'
            walkArea.add(player)

            root.add(make_ui())
        except yaml.YAMLError as exc:
            print(exc)


def on_enter_verb(node):
    node.set_palette(2)

def on_leave_verb(node):
    node.set_palette(1)

def on_click_verb(node, pos, btn, act):

    n = monkey.get_node(settings.ids.current_action)
    n.set_model(monkey.models.text(text=node.text, font='main/small',
        halign=monkey.ALIGN_CENTER), batch='ui')
    n.set_palette(3)
    print(node.text)