import json
import os
import re
import urllib.request
from urllib.error import URLError

from xmm.map import MapPackage

from xmm.exceptions import PackageLookupError
from xmm.exceptions import RepositoryLookupError
from xmm.exceptions import RepositoryUpdateError
from xmm.base import Base
from xmm.util import zcolors
from xmm.util import cprint
from xmm import util


class Collection(Base):
    """
    A *Collection* is a collection of *Repository* objects

    :returns object: *Collection*

    >>> from xmm.repository import Collection
    >>> from xmm.repository import Repository
    >>> repositories = Collection()
    >>> repository = Repository(name='default', download_url='http://dl.repo.url/',
    >>>                         api_data_url='http://api.repo.url/maps.json', api_data_file='~/.xmm/maps.json')
    >>> repositories.add_repository(repository)

    """
    def __init__(self):
        super().__init__()
        self.sources = []

    def __repr__(self):
        return str(vars(self))

    def __json__(self):
        return {
            'sources': self.sources,
        }

    def to_json(self):
        """
        :returns: A **JSON** encoded version of this object
        """
        return json.dumps(self, cls=util.ObjectEncoder)

    def list_repositories(self):
        """
        Prints a list of servers
        """
        for repo in self.conf['sources']:
            print(repo)

    def get_repository(self, repository_name):
        """
        :param repository_name:
        :type repository_name: ``str``

        :returns: A **Repository** object or false if name not found

        >>> from xmm.repository import Collection
        >>> from xmm.repository import Repository
        >>> repositories = Collection()
        >>> repository = Repository(name='default', download_url='http://dl.repo.url/',
        >>>                         api_data_url='http://api.repo.url/maps.json', api_data_file='~/.xmm/maps.json')
        >>> repositories.add_repository(repository)
        >>> print(repositories.get_repository('default'))
        """
        self.logger.info("Getting repository: {}".format(repository_name))

        repo = False
        for source in self.sources:
            if source.name == repository_name:
                repo = source

        if not repo:
            raise RepositoryLookupError

        return repo

    def add_repository(self, repository):
        """
        Add a *Repository* to the *Collection*

        :param repository:
        :type repository: ``Repository``

        >>> from xmm.repository import Collection
        >>> from xmm.repository import Repository
        >>> repositories = Collection()
        >>> repository = Repository(name='default', download_url='http://dl.repo.url/',
        >>>                         api_data_url='http://api.repo.url/maps.json', api_data_file='~/.xmm/maps.json')
        >>> repositories.add_repository(repository)
        >>> print(repositories.get_repository('default'))
        """
        self.sources.append(repository)

    def search_all(self, bsp_name=False, gametype=False, author=False, title=False, pk3_name=False, shasum=False, detail=None, highlight=False):
        """
        Searches all *Repository* objects in the *Collection* for maps matching criteria

        :param bsp_name:
            Search by bsp name
        :type bsp_name: ``str``

        :param gametype:
            Search by gametype
        :type gametype: ``str``

        :param author:
            Search by author
        :type author: ``str``

        :param title:
            Search by title
        :type title: ``str``

        :param pk3_name:
            Search by pk3_name
        :type pk3_name: ``str``

        :param shasum:
            Search by shasum
        :type shasum: ``str``

        :param detail:
            How much detail in the results, [short, None, long]
        :type detail: ``str``

        :param highlight:
            Whether to highlight the search string
        :type highlight: ``bool``

        >>> from xmm.repository import Collection
        >>> from xmm.repository import Repository
        >>> repositories = Collection()
        >>> repository = Repository(name='default', download_url='http://dl.repo.url/',
        >>>                         api_data_url='http://api.repo.url/maps.json', api_data_file='~/.xmm/maps.json')
        >>> repositories.add_repository(repository)
        >>> print(repositories.search_all(bsp_name='vinegar_v3'))
        """

        self.logger.info("Searching all repositories.")

        for repo in self.sources:
            repo.search_maps(bsp_name=bsp_name, gametype=gametype, author=author, title=title, pk3_name=pk3_name, shasum=shasum, detail=detail, highlight=highlight)

    def update_all(self):
        """
        Update the data for all *Repository* objects in the *Collection*

        >>> from xmm.repository import Collection
        >>> from xmm.repository import Repository
        >>> repositories = Collection()
        >>> repository = Repository(name='default', download_url='http://dl.repo.url/',
        >>>                         api_data_url='http://api.repo.url/maps.json', api_data_file='~/.xmm/maps.json')
        >>> repositories.update_all()
        """

        self.logger.info("Updating all sources.")

        for repo in self.sources:
            self.logger.debug("Updating source: {}".format(repo.name))
            repo.update_repo_data()

    def export_all_hash_index(self, filename=None):
        """
        :param filename:
            Name for the exported json file, default ``all-repos-maps.json.shasums``
        :type filename: ``str``

        :returns: False if fails

        >>> from xmm.repository import Collection
        >>> from xmm.repository import Repository
        >>> repositories = Collection()
        >>> repository = Repository(name='default', download_url='http://dl.repo.url/',
        >>>                         api_data_url='http://api.repo.url/maps.json', api_data_file='~/.xmm/maps.json')
        >>> repositories.export_all_hash_index()
        """
        if not filename:
            filename = 'all-repos-maps.json.shasums'

        self.logger.info("exporting shasums from all sources to file: {}".format(filename))

        data = []
        for repo in self.sources:
            lines = repo.get_hash_index()
            data.extend(lines)

        if data:
            try:
                with open(filename, 'w') as f:
                    f.write('\n'.join(data))
            except EnvironmentError as e:
                self.logger.error(e)
                return False

    def export_all_packages(self, filename=None):
        """
        :param filename:
            Name for the exported json file, default ``maps.json``
        :type filename: ``str``

        :returns: False if fails

        >>> from xmm.repository import Collection
        >>> from xmm.repository import Repository
        >>> repositories = Collection()
        >>> repository = Repository(name='default', download_url='http://dl.repo.url/',
        >>>                         api_data_url='http://api.repo.url/maps.json', api_data_file='~/.xmm/maps.json')
        >>> repositories.export_all_packages()
        """
        if not filename:
            filename = 'all-repos-maps.json'

        self.logger.info("exporting maps as: {}".format(filename))

        data = []
        for repo in self.sources:
            lines = repo.get_packages()
            data.extend(lines)

        if data:
            try:
                with open(filename, 'w') as f:
                    f.write(json.dumps(data, cls=util.ObjectEncoder))
            except EnvironmentError as e:
                self.logger.error(e)
                return False


