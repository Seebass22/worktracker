import json
import os.path
import datetime

def update_json_file(activity, time_difference):
    json_file = 'history.json'

    current_date = datetime.datetime.now().strftime('%Y-%m-%d')

    if os.path.isfile(json_file):
        with open(json_file, 'r') as infile:
            a = json.load(infile)
    else:
        a = dict()

    if current_date in a:
        if activity in a[current_date]:
            past_time = int(a[current_date][activity])
            new_time = past_time + time_difference
            a[current_date][activity] = new_time
        else:
            a[current_date][activity] = time_difference
    else:
        a[current_date] = { activity: time_difference }


    with open(json_file, 'w') as output:
        json.dump(a, output, indent=4)
