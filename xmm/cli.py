#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
# A tool to help manage Xonotic maps
# z@xnz.me

import argcomplete
import argparse
import logging
import os

from xmm import __version__
from xmm.config import conf

from xmm.server import LocalServer
from xmm.server import ServerCollection

from xmm.exceptions import HashMismatchError
from xmm.exceptions import PackageMetadataWarning
from xmm.exceptions import PackageNotTrackedWarning
from xmm.exceptions import PackageLookupError
from xmm.exceptions import RepositoryLookupError
from xmm.exceptions import RepositoryUpdateError
from xmm.exceptions import ServerLookupError
from xmm.plugins import pluginbase
from xmm.plugins import pluginloader
from xmm.logger import ClassPrefixAdapter
from xmm.util import cprint
from xmm.util import zcolors
from xmm import util

plugins = {}

cli_logger = ClassPrefixAdapter(prefix='cli', logger=logging.getLogger(__name__))


def main():

    pluginbase.set_config(conf)
    args = parse_args()
    server = None

    # Just install
    if args.target:
        if args.command != 'install':
            cprint("This flag only works with 'install' sub-command.", style='FAIL')

        target_dir = args.target
        cli_logger.info("Installing to target directory: {}".format(target_dir))

        if not os.path.exists(target_dir):
            cli_logger.error("Target directory does not exist: {}.".format(target_dir))
            cprint("Target directory does not exist.", style='FAIL')
            raise SystemExit

        filename_with_path = os.path.join(target_dir, args.pk3)
        url_with_file = '{}/{}'.format(conf['default']['download_url'], args.pk3)

        success = util.download_file(filename_with_path=filename_with_path, url=url_with_file, use_curl=conf['default']['use_curl'])

        if not success:
            cli_logger.warning("{} already exists, not installing.".format(args.pk3))

        exit(0)

    # Use all source repositories
    else:
        try:
            server = LocalServer(server_name=args.server)
        except NotADirectoryError as e:
            create_directory = util.query_yes_no("Directory '{}' does not exist, would you like to create it?".format(e))
            if create_directory:
                server = LocalServer(server_name=args.server, make_dirs=True)
            else:
                cprint("Canceled.", style='INFO')
                raise SystemExit
        except ServerLookupError as e:
            cprint("server '{}' does not exist in ~/.xmm/servers.json".format(e), style='FAIL')

    # Sort out defaults
    if 'long' in args and args.long:
        detail = 'long'
    elif 'short' in args and args.short:
        detail = 'short'
    else:
        detail = None

    highlight = False
    if 'highlight' in args and args.highlight:
        highlight = True

    # Commands
    if args.command == 'search':

        try:
            server.repositories.search_all(bsp_name=args.string, gametype=args.gametype, author=args.author,
                                           title=args.title, pk3_name=args.pk3, shasum=args.shasum, detail=detail,
                                           highlight=highlight)
        except Exception:
            cprint('Failed.', style='FAIL')

    elif args.command == 'install':

        if not args.pk3:
            cprint("package name not specified", style='FAIL')
            raise SystemExit

        cprint("Installing map: {}".format(args.pk3), style='BOLD')

        try:
            server.library.install_map(pk3_name=args.pk3, repository_name=args.repository)
        except SystemExit:
            cprint("Canceled.", style='INFO')
        except NotADirectoryError as e:
            cprint("package directory does not exist: {}".format(e), style='FAIL')
        except PackageMetadataWarning:
            cprint("package does not exist in the repository it won't be tracked (xmm list).", style='WARNING')
        except RepositoryLookupError:
            cprint("Repository does not exist!", style='FAIL')
        except PackageLookupError:
            cprint("package does not exist in the repository. cannot install.", style='FAIL')

    elif args.command == 'remove':

        if not args.pk3:
            cprint("package name not specified", style='FAIL')
            raise SystemExit

        cprint("Removing package: {}".format(args.pk3), style='BOLD')

        try:
            server.library.remove_map(pk3_name=args.pk3)
            cprint("Done.", style='INFO')
        except FileNotFoundError:
            cprint("package does not exist or is not tracked. try removing using full path if not tracked.", style='FAIL')
        except NotADirectoryError as e:
            cprint("package directory does not exist: {}".format(e), style='FAIL')

    elif args.command == 'discover':

        repository_name = None

        if args.repository:
            repository_name = args.repository
            cprint("Using repo '{}'".format(args.repository), style='HEADER')
            try:
                repo = server.repositories.get_repository(repository_name)
            except RepositoryLookupError:
                cprint("Repository doesn't exist in sources.json", style="FAIL")
                raise SystemExit

        try:
            server.library.discover_maps(add=args.add, repository_name=repository_name, detail=detail)
        except NotADirectoryError as e:
            cprint("package directory does not exist: {}".format(e), style='FAIL')

    elif args.command == 'list':

        try:
            total = server.library.list_installed(detail=detail)
            print("\n{}Total packages found:{} {}{}{}".format(zcolors.INFO, zcolors.ENDC, zcolors.BOLD, str(total), zcolors.ENDC))
        except Exception:
            cprint("Failed.", style='FAIL')

    elif args.command == 'show':

        if not args.pk3:
            cprint("package name not specified", style='FAIL')
            raise SystemExit

        if not detail:
            detail = 'long'

        # Use local package store for lookup
        if args.local:

            try:
                server.library.show_map(pk3_name=args.pk3, detail=detail, highlight=highlight)
            except HashMismatchError:
                print("\n{}{}{} {}hash different from repositories{}".format(zcolors.BOLD, args.pk3, zcolors.ENDC, zcolors.WARNING, zcolors.ENDC))
            except PackageNotTrackedWarning:
                print("\n{}{}{} {}package not currently tracked{}".format(zcolors.BOLD, args.pk3, zcolors.ENDC, zcolors.WARNING, zcolors.ENDC))

        # Use repositories for lookup
        else:

            if args.repository:

                try:
                    repo = server.repositories.get_repository(args.repository)
                except RepositoryLookupError:
                    cprint("Repository doesn't exist in sources.json", style="FAIL")
                    raise SystemExit

                repo.show_map(pk3_name=args.pk3, detail=detail, highlight=highlight)

            else:

                try:
                    for repo in server.repositories.sources:
                        cprint("Using repo '{}'".format(repo.name), style='HEADER')
                        map_found = repo.show_map(pk3_name=args.pk3, detail=detail, highlight=highlight)
                        if map_found:
                            break
                except PackageLookupError:
                    cprint("Map was not found in repository", style="FAIL")

    elif args.command == 'export':

        repository_name = None

        if args.server and args.repository:
            cprint("'-R' and '-S' flags are mutually exclusive on this command.", style="FAIL")
            raise SystemExit

        if args.repository:
            cprint("Using repo '{}'".format(args.repository), style='HEADER')
            repository_name = args.repository

        if args.format == 'json':

            if args.subcommand == 'local':

                server.library.export_map_packages(filename=args.filename)

            elif args.subcommand == 'repos':

                if repository_name:
                    try:
                        server.library.repositories.get_repository(repository_name).export_packages(filename=args.filename)
                    except RepositoryLookupError:
                        cprint("Repository doesn't exist in sources.json", style="FAIL")
                        raise SystemExit
                else:
                    server.library.repositories.export_all_packages(filename=args.filename)

        if args.format == 'maplist':

            if args.subcommand == 'local':

                server.library.export_maplist(filename=args.filename)

            elif args.subcommand == 'repos':

                # TODO: implement
                print('sorry exporting bsp names from repos is not supported yet')
                exit(0)

        elif args.format == 'shasums':

            if args.subcommand == 'local':

                if not repository_name:
                    server.library.export_hash_index(filename=args.filename)
                else:
                    # TODO: limit export by repository name
                    cprint('this combination is not yet possible')

            elif args.subcommand == 'repos':

                if repository_name:
                    try:
                        server.library.repositories.get_repository(repository_name).export_hash_index(filename=args.filename)
                    except RepositoryLookupError:
                        cprint("Repository doesn't exist in sources.json", style="FAIL")
                        raise SystemExit
                else:
                    server.library.repositories.export_all_hash_index(filename=args.filename)

    elif args.command == 'servers':

        servers = ServerCollection(servers=[])

        if args.subcommand == 'list':
            servers.list_servers()

    elif args.command == 'repos':

        if args.subcommand == 'list':
            server.repositories.list_repositories()

    elif args.command == 'update':

        try:
            server.repositories.update_all()
        except RepositoryUpdateError:
            cprint('One or more repositories have failed to update.', style='FAIL')

    # Plugins
    for cmd, value in plugins.items():
        if args.command == cmd:
            plugins[cmd].run()
            break


