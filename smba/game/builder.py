import monkey_toolkit
import game.settings as settings


def platform(**kwargs):
    def f(x, y, width, height):
        return monkey_toolkit.platformer.platform(x, y, width, height, tile=kwargs.get('tile'))
    return f


def object(**kwargs):
    def f(x, y):
        return monkey_toolkit.platformer.tiled(x, y, settings.models[kwargs.get('model')])
    return f

