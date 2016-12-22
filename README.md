# xonotic-map-manager

[![Build Status](https://travis-ci.org/z/xonotic-map-manager.svg?branch=master)](https://travis-ci.org/z/xonotic-map-manager) [![Documentation Status](https://readthedocs.org/projects/xonotic-map-manager/badge/?version=latest)](http://xonotic-map-manager.readthedocs.io/en/latest/?badge=latest)

A command-line package manager for the [xonotic-map-repository](https://github.com/z/xonotic-map-repository) project.

Used with the unofficial Xonotic map repository, [xonotic.co](http://xonotic.co), by default.

[![asciicast of xmm](https://raw.githubusercontent.com/z/xonotic-map-manager/master/resources/images/xmm.gif)](https://asciinema.org/a/3vrfld4k0tj91hgztw0obmnbl)

The JSON provides rich metadata about map packages which makes it easier
to discern differences between them.

For information about what data is available check [JSON Structure](#JSON-structure).
## Requirements

### Debian/Ubuntu

If you do not already have **pip** and **setuptools** for Python 3:

```
sudo apt install python3-pip python3-setuptools
```

## Installation

```
pip3 install xmm --user
```

or for development:

```
git clone https://github.com:z/xonotic-map-manager.git
cd xonotic-map-manager
python3 setup.py develop
```

## Usage

```
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
```


## Documentation

Documentation is hosted on [readthedocs.io](http://xonotic-map-manager.readthedocs.io/en/latest).

## Contributing

Contributions to this project are welcome, please read [CONTRIBUTING.md](https://github.com/z/xonotic-map-manager/blob/master/CONTRIBUTING.md).

## License

Copyright (c) 2016 Tyler Mulligan (z@xnz.me) and contributors.

Distributed under the MIT license. See the LICENSE file for more details.