import monkey
from . import globals
from .actions import *
import yaml


def ciao():
    print('suca')









class tiled_model():
    def __init__(self, sheet_id, desc, pal=None):
        self.sheet_id = sheet_id
        self.desc = desc
        self.pal = pal

    def __hash__(self):
        return hash((self.sheet_id, self.desc, self.pal))

    def __eq__(self, other):
        return self.sheet_id == other.sheet_id and self.desc == other.desc and self.pal == other.pal

    def make(self):
        return monkey.models.tiled(sheet=self.sheet_id, desc=self.desc, palette=self.pal)


class anim_tiled_model():
    def __init__(self, sheet_id, desc, pal=None):
        self.sheet_id = sheet_id
        self.desc = tuple(desc)
        self.pal = pal

    def __hash__(self):
        return hash((self.sheet_id, self.desc, self.pal))

    def __eq__(self, other):
        return self.sheet_id == other.sheet_id and self.desc == other.desc and self.pal == other.pal

    def make(self):
        return monkey.models.tiled_animated(sheet=self.sheet_id, frames=self.desc, palette=self.pal)





class flags:
    player = 1
    platform = 2
    foe = 4
    player_hit = 8
    platform_passthrough = 1 << 5
    ladder_stop = 1 << 6


class tags:
    player = 1
    platform = 2
    ladder = 3
    player_attack = 4
    door = 5
    nogo_area = 6
    warp = 7            # change room

    # powerup = 3
    # sensor = 4
    # foe = 5
    # goomba = 6
    # koopa = 7
    # hotspot = 8
    # coin = 9
    # fire = 10
    # pickup_sensor =11
    # player_attack = 12
    # pickup_sensor_platform = 13
    # door = 14


class Action:
    climb = 1
    duck = 2
    fire = 3
    attack = 4
    enter_door = 5


class callback():
    def __init__(self):
        self.f = []
    def add(self, a):
        self.f.append(a)
    def get(self):
        def g():
            for a in self.f:
                a()
        return g



def initialize(settings, **kwargs):
    return
    globals.state = settings


def _load_model(**kwargs):
    model = kwargs.get('model')
    if model:
        return monkey.get_sprite(model)
    else:
        desc = kwargs.get('desc')
        if desc:
            return get_model(desc)
        else:
            return None

def get_model(model: tiled_model):
    if model not in globals.cache:
        globals.cache[model] = model.make()
    return globals.cache[model]

def tiled(x, y, model_desc, **kwargs):
    ts = getattr(globals.state, 'tile_size', (1, 1))
    node = monkey.Node()
    z = kwargs.get('z', 0)
    size = kwargs.get('size', None)
    node.set_model(get_model(model_desc))
    node.set_position(x * ts[0], y * ts[1], z)
    if size:
        solid = kwargs.get('solid', True)
        if solid:
            shape = monkey.rect(ts[0] * size[0], ts[1] * size[1])
            flag = flags.platform
        else:
            shape = monkey.segment(0, size[1] * ts[1], size[0] * ts[0], size[1] * ts[1])
            flag = flags.platform_passthrough
        node.add_component(monkey.collider(shape, flag, 0, tags.platform))
    return node


def platformer_room(room, world_width, world_height, **kwargs):
    #room = monkey.Room("mario")
    ce = monkey.collision_engine(80, 80, 0)
    # ce.add_response(tags.player, tags.ladder, on_start=enable_stairs, on_end=disable_stairs)
    # ce.add_response(tags.player, tags.door, on_start=enter_door, on_end=leave_door)
    # ce.add_response(tags.player, tags.nogo_area, on_start=enter_nogo_area)
    # ce.add_response(tags.player, tags.warp, on_start=enter_warp)
    collision_responses = kwargs.get('collision', [])
    for r in collision_responses:
        ce.add_response(r.tag1, r.tag2, on_start=r.on_start, on_end=r.on_end)
    #globals.state.collision_engine = ce
    room.add_runner(ce)
    room.add_runner(monkey.scheduler())
    room.add_runner(monkey.scheduler())
    root = room.root()
    kb = monkey.keyboard()
    kb.add(299, 1, 0, restart)
    root.add_component(kb)

    # create camera
    assert globals.gravity != None, "<gravity> must be specified in toolkit!"
    assert globals.device_size != None, "<device_size> must be specified in toolkit!"
    device_size = globals.device_size

    device_width = device_size[0]
    device_height = device_size[1]
    device_half_width = device_width // 2
    device_half_height = device_height // 2

    # setting the main cam
    #cam_node = monkey.Node()
    #cam =None
    #state.cn = cam_node.id
    #cam = monkey.camera_ortho(device_width, device_height)
    #cam.set_bounds(device_half_width, world_width - device_half_width, device_half_height, world_height - device_half_height, -100, 100)
    #cam_node.set_camera(cam)
    #room.set_main_cam(cam)
    #root.add(cam_node)
    #state.main_cam = cam
    #globals.state.main_cam = cam
    #return room#, cam, cam_node



