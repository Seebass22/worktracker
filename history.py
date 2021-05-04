import json
import os.path
from datetime import datetime, timedelta

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
            try:
                data = json.load(infile)
            except json.decoder.JSONDecodeError:
                return('invalid json file')

    else:
        return('no history file')

    if date_string not in data:
        return('no work')

    today = data[date_string]
    total_seconds = 0

    outstring = ''
    for activity, seconds in today.items():
        total_seconds += seconds
        time_string = to_time_string(seconds)
        outstring += f'{activity}: {time_string}\n'

    total_string = to_time_string(total_seconds)
    outstring += f'\ntotal: {total_string}'
    return outstring


def today(json_file):
    current_date = datetime.now().strftime('%Y-%m-%d')
    return summarize_day(json_file, current_date)


def yesterday(json_file):
    today = datetime.now()
    yesterday = (today - timedelta(days=1)).strftime('%Y-%m-%d')
    return summarize_day(json_file, yesterday)
