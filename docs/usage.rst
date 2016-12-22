.. _usage:

Usage
=====

Basic Usage
-----------

CLI help docs for ``xmm``::

    usage: xmm [-h] [--version] [-S [SERVER]] [-T [TARGET]] [-R [REPOSITORY]]
               {search,install,remove,discover,list,show,export,servers,repos,update,hello}
               ...

    Xonotic Map Manager is a tool to help manage Xonotic maps

    positional arguments:
      {search,install,remove,discover,list,show,export,servers,repos,update,hello}
        search              search for maps based on bsp names
        install             install a map from the repository, or specify a URL.
        remove              remove based on pk3 name
        discover            discover packages in a target directory
        list                list locally installed packages
        show                show details of remote or locally installed packages
        export              export locally managed packages to a file
        servers             subcommands on servers described in servers.json
        repos               subcommands on repos described in sources.json
        update              update sources json
        hello               hello is an example plugin

    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      -S [SERVER], --server [SERVER]
                            target server as defined in servers.json
      -T [TARGET], --target [TARGET]
                            target directory
      -R [REPOSITORY], --repository [REPOSITORY]
                            repository to use (defaults to all available)



Searching
~~~~~~~~~

by bsp name::

    xmm search snowdance
    Searching for packages with the following criteria:
    bsp: snowdance
    ---

    snowdance2.pk3 [snowdance2]
    http://dl.xonotic.co/snowdance2.pk3

    snowdance_xon.pk3 [snowdance2]
    http://dl.xonotic.co/snowdance_xon.pk3
    ---
    Total packages found: 2


with pk3 name and detailed results::

    xmm search --pk3 bloodrage_v2.pk3 --long
    Using repo 'default'
    Searching for packages with the following criteria:
    pk3: bloodrage_v2.pk3
    ---

             pk3: bloodrage_v2.pk3
             bsp: bloodrage_v2
           title:  Bloodrage
     description:  Small, brutal and violent 1on1 map
          author:  Cortez and FruitieX
          shasum: 488b05976e73456bf6f9833e353f72d3a8d0cbce
          shasum: bloodrage_v2.pk3
            date: 2009-10-17
            size: 1MB
              dl: http://dl.xonotic.co/bloodrage_v2.pk3
    ---
    Total packages found: 1


Inline help is available on all sub-commands::

    xmm search -h
    usage: xmm search [-h] [--gametype [GAMETYPE]] [--pk3 [PK3]] [--title [TITLE]]
                      [--author [AUTHOR]] [--shasum [SHASUM]] [--long] [--short]
                      [--color]
                      [string]

    positional arguments:
      string                bsp name found in a package, works on packages with
                            many bsps

    optional arguments:
      -h, --help            show this help message and exit
      --gametype [GAMETYPE]
                            filter by gametype
      --pk3 [PK3]           filter by pk3 name
      --title [TITLE]       filter by title
      --author [AUTHOR]     filter by author
      --shasum [SHASUM]     filter by shasum
      --long, -l            show long format
      --short, -s           show short format
      --color, -c           highlight search term in results


Installing from the repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Installing a new pk3::

    xmm install snowdance_xon.pk3
    Installing map: snowdance_xon.pk3
    ...100%, 5 MB, 2438 KB/s, 2 seconds passed. Done.

You will be prompted to overwrite an existing pk3::

    xmm install snowdance_xon.pk3
    Installing map: snowdance_xon.pk3
    snowdance_xon.pk3 already exists.
    continue? [y/N] N
    Canceled.

You cannot install a pk3 that doesn't existent in the repo::

    Installing map: fake.pk3
    package does not exist in the repository. cannot install.

Example below is also showing the use of curl instead of python's urllib if you prefer::

    xmm install http://somerepo.org/snowdance2.pk3
    Adding map: http://somerepo.org/snowdance2.pk3
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100 5530k  100 5530k    0     0   205k      0  0:00:26  0:00:26 --:--:--  179k
    Done.

You can install from any URL (buy lack detailed meta information about maps)::

    xmm install http://somerepo.org/some-other-map.pk3
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
    Removing package: snowdance_xon.pk3
    package does not exist or is not tracked. try removing using full path if not tracked.

Discover
~~~~~~~~

You can pulled additional meta information about pk3s and verify their shasums against the repo with the discover command.

