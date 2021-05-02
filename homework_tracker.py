import argparse
import os.path
import time

statusfile = 'status.txt'


def write_time():
    current_time = int(time.time())

    f = open(statusfile, 'w')
    f.write('started\n')
    f.write(str(current_time))
    f.write('\n')
    f.close()


def start():
    if os.path.isfile(statusfile):
        with open(statusfile) as f:
            data = f.readlines()

        if data[0] == 'started\n':
            print('already started')
        else:
            write_time()
    else:
        write_time()


def calculate_time_difference(data):
    start_time = int(data[1].rstrip('\n'))
    current_time = int(time.time())
    time_difference = current_time - start_time
    return time_difference


def stop():
    if os.path.isfile(statusfile):
        with open(statusfile, 'r') as f:
            data = f.readlines()

        if data[0] == 'started\n':
            time_difference = calculate_time_difference(data)

            print(time_difference)
            with open(statusfile, 'w') as f:
                f.write('stopped\n')
        else:
            print('already stopped')
    else:
        print('already stopped')


def status():
    if os.path.isfile(statusfile):
        with open(statusfile, 'r') as f:
            data = f.readlines()

        if data[0] == 'started\n':
            time_difference = calculate_time_difference(data)
            print('working for {s} seconds'.format(s=time_difference))
        else:
            print('stopped')
    else:
        print('stopped')


def main():
    parser = argparse.ArgumentParser(description='track your work')
    parser.add_argument('command', help='start, stop, status')
    parser.add_argument('--verbose', help='display verbose output')
    args = parser.parse_args()

    if args.command == 'start':
        start()
    elif args.command == 'stop':
        stop()
    elif args.command == 'status':
        status()
    else:
        print('not a command')


if __name__ == '__main__':
    main()
