import yaml
from . import settings



def init():
    with open("game/worlds/common.yaml", "r") as stream:
        try:
            data = yaml.safe_load(stream)
            for key, value in data['tiles'].items():
                settings.tiles[key] = value
            for key, value in data['multi_tiles'].items():
                settings.multi_tiles[key] =value
        except yaml.YAMLError as exc:
            print(exc)