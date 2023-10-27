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


def pipe(**kwargs):
    def f(x, y, height):
        assert (height > 2)
        model = {
            'sheet': 'mario',
            'size': [4, height],
            'animations': {
                'main': {
                    'frames': [
                        { 'data': [0x50000+kwargs.get('pal'), 0x10000 + (height-2), 38, 39, 134, 40, 0x20000, 166, 167, 168, 169, 102, 103, 104, 105]}
                    ]
                }
            }
        }
        return monkey_toolkit.platformer.tiled(x, y, model, platform=1)
    return f