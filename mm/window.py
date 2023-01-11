import pyglet
from camera import  Camera
import math


class GameWindow(pyglet.window.Window):
    def __init__(self):
        super(GameWindow, self).__init__(width=640, height=400, resizable=True, caption='pplot', vsync=True)

        self.world_camera = Camera(scroll_speed=1, min_zoom=1, max_zoom=4)
        self.b = pyglet.graphics.Batch()
        self.btext = pyglet.graphics.Batch()
        y0 = 0
        self.shapes = []

        label = pyglet.text.Label('Push', color=(0, 170, 0, 255), font_size=16, x=0, y=80, batch=self.btext)
        pyglet.text.Label('Pull', color=(0, 170, 0, 255), font_size=16, x=0, y=64, batch=self.btext)



    def on_draw(self):
        self.clear()
        #self.label.draw()
        # Draw your world scene using the world camera
        with self.world_camera:
            self.b.draw()
            self.btext.draw()
        #self.b.draw()

