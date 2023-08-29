title='New game'

window_size=[320, 200]
device_size=window_size
enable_framebuffer = True
enable_mouse = True
debug_collision = True

room='hello_world'

player_script_id = '_player'

speed = 100

x=0
x1=0
main_node=0

spritesheets = {
    'main': '../assets/spritesheet/mi1'
}

class ids:
    current_action = None


objects = dict()
objects_in_room = dict()