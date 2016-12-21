import json

from xmm.map import MapPackage

from xmm.base import Base
from xmm import util


class Store(Base):
    """
    *Store* is for interacting with the datastore for a *Library*

    :param package_store_file:
        The file where the data is stored
    :type package_store_file: ``str``

    >>> import os
    >>> from xmm.store import Store
    >>> package_store_file = os.path.expanduser('~/.xmm/library.json')
    >>> store = Store(package_store_file=package_store_file)

    :returns object: ``Store``

    """
    def __init__(self, package_store_file):
        super().__init__()

        if package_store_file:
            util.create_if_not_exists(package_store_file, json.dumps([]))

        self.data_file = package_store_file
        self.data = self.get_package_db()

    def __repr__(self):
        return str(vars(self))

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

        >>> import os
        >>> from xmm.store import Store
        >>> package_store_file = os.path.expanduser('~/.xmm/library.json')
        >>> store = Store(package_store_file=package_store_file)
        >>> store.get_package_db()

        :returns: ``dict``
        """

        self.logger.debug('Getting package db')

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

        >>> import os
        >>> from xmm.map import MapPackage
        >>> from xmm.store import Store
        >>> package_store_file = os.path.expanduser('~/.xmm/library.json')
        >>> with open('my_map.json') as f:
        >>>     data = f.read()
        >>>     my_map = MapPackage(map_package_json=data)
        >>> store = Store(package_store_file=package_store_file)
        >>> store.add_package(my_map)


        :returns: False if fails
        """

        self.logger.info('Adding package: pk3={pk3}, filesize={filesize}, date={date}, shasum={shasum}'
                         .format(pk3=package.pk3_file,
                                 filesize=util.convert_size(package.filesize),
                                 date=package.date,
                                 shasum=package.shasum,
                                 )
                         )

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

        >>> import os
        >>> from xmm.map import MapPackage
        >>> from xmm.store import Store
        >>> package_store_file = os.path.expanduser('~/.xmm/library.json')
        >>> with open('my_map.json') as f:
        >>>     data = f.read()
        >>>     my_map = MapPackage(map_package_json=data)
        >>> store = Store(package_store_file=package_store_file)
        >>> store.remove_package(my_map)

        :returns: False if fails
        """

        self.logger.info('Removing package: pk3={pk3}, filesize={filesize}, date={date}, shasum={shasum}'
                         .format(pk3=package.pk3_file,
                                 filesize=util.convert_size(package.filesize),
                                 date=package.date,
                                 shasum=package.shasum,
                                 )
                         )

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
        >>> # Setup the store automatically with an instance of *LocalServer*
        >>> server = LocalServer()
        >>> server.library.store.export_packages(filename='test.json')
        """
        if not filename:
            filename = 'xmm-export.maps.json'

        data_out = []
        for m in self.data:
            data_out.append(json.loads(m.to_json()))

        self.logger.info('exporting maps as: {}'.format(filename))

        try:
            with open(filename, 'w') as f:
                f.write(json.dumps(data_out))
        except EnvironmentError as e:
            self.logger.error(e)
            return False
