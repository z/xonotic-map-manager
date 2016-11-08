import json
from xmm.base import Base
from xmm.library import Library
from xmm.repository import SourceRepository
from xmm.repository import SourceCollection
from xmm.store import Store
from xmm import util


class ServerCollection(Base):
    """
    A *ServerCollection* is a group of *LocalServer* objects
    """
    def __init__(self, servers):
        super().__init__()
        self.servers = servers

    def __repr__(self):
        return str(vars(self))

    def __json__(self):
        return self.servers

    def to_json(self):
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

        * ``SourceCollection``

            * ``Repository``

    :returns object: ``LocalServer``
        Commands are available off ``self.library``.

    :Example:

    >>> from xmm.server import LocalServer
    >>> server = LocalServer(server_name='myserver1')
    >>> print(server)
    """

    def __init__(self, server_name, source_name=None):
        super().__init__()

        store = Store(server_name=server_name)

        if source_name:
            # default
            one_repo = self.conf['sources'][source_name]
            map_dir = self.conf['default']['target_dir']
            source_repository = SourceRepository(name=source_name, download_url=one_repo['download_url'],
                                                 api_data_url=one_repo['api_data_url'], api_data_file=one_repo['api_data_file'])
        else:
            # TODO: for each source in one_repo
            # for source in self.conf['sources']:
            map_dir = self.conf['servers'][server_name]['target_dir']
            source_repository = SourceRepository(name='default', download_url=self.conf['default']['download_url'],
                                                 api_data_url=self.conf['default']['api_data_url'], api_data_file=self.conf['default']['api_data_file'])

        self.source_collection = SourceCollection()
        self.source_collection.add_repository(source_repository)

        self.library = Library(store=store, source_collection=self.source_collection, map_dir=map_dir)

    def __repr__(self):
        return str(vars(self))

    def __json__(self):
        return {
            'source_collection': self.source_collection,
            'library': self.library,
        }

    def to_json(self):
        return json.dumps(self, cls=util.ObjectEncoder)