# class platformer_toolkit():
#     def __init__(self, settings, **kwargs):
#         #global state
#         self.s = settings
#         settings.on_restart = kwargs.get('on_restart', None)
#         globals.state = settings
#         globals.state.on_stairs = False
#         self.tile_size = getattr(settings, 'tile_size', (1, 1))
#         print('tile size ', self.tile_size)
#         self.tw = self.tile_size[0]
#         self.th = self.tile_size[1]
#         self.cache = dict()
#
#     def get_model(self, model: tiled_model):
#         if model not in self.cache:
#             self.cache[model] = model.make()
#         return self.cache[model]
#


def door(x, y, width, height, world, **kwargs):
    ts = getattr(globals.state, 'tile_size', (1, 1))
    node = monkey.Node()
    z = kwargs.get('z', 0)
    shape = monkey.aabb(0, width * ts[0], 0, height * ts[1])
    node.add_component(monkey.collider(shape, flags.foe, flags.player, tags.door))
    node.set_position(x * ts[0], y * ts[1], z)
    node.user_data = {'world': world, 'has_sprite': kwargs.get('model')}
    model = _load_model(**kwargs)
    if model:
        node.set_model(model)
    return node


def hotspot(x, y, width, height, tag, **kwargs):
    ts = getattr(globals.state, 'tile_size', (1, 1))
    node = monkey.Node()
    z = kwargs.get('z', 0)
    shape = monkey.aabb(0, width * ts[0], 0, height * ts[1])
    node.add_component(monkey.collider(shape, flags.foe, flags.player, tag))
    node.set_position(x * ts[0], y * ts[1], z)
    model = _load_model(**kwargs)
    if model:
        node.set_model(model)
    return node


def nogo_area(x, y, width, height, **kwargs):
    return hotspot(x, y, width, height, tags.nogo_area, **kwargs)

def warp(x, y, width, height, **kwargs):
    node = hotspot(x, y, width, height, tags.warp, **kwargs)
    node.user_data = {'room': kwargs['room'], 'pos': kwargs['pos']}
    return node

#
#
#     # def tiled_anim(self, sheet_id, x, y, frames, pal=None, z=0):
#     #     node = monkey.Node()
#     #     node.set_model(monkey.models.tiled_animated(sheet=sheet_id, frames=frames, palette=pal))  # 'pal/0'))
#     #     node.set_position(x * 16, y * 16, z)
#     #     return node
#
# you need to supply the tile description
def rounded_platform(desc, x, y, w, h, z=0, pal=None):
    assert(w >= 2)
    ts = getattr(globals.state, 'tile_size', (1, 1))

    node = monkey.Node()
    sheet = desc['sheet']
    #fmt = "{}, {}, "
    top = desc.get('top')
    top_l = desc.get('top_left', top)
    top_r = desc.get('top_right', top)
    bottom = desc.get('bottom', top)
    l = desc.get('left', bottom)
    r = desc.get('right', bottom)
    if w > 2:
        dstr = ['W', w, 'R', h - 1, l[0], l[1], 'R', w - 2, bottom[0], bottom[1], 'E', r[0], r[1], 'E', top_l[0],
                top_l[1], 'R', w - 2, top[0], top[1], 'E', top_r[0], top_r[1]]
    else:
        dstr = ['W', w, 'R', h-1, l[0], l[1], r[0], r[1], 'E', top_l[0], top_l[1], top_r[0], top_r[1]]
    ds = ", ".join(str(x) for x in dstr)
    a = get_model(tiled_model(sheet, ds, pal))
    shape1 = monkey.segment(0, h * ts[1], w * ts[0], h * ts[1])
    node.set_model(a)
    node.set_position(x*ts[0], y*ts[1], z)
    node.add_component(monkey.collider(shape1, flags.platform_passthrough, 0, tags.platform))
    return node



# make rectangular or line platform with no model
def platform( x, y, w, h, **kwargs):
    node = monkey.Node()
    ts = getattr(globals.state, 'tile_size', (1, 1))

    z = kwargs.get('z', 0)
    flag = flags.platform
    if h > 0:
        shape = monkey.rect(ts[0] * w, ts[1] * h)
    else:
        passthrough = kwargs.get('passthrough', True)
        if passthrough:
            flag = flags.platform_passthrough
        shape = monkey.segment(0, 0, w * ts[0], 0)
    node.set_position(x * ts[0], y * ts[1], z)
    node.add_component(monkey.collider(shape, flag, 0, tags.platform))
    return node



