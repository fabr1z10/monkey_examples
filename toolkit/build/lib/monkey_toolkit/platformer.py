import monkey
from . import globals
from . import helper
from . import factory
import yaml

from enum import Enum

# class syntax

class PlatformType(Enum):
    NONE = 0
    SOLID = 1
    LINE = 2






def moving_platform(batch, **kwargs):
    w = kwargs['width']
    ts = globals.tile_size[0]
    node = monkey.Node()
    shape = monkey.segment(0, ts, w * ts, ts)
    node.add_component(monkey.platform())
    node.add_component(monkey.collider(shape, 32, 0, 2))
    points = kwargs['points']
    loop = kwargs.get('loop', 0)
    pts = []
    for p in points:
        pts.append( {'pos': (p['pos'][0] * ts, p['pos'][1] * ts), 't': p['t'], 'z': p.get('z', 0)})
    node.add_component(monkey.move_translate(points=pts, loop=loop))
    pal = kwargs.get('pal', 0)
    model = kwargs.get('model')
    #model = _load_model(**kwargs)
    node.set_model(model)
    return node


#def pino(batch, **kwargs):


def platform(**kwargs): # x, y, width, height, tex_coords, pal, z = 0):
    print('figo')
    print(kwargs.get('sheet'))
    a = monkey.Node()
    size = kwargs['size']
    tex_coords = kwargs.get('tile')
    width = size[0]
    height = size[1]
    pos = kwargs.get('pos', (0, 0))
    z = kwargs.get('z', 0)
    pal = kwargs.get('pal', 0)
    assert(width >= 1)
    assert(height >= 1)
    a.set_position(pos[0] * globals.tile_size[0], pos[1] * globals.tile_size[1], z)
    # b = helper.get_quad(batch, frames=[
    #     {'quads': [
    #         {'size': (width * globals.tile_size[0], height * globals.tile_size[1]),
    #          'tex_coords': tex_coords, 'repeat': (width, height), 'palette': pal}]}
    # ])
    if tex_coords:
        b = monkey.models.quad(sheet=kwargs['sheet'], frames=[
            {'quads': [
                {'size': (width * globals.tile_size[0], height * globals.tile_size[1]),
                 'tex_coords': tex_coords, 'repeat': (width, height), 'palette': pal}]}
        ])
        a.set_model(b)
    shape = monkey.rect(width * globals.tile_size[0], height * globals.tile_size[1])
    a.add_component(monkey.collider(shape, 2, 0, 2))
    # add to batch

    monkey.get_batch(0, 0).add(a)
    return a




def platform_border(batch, x, y, width, height, tex_coords, pal, z = 0, platform_type = PlatformType.SOLID):
    assert(width >= 2)
    assert(height >= 1)
    a = monkey.Node()
    a.set_position(x * globals.tile_size[0], y * globals.tile_size[1], z)
    tw = globals.tile_size[0]
    th = globals.tile_size[1]
    y1 = (height - 1) * th
    x1 = (width - 1) * tw
    quads = []
    # appending top left
    quads.append({'pos': (0, y1),  'size': globals.tile_size, 'tex_coords': tex_coords['top_left'], 'repeat': (1, 1), 'palette': pal})
    # appending top right
    quads.append({'pos': (x1, y1),  'size': globals.tile_size, 'tex_coords': tex_coords['top_right'], 'repeat': (1, 1), 'palette': pal})
    if width > 2:
        # appending top
        quads.append({'pos': (tw, y1), 'size': ((width - 2) * tw, th), 'tex_coords': tex_coords['top'], 'repeat': (width - 2, 1), 'palette': pal})
    if height > 1:
        # appending border left
        quads.append({'pos': (0, 0), 'size': (tw, (height - 1) * th), 'tex_coords': tex_coords['left'], 'repeat': (1, height-1), 'palette': pal})
        # appending border right
        quads.append({'pos': (x1, 0), 'size': (tw, (height - 1) * th), 'tex_coords': tex_coords['right'], 'repeat': (1, height-1), 'palette': pal})
        # appending center
        if width > 2:
            # appending center
            quads.append({'pos': (tw, 0), 'size': ((width - 2) * tw, (height-1)*th), 'tex_coords': tex_coords['center'],
                          'repeat': (width - 2, height-1), 'palette': pal})
    print(quads)
    b = monkey.models.quad(batch, frames=[{'quads': quads}])
    if platform_type == PlatformType.SOLID:
        shape = monkey.rect(width * tw, height * th)
        a.add_component(monkey.collider(shape, 2, 0, 2))
    elif platform_type == PlatformType.LINE:
        shape = monkey.segment(0, height*th, width * tw, height*th)
        a.add_component(monkey.collider(shape, 1 << 5, 0, 2))
    a.set_model(b)
    return a