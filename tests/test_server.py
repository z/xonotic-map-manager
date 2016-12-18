import os
import pytest

from xmm.map import MapPackage
from xmm.server import LocalServer

root_dir = os.path.dirname(os.path.abspath(__file__))
package_store_file = os.path.join('{}/data/library.json'.format(root_dir))
package_dir = os.path.join('{}/data/maps'.format(root_dir))

os.makedirs(os.path.expanduser('~/.xonotic/data'), exist_ok=True)
os.makedirs(os.path.expanduser(package_dir), exist_ok=True)


def test_server_init():
    server = LocalServer()
    assert hasattr(server, 'library')
    assert hasattr(server.library, 'store')
    assert hasattr(server.library, 'maps')
    assert hasattr(server, 'repositories')
    assert hasattr(server.repositories, 'sources')


def test_server_add_map_package():
    server = LocalServer()
    with open('{}/data/map.json'.format(root_dir)) as f:
        data = f.read()
        my_map = MapPackage(map_package_json=data)
    server.library.add_map_package(package=my_map)
    assert server.library.maps[0].pk3_file == 'map-vapor_alpha_2.pk3'


def test_server_remove_map():
    server = LocalServer()
    assert len(server.library.maps) == 0
    with open('{}/data/map.json'.format(root_dir)) as f:
        data = f.read()
        my_map = MapPackage(map_package_json=data)
    server.library.add_map_package(package=my_map)
    assert len(server.library.maps) == 1
    assert server.library.maps[0].pk3_file == 'map-vapor_alpha_2.pk3'
    with pytest.raises(FileNotFoundError):
        server.library.remove_map(pk3_name='map-vapor_alpha_2.pk3')
        assert len(server.library.maps) == 0


def test_server_install_map():
    server = LocalServer()
    server.library.install_map(pk3_name='vinegar_v3.pk3', overwrite=True, add_to_store=False)
    assert server.library.maps[0].pk3_file == 'vinegar_v3.pk3'
    server.library.remove_map(pk3_name='vinegar_v3.pk3')