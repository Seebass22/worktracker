#!/usr/bin/python
import argparse
import time
from pathlib import Path

import json_exporter
import history
import merge


class worktracker:
    def __init__(self, status_file=None, json_file=None):
        self.init_config()

        if status_file is not None:
            self.status_file = status_file
        if json_file is not None:
            self.json_file = json_file
        self.exporter = json_exporter.json_exporter(self.json_file)

    def init_config(self):
        config_path = Path.home() / '.config/worktracker'
        config_path.mkdir(parents=True, exist_ok=True)
        self.status_file = config_path / 'status.txt'
        self.json_file = config_path / 'history.json'

    def write_time(self, activity):
        current_time = int(time.time())

        f = open(self.status_file, 'w')
        f.write('started\n')
        f.write(str(current_time))
        f.write('\n')

        if (activity != ''):
            f.write(activity)
            f.write('\n')

        f.close()

    def start(self, activity):
        if self.status_file.exists():
            with self.status_file.open('r') as f:
                data = f.readlines()

            if data[0] == 'started\n':
                return 'already started\n'
            else:
                self.write_time(activity)
                return ''
        else:
            self.write_time(activity)
            return ''

    def calculate_time_difference(self, data):
        start_time = int(data[1].rstrip('\n'))
        current_time = int(time.time())
        time_difference = current_time - start_time
        return time_difference

    def stop(self):
        time_difference, activity = self.get_status()
        if time_difference is not None:
            time_string = history.to_time_string(time_difference)
            if activity is not None:
                self.exporter.update_json_file(activity, time_difference)
                ret = f'worked on {activity} for {time_string}'
            else:
                self.exporter.update_json_file('default', time_difference)
                ret = f'worked for {time_string}'

            with open(self.status_file, 'w') as f:
                f.write('stopped\n')
            return ret

        else:
            return 'already stopped'

    # return time spent on current task, activity (None if unspecified)
    # return None, None if stopped
    def get_status(self):
        activity = None
        time_difference = 0

        if self.status_file.exists():
            with self.status_file.open('r') as f:
                data = f.readlines()

            if data[0] == 'started\n':
                time_difference = self.calculate_time_difference(data)
                if len(data) == 3:
                    activity = data[2].rstrip('\n')
            else:
                return None, None

            return time_difference, activity
        else:
            return None, None

    def status(self):
        time_difference, activity = self.get_status()
        if time_difference is not None:
            time_string = history.to_time_string(time_difference)
            if activity is not None:
                return f'working on {activity} for {time_string}'
            else:
                return f'working for {time_string}'
        else:
            return 'stopped'

    def main(self):
        parser = argparse.ArgumentParser(description='track your work')
        group = parser.add_mutually_exclusive_group()

        group.add_argument('--start', nargs='?', const='',
                           metavar='activity', help='start tracking')
        group.add_argument('--stop', help='stop tracking',
                           action='store_true')
        group.add_argument('--status', help='display status',
                           action='store_true')
        group.add_argument('--today', help='display work done today',
                           action='store_true')
        group.add_argument('--yesterday', help='display work done yesterday',
                           action='store_true')
        group.add_argument('--days-ago', metavar='DAYS', type=int,
                           help='display work done DAYS days ago')
        group.add_argument('--date', help='display work done on specific date,\
                           YYYY-MM-DD format')
        group.add_argument('--days', help='display work done the past X days',
                           type=int)
        group.add_argument('--week', help='display work done the past 7 days',
                           action='store_true')
        group.add_argument('--month', help='display work done the past \
                           30 days', action='store_true')
        group.add_argument('--merge', metavar='FILE', help='merge FILE into\
                           current history file')

        args = parser.parse_args()

        if args.start is not None:
            print(self.start(args.start), end='')
        elif args.stop:
            print(self.stop())
        elif args.today:
            print(history.today(self.json_file))
        elif args.yesterday:
            print(history.yesterday(self.json_file))
        elif args.days_ago is not None:
            print(history.days_ago(self.json_file, args.days_ago))
        elif args.days is not None:
            print(history.days(self.json_file, args.days))
        elif args.date is not None:
            print(history.summarize_day(self.json_file, args.date))
        elif args.week:
            print(history.week(self.json_file))
        elif args.month:
            print(history.month(self.json_file))
        elif args.merge is not None:
            merge.merge_json(self.json_file, Path(args.merge))
        elif args.status:
            print(self.status())
        else:
            parser.print_help()


if __name__ == '__main__':
    hw = worktracker()
    hw.main()
