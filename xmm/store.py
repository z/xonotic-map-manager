import json
import os

from xmm.map import MapPackage

from xmm.base import Base
from xmm import util


class Store(Base):
    """
    *Store* is for interacting with the datastore for a *Library*

    :param server_name:
        Positional arguments
    :type server_name: ``tuple``

    :returns object: ``Store``

    """
    def __init__(self, server_name):
        super().__init__()

        package_store_file = None

        if server_name:
            server_data = self.conf['servers']
            if server_name in server_data:
                package_store_file = os.path.expanduser(server_data[server_name]['library'])
            else:
                print('server not defined in: ' + self.conf['servers_config'])
                Exception('Server not defined.')
        else:
            package_store_file = os.path.expanduser(self.conf['default']['library'])

        if package_store_file:
            util.create_if_not_exists(package_store_file, json.dumps([]))

        self.data_file = package_store_file
        self.data = self.get_package_db()

    def __json__(self):
        return {
            'data': self.data,
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
                new_map = MapPackage(map_package_json=m)
                repo_data.append(new_map)

        return repo_data

    def add_package(self, package):
        """
        Adds a *MapPackage* to the *Library* *Store*

        :param package:
            MapPackage to add
        :type package: ``MapPackage``

        :returns: False if fails
        """
        package_data = self.data
        package_data.append(package)

        # fix this
        data_out = []
        for m in package_data:
            data_out.append(json.loads(m.to_json()))

        try:
            with open(self.data_file, 'w+') as f:
                json.dump(data_out, f)
        except EnvironmentError as e:
            self.logger.error(e)
            return False

    def remove_package(self, package):
        """
        Removes a *MapPackage* to the *Library* *Store*

        :param package:
            MapPackage to remove
        :type package: ``MapPackage``

        :returns: False if fails
        """
        package_store = []

        if not util.file_is_empty(self.data_file):
            with open(self.data_file, 'r+') as f:
                package_store = json.load(f)
                package_store[:] = [m for m in package_store if (m.get('shasum') != package.shasum and m.get('pk3') != package.pk3_file)]

        try:
            with open(self.data_file, 'w+') as f:
                json.dump(package_store, f)
        except EnvironmentError as e:
            self.logger.error(e)
            return False

    def export_packages(self, filename=None):
        """
        Exports all *MapPackage* objects from the *Library* *Store*

        :param filename:
            Name for the exported json file, default ``xmm-export.json``
        :type filename: ``str``

        :returns: False if fails
        >>> from xmm.server import LocalServer
        >>> server = LocalServer(server_name='myserver1')
        """
        default_export_name = 'xmm-export.json'

        data_out = []
        for m in self.data:
            data_out.append(json.loads(m.to_json()))

        if not filename:
            filename = default_export_name

        try:
            with open(filename, 'w') as f:
                f.write(json.dumps(data_out))
        except EnvironmentError as e:
            self.logger.error(e)
            return False
