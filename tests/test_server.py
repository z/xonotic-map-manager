import os

from xmm.server import LocalServer

root_dir = os.path.dirname(os.path.abspath(__file__))


def test_server_init():
    server = LocalServer()
    assert hasattr(server, 'library')
    assert hasattr(server.library, 'store')
    assert hasattr(server.library, 'maps')
    assert hasattr(server, 'source_collection')
    assert hasattr(server.source_collection, 'sources')
