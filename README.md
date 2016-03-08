# xonotic-map-manager

I'm going to let the output do the talking for the majority of this
documentation.

Usage is pretty straight forward and the command-line documentation is 
there to help.

```
usage: xmm.py [-h] [-T [T]] {search,install,remove,update,save,hello} ...

Xonotic Map Manager is a tool to help manage Xonotic maps

positional arguments:
  {search,install,remove,update,save,hello}
    search              search for maps based on bsp names
    install             install a map from the repository, or specify a URL.
    remove              remove based on pk3 name
    update              update sources json
    save                export locally managed packages to a file
    hello               hello is an example plugin

optional arguments:
  -h, --help            show this help message and exit
  -T [T]                target directory

Very early alpha. Please be patient.
```

This application works by reading a locally cached json file generated.
 This file is accessible as a web-frontend at http://xonotic.co, which is using the [xonotic-map-repository](https://github.com/z/xonotic-map-repository) to
generate it from a directory of map packages (pk3 files).

The data set you find in the JSON is more rich than what you see in game.
It also makes it easier to discern differences in packages.

For information about what data is available check [JSON Structure](#JSON structure).

It's possible to host your own collection of curated maps with a web-frontend
 and point this tool at it to manage maps on a server.

## Configuration

The default settings are likely similar to yours, however, you will need
to edit `config.ini` if you actually want to use install or remove.

### Searching

```
./xmm.py search snowdance
Searching for: snowdance
snowdance2
http://dl.xonotic.co/snowdance2.pk3
snowdance2
http://dl.xonotic.co/snowdance_xon.pk3
```

```
./xmm.py search -p bloodrage_v2.pk3 --long  
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
./xmm.py search -h                
usage: xmm.py search [-h] [--gametype [GAMETYPE]] [--pk3 [PK3]]
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
./xmm.py install snowdance_xon.pk3
Installing map from repository: snowdance_xon.pk3
...100%, 5 MB, 2438 KB/s, 2 seconds passed. Done.
```

```
./xmm.py install snowdance_xon.pk3 
Installing map from repository: snowdance_xon.pk3
package already exists, please remove first.
```

```
./xmm.py install fake.pk3   
Installing map from repository: fake.pk3
package does not exist in the repository.
```

Example below is also showing the use of curl instead of python's urllib:

```
./xmm.py install http://somerepo.org/snowdance2.pk3
Adding map: http://somerepo.org/snowdance2.pk3
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 5530k  100 5530k    0     0   205k      0  0:00:26  0:00:26 --:--:--  179k
Done.
```

```
./xmm.py install http://somerepo.org/snowdance2.pk3
Adding map: http://somerepo.org/snowdance2.pk3
map already exists, please remove first.
```

### Removing

```
./xmm.py remove snowdance2.pk3
Removing map: snowdance2.pk3
Done.
```

```
./xmm.py remove snowdance2.pk3
Removing map: snowdance2.pk3
map does not exist.
```

### Update

```
./xmm.py update
Updating sources json.
...100%, 7 MB, 2559 KB/s, 3 seconds passed. Done.
```

### Export

```
% ./xmm.py save test.json
% cat test.json
[{"ef00d43838430b2d1673f03bbe1440eef100ece6dance.pk3": "1"}]%  
```

## Developers

### Plugin System

Checkout the examples in the `plugins` directory.

```python
from plugins import pluginbase

config = pluginbase.config

def get_args():
    command='hello'
    command_help={'help': 'help for hello'}
    args=['-f', '--foo']
    kwargs={'type': int, 'nargs': '?', 'help': 'this is a help line'}
    return command, command_help, args, kwargs


def run():
    print("Hello from a plugin!")
    print("Look, I have access to the config: " + config['api_data'])
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