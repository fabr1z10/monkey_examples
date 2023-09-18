import monkey
from . import settings
import yaml
from . import scripts


def ciao():
    print('sucalo')


def update_current_action_label():
    node = monkey.get_node(settings.ids.current_action)
    verb = settings.verbs[settings.current_action[0]]

    text = settings.strings[verb['text']]
    if len(settings.current_action) == 2:
        object_id = settings.current_action[1]
        obj = settings.objects[object_id]
        print(settings.current_action[1], 'figone')
        if object_id in settings.inventory:
            quantity = settings.inventory[object_id]
            if quantity == 1:
                text_id = settings.strings[obj['text']]
            else:
                text_id = str(quantity) + ' ' + settings.strings[obj['plural']]
        else:
            text_id = settings.strings[obj['text']]
        text += ' ' + text_id
    node.set_model(monkey.models.text(text=text, font='main/small',
                                      halign=monkey.ALIGN_CENTER), batch='ui')

    node.set_palette(3)


def main_click(node, pos, btn, act):
    # walk on left button CLICK
    if btn == 0 and act == 1:
        a = monkey.script(id=settings.player_script_id)
        a.add(monkey.actions.walk(target=pos, tag='player'))
        monkey.play(a)


def make_ui(type):
    ui = monkey.Node()
    # keys = [
    #     ('Open', 2, 40),
    #     ('Close', 2, 31),
    #     ('Push', 2, 22),
    #     ('Pull', 2, 13),
    #     ('Walk to', 48, 40),
    #     ('Pick up', 48, 31),
    #     ('Talk to', 48, 22),
    #     ('Give', 48, 13),
    #     ('Use', 100, 40),
    #     ('Look at', 100, 31),
    #     ('Turn on', 100, 22),
    #     ('Turn off', 100, 13)
    # ]
    keys = settings.verbs
    default_verb = None
    ui_main = monkey.Node()
    for verb_id, info in keys.items():
        k = monkey.Node()
        pos = info['pos']
        dv = info.get('default')
        if dv:
            default_verb = verb_id
        #print(info)
        #print(settings.strings)
        k.set_model(monkey.models.text(text=settings.strings[info['text']],
                                       font='main/small'), batch='ui')
        hs = monkey.text_hotspot(batch='ui_line')
        hs.set_on_enter(on_enter_verb)
        hs.set_on_leave(on_leave_verb)
        hs.set_on_click(on_click_verb(verb_id))
        k.add_component(hs)
        k.set_position(pos[0], pos[1] + 9, 0)
        k.set_palette(1)
        ui_main.add(k)
    settings.default_verb = default_verb
    settings.current_action = [default_verb]
    lbl_current_action = monkey.Node()
    lbl_current_action.set_position(160, 58, 0)

    ui_main.add(lbl_current_action)
    settings.ids.current_action = lbl_current_action.id
    update_current_action_label()

    inventory = monkey.ItemList(font='main/small', height=3, line_height=8, batch='ui', use_mouse=True,
                                on_enter=on_enter_inventory_item, on_click=on_click_inventory_item,
                                on_leave=on_leave_inventory_item, palette=5, arrow_down='main/arrow_down',
                                arrow_down_pos=(-8, -6 * 8, 0), arrow_palette=7,
                                arrow_palette_selected=8, arrow_up='main/arrow_up', arrow_up_pos=(-8, -20, 0))
    settings.ids.inventory = inventory.id
    ui_main.add(inventory)
    ui.add(ui_main)

    dialogue = monkey.ItemList(font='main/small', height=6, line_height=8, batch='ui', use_mouse=True,
                               on_enter=on_enter_dialogue_item, on_click=on_click_dialogue_item,
                               on_leave=on_leave_dialogue_item, palette=settings.palettes.dialogue_unselected_palette, arrow_down='main/arrow_down',
                               arrow_down_pos=(0, -6*8, 0), arrow_palette=9,
                               arrow_palette_selected=10, arrow_up='main/arrow_up', arrow_up_pos=(0, -20, 0))
    settings.ids.dialogue = dialogue.id
    ui.add(dialogue)


    for key, quantity in settings.inventory.items():
        add_to_inventory(key, quantity)
    #inventory.add_item('pieces_of_eight', 1)
    #inventory.add_item('pisdiez')
    #inventory.add_item('yellow petal')
    #inventory.add_item('gino')
    #inventory.add_item('pollo')
    #inventory.add_item('scamandro')

    inventory.set_position(176, 49, 0)
    dialogue.set_position(0, 56, 0)
    if type == 0:
        dialogue.active = False
    elif type == 1:
        ui_main.active = False

    return ui

