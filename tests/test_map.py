import os

from xmm.store import Store
from xmm.map import MapPackage

root_dir = os.path.dirname(os.path.abspath(__file__))
package_store_file = os.path.join('{}/data/library.json'.format(root_dir))
store = Store(package_store_file=package_store_file)


def test_map_init():
    with open('{}/data/my_map.json'.format(root_dir)) as f:
        data = f.read()
        my_map = MapPackage(map_package_json=data)
    assert my_map.pk3_file == 'map-vapor_alpha_2.pk3'
