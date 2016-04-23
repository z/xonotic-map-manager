#!/usr/bin/env python3
# A tool to help manage Xonotic maps
# z@xnz.me

import argparse
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

    if args.command == 'discover':
        discover_maps(args)

    if args.command == 'list':
        list_installed(args)

    if args.command == 'show':
        show_map(args.pk3, 'installed', args)

    if args.command == 'export':
        db_export_packages(args)

    if args.command == 'update':
        update_repo_data()

    # Plugins
    for cmd, value in plugins.items():
        if args.command == cmd:
            plugins[cmd].run()
            break


def search_maps(args):

    maps_json = get_repo_data()
    fmaps_json = []
    criteria = []

    # Handle search string
    if args.string:
        search_string = args.string
    else:
        search_string = ''

    # Filter based on args
    total = 0
    for m in maps_json:

        show = False
        for bsp in m['bsp']:
            if re.search('^.*' + search_string + '.*$', bsp):
                criteria.append(('bsp', search_string))
                show = True

            if args.gametype in m['bsp'][bsp]['gametypes']:
                criteria.append(('gametype', args.gametype))
                show = True

            if re.search('^.*' + str(args.author) + '.*$', m['bsp'][bsp]['author']):
                criteria.append(('author', args.author))
                show = True

            if re.search('^.*' + str(args.title) + '.*$', m['bsp'][bsp]['title']):
                criteria.append(('title', args.title))
                show = True

        if args.pk3:
            criteria.append(('pk3', args.pk3))
            show = True

        if args.shasum:
            criteria.append(('shasum', args.shasum))
            show = True

        if show:
            total += 1
            fmaps_json.append(m)

    criteria = list(set(criteria))

    if len(criteria) > 0:
        print(bcolors.HEADER + 'Searching for packages with the following criteria:' + bcolors.ENDC)
        for c in criteria:
            print(bcolors.BOLD + str(c[0]) + bcolors.ENDC + ': ' + str(c[1]))

    for m in fmaps_json:
        bsps = m['bsp']
        keys = list(bsps)
        keys.sort()

        shown = False
        for bsp in keys:
            if re.search('^.*' + search_string + '.*$', bsp) and not shown:
                show_map_details(m, args)
                shown = True

    print('\n' + bcolors.OKBLUE + 'Total packages found:' + bcolors.ENDC + ' ' + bcolors.BOLD + str(total) + bcolors.ENDC)


def install_maps(args):

    map_dir = get_map_dir(args)
    installed_packages = get_package_db(args)

    if installed_packages:
        for m in installed_packages:
            if m['pk3'] == args.pk3:
                print(bcolors.FAIL + args.pk3 + " already exists." + bcolors.ENDC)
                install = util.query_yes_no('continue?', 'no')
                if not install:
                    raise SystemExit

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
            db_add_package(m, args)
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
            urllib.request.urlretrieve(url, os.path.expanduser(pk3_with_path), util.reporthook)
        else:
            subprocess.call(['curl', '-o', pk3_with_path, url])

        print(bcolors.OKBLUE + 'Done.' + bcolors.ENDC)

    else:
        print(bcolors.FAIL + 'package already exists, please remove first.' + bcolors.ENDC)
        raise SystemExit


def remove_maps(args):

    pk3 = args.pk3
    map_dir = os.path.expanduser(get_map_dir(args))

    print('Removing package: ' + bcolors.BOLD + pk3 + bcolors.ENDC)

    if os.path.exists(map_dir):
        pk3_with_path = os.path.join(os.path.dirname(map_dir), pk3)

        if os.path.exists(pk3_with_path):
            os.remove(pk3_with_path)

            repo_data = get_repo_data()

            for m in repo_data:
                if m['pk3'] == pk3:
                    db_remove_package(m, args)

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


def discover_maps(args):

    map_dir = os.path.expanduser(get_map_dir(args))
    packages = get_package_db(args)

    for file in os.listdir(map_dir):
        if file.endswith('.pk3'):
            args.pk3 = file
            args.shasum = util.hash_file(os.path.join(map_dir, file))
            map_found = show_map(file, 'all', args)

            if map_found and args.add:
                installed = False
                if packages:
                    for p in packages:
                        if p['pk3'] == args.pk3:
                            installed = True

                    if not installed:
                        db_add_package(map_found, args)