class Repository(Base):
    """
    A *Repository* contains a url which hosts content matching the
    **JSON** format described in the documentation

    :param name:
        A name for this *Repository*
    :type name: ``str``

    :param download_url:
        The url where the pk3 files should be downloaded from
    :type download_url: ``str``

    :param api_data_url:
        URL serving maps in the *JSON* format described in the documentation
    :type api_data_url: ``str``

    :param api_data_file:
        Local cache fo the repo data.
    :type api_data_file: ``str``

    :returns object: ``Repository``


    >>> from xmm.repository import Repository
    >>> repository = Repository(name='default', download_url='http://dl.repo.url/',
    >>>                         api_data_url='http://api.repo.url/maps.json', api_data_file='~/.xmm/maps.json')
    """
    def __init__(self, name, download_url, api_data_url, api_data_file):
        super().__init__()
        self.name = name
        self.api_data_url = api_data_url
        self.download_url = download_url
        self.api_data = None
        self.api_data_file = os.path.expanduser(api_data_file)
        self.repo_data = {}

    def __repr__(self):
        return str(vars(self))

    def __json__(self):
        return {
            'name': self.name,
            'api_data_url': self.api_data_url,
            'download_url': self.download_url,
            'api_data_file': self.api_data_file,
        }

    def to_json(self):
        """
        :returns: A **JSON** encoded version of this object
        """
        return json.dumps(self, cls=util.ObjectEncoder)

    def search_maps(self, bsp_name=False, gametype=False, author=False, title=False, pk3_name=False, shasum=False, detail=None, highlight=False):
        """
        Searches the repository for maps matching criteria

        :param bsp_name:
            Search by bsp name
        :type bsp_name: ``str``

        :param gametype:
            Search by gametype
        :type gametype: ``str``

        :param author:
            Search by author
        :type author: ``str``

        :param title:
            Search by title
        :type title: ``str``

        :param pk3_name:
            Search by pk3_name
        :type pk3_name: ``str``

        :param shasum:
            Search by shasum
        :type shasum: ``str``

        :param detail:
            How much detail in the results, [short, None, long]
        :type detail: ``str``

        :param highlight:
            Whether to highlight the search string
        :type highlight: ``bool``

        >>> from xmm.repository import Repository
        >>> repository = Repository(name='default', download_url='http://dl.repo.url/',
        >>>                         api_data_url='http://api.repo.url/maps.json', api_data_file='~/.xmm/maps.json')
        >>> repository.search_maps(bsp_name='dance' gametype='ctf')
        """

        self.logger.info("Searching maps.")

        maps_json = self.get_packages()
        fmaps_json = []
        criteria = []

        if not bsp_name:
            bsp_name = ''

        # Filter based on args
        total = 0
        for m in maps_json:

            show = False
            for bsp in m.bsp:
                if bsp_name and re.search('^.*' + bsp_name + '.*$', bsp):
                    criteria.append(('bsp', bsp_name))
                    show = True

                if gametype in m.bsp[bsp]['gametypes']:
                    criteria.append(('gametype', gametype))
                    show = True

                if re.search('^.*' + str(author) + '.*$', m.bsp[bsp]['author']):
                    criteria.append(('author', author))
                    show = True

                if re.search('^.*' + str(title) + '.*$', m.bsp[bsp]['title']):
                    criteria.append(('title', title))
                    show = True

            if pk3_name and re.search('^.*' + pk3_name + '.*$', m.pk3_file):
                criteria.append(('pk3', pk3_name))
                show = True

            if shasum == m.shasum:
                criteria.append(('shasum', shasum))
                show = True

            if show:
                total += 1
                fmaps_json.append(m)

        criteria = list(set(criteria))

        if len(criteria) > 0:
            cprint("Using repo '{}'".format(self.name), style="HEADER")
            cprint("Searching for packages with the following criteria:", style='INFO')
            for c in criteria:
                print("{}{}{}: {}".format(zcolors.BOLD, str(c[0]), zcolors.ENDC, str(c[1])))
            print('---')

        for m in fmaps_json:
            bsps = m.bsp
            keys = list(bsps)
            keys.sort()

            shown = False
            for bsp in keys:
                if re.search('^.*' + bsp_name + '.*$', bsp) and not shown:
                    if bsp_name:
                        m.show_map_details(search_string=bsp_name, detail=detail, highlight=highlight)
                    elif pk3_name != '':
                        m.show_map_details(search_string=pk3_name, detail=detail, highlight=highlight)
                    else:
                        m.show_map_details(detail=detail, highlight=highlight)

                    shown = True
        print('---')
        print("{}Total packages found:{} {}{}{}".format(zcolors.INFO, zcolors.ENDC, zcolors.BOLD, str(total), zcolors.ENDC))

    # remote data
    def update_repo_data(self):
        """
        Updates sources cache with latest maps from *Repository*

        >>> from xmm.repository import Repository
        >>> repository = Repository(name='default', download_url='http://dl.repo.url/',
        >>>                         api_data_url='http://api.repo.url/maps.json', api_data_file='~/.xmm/maps.json')
        >>> repository.update_repo_data()
        """
        try:
            cprint("Updating {} sources json...".format(self.name), style='INFO')
            self.logger.info("Updating {} sources json...".format(self.name))
            util.download_file(self.api_data_file, url=self.api_data_url, use_curl=self.conf['default']['use_curl'], overwrite=True)
        except URLError as e:
            self.logger.debug('Error updating repo data: {}'.format(e))
            raise RepositoryUpdateError

    def get_packages(self):
        """
        Gets the cached map list from *Repository* or reads from file if cache not available

        :returns: ``json``

        >>> from xmm.repository import Repository
        >>> repository = Repository(name='default', download_url='http://dl.repo.url/',
        >>>                         api_data_url='http://api.repo.url/maps.json', api_data_file='~/.xmm/maps.json')
        >>> print(repository.get_packages())
        """

        self.logger.debug("getting repo data")

        if not self.repo_data:

            repo_data = []

            if not os.path.exists(self.api_data_file):
                cprint("Could not find a repo file. Using maplist shipped with release. For the latest maps, run xmm update.".format(self.name), style='WARNING')
                self.logger.info("Could not find a repo file. Using maplist shipped with release. For the latest maps, run xmm update.".format(self.name))

                import zipfile
                zip_ref = zipfile.ZipFile(self.conf['default']['api_data_file_seed'], 'r')
                zip_ref.extract('maps.json', os.path.dirname(self.api_data_file))
                zip_ref.close()

            with open(self.api_data_file) as f:
                data = f.read()
                maps = json.loads(data)['data']

            for m in maps:
                new_map = MapPackage(map_package_json=m)
                repo_data.append(new_map)

            self.repo_data = repo_data

        return self.repo_data

    def export_packages(self, filename=None):
        """
        :param filename:
            Name for the exported json file, default ``maps.json``
        :type filename: ``str``

        :returns: False if fails

        >>> from xmm.repository import Repository
        >>> repository = Repository(name='default', download_url='http://dl.repo.url/',
        >>>                         api_data_url='http://api.repo.url/maps.json', api_data_file='~/.xmm/maps.json')
        >>> repository.export_packages('test.json')
        """
        if not filename:
            filename = 'xmm-export.maps.json'

        self.logger.info("exporting maps as: {}".format(filename))

        data = self.get_packages()

        if data:
            try:
                with open(filename, 'w') as f:
                    f.write(json.dumps(data, cls=util.ObjectEncoder))
            except EnvironmentError as e:
                self.logger.error(e)
                return False

    def get_hash_index(self):
        """
        Gets a list of all pk3s and their shasums

        :returns: False if fails

        >>> from xmm.repository import Repository
        >>> repository = Repository(name='default', download_url='http://dl.repo.url/',
        >>>                         api_data_url='http://api.repo.url/maps.json', api_data_file='~/.xmm/maps.json')
        >>> print(repository.get_hash_index())
        """
        maps_json = self.get_packages()
        lines = []
        for m in maps_json:
            lines.append("{} {}".format(m.shasum, m.pk3_file))

        return lines

    def export_hash_index(self, filename=None):
        """
        :param filename:
            Name for the exported json file, default ``maps.json.shasums``
        :type filename: ``str``

        :returns: False if fails

        >>> from xmm.repository import Repository
        >>> repository = Repository(name='default', download_url='http://dl.repo.url/',
        >>>                         api_data_url='http://api.repo.url/maps.json', api_data_file='~/.xmm/maps.json')
        >>> repository.export_hash_index('test.shasums')
        """
        if not filename:
            filename = 'xmm-export.maps.shasums'

        self.logger.info("exporting shasums to file: {}".format(filename))

        lines = self.get_hash_index()

        if lines:
            try:
                with open(filename, 'w') as f:
                    f.write('\n'.join(lines))
            except EnvironmentError as e:
                self.logger.error(e)
                return False

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

        >>> from xmm.repository import Repository
        >>> repository = Repository(name='default', download_url='http://dl.repo.url/',
        >>>                         api_data_url='http://api.repo.url/maps.json', api_data_file='~/.xmm/maps.json')
        >>> repository.show_map(pk3_name='vinegar_v3.pk3')
        """

        self.logger.debug("Showing map with helper")

        packages = self.get_packages()
        found_map = False

        for p in packages:
            if p.pk3_file == pk3_name:
                p.show_map_details(search_string=pk3_name, detail=detail, highlight=highlight)
                found_map = p

        if not found_map:
            raise PackageLookupError

        return found_map
