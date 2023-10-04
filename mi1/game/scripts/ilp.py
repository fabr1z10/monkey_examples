from game.scripts.helper import _dl
import monkey_toolkit.scumm.actions as sa
import monkey
from .. import settings

def dial_ilp_1_10(s):
    s.add(sa.say(tag='player', line=1178))
    s.add(sa.say(tag='scummbar_important_pirate1', line=1181))

def dial_ilp_1_30(s):
    s.add(sa.say(tag='player', line=1180))
    s.add(sa.say(tag='scummbar_important_pirate1', line=1181))

def dial_ilp_1_20(s):
    s.add(sa.say(tag='player', line=1179))
    s.add(sa.say(tag='scummbar_important_pirate1', line=1183))
    s.add(sa.say(tag='scummbar_important_pirate2', line=1184))
    s.add(sa.say(tag='scummbar_important_pirate3', line=1185))
    s.add(sa.say(tag='scummbar_important_pirate1', line=1186))
    s.add(sa.say(tag='scummbar_important_pirate3', line=1187))
    s.add(sa.say(tag='scummbar_important_pirate1', line=1188))
    s.add(sa.say(tag='scummbar_important_pirate1', line=1189))
    s.add(sa.say(tag='player', line=1190))
    s.add(sa.say(tag='scummbar_important_pirate1', line=1191))
    s.add(sa.say(tag='scummbar_important_pirate1', line=1192))
    a1 = s.add(sa.say(tag='scummbar_important_pirate3', line=1193))
    s.add(sa.say(tag='scummbar_important_pirate1', line=1194), after=[a1])
    s.add(sa.say(tag='scummbar_important_pirate2', line=1194), after=[a1])
    s.add(sa.say(tag='scummbar_important_pirate3', line=1194), after=[a1])
    s.add(sa.say(tag='player', line=1195))
    s.add(sa.say(tag='player', line=1196))
    s.add(sa.say(tag='scummbar_important_pirate2', line=1197))
    s.add(sa.say(tag='scummbar_important_pirate1', line=1198))
    s.add(sa.say(tag='scummbar_important_pirate2', line=1199))
    s.add(sa.say(tag='scummbar_important_pirate3', line=1200))
    s.add(sa.say(tag='scummbar_important_pirate2', line=1201))
    s.add(sa.say(tag='scummbar_important_pirate3', line=1202))
    s.add(sa.say(tag='scummbar_important_pirate2', line=1203))
    s.add(sa.say(tag='scummbar_important_pirate2', line=1204))
    s.add(sa.say(tag='scummbar_important_pirate2', line=1205))
    s.add(sa.say(tag='scummbar_important_pirate2', line=1206))
    a2 = s.add(sa.say(tag='scummbar_important_pirate1', line=1207))
    s.add(sa.say(tag='scummbar_important_pirate1', line=1208), after=[a2])
    s.add(sa.say(tag='scummbar_important_pirate2', line=1208), after=[a2])
    s.add(sa.say(tag='scummbar_important_pirate3', line=1208), after=[a2])


def dial_ilp_2_10(s):
    s.add(sa.say(tag='player', line=1209))
    s.add(sa.say(tag='scummbar_important_pirate1', line=1215))
    s.add(sa.say(tag='scummbar_important_pirate1', line=1216))
    s.add(sa.say(tag='scummbar_important_pirate1', line=1217))
    s.add(sa.say(tag='scummbar_important_pirate1', line=1218))
    s.add(sa.say(tag='scummbar_important_pirate1', line=1219))
    s.add(sa.say(tag='scummbar_important_pirate3', line=1220))
    a1 = s.add(sa.say(tag='scummbar_important_pirate3', line=1221))
    s.add(sa.say(tag='scummbar_important_pirate1', line=1222), after=[a1])
    s.add(sa.say(tag='scummbar_important_pirate2', line=1222), after=[a1])
    s.add(sa.say(tag='scummbar_important_pirate3', line=1222), after=[a1])

def dial_ilp_2_11(s):
    s.add(sa.say(tag='player', line=1223))
    s.add(sa.say(tag='scummbar_important_pirate1', line=1215))
    s.add(sa.say(tag='scummbar_important_pirate1', line=1216))
    s.add(sa.say(tag='scummbar_important_pirate1', line=1217))
    s.add(sa.say(tag='scummbar_important_pirate3', line=1224))

def dial_ilp_2_20(s):
    s.add(sa.say(tag='player', line=1210))
    s.add(sa.say(tag='scummbar_important_pirate2', line=1225))
    s.add(sa.say(tag='scummbar_important_pirate1', line=1226))
    s.add(sa.say(tag='scummbar_important_pirate3', line=1227))
    s.add(sa.say(tag='scummbar_important_pirate2', line=1228))
    s.add(sa.say(tag='scummbar_important_pirate1', line=1229))
    s.add(sa.say(tag='scummbar_important_pirate3', line=1230))
    s.add(sa.say(tag='scummbar_important_pirate1', line=1231))
    s.add(sa.say(tag='scummbar_important_pirate1', line=1232))

def dial_ilp_2_21(s):
    s.add(sa.say(tag='player', line=1233))
    s.add(sa.say(tag='scummbar_important_pirate2', line=1228))
    s.add(sa.say(tag='scummbar_important_pirate1', line=1229))
    s.add(sa.say(tag='scummbar_important_pirate3', line=1230))
    s.add(sa.say(tag='scummbar_important_pirate1', line=1231))
    s.add(sa.say(tag='scummbar_important_pirate1', line=1232))