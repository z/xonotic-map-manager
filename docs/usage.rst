Usage
=====

Basic Usage
-----------

CLI help docs for ``xmm``::

    usage: xmm [-h] [-s [SERVER]] [-T [TARGET]]
               {search,install,remove,discover,list,show,export,update,hello} ...

    Xonotic Map Manager is a tool to help manage Xonotic maps

    positional arguments:
      {search,install,remove,discover,list,show,export,update,hello}
        search              search for maps based on bsp names
        install             install a map from the repository, or specify a URL.
        remove              remove based on pk3 name
        discover            discover packages in a target directory
        list                list locally installed packages
        show                show details of locally installed package
        export              export locally managed packages to a file
        update              update sources json
        hello               hello is an example plugin

    optional arguments:
      -h, --help            show this help message and exit
      -s [SERVER], --server [SERVER]
                            target server as defined in servers.json
      -T [TARGET], --target [TARGET]
                            target directory


Searching
~~~~~~~~~

by bsp name::

    xmm search snowdance
    Searching for: snowdance
    snowdance2
    http://dl.xonotic.co/snowdance2.pk3
    snowdance2
    http://dl.xonotic.co/snowdance_xon.pk3


with pk3 name and detailed results::

    xmm search -p bloodrage_v2.pk3 --long
    Searching for packages with the following criteria:
    pk3: bloodrage_v2.pk3

             pk3: bloodrage_v2.pk3
             bsp: bloodrage_v2
           title: Bloodrage
     description: Small, brutal and violent 1on1 map
          author: Cortez and FruitieX
          shasum: 488b05976e73456bf6f9833e353f72d3a8d0cbce
            date: 2009-10-17
            size: 1MB
              dl: http://dl.xonotic.co/bloodrage_v2.pk3

    Total packages found: 1


Inline help is available on all sub-commands::

    xmm search -h
    usage: xmm search [-h] [--gametype [GAMETYPE]] [--pk3 [PK3]] [--title [TITLE]]
                      [--author [AUTHOR]] [--shasum [SHASUM]] [--long] [--short]
                      [--highlight]
                      [string]

    positional arguments:
      string                bsp name found in a package, works on packages with
                            many bsps

    optional arguments:
      -h, --help            show this help message and exit
      --gametype [GAMETYPE], -g [GAMETYPE]
                            filter by gametype
      --pk3 [PK3], -p [PK3]
                            filter by pk3 name
      --title [TITLE], -t [TITLE]
                            filter by title
      --author [AUTHOR], -a [AUTHOR]
                            filter by author
      --shasum [SHASUM]     filter by shasum
      --long, -l            show long format
      --short, -s           show short format
      --highlight, -H       highlight search term in results


Installing from the repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Installing a new pk3::

    xmm install snowdance_xon.pk3
    Installing map from repository: snowdance_xon.pk3
    ...100%, 5 MB, 2438 KB/s, 2 seconds passed. Done.


You cannot overwrite an existing pk3::

    xmm install snowdance_xon.pk3
    Installing map from repository: snowdance_xon.pk3
    package already exists, please remove first.


You cannot install a pk3 that doesn't existent in the repo::

    xmm install fake.pk3
    Installing map from repository: fake.pk3
    package does not exist in the repository.

Example below is also showing the use of curl instead of python's urllib if you prefer::

    xmm install http://somerepo.org/snowdance2.pk3
    Adding map: http://somerepo.org/snowdance2.pk3
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100 5530k  100 5530k    0     0   205k      0  0:00:26  0:00:26 --:--:--  179k
    Done.


You can install from any URL (buy lack detailed meta information about maps)::

    xmm install http://somerepo.org/snowdance2.pk3
    Adding map: http://somerepo.org/snowdance2.pk3
    ...100%, 5 MB, 2438 KB/s, 2 seconds passed. Done.


Removing
~~~~~~~~

Remove a map::

    xmm remove snowdance2.pk3
    Removing map: snowdance2.pk3
    Done.

You cannot remove a map that doesn't exist::

    xmm remove snowdance2.pk3
    Removing map: snowdance2.pk3
    map does not exist.



Discover
~~~~~~~~

You can pulled additional meta information about pk3s and verify their shasums against the repo with the discover command.

A summary of discovered packages::

    xmm -s myserver1 discover

    map-ctf-moonstone_nex_r3.pk3 [moonstone_nex_r3]
    http://dl.xonotic.co/map-ctf-moonstone_nex_r3.pk3

    map-ctf-mIKEctf1_nex_r1.pk3 package was not found in repository

    dance.pk3 [dance]
    http://dl.xonotic.co/dance.pk3


    snowdance_xon.pk3 [snowdance2]
    http://dl.xonotic.co/snowdance_xon.pk3


    dance-fixed.pk3 [dance-fixed]
    http://dl.xonotic.co/dance-fixed.pk3


    got_wood-on-xctf3.pk3 [got_wood]
    http://dl.xonotic.co/got_wood-on-xctf3.pk3


    map-ctf-mikectf3_nex_r3_fix.pk3 [mIKEctf3_nex_r3]
    http://dl.xonotic.co/map-ctf-mikectf3_nex_r3_fix.pk3

    map-vapor_alpha_2.pk3 hash different from repositories

