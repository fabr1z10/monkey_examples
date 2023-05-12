#!/usr/bin/python3

import monkey
import monkey_toolkit
from game import settings
#from rooms.chars import init
from game import init





monkey_toolkit.settings = settings
#init()
init.init()

a = monkey.engine()

a.start()

def ciappo():
    print(settings.main_batch)
    settings.main_batch = None



main_camera = monkey.camera_ortho(256, 240, viewport=(0,0,256,240))

settings.main_cam = main_camera

quad_batch = monkey.sprite_batch(1000, cam=main_camera, sheet='smb2i.png')#monkey.sheet = 'smb2i.png', shader_type=monkey.SHADER_BATCH, max_quads=1000, cam=settings.main_cam))
settings.main_batch = quad_batch
#settings.on_close = ciappo
a.add_batch (0, quad_batch)






#a.add_batch(monkey.sprite_batch(sheet = 'smb2i.png', shader_type=monkey.SHADER_BATCH, max_quads=1000, cam=settings.main_cam))
#a.add_batch(monkey.line_batch(max_lines=200, cam=settings.main_cam))
a.run()
a.shutdown()
