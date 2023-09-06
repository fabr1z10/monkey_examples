import monkey
from . import settings
from . import scumm


def sh(s, c):
    b = monkey.Node()
    b.set_model(monkey.models.from_shape(s, c))
    return b

import random

def g():
    print('sucamilcazzo')








def hello_world(r):
    scumm.room_loader(r, 'village1')
    return
    r.add_runner(monkey.hotspot_manager())

    r.add_runner(monkey.scheduler())
    #r.add_spritesheet('main')
    cam = monkey.camera_ortho(320, 144, viewport=(0, 56, 320, 144), bounds_x=(160, 160), bounds_y=(72,72))
    r.add_camera(cam)

    ui_cam = monkey.camera_ortho(320, 56,
                                 viewport=(0,0,320,56),
                                 bounds_x=(160, 160),
                                 bounds_y=(28,28))
    r.add_camera(ui_cam)


    r.add_batch('sprites', monkey.sprite_batch(max_elements=10000, cam=0, sheet='main'))
    r.add_batch('bg', monkey.sprite_batch(max_elements=1000, cam=0, sheet='lookout'))
    r.add_batch('ui', monkey.sprite_batch(max_elements=1000, cam=1, sheet='main'))
    r.add_batch('line', monkey.line_batch(max_elements=1000, cam=0))
    r.add_batch('ui_line', monkey.line_batch(max_elements=1000, cam=1))

    root = r.root()

    playableArea = monkey.Node()
    hs = monkey.hotspot(monkey.aabb(0, 320, 0, 200), batch='line')
    hs.set_on_click(f1)
    playableArea.add_component(hs)
    root.add(playableArea)



    walkArea = monkey.walkarea(poly=[1,1,200,1,200,50,320,50,320,70,180,70,180,30,1,30], batch='line')
    root.add(walkArea)
    for i in range(0, 1):
        a = monkey.get_multi('main/guybrush', 'sprites')
        a.add_component(monkey.scumm_char(speed=settings.speed))
        a.set_animation('walk_e')
        a.set_position(20, 10, 0)#random.randint(-160, 160), random.randint(-72,72), 0)

        a.tag ='player'
        walkArea.add(a)

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
        hs.set_on_enter(scumm.on_enter_verb)
        hs.set_on_leave(scumm.on_leave_verb)
        hs.set_on_click(scumm.on_click_verb)
        k.add_component(hs)
        k.set_position(key[1], key[2] + 9, 0)
        k.set_palette(1)
        root.add(k)

    lbl_current_action = monkey.Node()
    lbl_current_action.set_model(monkey.models.text(text='sucamisucamisucamisucami', font='main/small',
                                                    halign=monkey.ALIGN_CENTER), batch='ui')
    lbl_current_action.set_position(160, 58, 0)
    lbl_current_action.set_palette(3)
    settings.ids.current_action = lbl_current_action.id
    root.add(lbl_current_action)

    #root.add(sh(monkey.aabb(0, 20, 0, 10), (1,1,1,1)))
    #root.add(sh(monkey.rect(50,100), (1,0,0,1)))
    # #root.add(sh(monkey.circle(10), (0,1,0,1)))
    # b = monkey.Node()
    # b.add_component(monkey.hotspot(monkey.aabb(0,20,0,10)))
    # root.add(b)