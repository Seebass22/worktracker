import json
import os.path
import datetime

def update_json_file(activity, time_difference):
    json_file = 'history.json'

    current_date = datetime.datetime.now().strftime('%Y-%m-%d')

    if os.path.isfile(json_file):
        with open(json_file, 'r') as infile:
            data = json.load(infile)
    else:
        data = dict()

    if current_date in data:
        if activity in data[current_date]:
            past_time = int(data[current_date][activity])
            new_time = past_time + time_difference
            data[current_date][activity] = new_time
        else:
            data[current_date][activity] = time_difference
    else:
        data[current_date] = { activity: time_difference }

    with open(json_file, 'w') as output:
        json.dump(data, output, indent=4)
