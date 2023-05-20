from . import settings

def on_restart():
    settings.invincible = False
    settings.current_door =None
    settings.held_item = None
    settings.pickup_item = None
    settings.pickup_platform_item = dict()
    settings.active_door=None