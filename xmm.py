#!/usr/bin/env python3
# z@xnz.me
#
# TODO: exception handling
# TODO: Inspection of packages

import argparse
import configparser
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import pickle
from plugins import pluginbase
from plugins import pluginloader

config_file = 'config.ini'
config = {}
plugins = {}
repo_data = {}


def main():

    global config
    global repo_data

    config = read_config(config_file)
    pluginbase.set_config(config)
    args = parse_args()

    # print(args)

    if args.command == 'search':
        search_maps(args)

    if args.command == 'save':
        db_export_packages(args)

    if args.command == 'install':
        install_maps(args)

    if args.command == 'remove':
        remove_maps(args)

    if args.command == 'update':
        update_repo_data()

    # Plugins
    for cmd, value in plugins.items():
        if args.command == cmd:
            plugins[cmd].run()
            break


def search_maps(args):

    # Get the api data
    if not os.path.isfile(config['api_data']):
        print(bcolors.FAIL + config['api_data'] + ' not found. Trying running update.' + bcolors.ENDC)
        raise SystemExit

    filtered_maps_json = get_repo_data()
    criteria = []

    # Filter based on args
    if args.gametype:
        filtered_maps_json = [x for x in filtered_maps_json if args.gametype in str(x['gametypes'])]
        criteria.append(('gametype', args.gametype))

    if args.pk3:
        filtered_maps_json = [x for x in filtered_maps_json if args.pk3 in str(x['pk3'])]
        criteria.append(('pk3', args.pk3))

    if args.author:
        filtered_maps_json = [x for x in filtered_maps_json if args.author in str(x['author'])]
        criteria.append(('author', args.author))

    if args.title:
        filtered_maps_json = [x for x in filtered_maps_json if args.title in str(x['title'])]
        criteria.append(('title', args.title))

    if args.shasum:
        filtered_maps_json = [x for x in filtered_maps_json if args.shasum in str(x['shasum'])]
        criteria.append(('shasum', args.shasum))

    # Handle search string
    if args.string:
        search_string = args.string
        print(bcolors.HEADER + 'Searching for packages names matching: ' + bcolors.ENDC + bcolors.BOLD + search_string + bcolors.ENDC)
    else:
        search_string = ''

    if len(criteria) > 0:
        print(bcolors.HEADER + 'Searching for packages with the following criteria:' + bcolors.ENDC)
        for c in criteria:
            print(bcolors.BOLD + c[0] + bcolors.ENDC + ': ' + c[1])

    # Print out all matching packages
    total = 0

    for m in filtered_maps_json:
        bsps = m['bsp']
        keys = list(bsps)
        keys.sort()

        for bsp in keys:
            if re.search('^.*' + search_string + '.*$', bsp):
                print('')
                if not args.long:
                    print(bcolors.BOLD + m['pk3'] + bcolors.ENDC)
                    print(bcolors.OKBLUE + bsp + bcolors.ENDC)
                    print(config['repo_url'] + m['pk3'])
                else:
                    print('         pk3: ' + bcolors.BOLD + str(m['pk3']) + bcolors.ENDC)
                    print('         bsp: ' + bcolors.OKBLUE + bsp + bcolors.ENDC)
                    print('       title: ' + str(m['title']))
                    print(' description: ' + str(m['description']))
                    print('      author: ' + str(m['author']))
                    print('      shasum: ' + str(m['shasum']))
                    print('        date: ' + time.strftime('%Y-%m-%d', time.localtime(m['date'])))
                    print('        size: ' + convert_size(m['filesize']).strip())
                    print('          dl: ' + config['repo_url'] + m['pk3'])
                total += 1

    print('\n' + bcolors.OKBLUE + 'Total packages found:' + bcolors.ENDC + ' ' + bcolors.BOLD + str(total) + bcolors.ENDC)


def install_maps(args):

    map_dir = args.T if args.T else config['map_dir']

    is_url = False
    if re.match('^(ht|f)tp(s)?://', args.pk3):
        url = args.pk3
        pk3 = os.path.basename(url)
        is_url = True
    else:
        pk3 = args.pk3
        url = config['repo_url'] + pk3

    pk3_with_path = os.path.join(os.path.dirname(map_dir), pk3)

    print('Installing map from repository: ' + bcolors.BOLD + pk3 + bcolors.ENDC)

    maps_json = get_repo_data()
    map_in_repo = False
    for m in maps_json:
        if m['pk3'] == pk3 or is_url:
            db_add_package(m['shasum'], m['pk3'])
            add_map(pk3_with_path, url)
            map_in_repo = True
            break

    if not map_in_repo:
        print(bcolors.FAIL + 'package does not exist in the repository.' + bcolors.ENDC)
        raise SystemExit


def add_map(pk3_with_path, url):

    if not os.path.exists(pk3_with_path):

        if config['use_curl'] == 'False':
            urllib.request.urlretrieve(url, pk3_with_path, reporthook)
        else:
            subprocess.call(['curl', '-o', pk3_with_path, url])

        print(bcolors.OKBLUE + 'Done.' + bcolors.ENDC)

    else:
        print(bcolors.FAIL + 'package already exists, please remove first.' + bcolors.ENDC)
        raise SystemExit


