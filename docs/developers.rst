Developers
==========

JSON structure
--------------

Same structure used by `xonotic-map-repository`_:

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

.. _xonotic-map-repository: https://github.com/z/xonotic-map-repository

Plugin System
-------------

Checkout the examples in the ``./xmmc/plugins`` directory.

.. code-block:: python

    from xmm.plugins import pluginbase
    from xmm.util import zcolors
    from xmm.util import cprint

    config = pluginbase.get_config()


    def get_args():
        command='hello'
        command_help={'help': 'hello is an example plugin'}
        args=['-f', '--foo']
        kwargs={'type': int, 'nargs': '?', 'help': 'this is a help line'}
        return command, command_help, args, kwargs


    def run():
        print("Hello from a plugin!")
        cprint("I share the xmm util module", style='INFO')
        print("{}Look, I have access to the config: {}".format(zcolors.SUCCESS, config['api_data']))

.. warning::

    This plugin system needs to be revisited and will likely change by the next minor release.

Debugging
---------

The default logging configuration comes with two file handlers, info and debug, which info enabled by default.

To enable debug, in `~/.xmm/xmm.logging.ini` change:

.. code-block:: ini

    [logger_root]
    level    = NOTSET
    handlers = stream, info

    [handlers]
    keys = stream, info

To:

.. code-block:: ini

    [logger_root]
    level    = NOTSET
    handlers = stream, debug

    [handlers]
    keys = stream, debug

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
