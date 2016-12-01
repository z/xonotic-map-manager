# xonotic-map-manager

[![Build Status](https://travis-ci.org/z/xonotic-map-manager.svg?branch=develop)](https://travis-ci.org/z/xonotic-map-manager) [![Documentation Status](https://readthedocs.org/projects/xonotic-map-manager/badge/?version=latest)](http://xonotic-map-manager.readthedocs.io/en/latest/?badge=latest)

A command-line package manager for the [xonotic-map-repository](https://github.com/z/xonotic-map-repository) project.

Used with the unofficial Xonotic map repository, [xonotic.co](http://xonotic.co), by default.

![xmm in action](resources/images/xmm.png)

The JSON provides rich metadata about map packages which makes it easier
to discern differences between them.

For information about what data is available check [JSON Structure](#JSON-structure).

## Installation

```
pip install https://github.com/z/xonotic-map-manager/archive/develop.zip#egg=xmm
```

or for development:

```
git clone https://github.com:z/xonotic-map-manager.git
cd xonotic-map-manager
python3 setup.py develop
```

## Usage

```
usage: xmm [-h] [-s [SERVER]] [-T [TARGET]] [-R [REPOSITORY]]
           {search,install,remove,discover,list,show,export,update,hello} ...

Xonotic Map Manager is a tool to help manage Xonotic maps

positional arguments:
  {search,install,remove,discover,list,show,export,update,hello}
    search              search for maps based on bsp names
    install             install a map from the repository, or specify a URL.
    remove              remove based on pk3 name
    discover            discover packages in a target directory
    list                list locally installed packages
    show                show details of remote or locally installed packages
    export              export locally managed packages to a file
    update              update sources json
    hello               hello is an example plugin

optional arguments:
  -h, --help            show this help message and exit
  -s [SERVER], --server [SERVER]
                        target server as defined in servers.json
  -T [TARGET], --target [TARGET]
                        target directory
  -R [REPOSITORY], --repository [REPOSITORY]
                        repository to use (defaults to all available)
```


## Documentation

Documentation is hosted on [readthedocs.io](http://xonotic-map-manager.readthedocs.io/en/latest).

## License

Copyright (c) 2016 Tyler Mulligan (z@xnz.me) and contributors.

Distributed under the MIT license. See the LICENSE file for more details.