def remove_maps(args):

    pk3 = args.pk3
    map_dir = args.T if args.T else config['map_dir']

    print('Removing package: ' + bcolors.BOLD + pk3 + bcolors.ENDC)

    if os.path.exists(map_dir):
        pk3_with_path = os.path.join(os.path.dirname(map_dir), pk3)

        if os.path.exists(pk3_with_path):
            os.remove(pk3_with_path)

            repo_data = get_repo_data()

            for m in repo_data:
                if m['pk3'] == pk3:
                    db_remove_package(str(m['shasum']), str(m['pk3']))

            print(bcolors.OKBLUE + 'Done.' + bcolors.ENDC)
        else:
            print(bcolors.FAIL + 'package does not exist.' + bcolors.ENDC)
            raise SystemExit

    else:
        print(bcolors.FAIL + 'directory does not exist.' + bcolors.ENDC)
        raise SystemExit


# remote data
def update_repo_data():
    print('Updating sources json...')
    urllib.request.urlretrieve(config['api_data_url'], config['api_data'], reporthook)
    print(bcolors.OKBLUE + 'Done.' + bcolors.ENDC)


def get_repo_data():

    global repo_data

    if not repo_data:
        f = open(config['api_data'])
        data = f.read()
        repo_data = json.loads(data)['data']
        f.close()

    return repo_data


# local data
def get_package_db():

    if file_is_empty(config['package_store']):
        package_store = {}
    else:
        db = open(config['package_store'], 'rb')
        package_store = pickle.load(db)
        db.close()

    return package_store


def db_add_package(shasum, pk3):

    # shasum + pk3 need to be used together to be unique
    # this should be hashed into a shorter/safer key
    data = { shasum + pk3: '1' }

    package_store = []

    if os.path.exists(config['package_store']):
        if not file_is_empty(config['package_store']):
            db_in = open(config['package_store'], 'rb+')
            package_store = pickle.load(db_in)
            package_store.append(data)
            db_in.close()
    else:
        package_store = [ data ]

    db_out = open(config['package_store'], 'wb+')
    pickle.dump(package_store, db_out)
    db_out.close()


def db_remove_package(shasum, pk3):

    package_store = []

    if not file_is_empty(config['package_store']):
        db_in = open(config['package_store'], 'rb+')
        package_store = pickle.load(db_in)
        package_store[:] = [d for d in package_store if d.get(shasum + pk3) == 1]
        db_in.close()

    db_out = open(config['package_store'], 'wb+')
    pickle.dump(package_store, db_out)
    db_out.close()


def db_export_packages(args):

    data = get_package_db()
    package_store = json.dumps(data)

    f = open(args.file, 'w')
    f.write(package_store)
    f.close()


def file_is_empty(path):
    return os.stat(path).st_size == 0


def convert_size(num):
    for x in ['B', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1d%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')


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


def read_config(config_file):

    if not os.path.isfile(config_file):
        print(bcolors.FAIL + config_file + ' not found, please create one.' + bcolors.ENDC)
        raise SystemExit

    conf = configparser.ConfigParser()
    conf.read(config_file)

    return conf['default']


def parse_args():

    global plugins

    parser = argparse.ArgumentParser(description='Xonotic Map Manager is a tool to help manage Xonotic maps',
                                     epilog="Very early alpha. Please be patient.")

    parser.add_argument("-T", nargs='?', help="target directory", type=str)

    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    parser_search = subparsers.add_parser('search', help='search for maps based on bsp names')
    parser_search.add_argument('string', nargs='?', help='bsp name found in a package, works on packages with many bsps', type=str)
    parser_search.add_argument('--gametype', '-g', nargs='?', help='filter by gametype', type=str)
    parser_search.add_argument('--pk3', '-p', nargs='?', help='filter by pk3 name', type=str)
    parser_search.add_argument('--title', '-t', nargs='?', help='filter by title', type=str)
    parser_search.add_argument('--author', '-a', nargs='?', help='filter by author', type=str)
    parser_search.add_argument('--shasum', '-s', nargs='?', help='filter by shasum', type=str)
    parser_search.add_argument('--long', '-l', help='show long format', action='store_true')

    parser_add = subparsers.add_parser('install', help='install a map from the repository, or specify a URL.')
    parser_add.add_argument('pk3', nargs='?', help='use a pk3 name', type=str)

    parser_remove = subparsers.add_parser('remove', help='remove based on pk3 name')
    parser_remove.add_argument('pk3', nargs='?', help='pk3', type=str)

    parser_update = subparsers.add_parser('update', help='update sources json')

    parser_remove = subparsers.add_parser('save', help='export locally managed packages to a file')
    parser_remove.add_argument('--type', '-t', nargs='?', help='type to export: db, flat', type=str)
    parser_remove.add_argument('file', nargs='?', help='file name to export to', type=str)

    # Handle plugins
    for i in pluginloader.get_plugins():
        #print("Loading plugin: " + i["name"])
        command = i['name']
        plugin = pluginloader.load_plugin(i)
        plugin_args = [plugin.get_args()]
        plugins[command] = plugin

        # Import args from plugins
        for p in plugin_args:
            parser_plugin = subparsers.add_parser(p[0], **p[1])
            parser_plugin.add_argument(*p[2], **p[3])

    return parser.parse_args()


if __name__ == "__main__":
    main()
