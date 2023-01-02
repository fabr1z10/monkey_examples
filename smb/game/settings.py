import monkey

window_size = (256, 240)
device_size = (256, 240)
title = 'ciao belo!'
room = 'w11i'
#shaders = (monkey.SHADER_COLOR, monkey.SHADER_TEXTURE)
shaders = {
    monkey.SHADER_COLOR: 0,
    monkey.SHADER_TEXTURE: 0,
    monkey.SHADER_TEXTURE_PALETTE: 0}

fire_button = 68        # GLFW_KEY_D

debug_collision = True



tilesets = {
    0: {'img': 'assets/smb1.png', 'tile_size': (16, 16)},
    1: {'img': 'assets/smbi.png', 'tile_size': (16, 16)},
    2: {'img': 'assets/smb2i.png', 'tile_size': (16, 16)},

}