def add_to_inventory(object_id, quantity):

    inv = monkey.get_node(settings.ids.inventory)
    obj = settings.objects[object_id]
    if quantity == 1:
        text = settings.strings[obj['text']]
    else:
        text = str(quantity) + ' ' + settings.strings[obj['plural']]
    inv.add_item(text=text, user_data=object_id)



def start_dialogue(dialogue_id):
    d = monkey.get_node(settings.ids.dialogue)
    dset = settings.dialogue[dialogue_id][1]
    for id, line in dset.items():
        active = line.get('active', True)
        if active:
            d.add_item(text=settings.strings[line['text']])

    pass

def room_loader(room, id):
    with open("assets/rooms.yaml", "r") as stream:
        try:
            data = yaml.safe_load(stream)
            world = data['rooms'][id]
            room.add_runner(monkey.hotspot_manager())
            room.add_runner(monkey.scheduler())
            # r.add_spritesheet('main')
            size = world['size']
            type = world.get('type', 0)
            cam = monkey.camera_ortho(320, 144,
                                      viewport=(0, 56, 320, 144),
                                      bounds_x=(160, size[0] - 160), bounds_y=(72, size[1] - 72))
            room.add_camera(cam)
            ui_cam = monkey.camera_ortho(320, 56,
                                         viewport=(0, 0, 320, 56),
                                         bounds_x=(160, 160),
                                         bounds_y=(28, 28))
            room.add_camera(ui_cam)
            room.add_batch('sprites', monkey.sprite_batch(max_elements=10000, cam=0, sheet='main'))
            bg = world.get('bg', None)
            if bg:
                room.add_batch('bg', monkey.sprite_batch(max_elements=100, cam=0, sheet=bg))
            room.add_batch('line', monkey.line_batch(max_elements=1000, cam=0))
            room.add_batch('ui', monkey.sprite_batch(max_elements=1000, cam=1, sheet='main'))
            room.add_batch('ui_line', monkey.line_batch(max_elements=1000, cam=1))
            root = room.root()

            if type == 0:
                playableArea = monkey.Node()
                playableArea.set_position(0, 0, -5)
                hs = monkey.hotspot(monkey.aabb(0, size[0], 0, size[1]), batch='line')
                hs.set_on_click(main_click)
                playableArea.add_component(hs)
                root.add(playableArea)
            walkareas = []
            if 'walk_areas' in world:
                for wa in world['walk_areas']:
                    if wa['type'] == 'poly':
                        outline = wa['outline']
                        walkArea = monkey.walkarea(poly=outline, batch='line')
                    else:
                        walkArea = monkey.walkarea_line(nodes=wa['nodes'], edges=wa['edges'], batch='line')
                    if 'z_func' in wa:
                        walkArea.set_z_function(monkey.func_ply(wa['z_func']))
                    if 'scale_func' in wa:
                        walkArea.set_scale_function(monkey.func_ply(wa['scale_func']))
                    root.add(walkArea)
                    walkareas.append(walkArea)

            # add player
            # player = monkey.get_multi('main/guybrush', 'sprites')
            # player.add_component(monkey.scumm_char(speed=settings.speed, text_pal=4))
            # player.set_animation('idle_e')
            # player.set_position(20, 10, 0)  # random.randint(-160, 160), random.randint(-72,72), 0)

            # walkArea.add(player)

            # ADD UI
            root.add(make_ui(type))

            # add objects
            for obj in settings.objects_in_room.get(id, []):
                add_object(obj, settings.objects[obj], root, walkareas)
            for obj in world.get('objects', []):
                add_object(None, obj, root, walkareas)

            # ON STARTUP
            if type == 1:
                start_dialogue(world.get('dialogue'))
            # add static bg
            # if bg:
            #     for item in bg['items']:
            #         bg1 = monkey.Node()
            #         tex_coords = item['tex_coords']
            #         pos = item.get('pos', (0, 0, 0))
            #         m1 = monkey.models.quad(tex_coords=tex_coords)
            #         bg1.set_position(pos[0], pos[1], pos[2])
            #         bg1.set_model(m1, batch='bg')
            #         root.add(bg1)


        except yaml.YAMLError as exc:
            print(exc)