def parse_args():

    global plugins

    parser = argparse.ArgumentParser(description='Xonotic Map Manager is a tool to help manage Xonotic maps')

    parser.add_argument('--version', action='version', version='%(prog)s {0}'.format(__version__))
    parser.add_argument("-S", '--server', nargs='?', help="target server as defined in servers.json", type=str)
    parser.add_argument("-T", '--target', nargs='?', help="target directory", type=str)
    parser.add_argument("-R", '--repository', nargs='?', help="repository to use (defaults to all available)", type=str, default=None)

    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    parser_search = subparsers.add_parser('search', help='search for maps based on bsp names')
    parser_search.add_argument('string', nargs='?', help='bsp name found in a package, works on packages with many bsps', type=str)
    parser_search.add_argument('--gametype', nargs='?', help='filter by gametype', type=str)
    parser_search.add_argument('--pk3', nargs='?', help='filter by pk3 name', type=str)
    parser_search.add_argument('--title', nargs='?', help='filter by title', type=str)
    parser_search.add_argument('--author', nargs='?', help='filter by author', type=str)
    parser_search.add_argument('--shasum', nargs='?', help='filter by shasum', type=str)
    parser_search.add_argument('--long', '-l', help='show long format', action='store_true')
    parser_search.add_argument('--short', '-s', help='show short format', action='store_true')
    parser_search.add_argument('--color', '-c', help='highlight search term in results', action='store_true')

    parser_install = subparsers.add_parser('install', help='install a map from the repository, or specify a URL.')
    parser_install.add_argument('pk3', nargs='?', help='use a pk3 name of map package, or specify a URL of a pk3.', type=str)

    parser_remove = subparsers.add_parser('remove', help='remove based on pk3 name')
    parser_remove.add_argument('pk3', nargs='?', help='pk3', type=str)

    parser_discover = subparsers.add_parser('discover', help='discover packages in a target directory')
    parser_discover.add_argument('--long', '-l', help='show long format', action='store_true')
    parser_discover.add_argument('--short', '-s', help='show short format', action='store_true')
    parser_discover.add_argument('--add', '-a', help='add discovered files to the db', action='store_true')

    parser_list = subparsers.add_parser('list', help='list locally installed packages')
    parser_list.add_argument('--long', '-l', help='show long format', action='store_true')
    parser_list.add_argument('--short', '-s', help='show short format', action='store_true')

    parser_show = subparsers.add_parser('show', help='show details of remote or locally installed packages')
    parser_show.add_argument('pk3', nargs='?', help='pk3 to show details for', type=str)
    parser_show.add_argument('--local', '-L', help='whether to show from local packages only or all repos', action='store_true')
    parser_show.add_argument('--long', '-l', help='show long format', action='store_true')
    parser_show.add_argument('--short', '-s', help='show short format', action='store_true')

    parser_export = subparsers.add_parser('export', help='export locally managed packages to a file')
    parser_export.add_argument('subcommand', choices=['local', 'repos'], help='what context to export?', default='local', type=str)
    parser_export.add_argument('filename', nargs='?', help='filename to export to', type=str)
    parser_export.add_argument('--format', '-f', choices=['json', 'shasums', 'maplist'], default='json')

    parser_servers = subparsers.add_parser('servers', help='subcommands on servers described in servers.json')
    parser_servers.add_argument('subcommand', choices=['list'], help='list all servers in servers.json', type=str)

    parser_servers = subparsers.add_parser('repos', help='subcommands on repos described in sources.json')
    parser_servers.add_argument('subcommand', choices=['list'], help='list all servers in sources.json', type=str)

    parser_update = subparsers.add_parser('update', help='update sources json')

    # Handle plugins
    for i in pluginloader.get_plugins():
        cli_logger.debug("Loading plugin: " + i["name"])
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
