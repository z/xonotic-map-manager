import json
import os

from xmm.map import MapPackage

from xmm.base import Base
from xmm.util import bcolors
from xmm import util


class Store(Base):
    """
    *Store* is for interacting with the datastore for a *Library*

    :param conf:
        The conf dictionary from ``config.py``
    :type conf: ``dict``

    :param server_name:
        Positional arguments
    :type server_name: ``tuple``

    :returns object: ``Store``

    """
    def __init__(self, conf, server_name):
        super().__init__(conf)

        if server_name:
            server_data = self.conf['servers']
            if server_name in server_data:
                package_store_file = os.path.expanduser(server_data[server_name]['library'])
            else:
                print('server not defined in: ' + self.conf['servers_config'])
                raise SystemExit
        else:
            package_store_file = os.path.expanduser(self.conf['servers']['myserver1']['library'])

        util.create_if_not_exists(package_store_file, json.dumps([]))

        self.data_file = package_store_file
        self.data = self.get_package_db()

    def __json__(self):
        return {
            'data_file': self.data_file,
        }

    def to_json(self):
        """
        :returns: A **JSON** encoded version of this object
        """
        return json.dumps(self, cls=util.ObjectEncoder)

    def get_package_db(self):
        """
        Searches the repository for maps matching criteria

        :returns: ``dict``
        """
        package_data = []
        repo_data = []

        util.create_if_not_exists(self.data_file, json.dumps(package_data))

        if not util.file_is_empty(self.data_file):
            repo_data = []

            with open(self.data_file) as f:
                data = f.read()
                package_data = json.loads(data)

            for m in package_data:
                new_map = MapPackage(conf=self.conf, map_package_json=m)
                repo_data.append(new_map)

        return repo_data

    def add_package(self, package):
        """
        Adds a *MapPackage* to the *Library* *Store*

        :param package:
            MapPackage to add
        :type package: ``MapPackage``
        """
        package_data = self.data
        package_data.append(package)

        # fix this
        data_out = []
        for m in package_data:
            data_out.append(json.loads(m.to_json()))

        with open(self.data_file, 'w+') as f:
            json.dump(data_out, f)

    def remove_package(self, package):
        """
        Removes a *MapPackage* to the *Library* *Store*

        :param package:
            MapPackage to remove
        :type package: ``MapPackage``
        """
        package_store = []

        if not util.file_is_empty(self.data_file):
            with open(self.data_file, 'r+') as f:
                package_store = json.load(f)
                package_store[:] = [m for m in package_store if (m.get('shasum') != package.shasum and m.get('pk3') != package.pk3_file)]

        with open(self.data_file, 'w+') as f:
            json.dump(package_store, f)

    def export_packages(self, filename=None):
        """
        Exports all *MapPackage* objects from the *Library* *Store*

        :param filename:
            Name for the exported json file, default ``xmm-export.json``
        :type filename: ``str``

        >>> from xmm.server import LocalServer
        >>> from xmm.config import conf
        >>> server = LocalServer(conf=conf, server_name='myserver1')
        """
        # fix this
        data_out = []
        for m in self.data:
            data_out.append(json.loads(m.to_json()))

        if not filename:
            default_name = 'xmm-export.json'
            print(bcolors.WARNING + 'a name wasn\'t given. Exporting as: ' + default_name + bcolors.ENDC)
            filename = default_name

        with open(filename, 'w') as f:
            f.write(json.dumps(data_out))
