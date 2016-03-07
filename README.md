# xonotic-map-manager

```
z@zap:~/dev/xonotic-map-manager % ./map_manager.py -h
usage: map_manager.py [-h] {search,add,remove,update} ...

A tool to help manage xonotic maps

positional arguments:
  {search,add,remove,update}
                        sub-command help
    search              search for maps based on bsp names
    add                 add a map based on url
    remove              remove based on pk3 name
    update              update sources json

optional arguments:
  -h, --help            show this help message and exit

Very early alpha. Please be patient.
```

### Searching

```
z@zap:~/dev/xonotic-map-manager % ./map_manager.py search snowdance
Searching for: snowdance
snowdance2
http://dl.xonotic.co/snowdance2.pk3
snowdance2
http://dl.xonotic.co/snowdance_xon.pk3
```

### Adding

```
z@zap:~/dev/xonotic-map-manager % ./map_manager.py add http://dl.xonotic.co/snowdance2.pk3
Adding map: http://dl.xonotic.co/snowdance2.pk3
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 5530k  100 5530k    0     0   205k      0  0:00:26  0:00:26 --:--:--  179k
Done.
```

```
z@zap:~/dev/xonotic-map-manager % ./map_manager.py add http://dl.xonotic.co/snowdance2.pk3
Adding map: http://dl.xonotic.co/snowdance2.pk3
map already exists, please remove first.
```

### Removing

```
z@zap:~/dev/xonotic-map-manager % ./map_manager.py remove snowdance2.pk3
Removing map: snowdance2.pk3
Done.
```

```
z@zap:~/dev/xonotic-map-manager % ./map_manager.py remove snowdance2.pk3
Removing map: snowdance2.pk3
map does not exist.
```

### Update

```
z@zap:~/dev/xonotic-map-manager % ./map_manager.py update
100.1% 8167424 / 8159512
```