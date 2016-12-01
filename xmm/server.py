import json
import os

from xmm.base import Base
from xmm.library import Library
from xmm.repository import Repository
from xmm.repository import Collection
from xmm.store import Store
from xmm import util


class ServerCollection(Base):
    """
    A *ServerCollection* is a group of *LocalServer* objects. Currently unused.
    """
    def __init__(self, servers):
        super().__init__()
        self.servers = servers

    def __repr__(self):
        return str(vars(self))

    def __json__(self):
        return self.servers

    def to_json(self):
        """
        :returns: A **JSON** encoded version of this object
        """
        return json.dumps(self.servers, cls=util.ObjectEncoder)


class LocalServer(Base):
    """This class sets up the *LocalServer* object

    During instantiation, new objects are created based on configuration.

    The hierarchy of these objects looks like:

    * ``LocalServer``

        * ``Library``

            * ``Store``

            * ``MapPackage``

                * ``Bsp``

        * ``Collection``

            * ``Repository``

    :returns object: ``LocalServer``
        Commands are available off ``self.library``.

    :Example:

    >>> from xmm.server import LocalServer
    >>> server = LocalServer(server_name='myserver1')
    >>> print(server)
    """

    def __init__(self, server_name='default', source_name=None):
        super().__init__()

        map_dir = self.conf['default']['target_dir']
        package_store_file = os.path.expanduser(self.conf['default']['library'])

        if server_name and server_name != 'default':
            map_dir = self.conf['servers'][server_name]['target_dir']
            server_data = self.conf['servers']
            if server_name in server_data:
                package_store_file = os.path.expanduser(server_data[server_name]['library'])

        store = Store(package_store_file=package_store_file)

        self.repositories = Collection()

        if source_name:
            one_repo = self.conf['sources'][source_name]
            repository = Repository(name=source_name,
                                    download_url=one_repo['download_url'],
                                    api_data_url=one_repo['api_data_url'],
                                    api_data_file=one_repo['api_data_file']
                                    )

            self.repositories.add_repository(repository)

        else:
            for source_name in self.conf['sources']:
                repository = Repository(name=source_name,
                                        download_url=self.conf['sources'][source_name]['download_url'],
                                        api_data_url=self.conf['sources'][source_name]['api_data_url'],
                                        api_data_file=self.conf['sources'][source_name]['api_data_file']
                                        )

                self.repositories.add_repository(repository)

        self.library = Library(store=store, repositories=self.repositories, map_dir=map_dir)

    def __repr__(self):
        return str(vars(self))

    def __json__(self):
        return {
            'repositories': self.repositories,
            'library': self.library,
        }

    def to_json(self):
        """
        :returns: A **JSON** encoded version of this object
        """
        return json.dumps(self, cls=util.ObjectEncoder)
