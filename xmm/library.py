import os
import re
import json

from xmm.exceptions import PackageMetadataWarning
from xmm.exceptions import PackageNotTrackedWarning
from xmm.exceptions import PackageLookupError
from xmm.exceptions import RepositoryLookupError
from xmm.exceptions import HashMismatchError
from xmm.server import Base
from xmm.util import zcolors
from xmm.util import cprint
from xmm import util


class Library(Base):
    """
    A *Library* is a collection of *MapPackage* objects and commands for managing maps in the *Library*

    :param repositories:
        A *Collection* object with *Repository* objects
    :type repositories: ``Collection``

    :param store:
        A *Store* object for communicate with the data store for this *Library*
    :type store: ``Store``

    :param map_dir:
        The directory this *Library* is associated with
    :type map_dir: ``str``

    :returns object: ``Library``

    """
    def __init__(self, repositories, store, map_dir):
        super().__init__()
        self.maps = []
        self.repositories = repositories
        self.store = store
        self.map_dir = os.path.expanduser(map_dir)

    def __repr__(self):
        return str(vars(self))

    def __json__(self):
        return {
            'maps': self.maps,
            'repositories': self.repositories,
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
        Gets the *Collection* from the *Library* of the specified *LocalServer* from ``self.repositories``
        as cache, or from the ``sources.json`` targeted by ``servers.json`` if it is not already set.

        :param server_name:
            Server name
        :type server_name: ``str``

        :returns: ``Collection``
        """
        if server_name:
            repo_sources = self.conf['servers'][server_name]['sources']

            with open(repo_sources) as f:
                data = f.read()
                sources = json.loads(data)
                self.repositories = sources
        else:
            repo_sources = self.repositories

        return repo_sources

    def install_map(self, pk3_name, repository_name=None):
        """
        Install a *MapPackage* from a *Repository*

        :param pk3_name:
            A pk3 name such as ``vinegar_v3.pk3``, to install from the repository.'
            Optionally prefixed with a URL to install map not in the repository.
            URL-only maps will not include rich metadata available to maps installed via the repo.
        :type pk3_name: ``str``

        :param repository_name:
            A name of a repository in the repository *Collection*
        :type repository_name: ``str``

        >>> from xmm.server import LocalServer
        >>> server = LocalServer(server_name='myserver1')
        >>> server.library.install_map(pk3_name='vinegar_v3.pk3')
        >>> print(server.library.maps)
        """
        map_dir = self.map_dir
        installed_packages = self.store.get_package_db()
        add_to_store = True
        map_found_in_repo = False
        found_map = None
        overwrite = False
        installed = False
        is_url = False

        if not os.path.exists(map_dir):
            raise NotADirectoryError(map_dir)

        if repository_name:
            repo = self.repositories.get_repository(repository_name)
            if repo:
                sources = [repo]
            else:
                raise RepositoryLookupError
        else:
            sources = self.repositories.sources

        if installed_packages:
            for m in installed_packages:
                if m.pk3_file == pk3_name:
                    cprint("{} already exists.".format(pk3_name), style='WARNING')
                    install = util.query_yes_no('continue?', 'no')
                    if not install:
                        raise SystemExit
                    else:
                        overwrite = True
                        add_to_store = False

        if re.match('^(ht|f)tp(s)?://', pk3_name):
            url = pk3_name
            pk3 = os.path.basename(pk3_name)
            is_url = True
            overwrite = False
        else:
            pk3 = pk3_name
            url = self.conf['default']['download_url'] + pk3

        pk3_with_path = os.path.join(os.path.dirname(map_dir), pk3)

        for repo in sources:
            if not map_found_in_repo:
                maps_json = repo.get_repo_data()
                for m in maps_json:
                    if m.pk3_file == pk3:
                        found_map = m
                        self.add_map_package(found_map)
                        map_found_in_repo = True
                        cprint("Found in: {}".format(repo.name))
                        break

        if map_found_in_repo or is_url:
            util.download_file(filename_with_path=pk3_with_path, url=url, use_curl=self.conf['default']['use_curl'], overwrite=overwrite)
            installed = True

        if installed and add_to_store and found_map:
            self.store.add_package(found_map)

        if not map_found_in_repo:
            if installed:
                raise PackageMetadataWarning
            else:
                raise PackageLookupError

    def remove_map(self, pk3_name):
        """
        Removes a map from the *Library*

        :param pk3_name:
            The name of a pk3, such as ``vinegar_v3.pk3``
        :type pk3_name: ``str``

        >>> from xmm.server import LocalServer
        >>> server = LocalServer(server_name='myserver1')
        >>> server.library.install_map(pk3_name='vinegar_v3.pk3')
        >>> print(server.library.maps)
        >>> server.library.remove_map(pk3_name='vinegar_v3.pk3')
        >>> print(server.library.maps)
        """
        map_dir = os.path.expanduser(self.map_dir)

        if os.path.exists(map_dir):
            pk3_with_path = os.path.join(os.path.dirname(map_dir), pk3_name)

            installed_packages = self.store.get_package_db()

            for m in installed_packages:
                if m.pk3_file == pk3_name:
                    self.store.remove_package(m)

            if os.path.exists(pk3_with_path):
                os.remove(pk3_with_path)
            else:
                raise FileNotFoundError(pk3_with_path)

        else:
            raise NotADirectoryError(map_dir)

    def discover_maps(self, add=False, repository_name=None):
        """
        Searches the *Server*'s map_dir for map packages known by the *Repository*

        :param add:
            Whether to add the discovered maps or not
        :type add: ``bool``

        :param repository_name:
            A name of a repository in the repository *Collection*
        :type repository_name: ``str``

        >>> from xmm.server import LocalServer
        >>> server = LocalServer()
        >>> server.library.discover_maps(add=False)
        """
        map_dir = os.path.expanduser(self.map_dir)
        local_maps = self.store.get_package_db()

        if repository_name:
            repo = self.repositories.get_repository(repository_name)
            if repo:
                sources = [repo]
            else:
                raise RepositoryLookupError
        else:
            sources = self.repositories.sources

        if not os.path.exists(map_dir):
            raise NotADirectoryError(map_dir)

        for pk3_file in os.listdir(map_dir):

            map_found = False
            hash_match = False

            if pk3_file.endswith('.pk3'):
                shasum = util.hash_file(os.path.join(map_dir, pk3_file))

                try:
                    for repo in sources:
                        map_found = repo.show_map(pk3_file)
                        if map_found:
                            break
                except PackageLookupError:
                    pass

                if map_found:

                    if map_found.shasum == shasum:
                        hash_match = True
                    else:
                        cprint("{} hash does not match repository's".format(pk3_file), style='WARNING')

                    if hash_match and add:
                        map_already_installed = False
                        for m in local_maps:
                            if m.pk3_file == pk3_file and m.shasum == shasum:
                                map_already_installed = True

                        if not map_already_installed:
                            self.store.add_package(map_found)

    # local data
    def list_installed(self, detail=None):
        """
        List maps currently tracked by the *Library*

        :param detail:
            How much detail to show, [short, None, long]
        :type detail: ``str``

        :returns: ``int`` total count

        >>> from xmm.server import LocalServer
        >>> server = LocalServer()
        >>> server.library.list_installed()
        """
        packages = self.store.data

        total = 0
        if packages:
            for m in packages:
                m.show_map_details(detail=detail)
                total += 1

        return total

    def show_map(self, pk3_name, detail=None, highlight=False):
        """
        Convenience function to use the show_map_details helper

        :param pk3_name:
            The name of a pk3, such as ``vinegar_v3.pk3``
        :type pk3_name: ``str``

        :param detail:
            How much detail to show, [short, None, long]
        :type detail: ``str``

        :param highlight:
            Whether to highlight the results
        :type highlight: ``bool``

        :returns: ``MapPackage``

        >>> from xmm.server import LocalServer
        >>> server = LocalServer()
        >>> server.library.show_map('vinegar_v3.pk3', detail='long')
        """
        packages = self.store.get_package_db()

        found_map = False
        hash_match = False

        for p in packages:
            if p.pk3_file == pk3_name:
                shasum = util.hash_file(os.path.join(self.map_dir, pk3_name))
                if p.shasum == shasum:
                    hash_match = True
                    p.show_map_details(search_string=pk3_name, detail=detail, highlight=highlight)
                    found_map = p
                else:
                    raise HashMismatchError

        if not found_map and not hash_match:
            raise PackageNotTrackedWarning

        return found_map
