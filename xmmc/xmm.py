#!/usr/bin/env python3
# z@xnz.me
#
# TODO: exception handling / file exists checks
# TODO: Inspection of packages

import argparse
import argcomplete # still figuring this out
import json
import os
import pickle
import re
import subprocess
import time
import urllib.request

from xmmc.plugins import pluginbase
from xmmc.plugins import pluginloader
from . import util

bcolors = util.bcolors

config = {}
plugins = {}
repo_data = {}


def main():

    global config
    global repo_data

    config_file = '.xmm.cfg'
    home = os.path.expanduser('~')
    config_file_with_path = os.path.join(home, config_file)

    util.check_if_not_create(config_file_with_path, 'config/xmm.cfg')

    config = util.parse_config(config_file_with_path)
    pluginbase.set_config(config)
    args = parse_args()

    # print(args)

    if args.command == 'search':
        search_maps(args)

    if args.command == 'install':
        install_maps(args)

    if args.command == 'remove':
        remove_maps(args)

    if args.command == 'update':
        update_repo_data()

    if args.command == 'list':
        list_installed(args)

    if args.command == 'show':
        show_map(args.pk3, args)

    if args.command == 'export':
        db_export_packages(args)

    # Plugins
    for cmd, value in plugins.items():
        if args.command == cmd:
            plugins[cmd].run()
            break


def search_maps(args):

    maps_json = get_repo_data()
    criteria = []

    # Filter based on args
    if args.gametype:
        maps_json = [x for x in maps_json if args.gametype in str(x['gametypes'])]
        criteria.append(('gametype', args.gametype))

    if args.pk3:
        maps_json = [x for x in maps_json if args.pk3 in str(x['pk3'])]
        criteria.append(('pk3', args.pk3))

    if args.author:
        maps_json = [x for x in maps_json if args.author in str(x['author'])]
        criteria.append(('author', args.author))

    if args.title:
        maps_json = [x for x in maps_json if args.title in str(x['title'])]
        criteria.append(('title', args.title))

    if args.shasum:
        maps_json = [x for x in maps_json if args.shasum in str(x['shasum'])]
        criteria.append(('shasum', args.shasum))

    # Handle search string
    if args.string:
        search_string = args.string
        print('\n' + bcolors.HEADER + 'Searching packages with bsps matching: ' + bcolors.ENDC + bcolors.BOLD + search_string + bcolors.ENDC)
    else:
        search_string = ''

    if len(criteria) > 0:
        print(bcolors.HEADER + 'Searching for packages with the following criteria:' + bcolors.ENDC)
        for c in criteria:
            print(bcolors.BOLD + c[0] + bcolors.ENDC + ': ' + c[1])

    # Print out all matching packages
    total = 0

    for m in maps_json:
        bsps = m['bsp']
        keys = list(bsps)
        keys.sort()

        for bsp in keys:
            if re.search('^.*' + search_string + '.*$', bsp):
                show_map_details(m, args)
                total += 1

    print('\n' + bcolors.OKBLUE + 'Total packages found:' + bcolors.ENDC + ' ' + bcolors.BOLD + str(total) + bcolors.ENDC)


def install_maps(args):

    map_dir = get_map_dir(args)

    installed = False
    is_url = False
    if re.match('^(ht|f)tp(s)?://', args.pk3):
        url = args.pk3
        pk3 = os.path.basename(url)
        is_url = True
    else:
        pk3 = args.pk3
        url = config['repo_url'] + pk3

    pk3_with_path = os.path.join(os.path.dirname(map_dir), pk3)

    maps_json = get_repo_data()
    map_in_repo = False
    for m in maps_json:
        if m['pk3'] == pk3:
            db_add_package(m)
            map_in_repo = True
            break

    if map_in_repo or is_url:
        print('Installing map: ' + bcolors.BOLD + pk3 + bcolors.ENDC)
        add_map(pk3_with_path, url)
        installed = True

    if not map_in_repo:
        if installed:
            print(bcolors.WARNING + 'package does not exist in the repository, ' +
                                    'it won\'t be added to the local database.' + bcolors.ENDC)
        else:
            print(bcolors.FAIL + 'package does not exist in the repository. cannot install.' + bcolors.ENDC)
            raise SystemExit


def add_map(pk3_with_path, url):

    if not os.path.exists(pk3_with_path):

        if config['use_curl'] == 'False':
            urllib.request.urlretrieve(url, pk3_with_path, util.reporthook)
        else:
            subprocess.call(['curl', '-o', pk3_with_path, url])

        print(bcolors.OKBLUE + 'Done.' + bcolors.ENDC)

    else:
        print(bcolors.FAIL + 'package already exists, please remove first.' + bcolors.ENDC)
        raise SystemExit


def remove_maps(args):

    pk3 = args.pk3
    map_dir = get_map_dir(args)

    print('Removing package: ' + bcolors.BOLD + pk3 + bcolors.ENDC)

    if os.path.exists(map_dir):
        pk3_with_path = os.path.join(os.path.dirname(map_dir), pk3)

        if os.path.exists(pk3_with_path):
            os.remove(pk3_with_path)

            repo_data = get_repo_data()

            for m in repo_data:
                if m['pk3'] == pk3:
                    db_remove_package(m)

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
    urllib.request.urlretrieve(config['api_data_url'], os.path.expanduser(config['api_data']), util.reporthook)
    print(bcolors.OKBLUE + 'Done.' + bcolors.ENDC)


