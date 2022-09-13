import monkey

gravity = 500
mario_speed = 200
mario_state = 1
invincible = False
invincible_duration = 5
warp = 0
player_id = -1
start_position = 0
cn = None
main_cam = None
room_details = dict()
score = 0
coins = 0
world_name = '1-1'
time = 400
coin_label = 0

mario_states = [
    {'model': 'sprites/mario', 'size': monkey.vec3(10, 14, 0), 'center': monkey.vec3(5, 0, 0)},
    {'model': 'sprites/supermario', 'size': monkey.vec3(10, 30, 0), 'center': monkey.vec3(5, 0, 0)},
    {'model': 'sprites/fierymario', 'size': monkey.vec3(10, 30, 0), 'center': monkey.vec3(5, 0, 0)}
]
