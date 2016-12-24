import json
import operator

from xmm.map import MapPackage

from xmm.base import Base
from xmm import util
from xmm.exceptions import PackageLookupError

from tinydb import TinyDB, Query


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

        db_file = package_store_file.replace('library', 'db')
        db = TinyDB(db_file)

        self.data_file = package_store_file
        self.data_db_file = db_file
        self.db = db
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

        repo_data = []
        map_table = self.db.table('map_table')

        for m in map_table.all():
            new_map = MapPackage(map_package_json=m)
            repo_data.append(new_map)

        return sorted(repo_data, key=operator.attrgetter('pk3_file'))

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

        self.data.append(package)

        try:
            map_table = self.db.table('map_table')
            map_table.insert(json.loads(package.to_json()))
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

        map_table = self.db.table('map_table')
        Map = Query()

        try:
            selected_map = map_table.search((Map.shasum == package.shasum) & (Map.pk3 == package.pk3_file))
            map_table.remove(eids=[selected_map[0].eid])
        except PackageLookupError as e:
            self.logger.error(e)
            raise PackageLookupError

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

        map_table = self.db.table('map_table')

        self.logger.info('exporting maps as: {}'.format(filename))

        try:
            with open(filename, 'w') as f:
                f.write(json.dumps(map_table.all()))
        except EnvironmentError as e:
            self.logger.error(e)
            return False