def get_repo_data():

    global repo_data

    api_data_file = os.path.expanduser(config['api_data'])

    if not repo_data:
        if not os.path.exists(api_data_file):
            api_data_file = os.path.expanduser(config['api_data'])
            print(bcolors.WARNING + 'Could not find a repo file. Downloading one.' + bcolors.ENDC)
            util.check_if_not_create(api_data_file, './resources/data/maps.json')

        f = open(api_data_file)
        data = f.read()
        repo_data = json.loads(data)['data']
        f.close()

    return repo_data


# local data
def list_installed(args):

    packages = get_package_db()

    total = 0
    for p in packages:
        show_map_details(p, args)
        total += 1

    print('\n' + bcolors.OKBLUE + 'Total packages found:' + bcolors.ENDC + ' ' + bcolors.BOLD + str(total) + bcolors.ENDC)


def show_map(pk3, args):

    packages = get_package_db()
    map_found = False

    for p in packages:
        if p['pk3'] == pk3:
            show_map_details(p, args)
            map_found = True
            print('')

    if not map_found:
        print(bcolors.FAIL + 'Package not currently installed' + bcolors.ENDC)


def show_map_details(m, args):

    bsp = ''
    bsps = m['bsp']
    keys = list(bsps)
    keys.sort()

    for b in keys:
        bsp += b

    if args.long:
        print('')
        print('         pk3: ' + bcolors.BOLD + str(m['pk3']) + bcolors.ENDC)
        print('         bsp: ' + bcolors.OKBLUE + bsp + bcolors.ENDC)
        print('       title: ' + str(m['title']))
        print(' description: ' + str(m['description']))
        print('      author: ' + str(m['author']))
        print('      shasum: ' + str(m['shasum']))
        print('        date: ' + time.strftime('%Y-%m-%d', time.localtime(m['date'])))
        print('        size: ' + util.convert_size(m['filesize']).strip())
        print('          dl: ' + config['repo_url'] + m['pk3'])
    elif args.short:
        print(str(m['pk3']))
    else:
        print('')
        print(bcolors.BOLD + str(m['pk3']) + bcolors.ENDC + ' [' + bcolors.OKBLUE + bsp + bcolors.ENDC + ']')
        print(config['repo_url'] + str(m['pk3']))


def get_package_db():

    global repo_data

    package_store_file  = os.path.expanduser(config['package_store'])

    if os.path.exists(package_store_file ):
        db = open(package_store_file , 'rb')
        package_store = pickle.load(db)
        db.close()
    else:
        print(bcolors.WARNING + 'No package database found (don\'t worry, it will be created when you install a map' + bcolors.ENDC)
        raise SystemExit

    return package_store


def db_add_package(package):

    package_store = []
    package_store_file = os.path.expanduser(config['package_store'])

    if os.path.exists(package_store_file) and not util.file_is_empty(package_store_file ):
        db_in = open(package_store_file , 'rb+')
        package_store = pickle.load(db_in)
        package_store.append(package)
        db_in.close()
    else:
        package_store.append(package)

    db_out = open(package_store_file , 'wb+')
    pickle.dump(package_store, db_out)
    db_out.close()


def get_map_dir(args):
    return args.T if args.T else os.path.expanduser(config['map_dir'])


def db_remove_package(package):

    package_store = []
    package_store_file = os.path.expanduser(config['package_store'])

    if not util.file_is_empty(package_store_file):
        db_in = open(package_store_file, 'rb+')
        package_store = pickle.load(db_in)
        package_store[:] = [m for m in package_store if (m.get('shasum') != package['shasum'] and m.get('pk3') != package['pk3'])]
        db_in.close()

    db_out = open(package_store_file, 'wb+')
    pickle.dump(package_store, db_out)
    db_out.close()


def db_export_packages(args):

    data = get_package_db()
    package_store = json.dumps(data)

    f = open(args.file, 'w')
    f.write(package_store)
    f.close()


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
    parser_search.add_argument('--shasum', nargs='?', help='filter by shasum', type=str)
    parser_search.add_argument('--long', '-l', help='show long format', action='store_true')
    parser_search.add_argument('--short', '-s', help='show short format', action='store_true')

    parser_add = subparsers.add_parser('install', help='install a map from the repository, or specify a URL.')
    parser_add.add_argument('pk3', nargs='?', help='use a pk3 name', type=str)

    parser_remove = subparsers.add_parser('remove', help='remove based on pk3 name')
    parser_remove.add_argument('pk3', nargs='?', help='pk3', type=str)

    parser_update = subparsers.add_parser('update', help='update sources json')

    parser_list = subparsers.add_parser('list', help='list locally installed packages')
    parser_list.add_argument('--long', '-l', help='show long format', action='store_true')
    parser_list.add_argument('--short', '-s', help='show short format', action='store_true')

    parser_show = subparsers.add_parser('show', help='show details of locally installed package')
    parser_show.add_argument('pk3', nargs='?', help='pk3 to show details for', type=str)
    parser_show.add_argument('--long', '-l', help='show long format', action='store_true')
    parser_show.add_argument('--short', '-s', help='show short format', action='store_true')

    parser_export = subparsers.add_parser('export', help='export locally managed packages to a file')
    parser_export.add_argument('--type', '-t', nargs='?', help='type to export: db, flat', type=str)
    parser_export.add_argument('file', nargs='?', help='file name to export to', type=str)

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

    argcomplete.autocomplete(parser)

    return parser.parse_args()


if __name__ == "__main__":
    main()
