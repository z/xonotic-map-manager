import json
import os
import pytest

# from xmm.library import Library
from xmm.map import MapPackage
from xmm.repository import Repository
from xmm.repository import Collection
from xmm.server import LocalServer
from xmm.store import Store

root_dir = os.path.dirname(os.path.abspath(__file__))
package_store_file = os.path.join('{}/data/library.json'.format(root_dir))

os.makedirs(os.path.expanduser('~/.xonotic/data'), exist_ok=True)

store = Store(package_store_file=package_store_file)
repositories = Collection()

with open('{}/data/sources.json'.format(root_dir)) as f:
    data = json.loads(f.read())
    print(data)
    repository = Repository(name='default',
                            download_url=data['default']['download_url'],
                            api_data_url=data['default']['api_data_url'],
                            api_data_file=data['default']['api_data_file']
                            )

repositories.add_repository(repository)


def test_library_add_map_package():
    server = LocalServer()
    # library = Library(repositories=repositories, store=store, map_dir='{}/data/maps'.format(root_dir))
    with open('{}/data/map.json'.format(root_dir)) as f:
        data = f.read()
        my_map = MapPackage(map_package_json=data)
    server.library.add_map_package(package=my_map)
    assert server.library.maps[0].pk3_file == 'map-vapor_alpha_2.pk3'


def test_library_remove_map():
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


def test_library_install_map():
    server = LocalServer()
    server.library.install_map(pk3_name='vinegar_v3.pk3', overwrite=True, add_to_store=False)
    assert server.library.maps[0].pk3_file == 'vinegar_v3.pk3'