A summary of discovered packages::

    xmm -S myserver1 discover

    sxb1_testing_6.pk3 [sxb1_-1, sxb1_-2, sxb1_-3, sxb1_1-1, sxb1_1-2, sxb1_1-3, sxb1_1-4, sxb1_2-1, sxb1_2-2, sxb1_2-3, sxb1_2-4, sxb1_3-1, sxb1_3-2, sxb1_3-3, sxb1_3-4, sxb1_4-1, sxb1_4-2, sxb1_4-3, sxb1_4-4, sxb1_5-1, sxb1_5-2, sxb1_5-3, sxb1_5-4, sxb1_6-1, sxb1_6-2, sxb1_6-3, sxb1_6-4, sxb1_7-1, sxb1_7-2, sxb1_7-3, sxb1_7-4, sxb1_8-1, sxb1_8-2, sxb1_8-3, sxb1_8-4]
    http://dl.xonotic.co/sxb1_testing_6.pk3

    bloodprisonctf.pk3 [bloodprisonctf]
    http://dl.xonotic.co/bloodprisonctf.pk3
    bloodprisonctf.pk3 hash does not match repository's

    gasoline_02.pk3 [gasoline_02, gasoline_3teams_02, gasoline_4teams_02, gasoline_noteams_02]
    http://dl.xonotic.co/gasoline_02.pk3

    testie3.pk3 [testie3]
    http://dl.xonotic.co/testie3.pk3

    map-derail_v1r5.pk3 [derail_v1r5]
    http://dl.xonotic.co/map-derail_v1r5.pk3
    map-derail_v1r5.pk3 hash does not match repository's

    disarray_v1r2.pk3 [disarray_v1r2]
    http://dl.xonotic.co/disarray_v1r2.pk3

    eggandscrambled.pk3 [eggandscrambled]
    http://dl.xonotic.co/eggandscrambled.pk3

Add discovered maps::

    xmm -S myserver1 discover --add

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

You can export local maps from your library, or maps from a repository in different formats::

    usage: xmm export [-h] [--format {json,shasums}] {local,repos} [filename]

    positional arguments:
      {local,repos}         what context to export?
      filename              filename to export to

    optional arguments:
      -h, --help            show this help message and exit
      --format {json,shasums}, -f {json,shasums}

For example, export a maplist to a map-repo-friendly json format::

    % xmm export local test.json -f json
    % cat test.json
    [{"mapinfo": ["maps/dance.mapinfo"], "date": 1205715512, "title": "<TITLE>", "radar": [], "waypoints": [], "gametypes": ["ctf", "dm", "lms", "arena"], "mapshot": ["maps/dance.jpg"], "description": "<DESCRIPTION>", "shasum": "ef00d43838430b2d1673f03bbe1440eef100ece6", "filesize": 7468410, "pk3": "dance.pk3", "map": ["maps/dance.map"], "author": "<AUTHOR>", "license": false, "bsp": {"dance": {"entities": {"item_cells": 14, "item_bullets": 14, "info_player_team1": 10, "item_rockets": 16, "info_player_team2": 11, "item_invincible": 1, "weapon_hagar": 2, "item_flag_team1": 1, "weapon_electro": 2, "item_health_medium": 14, "item_health_small": 20, "weapon_machinegun": 2, "item_strength": 1, "weapon_vortex": 3, "item_armor_small": 19, "weapon_devastator": 2, "item_flag_team2": 1, "weapon_grenadelauncher": 2}}}}]%

Or a list of pk3s and their respective shasums::

    xmm export repos -f shasums
    tail all-repos-maps.json.shasums
    d88957aeff231471453f41e8ab2dad326b1875b2 acrossanocean12.pk3
    e3059ee1979985151fade8b0d317422dc71ec9bb cloisterctf_vehicles.pk3
    3f15789118762f469c9179f8f799747dced948cb dastower_vehicles.pk3
    5af57ca19b69560cd9b00f67cbbb7ee4526bc8ac duster_mod_01.pk3
    e06724125a3438a23bad4f0d3ec3b6a5ce89666a greatwall_remix_vehicles.pk3
    abc9e153c37784563e4e3c2669cc88af05649399 ons-reborn_vehicles.pk3


Servers
~~~~~~~

List servers with ``xmm servers list``::

    xmm servers list
    myserver2
    myserver1


Repos
~~~~~

List repositories with ``xmm repos list``::

    xmm repos list
    default
    gpl_only


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

To use these servers, use the ``-S`` flag to target the server::


    xmm -S myserver1 install dance.pk3
    xmm -S myserver1 list
    xmm -S myserver1 remove dance.pk3


Multi-repository support
~~~~~~~~~~~~~~~~~~~~~~~~

**xmm** can use multiple repositories, edit the ``~/.xmm/sources.json`` file to configure them, example below:

.. code-block:: json

    {
      "default": {
        "download_url": "http://dl.xonotic.co/",
        "api_data_file": "~/.xmm/maps.json",
        "api_data_url": "http://xonotic.co/resources/data/maps.json"
      }
    }

An example is available in ``./config/example.sources.json``

To use these servers, use the ``-R`` flag to target the server::

    xmm -R myrepo install dance.pk3
    xmm -R myrepo list
    xmm -R myrepo remove dance.pk3


Targeting Directories
~~~~~~~~~~~~~~~~~~~~~

Sometimes you may want to install a package to an arbitrary directory::

    xmm -T /path/to/directory/ install dance.pk3

.. note::

    This install will not be tracked in the library.


* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
