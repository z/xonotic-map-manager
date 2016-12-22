import json
import os
from shutil import copyfile

from xmm.store import Store
from xmm.map import MapPackage

root_dir = os.path.dirname(os.path.abspath(__file__))
package_store_file = os.path.join('{}/data/library.json'.format(root_dir))
store = Store(package_store_file=package_store_file)


def test_store_init():
    assert store.data_file == package_store_file


def test_store_init_no_file():
    test_library_file = os.path.join('{}/data/new.json'.format(root_dir))
    store = Store(package_store_file=test_library_file)
    assert store.data_file == test_library_file
    assert store.data == []
    os.remove(test_library_file)


def test_store_get_package_db():
    package_db = store.get_package_db()
    assert store.data_file == package_store_file
    assert package_db[0].pk3_file == 'dance.pk3'


def test_store_add_package():
    test_library_file = os.path.join('{}/data/new.json'.format(root_dir))
    store = Store(package_store_file=test_library_file)
    with open('{}/data/map.json'.format(root_dir)) as f:
        data = f.read()
        my_map = MapPackage(map_package_json=data)
    store.add_package(my_map)
    package_db = store.get_package_db()
    assert package_db[0].pk3_file == 'map-vapor_alpha_2.pk3'
    os.remove(test_library_file)


def test_store_remove_package():
    copyfile('{}/data/library.json'.format(root_dir), '{}/data/new.json'.format(root_dir))
    test_library_file = os.path.join('{}/data/new.json'.format(root_dir))
    store = Store(package_store_file=test_library_file)

    # direct attribute
    assert len(store.data) == 1
    with open('{}/data/map.json'.format(root_dir)) as f:
        data = f.read()
        my_map = MapPackage(map_package_json=data)
    store.add_package(my_map)
    assert len(store.data) == 2
    store.remove_package(my_map)

    # via helper
    assert len(store.get_package_db()) == 1
    assert store.get_package_db()[0].pk3_file == 'dance.pk3'
    os.remove(test_library_file)


def test_store_export_packages():
    test_library_file = os.path.join('{}/data/new.json'.format(root_dir))
    # clean up in case other test failed
    if os.path.exists(test_library_file):
        os.remove(test_library_file)
    store.export_packages(filename=test_library_file)
    assert os.path.exists(test_library_file)
    with open(test_library_file) as f:
        data = f.read()
        try:
            json_object = json.loads(data)
        except ValueError as e:
            Exception("not json")
    os.remove(test_library_file)