# def handle_keys(wkeys):
#     walk_keys = dict()
#     if wkeys:
#         for item in wkeys:
#             key = item[0]
#             value = item[1]
#             if key not in walk_keys:
#                 walk_keys[key] = callback()
#             if isinstance(value, int):
#                 if value == Action.climb:
#                     walk_keys[key].add(climb)
#                 elif value == Action.enter_door:
#                     walk_keys[key].add(door_in)
#             else:
#                 walk_keys[key].add(value)
#     if walk_keys:
#         for key in walk_keys.keys():
#
#             walk_keys[key] = walk_keys[key].get()
#     return walk_keys


def collectible(x, y, info, **kwargs):
    ts = getattr(globals.state, 'tile_size', (1, 1))
    node = monkey.Node()
    node.set_model(monkey.get_sprite(info['model']))
    node.set_position(ts[0] * x, ts[1] * y, kwargs.get('z', 0))
    coll_flag = flags.foe
    coll_mask = flags.player
    coll_tag = info['tag']
    node.add_component(monkey.sprite_collider(coll_flag, coll_mask, coll_tag))
    return node


def sprite(**kwargs):
    #batch = kwargs.get('batch', monkey.engine().get_batch(0, 0))
    model = kwargs['model']
    x, y = kwargs['pos']
    z = kwargs.get('z', 0)
    palette = kwargs.get('pal', 0)
    ts = globals.tile_size
    node = monkey.Node()
    if isinstance(model, str):
        node.set_model(monkey.get_sprite(model), pal=palette)
    else:
        node.set_model(model)
    batch = monkey.get_batch(0, 0)
    batch.add(node)

    node.set_position(ts[0] * x, ts[1] * y, z)
    return node


def multi_sprite(file, id):
    with open("assets/" + file + ".yaml", "r") as stream:
        try:
            a =yaml.safe_load(stream)
            b = a['multi_sprites'][id]
            c = monkey.models.multi_sprite(**b)
            return c
        except yaml.YAMLError as exc:
            print(exc)


def character(**kwargs):
    is_player = kwargs.get('player', False)
    #batch = kwargs.get('batch', globals.main_batch)

    size = kwargs['size']

    speed = kwargs['speed']
    pal = kwargs.get('pal', 0)
    jump_height = kwargs.get('jump_height', 80)
    fall = kwargs.get('fall_anim', None)
    print(size, 'sticaz', jump_height, fall)
    tta = kwargs.get('time_to_jump_apex', 0.5)
    controller_mask_up = kwargs.get('controller_mask_up', flags.platform)
    controller_mask_down = kwargs.get('controller_mask_down', flags.platform | flags.platform_passthrough)
    node = sprite(**kwargs)
    coll_flag = flags.player if is_player else flags.foe
    coll_mask = flags.foe if is_player else flags.player
    coll_tag = tags.player if is_player else kwargs['tag']
    coll_shape = kwargs.get('collision_shape', None)
    if coll_shape:
        node.add_component(monkey.collider(coll_shape, coll_flag, coll_mask, coll_tag))
    else:
        node.add_component(monkey.sprite_collider(coll_flag, coll_mask, coll_tag))
    node.add_component(monkey.controller_2d(size=size, center=kwargs.get('center', None),
                                            mask_up=controller_mask_up, mask_down=controller_mask_down))
    node.add_component(monkey.dynamics())
    sm = monkey.state_machine(gravity=globals.gravity, jump_height=jump_height,
                              time_to_jump_apex=tta, speed=speed, acc_time=0.1)
    if is_player:
        globals.internal.player_id = node.id
        can_climb = kwargs.get('climb', False)      # so far climb only for players... sorry
        walk_keys = kwargs.get('walk_keys', None)
        #print(walk_keys)
        sm.add('walk', monkey.walk_2d_player(), keys=walk_keys, fall_anim=fall)
            #"walk", speed=speed, gravity=globals.gravity, jump_height=jump_height,
            #time_to_jump_apex=tta, keys=walk_keys))
        #reference_cam = globals.state.sprite_batches[0]['cam']
        node.add_component(monkey.follow(monkey.get_camera('main'), (0, 0, 5), (0, 1, 0)))
        if can_climb:
            sm.add('climb', monkey.climb(), anim='climb', anim_idle='climb_idle') #"climb", speed=kwargs.get('climb_speed', speed), anim='climb', anim_idle='climb_idle',
                                #mask_up = flags.platform | flags.ladder_stop, mask_down = flags.platform | flags.platform_passthrough))
    else:
        flip = kwargs.get('flip', True)
        flip_on_edge = kwargs.get('flip_on_edge', True)
        sm.add(monkey.walk_2d_foe("walk", speed=speed, flip=flip, flip_on_edge=flip_on_edge,
            gravity=globals.gravity, jump_height=jump_height, time_to_jump_apex=tta, jump_anim=kwargs.get('jump_anim', 'walk'),
            idle_anim=kwargs.get('idle_anim', 'idle'), walk_anim = kwargs.get('walk_anim', 'walk')))
    sm.set_initial_state("walk")
    node.add_component(sm)
    return node




