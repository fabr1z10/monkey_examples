import monkey
from enum import Enum


title = 'ciao'

window_size = (256, 224)
device_size = (256, 224)

start_position = 0

room = 'prova'

shaders = [monkey.SHADER_BATCH]
clear_color = [0, 174/255.0, 1.0, 1.0]
gravity = 500

# player speed
speed = 200


class Sword(Enum):
    NO = 0
    GRADIUS = 1
    BROAD = 2
    GREAT = 3
    EXCALIBUR = 4
    LEGEND = 5


class Shield(Enum):
    NO = 0
    LIGHT = 1
    KNIGHT = 2
    HARD = 3
    LEGEND = 4


class Armour(Enum):
    NO = 0
    LIGHT = 1
    KNIGHT = 2
    HEAVY = 3
    HARD = 4
    LEGEND = 5


class Boots(Enum):
    NO = 0
    CLOTH = 1
    LEATHER = 2
    CERAMIC = 3
    LEGEND = 4


boots_sprite = {
    Boots.NO: ('boots_no', 0),
    Boots.CLOTH: ('boots_leather', 1),
    Boots.LEATHER: ('boots_leather', 0),
    Boots.CERAMIC: ('boots_leather', 2),
    Boots.LEGEND: ('boots_leather', 3)

}


sword = Sword.NO
shield = Shield.NO
armour = Armour.NO
boots = Boots.CERAMIC




class Keys:
    FIRE = 68
    UP = 265