# local data
def list_installed(args):

    packages = get_package_db(args)

    total = 0
    if packages:
        for p in packages:
            show_map_details(p, args)
            total += 1

    print('\n' + bcolors.OKBLUE + 'Total packages found:' + bcolors.ENDC + ' ' + bcolors.BOLD + str(total) + bcolors.ENDC)


def show_map(pk3, ftype, args):

    if ftype == 'all':
        packages = get_repo_data()
    elif ftype == 'installed':
        packages = get_package_db(args)

    found_map = False
    hash_match = True

    if packages:
        for p in packages:
            if p['pk3'] == pk3:
                if p['shasum'] == args.shasum:
                    show_map_details(p, args)
                    found_map = p
                    print('')
                else:
                    print(bcolors.BOLD + pk3 + bcolors.ENDC + bcolors.WARNING + " hash different from repositories" + bcolors.ENDC)
                    hash_match = False

    if not found_map and hash_match:
        if ftype == 'all':
            print(bcolors.BOLD + pk3 + bcolors.ENDC + bcolors.FAIL + ' package was not found in repository' + bcolors.ENDC)
        elif ftype == 'installed':
            print(bcolors.BOLD + pk3 + bcolors.ENDC + bcolors.FAIL + ' package not currently installed' + bcolors.ENDC)

    return found_map


def show_map_details(m, args):

    highlight = False
    search_string = ''

    if 'string' in args:
        search_string = args.string
    elif 'pk3' in args:
        search_string = args.pk3

    if 'highlight' in args and args.highlight:
        highlight = True

    bsps = m['bsp']
    keys = list(bsps)
    keys.sort()

    # little ugly here for a lot of pretty out
    if args.long:
        print('')
        print('         pk3: ' + bcolors.BOLD + str(m['pk3']) + bcolors.ENDC)

        for bsp in keys:
            # Handle Hightlight
            if search_string and highlight:
                print('         bsp: ' + bcolors.OKBLUE
                                            + bsp.replace(search_string, bcolors.ENDC + bcolors.OKGREEN + search_string + bcolors.ENDC + bcolors.OKBLUE)
                                        + bcolors.ENDC)
            else:
                print('         bsp: ' + bcolors.OKBLUE + bsp + bcolors.ENDC)

            # bsp specific
            print('       title:  ' + str(m['bsp'][bsp]['title']))
            print(' description:  ' + str(m['bsp'][bsp]['description']))
            print('      author:  ' + str(m['bsp'][bsp]['author']))

        # pk3 specific
        print('      shasum: ' + str(m['shasum']))
        print('        date: ' + time.strftime('%Y-%m-%d', time.localtime(m['date'])))
        print('        size: ' + util.convert_size(m['filesize']).strip())
        print('          dl: ' + config['repo_url'] + m['pk3'])

    # Formatting
    elif args.short:
        print(str(m['pk3']))
    else:
        bsp_string = '\n' + bcolors.BOLD + str(m['pk3']) + bcolors.ENDC + ' ['
        for bsp in keys:
            if search_string and highlight:
                bsp_string += bcolors.OKBLUE +\
                              bsp.replace(search_string, bcolors.ENDC + bcolors.OKGREEN + search_string + bcolors.ENDC + bcolors.OKBLUE)\
                              + bcolors.ENDC + ', '
            else:
                bsp_string += bcolors.OKBLUE + bsp + bcolors.ENDC + ', '
        bsp_string = util.replace_last(bsp_string, ', ', '')
        bsp_string += bcolors.ENDC + ']'
        print(bsp_string)
        print(config['repo_url'] + str(m['pk3']))


def get_map_dir(args):
    #return args.T if args.T else os.path.expanduser(config['map_dir'])

    if args.T:
        target_dir = args.T
    elif args.s:
        servers_file = os.path.expanduser(config['servers'])
        f = open(servers_file)
        data = f.read()
        server_data = json.loads(data)
        f.close()
        target_dir = server_data[args.s]['target_dir']
    else:
        target_dir = os.path.expanduser(config['map_dir'])

    return target_dir


