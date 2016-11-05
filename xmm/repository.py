import json
import os
import re
import urllib.request

from xmm.xonotic import Server
from xmm.util import bcolors
from xmm import util


class RepositoryCommand(Server):

    def __init__(self, args, conf):
        super().__init__(args, conf)
        self.repo_data = {}

    def search_maps(self, args):

        maps_json = self.get_repo_data()
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
                    self.show_map_details(m, args)
                    shown = True

        print('\n' + bcolors.OKBLUE + 'Total packages found:' + bcolors.ENDC + ' ' + bcolors.BOLD + str(total) + bcolors.ENDC)

    # remote data
    def update_repo_data(self):
        print('Updating sources json...')
        urllib.request.urlretrieve(self.conf['api_data_url'], os.path.expanduser(self.conf['api_data']), util.reporthook)
        print(bcolors.OKBLUE + 'Done.' + bcolors.ENDC)

    def get_repo_data(self):

        api_data_file = os.path.expanduser(self.conf['api_data'])

        if not self.repo_data:
            if not os.path.exists(api_data_file):
                api_data_file = os.path.expanduser(self.conf['api_data'])
                print(bcolors.WARNING + 'Could not find a repo file. Downloading one.' + bcolors.ENDC)
                util.check_if_not_create(api_data_file, './resources/data/maps.json')

            f = open(api_data_file)
            data = f.read()
            self.repo_data = json.loads(data)['data']
            f.close()

        return self.repo_data
