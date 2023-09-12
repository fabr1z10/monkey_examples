state = None

tile_size = (1, 1)
device_size = None
gravity = None

on_restart = None
on_stairs = 0
current_door = 0


jj = dict()






class CollisionResponse:
    def __init__(self, tag1, tag2, **kwargs):
        self.tag1 = tag1
        self.tag2 = tag2
        self.on_start = kwargs.get('on_start')
        self.on_end = kwargs.get('on_end')
        self.on_stay = kwargs.get('on_stay')


class internal:
    player_id = None


cache = dict()