def get_package_store(args):
    if args.s:
        servers_file = os.path.expanduser(config['servers'])
        f = open(servers_file)
        data = f.read()
        server_data = json.loads(data)
        f.close()
        if args.s in server_data:
            package_store_file = os.path.expanduser(server_data[args.s]['package_db'])
        else:
            print('server not defined in ' + config['servers'])
            raise SystemExit
    else:
        package_store_file = os.path.expanduser(config['package_store'])

    return package_store_file


def get_package_db(args):

    global repo_data

    package_store_file = get_package_store(args)

    if os.path.exists(package_store_file):
        db = open(package_store_file, 'rb')
        package_store = pickle.load(db)
        db.close()
    else:
        print(bcolors.WARNING + 'No package database found (don\'t worry, it will be created when you install a map)' + bcolors.ENDC)
        return False

    return package_store


def db_add_package(package, args):

    package_store = []
    package_store_file = get_package_store(args)

    if os.path.exists(package_store_file) and not util.file_is_empty(package_store_file):
        db_in = open(package_store_file, 'rb+')
        package_store = pickle.load(db_in)
        package_store.append(package)
        db_in.close()
    else:
        package_store.append(package)

    db_out = open(package_store_file, 'wb+')
    pickle.dump(package_store, db_out)
    db_out.close()


def db_remove_package(package, args):

    package_store = []
    package_store_file = get_package_store(args)

    if not util.file_is_empty(package_store_file):
        db_in = open(package_store_file, 'rb+')
        package_store = pickle.load(db_in)
        package_store[:] = [m for m in package_store if (m.get('shasum') != package['shasum'] and m.get('pk3') != package['pk3'])]
        db_in.close()

    db_out = open(package_store_file, 'wb+')
    pickle.dump(package_store, db_out)
    db_out.close()


def db_export_packages(args):

    data = get_package_db(args)
    package_store = json.dumps(data)

    if args.file:
        filename = args.file
    else:
        default_name = 'xmm-export.json'
        print(bcolors.WARNING + 'a name wasn\'t given. Exporting as: ' + default_name + bcolors.ENDC)
        filename = default_name

    f = open(filename, 'w')
    f.write(package_store)
    f.close()


def parse_args():

    global plugins

    parser = argparse.ArgumentParser(description='Xonotic Map Manager is a tool to help manage Xonotic maps',
                                     epilog="Very early alpha. Please be patient.")

    parser.add_argument("-T", nargs='?', help="target directory", type=str)
    parser.add_argument("-s", nargs='?', help="target server as defined in servers.json", type=str)

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
    parser_search.add_argument('--highlight', '-H', help='highlight search term in results', action='store_true')

    parser_add = subparsers.add_parser('install', help='install a map from the repository, or specify a URL.')
    parser_add.add_argument('pk3', nargs='?', help='use a pk3 name', type=str)

    parser_remove = subparsers.add_parser('remove', help='remove based on pk3 name')
    parser_remove.add_argument('pk3', nargs='?', help='pk3', type=str)

    parser_discover = subparsers.add_parser('discover', help='discover packages in a target directory')
    parser_discover.add_argument('--long', '-l', help='show long format', action='store_true')
    parser_discover.add_argument('--short', '-s', help='show short format', action='store_true')
    parser_discover.add_argument('--add', '-a', help='add discovered files to the db', action='store_true')

    parser_list = subparsers.add_parser('list', help='list locally installed packages')
    parser_list.add_argument('--long', '-l', help='show long format', action='store_true')
    parser_list.add_argument('--short', '-s', help='show short format', action='store_true')
    parser_list.add_argument('--highlight', '-H', help='highlight search term in results', action='store_true')

    parser_show = subparsers.add_parser('show', help='show details of locally installed package')
    parser_show.add_argument('pk3', nargs='?', help='pk3 to show details for', type=str)
    parser_show.add_argument('--long', '-l', help='show long format', action='store_true')
    parser_show.add_argument('--short', '-s', help='show short format', action='store_true')

    parser_export = subparsers.add_parser('export', help='export locally managed packages to a file')
    parser_export.add_argument('--type', '-t', nargs='?', help='type to export: db, flat', type=str)
    parser_export.add_argument('file', nargs='?', help='file name to export to', type=str)

    parser_update = subparsers.add_parser('update', help='update sources json')

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
