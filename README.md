# xonotic-map-manager

## About

This application works by reading a locally cached json file generated.
 This file is accessible as a web-frontend at http://xonotic.co, which is using the [xonotic-map-repository](https://github.com/z/xonotic-map-repository) to
generate it from a directory of map packages (pk3 files).

The data set you find in the JSON is more rich than what you see in game.
It also makes it easier to discern differences in packages.

For information about what data is available check [JSON Structure](#JSON-structure).

It's possible to host your own collection of curated maps with a web-frontend
 and point this tool at it to manage maps on a server.

## Installation

```
python3 setup.py install
```

## Configuration

The default settings are likely similar to yours, however, you may need
to edit `~/~.xmm.cfg` if you aren't using `~/.xonotic/data` as a path for
map packages.

`~/.xmm.cfg`:

```
[default]

# Where should xmm manage maps?
map_dir = ~/.xonotic/data/

# You don't need to change tehse unless you're running your own repo
repo_url = http://dl.xonotic.co/
api_data = ./resources/data/maps.json
api_data_url = http://xonotic.co/resources/data/maps.json

# This is only preference
use_curl = False

# This is for the future local tracking of installed packages
package_store = ./resources/data/packages.db
```

## Usage

```
usage: xmm [-h] [-T [T]]
              {search,install,remove,update,save,list,show,hello} ...

Xonotic Map Manager is a tool to help manage Xonotic maps

positional arguments:
  {search,install,remove,update,save,list,show,hello}
    search              search for maps based on bsp names
    install             install a map from the repository, or specify a URL.
    remove              remove based on pk3 name
    update              update sources json
    export              export locally managed packages to a file
    list                list locally installed packages
    show                show details of locally installed package
    hello               hello is an example plugin

optional arguments:
  -h, --help            show this help message and exit
  -T [T]                target directory

Very early alpha. Please be patient.
```

### Searching

```
xmm search snowdance
Searching for: snowdance
snowdance2
http://dl.xonotic.co/snowdance2.pk3
snowdance2
http://dl.xonotic.co/snowdance_xon.pk3
```

```
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
```

Inline help is available on all sub-commands:

```
xmm search -h                
usage: xmm search [-h] [--gametype [GAMETYPE]] [--pk3 [PK3]]
                             [--title [TITLE]] [--author [AUTHOR]]
                             [--shasum [SHASUM]] [--long]
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
  --shasum [SHASUM], -s [SHASUM]
                        filter by shasum
  --long, -l            show long format
```

### Installing from the repository

```
xmm install snowdance_xon.pk3
Installing map from repository: snowdance_xon.pk3
...100%, 5 MB, 2438 KB/s, 2 seconds passed. Done.
```

```
xmm install snowdance_xon.pk3 
Installing map from repository: snowdance_xon.pk3
package already exists, please remove first.
```

```
xmm install fake.pk3   
Installing map from repository: fake.pk3
package does not exist in the repository.
```

Example below is also showing the use of curl instead of python's urllib:

```
xmm install http://somerepo.org/snowdance2.pk3
Adding map: http://somerepo.org/snowdance2.pk3
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 5530k  100 5530k    0     0   205k      0  0:00:26  0:00:26 --:--:--  179k
Done.
```

```
xmm install http://somerepo.org/snowdance2.pk3
Adding map: http://somerepo.org/snowdance2.pk3
map already exists, please remove first.
```

### Removing

```
xmm remove snowdance2.pk3
Removing map: snowdance2.pk3
Done.
```

```
xmm remove snowdance2.pk3
Removing map: snowdance2.pk3
map does not exist.
```

### Update

```
xmm update
Updating sources json.
...100%, 7 MB, 2559 KB/s, 3 seconds passed. Done.
```

### List

```
xmm list

steelspace_v5.pk3
steelspace_v5
http://dl.xonotic.co/steelspace_v5.pk3

coolness_ut.pk3
coolness_ut
http://dl.xonotic.co/coolness_ut.pk3

dance.pk3
dance
http://dl.xonotic.co/dance.pk3

Total packages found: 3
```

```
xmm list -l

         pk3: steelspace_v5.pk3
         bsp: steelspace_v5
       title: False
 description: False
      author: False
      shasum: ed427e31628b70fb29d163c750ce815673eeb02a
        date: 2009-07-31
        size: 6MB
          dl: http://dl.xonotic.co/steelspace_v5.pk3

         pk3: coolness_ut.pk3
         bsp: coolness_ut
       title: False
 description: False
      author: False
      shasum: 908cda62276a0de299217f8d6e3a197b6334f06a
        date: 2015-07-03
        size: 2MB
          dl: http://dl.xonotic.co/coolness_ut.pk3

         pk3: dance.pk3
         bsp: dance
       title: <TITLE>
 description: <DESCRIPTION>
      author: <AUTHOR>
      shasum: ef00d43838430b2d1673f03bbe1440eef100ece6
        date: 2008-03-16
        size: 7MB
          dl: http://dl.xonotic.co/dance.pk3

Total packages found: 3
```

### Show

```
xmm show dance.pk3

dance.pk3
dance
http://dl.xonotic.co/dance.pk3
```

```
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
```

### Export

```
% xmm export test.json
% cat test.json
[{"mapinfo": ["maps/dance.mapinfo"], "date": 1205715512, "title": "<TITLE>", "radar": [], "waypoints": [], "gametypes": ["ctf", "dm", "lms", "arena"], "mapshot": ["maps/dance.jpg"], "description": "<DESCRIPTION>", "shasum": "ef00d43838430b2d1673f03bbe1440eef100ece6", "filesize": 7468410, "pk3": "dance.pk3", "map": ["maps/dance.map"], "author": "<AUTHOR>", "license": false, "bsp": {"dance": {"entities": {"item_cells": 14, "item_bullets": 14, "info_player_team1": 10, "item_rockets": 16, "info_player_team2": 11, "item_invincible": 1, "weapon_hagar": 2, "item_flag_team1": 1, "weapon_electro": 2, "item_health_medium": 14, "item_health_small": 20, "weapon_machinegun": 2, "item_strength": 1, "weapon_vortex": 3, "item_armor_small": 19, "weapon_devastator": 2, "item_flag_team2": 1, "weapon_grenadelauncher": 2}}}}]% 
```

## Developers

### Plugin System

Checkout the examples in the `./xmmc/plugins` directory.

```python
from plugins import pluginbase
from xmmc import util

bcolors = util.bcolors
config = pluginbase.get_config()


def get_args():
    command='hello'
    command_help={'help': 'hello is an example plugin'}
    args=['-f', '--foo']
    kwargs={'type': int, 'nargs': '?', 'help': 'this is a help line'}
    return command, command_help, args, kwargs


def run():
    print("Hello from a plugin!")
    print("Look, I have access to the config: " + config['api_data'])
    print(bcolors.BOLD + "and also utils" + bcolors.ENDC)
```

### JSON structure

Same structure as uses by xonotic-map-repository

```json
{
	"title": "Disarray",
	"map": ["maps/disarray_v1r2.map"],
	"description": "Fast-paced space CTF map",
	"mapshot": ["maps/disarray_v1r2.jpg"],
	"pk3": "disarray_v1r2.pk3",
	"mapinfo": ["maps/disarray_v1r2.mapinfo"],
	"shasum": "f1dbf1b4850266688d481baf7e5b26af0fb891ae",
	"bsp": {
		"disarray_v1r2": {
			"entities": {
				"info_player_team1": 6,
				"info_player_team2": 6,
				"item_armor_big": 2,
				"item_armor_large": 2,
				"item_armor_medium": 5,
				"item_armor_small": 36,
				"item_bullets": 4,
				"item_cells": 10,
				"item_flag_team1": 1,
				"item_flag_team2": 1,
				"item_health_large": 1,
				"item_health_medium": 12,
				"item_health_mega": 2,
				"item_health_small": 32,
				"item_rockets": 12,
				"item_shells": 4,
				"item_strength": 1,
				"weapon_crylink": 2,
				"weapon_devastator": 2,
				"weapon_grenadelauncher": 2,
				"weapon_machinegun": 2,
				"weapon_vortex": 2
			}
		}
	},
	"filesize": 3274139,
	"date": 1423534626,
	"license": false,
	"gametypes": ["ctf"],
	"author": "SpiKe",
	"waypoints": [],
	"radar": ["gfx/disarray_v1r2_mini.tga"]
}
```