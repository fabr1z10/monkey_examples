import monkey

window_size = (640, 400)
device_size = (320, 200)
title = 'ciao belo!'
room = 'start'
shaders = (monkey.SHADER_COLOR, monkey.SHADER_TEXTURE)
debug_collision = True
enable_mouse = True



tilesets = {
    0: {'img': 'assets/smb1.png', 'tile_size': (16, 16)}
}

def init():
    from . import rooms
    rooms.state.setup()


