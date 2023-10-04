import monkey

def hello_world(room):
    cam = monkey.camera_ortho(256, 256,
                              viewport=(0, 0, 256, 256),
                              bounds_x=(128, 128), bounds_y=(128, 128))
    room.add_camera(cam)
    room.add_batch('sprites', monkey.sprite_batch(max_elements=10000, cam=0, sheet='main'))
    node = monkey.Node()
    node.set_model(monkey.models.text(text='Hello world', font='main/small', halign=monkey.ALIGN_CENTER), batch='sprites')
    node.set_position(128, 128, 0)
    root = room.root()
    root.add(node)

