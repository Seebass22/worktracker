import json
import os.path
import datetime


class json_exporter:
    def __init__(self, json_file='history.json'):
        self.json_file = json_file

    def update_json_file(self, activity, time_difference):

        current_date = datetime.datetime.now().strftime('%Y-%m-%d')

        if os.path.isfile(self.json_file):
            with open(self.json_file, 'r') as infile:
                try:
                    data = json.load(infile)
                except json.decoder.JSONDecodeError:
                    print("invalid json file, couldn't update")
                    return
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
            data[current_date] = {activity: time_difference}

        with open(self.json_file, 'w') as output:
            json.dump(data, output, indent=4)
