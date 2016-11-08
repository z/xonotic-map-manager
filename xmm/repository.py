import json
import os
import re
import time
import urllib.request

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


class SourceRepository(Base):
    """
    A *SourceRepository* contains a url which hosts content matching the
    **JSON** format described in the documentation

    :param conf:
        The conf dictionary from ``config.py``
    :type conf: ``dict``

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
    def __init__(self, conf, name, download_url, api_data_url, api_data_file):
        super().__init__(conf)
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

    def search_maps(self, bsp_name=False, gametype=False, author=False, title=False, pk3_name=False, shasum=False, args=None):
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

        :param args:
            Positional arguments that will be *deprecated*
        :type args: ``tuple``
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
            print(bcolors.HEADER + 'Searching for packages with the following criteria:' + bcolors.ENDC)
            for c in criteria:
                print(bcolors.BOLD + str(c[0]) + bcolors.ENDC + ': ' + str(c[1]))

        for m in fmaps_json:
            bsps = m.bsp
            keys = list(bsps)
            keys.sort()

            shown = False
            for bsp in keys:
                if re.search('^.*' + bsp_name + '.*$', bsp) and not shown:
                    m.show_map_details(args=args)
                    shown = True

        print('\n' + bcolors.OKBLUE + 'Total packages found:' + bcolors.ENDC + ' ' + bcolors.BOLD + str(total) + bcolors.ENDC)

    # remote data
    def update_repo_data(self):
        """
        Updates sources cache with latest maps from *Repository*
        """
        print('Updating sources json...')
        urllib.request.urlretrieve(self.api_data_url, self.api_data, util.reporthook)
        print(bcolors.OKBLUE + 'Done.' + bcolors.ENDC)

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
                new_map = MapPackage(conf=self.conf, map_package_json=m)
                repo_data.append(new_map)

            self.repo_data = repo_data

        return self.repo_data