def add_object(id, obj, root, walkareas):
    batch = obj.get('batch', 'sprites')
    print('adding ', id, batch)
    obj_data = obj  # settings.objects[obj]
    pos = obj_data['pos']
    walkarea_id = obj_data.get('walkarea', -1)
    if 'multi' in obj_data:
        node = monkey.get_multi(obj_data['multi'], 'sprites')
    else:
        node = monkey.Node()

    node.set_position(pos[0], pos[1], pos[2])

    if 'character' in obj_data:
        node.add_component(monkey.scumm_char(**obj_data['character']))

    if 'sprite' in obj_data:
        print(batch, obj_data['sprite'])
        node.set_model(monkey.get_sprite(obj_data['sprite']), batch=batch)
    elif 'quad' in obj_data:
        print(obj_data['quad'])
        node.set_model(monkey.models.quad(tex_coords=obj_data['quad']), batch=batch)

    if id == settings.player:
        node.add_component(monkey.follow(cam=0, pos=(0, 0, 5)))
        node.tag = 'player'
    elif id:
        node.tag = id

    if walkarea_id == -1:
        parent_node = root
    else:
        parent_node = walkareas[walkarea_id]
    parent_node.add(node)
    if 'anim' in obj_data:
        node.set_animation(obj_data['anim'])
    if 'hotspot' in obj_data:
        box = obj_data['hotspot']['box']
        ohs = monkey.hotspot(monkey.aabb(box[0], box[2], box[1], box[3]), batch='line')
        # default on enter
        ohs.set_on_enter(on_enter_playable_item(id))
        ohs.set_on_leave(on_leave_playable_item(id))
        ohs.set_on_click(on_click_playable_item(id))
        node.add_component(ohs)


def change_text_color(pal):
    def f(node):
        print('OKKE')
        node.set_palette(pal)

    return f

def on_enter_inventory_item(node):
    node.set_palette(settings.palettes.inventory_selected_palette)
    settings.current_action.append(node.user_data)
    update_current_action_label()

def on_enter_dialogue_item(node):
    node.set_palette(settings.palettes.dialogue_selected_palette)



def on_leave_inventory_item(node):
    node.set_palette(settings.palettes.inventory_unselected_palette)
    if len(settings.current_action) > 1:
        settings.current_action.pop()
        update_current_action_label()

def on_leave_dialogue_item(node):
    node.set_palette(settings.palettes.dialogue_unselected_palette)


def on_click_inventory_item(node, pos, btn, act):
    if btn == 0 and act == 1:
        execute_action()

def on_click_dialogue_item(node, pos, btn, act):
    pass

def on_enter_verb(node):
    node.set_palette(2)


def on_leave_verb(node):
    node.set_palette(1)


def on_click_verb(verb_id):
    def on_click(node, pos, btn, act):
        settings.current_action = [verb_id]
        update_current_action_label()

    return on_click


def on_enter_playable_item(item_id):
    def on_enter(node):
        settings.current_action.append(item_id)
        update_current_action_label()

    return on_enter


def on_leave_playable_item(item_id):
    def on_leave(node):
        if len(settings.current_action) > 1:
            settings.current_action.pop()
            update_current_action_label()

    return on_leave


def execute_action():
    print('fottimi')
    if len(settings.current_action) <= 1:
        return
    if len(settings.current_action) == 4:
        action = settings.current_action[0] + '_' + settings.current_action[1] + '_' + settings.current_action[2]
    else:
        objid = settings.current_action[1]
        action = settings.current_action[0] + '_' + objid
        obj = settings.objects[objid]
        s = monkey.script(id=settings.player_script_id)
        # we have to walk to the object unless it's in our inventory
        if 'walkto' in obj and objid not in settings.inventory:
            s.add(monkey.actions.walk(target=obj['walkto'], tag='player'))
            if 'turn' in obj:
                s.add(monkey.actions.turn(dir=obj['turn'], tag='player'))
        f = getattr(scripts, action, None)
        if f:
            print('found')
            f(s)
            print('lclcc')
        else:
            print('not found')
            # get default for this verb
            f1 = getattr(scripts, '_' + settings.current_action[0], None)
            if f1:
                f1(s)
            else:
                print(' no default')
        monkey.play(s)
    #print('checking ', action)
    settings.current_action = [settings.default_verb]
    update_current_action_label()

def on_click_playable_item(item_id):
    def on_click(node, pos, btn, act):
        if btn == 0 and act == 1:
            execute_action()

    return on_click
