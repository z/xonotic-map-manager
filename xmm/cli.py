#!/usr/bin/env python3
# A tool to help manage Xonotic maps
# z@xnz.me

import argparse

from xmm.library import LibraryCommand
from xmm.library import Store
from xmm.repository import RepositoryCommand

from xmm.plugins import pluginbase
from xmm.plugins import pluginloader
from xmm.config import conf

plugins = {}


def main():

    pluginbase.set_config(conf)
    args = parse_args()

    store = Store(conf=conf)
    repository = RepositoryCommand(args=args, conf=conf)
    command = LibraryCommand(args=args, conf=conf, store=store, repository=repository)

    # print(args)

    if args.command == 'search':
        command.repository.search_maps(args)

    if args.command == 'install':
        command.install_maps(args)

    if args.command == 'remove':
        command.remove_maps(args)

    if args.command == 'discover':
        command.discover_maps(args)

    if args.command == 'list':
        command.list_installed(args)

    if args.command == 'show':
        command.show_map(args.pk3, 'installed', args)

    if args.command == 'export':
        command.store.db_export_packages(args)

    if args.command == 'update':
        command.repository.update_repo_data()

    # Plugins
    for cmd, value in plugins.items():
        if args.command == cmd:
            plugins[cmd].run()
            break


def parse_args():

    global plugins

    parser = argparse.ArgumentParser(description='Xonotic Map Manager is a tool to help manage Xonotic maps')

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
        # print("Loading plugin: " + i["name"])
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
