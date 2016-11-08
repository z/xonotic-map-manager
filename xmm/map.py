import time
import json

from xmm.base import Base
from xmm.util import bcolors
from xmm import util


class MapPackage(Base):
    """
    *MapPackage* contains top-level metadata about a pk3 file and list of *Bsp* objects inside this package

    :param conf:
        The conf dictionary from ``config.py``
    :type conf: ``dict``

    :param map_package_json:
        *JSON* as specified in the documentation
    :type map_package_json: ``json``

    :returns object: ``MapPackage``

    """
    def __init__(self, conf, map_package_json):
        super().__init__(conf)

        if not isinstance(map_package_json, dict):
            map_package = json.loads(map_package_json)
        else:
            map_package = map_package_json

        self.pk3_file = map_package['pk3']
        self.shasum = map_package['shasum']
        self._bsp = map_package['bsp']
        self.date = map_package['date']
        self.filesize = map_package['filesize']

    @property
    def bsp(self):
        return self._bsp

    @bsp.setter
    def bsp(self, key, value):
        self._bsp[key] = value

    @bsp.deleter
    def bsp(self, key):
        del self._bsp[key]

    def __repr__(self):
        return 'MapPackage(pk3=%s, shasum=%s, bsp=%s, date=%s, filesize=%s)' % (self.pk3_file, self.shasum, repr(self.bsp), self.date, self.filesize)

    def __json__(self):
        return {
            'pk3': self.pk3_file,
            'shasum': self.shasum,
            'filesize': self.filesize,
            'date': self.date,
            'bsp': self.bsp,
        }

    def to_json(self):
        return json.dumps(self, cls=util.ObjectEncoder)

    # TODO: improve this function
    def show_map_details(self, args):
        """
        Helper function for pretty printing details about a *MapPackage*
        """
        highlight = False
        search_string = ''

        if 'string' in args:
            search_string = args.string
        elif 'pk3' in args:
            search_string = args.pk3

        if 'highlight' in args and args.highlight:
            highlight = True

        bsps = self.bsp
        keys = list(bsps)
        keys.sort()

        # little ugly here for a lot of pretty out
        if args.long:
            print('')
            print('         pk3: ' + bcolors.BOLD + str(self.pk3_file) + bcolors.ENDC)

            for bsp in keys:
                # Handle Highlight
                if search_string and highlight:
                    print('         bsp: {}{}{}').format(bcolors.OKBLUE,
                                                         bsp.replace(search_string, bcolors.ENDC + bcolors.OKGREEN + search_string + bcolors.ENDC + bcolors.OKBLUE), bcolors.ENDC)
                else:
                    print('         bsp: {}'.format(bcolors.OKBLUE + bsp + bcolors.ENDC))

                # bsp specific
                print('       title:  {}'.format(str(self.bsp[bsp]['title'])))
                print(' description:  {}'.format(str(self.bsp[bsp]['description'])))
                print('      author:  {}'.format(str(self.bsp[bsp]['author'])))

            # pk3 specific
            print('      shasum: {}'.format(str(self.shasum)))
            print('      shasum: {}'.format(str(self.pk3_file)))
            print('        date: {}'.format(time.strftime('%Y-%m-%d', time.localtime(self.date))))
            print('        size: {}'.format(util.convert_size(self.filesize).strip()))
            print('          dl: {}'.format(self.conf['default']['download_url'] + self.pk3_file))

        # Formatting
        elif args.short:
            print(str(self.pk3_file))
        else:
            bsp_string = '\n' + bcolors.BOLD + str(self.pk3_file) + bcolors.ENDC + ' ['
            for bsp in keys:
                if search_string and highlight:
                    bsp_string += bcolors.OKBLUE + \
                        bsp.replace(search_string, bcolors.ENDC + bcolors.OKGREEN + search_string + bcolors.ENDC + bcolors.OKBLUE) \
                        + bcolors.ENDC + ', '
                else:
                    bsp_string += bcolors.OKBLUE + bsp + bcolors.ENDC + ', '
            bsp_string = util.replace_last(bsp_string, ', ', '')
            bsp_string += bcolors.ENDC + ']'
            print(bsp_string)
            print(self.conf['default']['download_url'] + str(self.pk3_file))


class Bsp(object):
    """
    A *Bsp* is a child of a *MapPackage* that holds metadata about this map

    :param pk3_file:
        The pk3_file name of the package this bsp is in
    :type pk3_file: ``str``

    :param bsp_name:
        The bsp_name of the bsp_file
    :type bsp_name: ``str``

    :param bsp_file:
        The bsp_file
    :type bsp_file: ``str``

    :param map_file:
        The map_file for the bsp_file if it exists
    :type map_file: ``str``

    :param mapshot:
        The mapshot for the bsp_file if it exists
    :type mapshot: ``str``

    :param title:
        The title for the bsp_file if it exists
    :type title: ``str``

    :param description:
        The description for the bsp_file if it exists
    :type description: ``str``

    :param mapinfo:
        The mapinfo for the bsp_file if it exists
    :type mapinfo: ``str``

    :param author:
        The author for the bsp_file if it exists
    :type author: ``str``

    :param gametypes:
        The gametypes for the bsp_file if it exists
    :type gametypes: ``list``

    :param entities:
        The entities for the bsp_file if they exists
    :type entities: ``str``

    :param waypoints:
        The waypoints for the bsp_file if it exists
    :type waypoints: ``str``

    :param license:
        The license for the bsp_file if it exists
    :type license: ``str``

    :returns object: ``Bsp``

    """
    def __init__(self, pk3_file='', bsp_name='', bsp_file='', map_file='', mapshot='', radar='', title='', description='', mapinfo='', author='', gametypes=None, entities=None, waypoints='', license=False):
        self.pk3_file = pk3_file
        self.bsp_name = bsp_name
        self.bsp_file = bsp_file
        self.map_file = map_file
        self.mapshot = mapshot
        self.radar = radar
        self.title = title
        self.description = description
        self.mapinfo = mapinfo
        self.author = author
        self.gametypes = gametypes
        self.entities = entities
        self.waypoints = waypoints
        self.license = license

    def __repr__(self):
        return 'Bsp(pk3_file=%s, bsp_name=%s, bsp_file=%s, map_file=%s, mapshot=%s, radar=%s, title=%s, description=%s, mapinfo=%s, author=%s, gametypes=%s,entities=%s, waypoints=%s, license=%s)' % (self.pk3_file, self.bsp_name, self.bsp_file, self.map_file, self.mapshot, self.radar, self.title, self.description, self.mapinfo, self.author, self.gametypes, self.entities, self.waypoints, self.license)

    def __json__(self):
        return {
            'map': self.map_file,
            'mapshot': self.mapshot,
            'radar': self.radar,
            'title': self.title,
            'description': self.description,
            'mapinfo': self.mapinfo,
            'author': self.author,
            'gametypes': self.gametypes,
            'entities': self.entities,
            'waypoints': self.waypoints,
            'license': self.license,
        }

    def to_json(self):
        """
        :returns: A **JSON** encoded version of this object
        """
        return json.dumps(self, cls=util.ObjectEncoder)

