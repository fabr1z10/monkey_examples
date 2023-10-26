#!/usr/bin/python3

import json
import glob
import argparse
import csv

# plan quality analysis
parser = argparse.ArgumentParser(description='Plan Quality Analysis.')
parser.add_argument('directory')
args = parser.parse_args()



planFilenamesList = glob.glob(args.directory +'/*_Plan.json')
if not planFilenamesList:
    print ('no plan files here.')
    exit(1)

planFilenamesList.sort()

# csv data
rows = []


class StationInfo:
    def __init__(self, id, timeIn, timeOut):
        self.id =id
        self.timeIn=timeIn
        self.timeOut = timeOut

    def __contains__(self, item):
        return item == self.id
    def __repr__(self):
        return self.id + ', ' + str(self.timeIn) + ', ' + str(self.timeOut)

def get_stations(schedule, now):
    stations = []
    for s in schedule:
        if 'station_route' in s:
            current = s['station_route']['station_id']
            if not stations or stations[-1].id != current:
                stations.append(StationInfo(current, s['time_in']-now, s['time_out']-now))
            else:
                stations[-1].timeOut = s['time_out']-now
    return stations

for file in planFilenamesList:
    # Opening JSON file
    f = open(file)
    print(' --- ',file)
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    res =data['result_code']
    row = {'file': file, 'result_code': res}
    now = data['planner_output']['status_time']
    row['status_time'] = now
    if res == 'NO_ERROR':
        tt = data['planner_output']['trains']
        for train in tt:
            if train['id'] == " ZBRG2B  10022023":
                for schedule in train['schedules']:
                    if 'station_route' in schedule and schedule['station_route']['station_id'] == '368':
                         print(file, '368', schedule['station_route']['route_id'], schedule.get('dwell', None))
                         break
                    #if 'track_circuit_id' in schedule and schedule['track_circuit_id'] == '633.2':
                    #    print('il treo passa qui e fa dwell di ', schedule.get('dwell', None))