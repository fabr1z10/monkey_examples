from . import factory


def start():
    r = factory.ScummRoom(320)
    r.add('dave', 0, 0)
    #r, c, cam = factory.room(320)
    #c.add(factory.character(cam, 'dave', 0, 0))

    return r.r
