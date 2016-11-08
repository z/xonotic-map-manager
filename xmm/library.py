import os
import re
import json

from xmm.server import Base
from xmm.util import bcolors
from xmm import util


class Library(Base):
    """
    A *Library* is a collection of *MapPackage* objects and commands for managing maps in the *Library*

    :param source_collection:
    :type source_collection: ``SourceCollection``
        A *SourceCollection* object with *Repository* objects

    :param store:
    :type store: ``Store``
        A *Store* object for communicate with the data store for this *Library*

    :param map_dir:
    :type map_dir: ``str``
        The directory this *Library* is associated with

    :returns object: ``Library``

    """
    def __init__(self, source_collection, store, map_dir):
        super().__init__()
        self.maps = []
        self.source_collection = source_collection
        self.store = store
        self.map_dir = os.path.expanduser(map_dir)

    def __repr__(self):
        return str(vars(self))

    def __json__(self):
        return {
            'maps': self.maps,
            'source_collection': self.source_collection,
            'store': self.store,
            'map_dir': self.map_dir,
        }

    def to_json(self):
        """
        :returns: A **JSON** encoded version of this object
        """
        return json.dumps(self, cls=util.ObjectEncoder)

    def add_map_package(self, package):
        """
        Adds a *MapPackage* object to ``self.maps``

        :param package:
            A *MapPackage* object for the *Library*
        :type package: ``MapPackage``
        """
        self.maps.append(package)

    def get_repository_sources(self, server_name):
        """
        Gets the *SourceCollection* from the *Library* of the specified *LocalServer* from ``self.source_collection``
        as cache, or from the ``sources.json`` targeted by ``servers.json`` if it is not already set.

        :param server_name:
            Server name
        :type server_name: ``str``

        :returns: ``SourceCollection``
        """
        if server_name:
            repo_sources = self.conf['servers'][server_name]['sources']

            with open(repo_sources) as f:
                data = f.read()
                sources = json.loads(data)
                self.source_collection = sources
        else:
            repo_sources = self.source_collection

        return repo_sources

    # TODO: Rewrite this
    def install_map(self, pk3_name):
        """
        Install a *MapPackage* from a *Repository*

        :param pk3_name:
            A pk3 name such as ``dance.pk3``, to install from the repository.'
            Optionally prefixed with a URL to install map not in the repository.
            URL-only maps will not include rich metadata available to maps installed via the repo.
        :type pk3_name: ``str``

        >>> from xmm.server import LocalServer
        >>> server = LocalServer(server_name='myserver1')
        >>> server.library.install_map(pk3_name='dance.pk3')
        >>> print(server.library.maps)
        """
        map_dir = self.map_dir
        installed_packages = self.store.get_package_db()
        add_to_store = True

        if installed_packages:
            for m in installed_packages:
                if m.pk3_file == pk3_name:
                    print(bcolors.FAIL + pk3_name + " already exists." + bcolors.ENDC)
                    install = util.query_yes_no('continue?', 'no')
                    if not install:
                        raise SystemExit
                    else:
                        add_to_store = False

        installed = False
        is_url = False
        if re.match('^(ht|f)tp(s)?://', pk3_name):
            url = pk3_name
            pk3 = os.path.basename(pk3_name)
            is_url = True
        else:
            pk3 = pk3_name
            url = self.conf['default']['download_url'] + pk3

        pk3_with_path = os.path.join(os.path.dirname(map_dir), pk3)

        maps_json = self.source_collection.sources[0].get_repo_data()
        map_in_repo = False
        for m in maps_json:
            if m.pk3_file == pk3 and add_to_store:
                self.store.add_package(m)
                self.add_map_package(m)
                map_in_repo = True
                break

        if map_in_repo or is_url:
            print('Installing map: ' + bcolors.BOLD + pk3 + bcolors.ENDC)
            util.download_file(filename_with_path=pk3_with_path, url=url, use_curl=self.conf['default']['use_curl'])
            installed = True

        if not map_in_repo:
            if installed:
                print(bcolors.WARNING + 'package does not exist in the repository, ' +
                                        'it won\'t be added to the local database.' + bcolors.ENDC)
            else:
                print(bcolors.FAIL + 'package does not exist in the repository. cannot install.' + bcolors.ENDC)
                Exception('package does not exist in the repository.')

    def remove_map(self, pk3_name):
        """
        Removes a map from the *Library*

        :param pk3_name:
            The name of a pk3, such as ``dance.pk3``
        :type pk3_name: ``str``

        >>> from xmm.server import LocalServer
        >>> server = LocalServer(server_name='myserver1')
        >>> server.library.install_map(pk3_name='dance.pk3')
        >>> print(server.library.maps)
        >>> server.library.remove_map(pk3_name='dance.pk3')
        >>> print(server.library.maps)
        """
        map_dir = os.path.expanduser(self.map_dir)

        print('Removing package: ' + bcolors.BOLD + pk3_name + bcolors.ENDC)

        if os.path.exists(map_dir):
            pk3_with_path = os.path.join(os.path.dirname(map_dir), pk3_name)

            repo_data = self.source_collection.sources[0].get_repo_data()

            for m in repo_data:
                if m.pk3_file == pk3_name:
                    self.store.remove_package(m)

            if os.path.exists(pk3_with_path):
                os.remove(pk3_with_path)
                print(bcolors.OKBLUE + 'Done.' + bcolors.ENDC)
            else:
                print(bcolors.FAIL + 'package does not exist.' + bcolors.ENDC)
                Exception('package does not exist.')

        else:
            print(bcolors.FAIL + 'directory does not exist.' + bcolors.ENDC)
            Exception('directory does not exist.')

    def discover_maps(self, args, add=False):
        """
        Searches the *Server*'s map_dir for map packages known by the *Repository*

        :param args:
            Positional arguments
        :type args: ``tuple``

        :param add:
            Whether to add the discovered maps or not
        :type add: ``bool``
        """
        map_dir = os.path.expanduser(self.map_dir)
        packages = self.store.get_package_db()

        for file in os.listdir(map_dir):
            if file.endswith('.pk3'):
                args.pk3 = file
                args.shasum = util.hash_file(os.path.join(map_dir, file))
                map_found = self.show_map(file, 'all', args)

                if map_found and add:
                        map_installed = False
                        if packages:
                            for p in packages:
                                if p['pk3'] == args.pk3:
                                    map_installed = True

                        if not map_installed:
                            self.store.add_package(map_found)

    # local data
    def list_installed(self, args):
        """
        List maps currently tracked by the *Library*

        :param args:
            Positional arguments
        :type args: ``tuple``

        :returns: ``SourceCollection``
        """
        packages = self.store.data

        total = 0
        if packages:
            for m in packages:
                m.show_map_details(args=args)
                total += 1

        print('\n' + bcolors.OKBLUE + 'Total packages found:' + bcolors.ENDC + ' ' + bcolors.BOLD + str(total) + bcolors.ENDC)

    def show_map(self, pk3_name, where, args):
        """
        Convenience function to use the show_map_details helper

        :param pk3_name:
            The name of a pk3, such as ``dance.pk3``
        :type pk3_name: ``str``

        :param where:
            Where [installed|all].
        :type where: ``str``

        :param args:
            Positional arguments
        :type args: ``tuple``

        :returns: ``MapPackage``
        """
        packages = None

        if where == 'all':
            packages = self.source_collection.sources[0].get_repo_data()

        if where == 'installed':
            packages = self.store.get_package_db()

        found_map = False
        hash_match = False

        for p in packages:
            if p.pk3_file == pk3_name:

                if where == 'installed':
                    shasum = util.hash_file(os.path.join(self.map_dir, pk3_name))
                    if p.shasum == shasum:
                        hash_match = True
                        # self.maps[p['bsp']].show_map_details(p, args)
                        p.show_map_details(args=args)
                        found_map = p
                        print('')
                    else:
                        print(bcolors.BOLD + pk3_name + bcolors.ENDC + bcolors.WARNING + " hash different from repositories" + bcolors.ENDC)
                else:
                    p.show_map_details(args=args)
                    found_map = p

        if not found_map and not hash_match:
            if where == 'installed':
                print(bcolors.BOLD + pk3_name + bcolors.ENDC + bcolors.FAIL + ' package not currently installed' + bcolors.ENDC)
            else:
                print(bcolors.BOLD + pk3_name + bcolors.ENDC + bcolors.FAIL + ' package was not found in repository' + bcolors.ENDC)

        return found_map
