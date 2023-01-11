import monkey

settings = None

def ciao():
    print('suca')

### create a basic room, with given width and height.
# adds a restart button (default F10)
def room_2d(world_width, world_height):
    room = monkey.Room("mario")
    room.add_runner(monkey.scheduler())
    root = room.root()
    kb = monkey.keyboard()
    kb.add(299, 1, 0, restart)
    root.add_component(kb)

    # create camera
    device_size = settings.device_size
    device_width = device_size[0]
    device_height = device_size[1]
    device_half_width = device_width // 2
    device_half_height = device_height // 2
    cam_node = monkey.Node()
    cam = monkey.camera_ortho(device_width, device_height)
    cam.set_bounds(device_half_width, world_width - device_half_width, device_half_height, world_height - device_half_height, -100, 100)
    cam_node.set_camera(cam)
    root.add(cam_node)


    return room, cam, cam_node