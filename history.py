import json
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


def format_summary(data):
    total_seconds = 0

    outstring = ''
    for activity, seconds in data.items():
        total_seconds += seconds
        time_string = to_time_string(seconds)
        outstring += f'{activity}: {time_string}\n'

    total_string = to_time_string(total_seconds)
    outstring += f'\ntotal: {total_string}'
    return outstring


def summarize_day(json_file, date_string):
    if json_file.exists():
        with json_file.open('r') as infile:
            try:
                data = json.load(infile)
            except json.decoder.JSONDecodeError:
                return('invalid json file')
    else:
        return('no history file')

    if date_string not in data:
        return('no work')

    today = data[date_string]
    return format_summary(today)


def summarize_days(json_file, starting_date, days):
    if json_file.exists():
        with json_file.open('r') as infile:
            try:
                data = json.load(infile)
            except json.decoder.JSONDecodeError:
                return('invalid json file')
    else:
        return('no history file')

    summary_data = {}
    date = datetime.strptime(starting_date, '%Y-%m-%d')

    for _ in range(days):
        date_string = date.strftime('%Y-%m-%d')

        if date_string in data:
            for activity in data[date_string].keys():
                if activity in summary_data:
                    summary_data[activity] += data[date_string][activity]
                else:
                    summary_data[activity] = data[date_string][activity]
        date -= timedelta(days=1)

    return format_summary(summary_data)


def today(json_file):
    current_date = datetime.now().strftime('%Y-%m-%d')
    return summarize_day(json_file, current_date)


def yesterday(json_file):
    today = datetime.now()
    yesterday = (today - timedelta(days=1)).strftime('%Y-%m-%d')
    return summarize_day(json_file, yesterday)


def days_ago(json_file, days):
    today = datetime.now()
    date = (today - timedelta(days=days)).strftime('%Y-%m-%d')
    return summarize_day(json_file, date)


def week(json_file):
    current_date = datetime.now().strftime('%Y-%m-%d')
    return summarize_days(json_file, current_date, 7)
