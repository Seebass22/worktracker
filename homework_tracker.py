#!/usr/bin/python
import argparse
import os.path
import time

statusfile = 'status.txt'


def write_time(activity):
    current_time = int(time.time())

    f = open(statusfile, 'w')
    f.write('started\n')
    f.write(str(current_time))
    f.write('\n')

    if (activity != ''):
        f.write(activity)
        f.write('\n')

    f.close()


def start(activity):
    if os.path.isfile(statusfile):
        with open(statusfile) as f:
            data = f.readlines()

        if data[0] == 'started\n':
            print('already started')
        else:
            write_time(activity)
    else:
        write_time(activity)


def calculate_time_difference(data):
    start_time = int(data[1].rstrip('\n'))
    current_time = int(time.time())
    time_difference = current_time - start_time
    return time_difference


def stop():
    time_difference, activity = get_status()
    if time_difference:
        if activity:
            print(f'worked on {activity} for {time_difference} seconds')
        else:
            print(f'worked for {time_difference} seconds')

        with open(statusfile, 'w') as f:
            f.write('stopped\n')

    else:
        print('already stopped')


def get_status():
    activity = None
    time_difference = 0

    if os.path.isfile(statusfile):
        with open(statusfile, 'r') as f:
            data = f.readlines()

        if data[0] == 'started\n':
            time_difference = calculate_time_difference(data)
            if len(data) == 3:
                activity = data[2].rstrip('\n')
        else:
            time_difference = 0

        return time_difference, activity
    else:
        return 0, activity


def status():
    time_difference, activity = get_status()
    if time_difference:
        if activity:
            print(f'working on {activity} for {time_difference} seconds')
        else:
            print(f'working for {time_difference} seconds')
    else:
        print('stopped')


def main():
    parser = argparse.ArgumentParser(description='track your work')
    group = parser.add_mutually_exclusive_group()

    group.add_argument('-s', '--start', nargs='?', const='',
                       metavar='activity', help='start tracking')

    group.add_argument('-k', '--stop', help='stop tracking',
                       action='store_true')

    group.add_argument('--status', help='display status', action='store_true')
    args = parser.parse_args()

    if args.start is not None:
        start(args.start)
    elif args.stop:
        stop()
    else:
        status()


if __name__ == '__main__':
    main()
