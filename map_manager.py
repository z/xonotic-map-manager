#!/usr/bin/env python3
# z@xnz.me
import configparser
import argparse
import os
import re
import json
import time
import urllib.request
import subprocess
import sys

config_file = 'config.ini'
config = {}


def main():
    global config

    config = read_config()
    args = parse_args()

    # print(args)

    if args.command == 'search':
        search_maps(args)

    if args.command == 'add':
        add_maps(args.url)

    if args.command == 'remove':
        remove_maps(args.pk3)

    if args.command == 'update':
        update_data()


def search_maps(args):
    if not os.path.isfile(config['api_data']):
        print(bcolors.FAIL + config['api_data'] + ' not found. Trying running update.' + bcolors.ENDC)
        raise SystemExit

    f = open(config['api_data'])
    data = f.read()
    maps_json = json.loads(data)['data']
    f.close()

    filtered_maps_json = maps_json

    if args.gametype:
        filtered_maps_json = [x for x in filtered_maps_json if args.gametype in str(x['gametypes'])]

    if args.author:
        filtered_maps_json = [x for x in filtered_maps_json if args.author in str(x['author'])]

    if args.string:
        search_string = args.string
    else:
        search_string = ''

    print('Searching for: ' + bcolors.BOLD + search_string + bcolors.ENDC)

    for m in filtered_maps_json:
        bsps = m['bsp']
        keys = list(bsps)
        keys.sort()

        for bsp in keys:
            if re.search('^.*' + search_string + '.*$', bsp):
                print(bcolors.BOLD + bsp + bcolors.ENDC)
                print(config['repo_url'] + m['pk3'])


def add_maps(url):
    print('Adding map: ' + bcolors.BOLD + url + bcolors.ENDC)

    pk3 = os.path.basename(url)
    pk3_with_path = os.path.join(os.path.dirname(config['map_dir']), pk3)

    if not os.path.exists(pk3_with_path):

        if config['use_curl'] == 'False':
            urllib.request.urlretrieve(url, pk3_with_path, reporthook)
        else:
            subprocess.call(['curl', '-o', pk3_with_path, url])

        print(bcolors.OKBLUE + 'Done.' + bcolors.ENDC)
        
    else:
        print(bcolors.FAIL + 'map already exists, please remove first.' + bcolors.ENDC)


def remove_maps(pk3):
    print('Removing map: ' + bcolors.BOLD + pk3 + bcolors.ENDC)

    pk3_with_path = os.path.join(os.path.dirname(config['map_dir']), pk3)

    if os.path.exists(pk3_with_path):
        os.remove(pk3_with_path)
        print(bcolors.OKBLUE + 'Done.' + bcolors.ENDC)

    else:
        print(bcolors.FAIL + 'map does not exist.' + bcolors.ENDC)


def update_data():
    print('Updating sources json.')
    urllib.request.urlretrieve(config['api_data_url'], config['api_data'], reporthook)
    print(bcolors.OKBLUE + 'Done.' + bcolors.ENDC)

def reporthook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed. " %
                    (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def read_config():
    global config_file

    if not os.path.isfile(config_file):
        print(bcolors.FAIL + config_file + ' not found, please create one.' + bcolors.ENDC)
        raise SystemExit

    conf = configparser.ConfigParser()

    conf.read(config_file)

    return conf['default']


def parse_args():
    parser = argparse.ArgumentParser(description='A tool to help manage xonotic maps',
                                     epilog="Very early alpha. Please be patient.")

    subparsers = parser.add_subparsers(help='sub-command help', dest='command')
    subparsers.required = True

    parser_search = subparsers.add_parser('search', help='search for maps based on bsp names')
    parser_search.add_argument('string', nargs='?', help='string', type=str)
    parser_search.add_argument('--gametype', nargs='?', help='gametype', type=str)
    parser_search.add_argument('--author', nargs='?', help='author', type=str)

    parser_add = subparsers.add_parser('add', help='add a map based on url')
    parser_add.add_argument('url', nargs='?', help='url', type=str)

    parser_remove = subparsers.add_parser('remove', help='remove based on pk3 name')
    parser_remove.add_argument('pk3', nargs='?', help='pk3', type=str)

    parser_update = subparsers.add_parser('update', help='update sources json')

    return parser.parse_args()


if __name__ == "__main__":
    main()
