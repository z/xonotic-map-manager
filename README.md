# xonotic-map-manager

```
./map_manager.py -h                           
usage: map_manager.py [-h] {search,add,install,remove,update,hello} ...

A tool to help manage xonotic maps

positional arguments:
  {search,add,install,remove,update,world,hello}
                        sub-command help
    search              search for maps based on bsp names
    add                 add a map based on url
    install             install a map from the repository
    remove              remove based on pk3 name
    update              update sources json
    hello               help for hello

optional arguments:
  -h, --help            show this help message and exit

Very early alpha. Please be patient.
```

### Searching

```
./map_manager.py search snowdance
Searching for: snowdance
snowdance2
http://dl.xonotic.co/snowdance2.pk3
snowdance2
http://dl.xonotic.co/snowdance_xon.pk3
```

```
./map_manager.py search -p nexdance --long
Searching for packages with the following criteria:
pk3: nexdance

         pk3: nexdance.pk3
         bsp: nexdance
       title: <TITLE>
 description: <DESCRIPTION>
      author: <AUTHOR>
      shasum: 73fb31ad90846e64bd87369e33d360c24f1bff41
        date: 2008-03-16
        size: 7MB
          dl: http://dl.xonotic.co/nexdance.pk3

Total packages found: 1
```

```
./map_manager.py search -h                
usage: map_manager.py search [-h] [--gametype [GAMETYPE]] [--pk3 [PK3]]
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
./map_manager.py install snowdance_xon.pk3
Installing map from repository: snowdance_xon.pk3
...100%, 5 MB, 2438 KB/s, 2 seconds passed. Done.
```

```
./map_manager.py install snowdance_xon.pk3 
Installing map from repository: snowdance_xon.pk3
package already exists, please remove first.
```

```
./map_manager.py install fake.pk3   
Installing map from repository: fake.pk3
package does not exist in the repository.
```

### Adding (from any URL)

```
./map_manager.py add http://dl.xonotic.co/snowdance2.pk3
Adding map: http://dl.xonotic.co/snowdance2.pk3
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 5530k  100 5530k    0     0   205k      0  0:00:26  0:00:26 --:--:--  179k
Done.
```

```
./map_manager.py add http://dl.xonotic.co/snowdance2.pk3
Adding map: http://dl.xonotic.co/snowdance2.pk3
map already exists, please remove first.
```

### Removing

```
./map_manager.py remove snowdance2.pk3
Removing map: snowdance2.pk3
Done.
```

```
./map_manager.py remove snowdance2.pk3
Removing map: snowdance2.pk3
map does not exist.
```

### Update

```
./map_manager.py update
Updating sources json.
...100%, 7 MB, 2559 KB/s, 3 seconds passed. Done.
```

## Developers

### Plugin System

Checkout the examples in the `plugins` directory.

```python
# Leave this
config = {}


def register(conf):
    global config
    config = conf


# Change this
def get_args():
    command='hello'
    command_help={'help': 'hello a command'}
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