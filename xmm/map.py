import time
import json

from xmm.base import Base
from xmm.util import zcolors
from xmm import util


class MapPackage(Base):
    """
    *MapPackage* contains top-level metadata about a pk3 file and list of *Bsp* objects inside this package

    :param map_package_json:
        A dict or *JSON* string that matches "specification" in the Developers section of the documentation.

        See basic example below:

        .. code-block:: json

            {
              "data": [
                {
                  "date": 1453749340,
                  "filesize": 7856907,
                  "bsp": {
                    "vapor_alpha_2": {
                      "radar": "gfx/vapor_alpha_2_mini.tga",
                      "waypoints": "",
                      "title": "Vapor",
                      "description": "Such CTF. Many Vehicles. Wow.",
                      "map": "maps/vapor_alpha_2.map",
                      "entities": {
                        "info_player_deathmatch": 4,
                        "info_player_team1": 11,
                        "info_player_team2": 11,
                        "item_armor_big": 10,
                        "item_armor_large": 4,
                        "item_armor_medium": 16,
                        "item_armor_small": 124,
                        "item_bullets": 10,
                        "item_cells": 14,
                        "item_flag_team1": 1,
                        "item_flag_team2": 1,
                        "item_health_large": 6,
                        "item_health_medium": 30,
                        "item_health_mega": 2,
                        "item_health_small": 100,
                        "item_invincible": 1,
                        "item_rockets": 20,
                        "item_strength": 1,
                        "weapon_crylink": 4,
                        "weapon_devastator": 6,
                        "weapon_electro": 2,
                        "weapon_grenadelauncher": 6,
                        "weapon_hagar": 4,
                        "weapon_machinegun": 6,
                        "weapon_vortex": 4
                      },
                      "mapinfo": "maps/vapor_alpha_2.mapinfo",
                      "author": "-z-",
                      "gametypes": [
                        "ctf",
                        "DM"
                      ],
                      "license": true,
                      "mapshot": "maps/vapor_alpha_2.jpg"
                    }
                  },
                  "shasum": "3df0143516f72269f465070373f165c8787964d5",
                  "pk3": "map-vapor_alpha_2.pk3"
                }
              ]
            }

    :type map_package_json: ``string|dict``

    :returns object: ``MapPackage``

    >>> from xmm.map import MapPackage
    >>> with open('my_map.json') as f:
    >>>     data = f.read()
    >>>     my_map = MapPackage(map_package_json=data)

    """
    def __init__(self, map_package_json):
        super().__init__()

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
        """
        :returns: A **JSON** encoded version of this object
        """
        return json.dumps(self, cls=util.ObjectEncoder)

    def show_map_details(self, detail=None, search_string='', highlight=False):
        """
        Helper function for pretty printing details about a *MapPackage*

        Convenience function to use the show_map_details helper

        :param detail:
            How much detail to show, [short, None, long]
        :type detail: ``str``

        :param search_string:
            A string to highlight with ``highlight=True``
        :type search_string: ``str``

        :param highlight:
            Whether to highlight the results
        :type highlight: ``bool``

        :returns: ``MapPackage``
        """

        self.logger.debug('Showing details for map: {}'.format(self.pk3_file))

        bsps = self.bsp
        keys = list(bsps)
        keys.sort()
        search_string = str(search_string)

        # Long view
        if detail == 'long':
            print('')
            print('         pk3: {}{}{}'.format(zcolors.BOLD, str(self.pk3_file), zcolors.ENDC))

            for bsp in keys:
                # Handle highlight
                string_highlighted = '{}{}{}{}{}'.format(zcolors.ENDC, zcolors.SUCCESS, search_string, zcolors.ENDC, zcolors.INFO)
                bsp_highlighted = bsp.replace(search_string, string_highlighted)
                if search_string and highlight:
                    print('         bsp: {}{}{}'.format(zcolors.INFO, bsp_highlighted, zcolors.ENDC))
                else:
                    print('         bsp: {}{}{}'.format(zcolors.INFO, bsp, zcolors.ENDC))

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

        # Short detail view
        elif detail == 'short':
            print(str(self.pk3_file))
        # Default view
        else:
            bsp_string = '\n{}{}{} ['.format(zcolors.BOLD, str(self.pk3_file), zcolors.ENDC)
            for bsp in keys:
                # Handle highlight
                string_highlighted = '{}{}{}{}{}'.format(zcolors.ENDC, zcolors.SUCCESS, search_string, zcolors.ENDC, zcolors.INFO)
                bsp_highlighted = bsp.replace(search_string, string_highlighted)
                if search_string and highlight:
                    bsp_string += '{}{}{}, '.format(zcolors.INFO, bsp_highlighted, zcolors.ENDC)
                else:
                    bsp_string += '{}{}{}, '.format(zcolors.INFO, bsp, zcolors.ENDC)
            bsp_string = util.replace_last(bsp_string, ', ', '')
            bsp_string += ']'.format(zcolors.ENDC)
            print(bsp_string)
            print('{}{}'.format(self.conf['default']['download_url'], str(self.pk3_file)))


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
