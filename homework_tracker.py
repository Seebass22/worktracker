#!/usr/bin/python
import argparse
import os.path
import time

import json_exporter
import history


class homework_tracker:
    def __init__(self, status_file='status.txt', json_file='history.json'):
        self.status_file = status_file
        self.json_file = json_file
        self.exporter = json_exporter.json_exporter(json_file)

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
        if os.path.isfile(self.status_file):
            with open(self.status_file) as f:
                data = f.readlines()

            if data[0] == 'started\n':
                print('already started')
            else:
                self.write_time(activity)
        else:
            self.write_time(activity)

    def calculate_time_difference(self, data):
        start_time = int(data[1].rstrip('\n'))
        current_time = int(time.time())
        time_difference = current_time - start_time
        return time_difference

    def stop(self):
        time_difference, activity = self.get_status()
        if time_difference:
            if activity:
                print(f'worked on {activity} for {time_difference} seconds')
                self.exporter.update_json_file(activity, time_difference)
            else:
                self.exporter.update_json_file('default', time_difference)
                print(f'worked for {time_difference} seconds')

            with open(self.status_file, 'w') as f:
                f.write('stopped\n')

        else:
            print('already stopped')

    # return time spent on current task, activity (None if unspecified)
    # return 0, None if stopped
    def get_status(self):
        activity = None
        time_difference = 0

        if os.path.isfile(self.status_file):
            with open(self.status_file, 'r') as f:
                data = f.readlines()

            if data[0] == 'started\n':
                time_difference = self.calculate_time_difference(data)
                if len(data) == 3:
                    activity = data[2].rstrip('\n')
            else:
                time_difference = 0

            return time_difference, activity
        else:
            return 0, activity

    def status(self):
        time_difference, activity = self.get_status()
        if time_difference:
            if activity:
                print(f'working on {activity} for {time_difference} seconds')
            else:
                print(f'working for {time_difference} seconds')
        else:
            print('stopped')

    def main(self):
        parser = argparse.ArgumentParser(description='track your work')
        group = parser.add_mutually_exclusive_group()

        group.add_argument('-s', '--start', nargs='?', const='',
                           metavar='activity', help='start tracking')

        group.add_argument('-k', '--stop', help='stop tracking',
                           action='store_true')

        group.add_argument('--status', help='display status',
                           action='store_true')
        group.add_argument('--today', help='display work done today',
                           action='store_true')
        group.add_argument('--date', help='display work done on specific date,\
                           YYYY-MM-DD format')
        args = parser.parse_args()

        if args.start is not None:
            self.start(args.start)
        elif args.stop:
            self.stop()
        elif args.today:
            history.today(self.json_file)
        elif args.date is not None:
            history.summarize_day(self.json_file, args.date)
        else:
            self.status()


if __name__ == '__main__':
    hw = homework_tracker()
    hw.main()
