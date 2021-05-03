import json
import os.path
import datetime

def to_time_string(seconds):
    outstring = ''
    hours = 0
    minutes = 0
    if seconds >= 3600:
        hours = seconds // 3600
        seconds = seconds % 3600
        outstring += f'{hours}h'
    if seconds > 60:
        minutes = seconds // 60
        seconds = seconds % 60

    if hours > 0 or minutes > 0:
        outstring += f' {minutes}m'

    if seconds > 0:
        outstring += f' {seconds}s'

    outstring = outstring.strip()
    return outstring


def summarize_day(json_file, date_string):
    if os.path.isfile(json_file):
        with open(json_file, 'r') as infile:
            data = json.load(infile)
    else:
        print('no history file')
        return

    if date_string not in data:
        print('no work')
        return

    today = data[date_string]
    total_seconds = 0

    for activity, seconds in today.items():
        total_seconds += seconds
        time_string = to_time_string(seconds)
        print(f'{activity}: {time_string}')

    total_string = to_time_string(total_seconds)
    print(f'\ntotal: {total_string}')


def today(json_file):
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    summarize_day(json_file, current_date)
