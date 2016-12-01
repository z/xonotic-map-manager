import json
import os
import re
import urllib.request
from urllib.error import URLError

from xmm.map import MapPackage

from xmm.base import Base
from xmm.util import bcolors
from xmm import util


class SourceCollection(object):
    """
    A *SourceCollection* is a collection of *SourceRepository* objects

    :returns object: *SourceCollection*
    """
    def __init__(self):
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

    def add_repository(self, repository):
        """
        Add a *SourceRepository* to the *SourceCollection*

        :param repository:
        :type repository: ``SourceRepository``
        """
        self.sources.append(repository)

    def search_all(self, bsp_name=False, gametype=False, author=False, title=False, pk3_name=False, shasum=False, detail=None, highlight=False):
        """
        Searches all *SourceRepository* objects in the *SourceCollection* for maps matching criteria

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
        """
        for repo in self.sources:
            repo.search_maps(bsp_name=bsp_name, gametype=gametype, author=author, title=title, pk3_name=pk3_name, shasum=shasum, detail=detail, highlight=highlight)

    def update_all(self):
        """
        Update the data for all *SourceRepository* objects in the *SourceCollection*
        """
        for repo in self.sources:
            repo.update_repo_data()


class SourceRepository(Base):
    """
    A *SourceRepository* contains a url which hosts content matching the
    **JSON** format described in the documentation

    :param name:
        A name for this *SourceRepository*
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

    :returns object: ``SourceRepository``

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
        """
        maps_json = self.get_repo_data()
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
            print(bcolors.HEADER + 'Searching ' + self.name + ' repo for packages with the following criteria:' + bcolors.ENDC)
            for c in criteria:
                print(bcolors.BOLD + str(c[0]) + bcolors.ENDC + ': ' + str(c[1]))

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

        print('\n' + bcolors.OKBLUE + 'Total packages found:' + bcolors.ENDC + ' ' + bcolors.BOLD + str(total) + bcolors.ENDC)

    # remote data
    def update_repo_data(self):
        """
        Updates sources cache with latest maps from *Repository*
        """
        try:
            print('Updating ' + self.name + ' sources json...')
            urllib.request.urlretrieve(self.api_data_url, self.api_data, util.reporthook)
            print(bcolors.OKBLUE + 'Done.' + bcolors.ENDC)
        except URLError as e:
            self.logger.debug('Error updating repo date: {}'.format(e))

    def get_repo_data(self):
        """
        Gets the cached map list from *Repository*

        :returns: ``json``
        """
        if not self.repo_data:

            repo_data = []

            if not os.path.exists(self.api_data_file):
                print(bcolors.WARNING + 'Could not find a repo file. Downloading one.' + bcolors.ENDC)
                util.check_if_not_create(self.api_data_file, './resources/data/maps.json')

            with open(self.api_data_file) as f:
                data = f.read()
                maps = json.loads(data)['data']

            for m in maps:
                new_map = MapPackage(map_package_json=m)
                repo_data.append(new_map)

            self.repo_data = repo_data

        return self.repo_data

    def show_map(self, pk3_name, detail=None, highlight=False):
        """
        Convenience function to use the show_map_details helper

        :param pk3_name:
            The name of a pk3, such as ``dance.pk3``
        :type pk3_name: ``str``

        :param detail:
            How much detail to show, [short, None, long]
        :type detail: ``str``

        :param highlight:
            Whether to highlight the results
        :type highlight: ``bool``

        :returns: ``MapPackage``
        """

        packages = self.get_repo_data()
        found_map = False

        for p in packages:
            if p.pk3_file == pk3_name:
                found_map = True
                p.show_map_details(search_string=pk3_name, detail=detail, highlight=highlight)

        if not found_map:
            print(bcolors.BOLD + pk3_name + bcolors.ENDC + bcolors.FAIL + ' package was not found in repository' + bcolors.ENDC)

        return found_map