Add discovered maps::

    xmm -s myserver1 discover --add

List Map Packages
~~~~~~~~~~~~~~~~~

simple list::

    xmm list

    gasoline_02.pk3 [gasoline_02, gasoline_3teams_02, gasoline_4teams_02, gasoline_noteams_02]
    http://dl.xonotic.co/gasoline_02.pk3

    dance.pk3 [dance]
    http://dl.xonotic.co/dance.pk3

    Total packages found: 2


detailed list::

    xmm list -l

             pk3: gasoline_02.pk3
             bsp: gasoline_02
           title:  Gasoline Powered
     description:  Retextured and glowy
          author:  FruitieX, Kid, Mario
             bsp: gasoline_3teams_02
           title:  Gasoline Powered
     description:  Retextured and glowy with 3 teams
          author:  FruitieX, Kid, Mario, Freddy
             bsp: gasoline_4teams_02
           title:  Gasoline Powered
     description:  Retextured and glowy with 4 teams
          author:  FruitieX, Kid, Mario
             bsp: gasoline_noteams_02
           title:  Gasoline Powered - Teamless
     description:  Retextured and glowy
          author:  FruitieX, Kid, Mario
          shasum: 099b0cc16fe998e5e29893dbecd5673683a5b69d
            date: 2015-10-17
            size: 14MB
              dl: http://dl.xonotic.co/gasoline_02.pk3

             pk3: dance.pk3
             bsp: dance
           title:  <TITLE>
     description:  <DESCRIPTION>
          author:  <AUTHOR>
          shasum: ef00d43838430b2d1673f03bbe1440eef100ece6
            date: 2008-03-16
            size: 7MB
              dl: http://dl.xonotic.co/dance.pk3


    Total packages found: 3

Show Map Package Details
~~~~~~~~~~~~~~~~~~~~~~~~

simple::

    xmm show dance.pk3

    dance.pk3
    dance
    http://dl.xonotic.co/dance.pk3

detailed::

    xmm show dance.pk3 -l

             pk3: dance.pk3
             bsp: dance
           title: <TITLE>
     description: <DESCRIPTION>
          author: <AUTHOR>
          shasum: ef00d43838430b2d1673f03bbe1440eef100ece6
            date: 2008-03-16
            size: 7MB
              dl: http://dl.xonotic.co/dance.pk3

Export
~~~~~~

You can export your maplist to a map-repo repository friend json format::

    % xmm export test.json
    % cat test.json
    [{"mapinfo": ["maps/dance.mapinfo"], "date": 1205715512, "title": "<TITLE>", "radar": [], "waypoints": [], "gametypes": ["ctf", "dm", "lms", "arena"], "mapshot": ["maps/dance.jpg"], "description": "<DESCRIPTION>", "shasum": "ef00d43838430b2d1673f03bbe1440eef100ece6", "filesize": 7468410, "pk3": "dance.pk3", "map": ["maps/dance.map"], "author": "<AUTHOR>", "license": false, "bsp": {"dance": {"entities": {"item_cells": 14, "item_bullets": 14, "info_player_team1": 10, "item_rockets": 16, "info_player_team2": 11, "item_invincible": 1, "weapon_hagar": 2, "item_flag_team1": 1, "weapon_electro": 2, "item_health_medium": 14, "item_health_small": 20, "weapon_machinegun": 2, "item_strength": 1, "weapon_vortex": 3, "item_armor_small": 19, "weapon_devastator": 2, "item_flag_team2": 1, "weapon_grenadelauncher": 2}}}}]%


Update
~~~~~~

Get the latest list of maps from the repository::

    xmm update
    Updating sources json.
    ...100%, 7 MB, 2559 KB/s, 3 seconds passed. Done.

Advanced Usage
--------------

Multi-server support
~~~~~~~~~~~~~~~~~~~~

xmm can facilitate the management of multiple servers with a ``~/.xmm/servers.json`` file to configure their settings, example below:

.. code-block:: json

    {
      "myserver1": {
        "target_dir": "~/.xonotic/myserver1/data/",
        "library": "~/.xmm/myserver1/library.json",
        "sources": "~/.xmm/sources.json"
      },
      "myserver2": {
        "target_dir": "~/.xonotic/myserver2/data/",
        "library": "~/.xmm/myserver2/library.json",
        "sources": "~/.xmm/myserver2/sources.json"
      }
    }


An example is available in ``./config/example.servers.json``

To use these servers, use the ``-s`` flag to target the server.::


    xmm -s myserver1 install dance.pk3
    xmm -s myserver1 list
    xmm -s myserver1 remove dance.pk3


Targeting Directories
~~~~~~~~~~~~~~~~~~~~~

Sometimes you may want to install a package to an arbitrary directory.::

    xmm -T /path/to/directory/ install dance.pk3

This install will not be tracked in the library.


* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
