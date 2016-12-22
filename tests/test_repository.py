import json
import os

from xmm.repository import Repository
from xmm.repository import Collection

root_dir = os.path.dirname(os.path.abspath(__file__))


def test_add_repository():
    repositories = Collection()

    with open('{}/data/sources.json'.format(root_dir)) as f:
        data = json.loads(f.read())
        repository = Repository(name='default',
                                download_url=data['default']['download_url'],
                                api_data_url=data['default']['api_data_url'],
                                api_data_file=data['default']['api_data_file']
                                )

    repositories.add_repository(repository)

    assert len(repositories.sources) == 1


def test_export_hashes():
    repositories = Collection()

    test_maps_file = os.path.join('{}/data/maps.json'.format(root_dir))
    test_hash_file = os.path.join('{}/data/default-maps.shasum'.format(root_dir))

    with open('{}/data/sources.json'.format(root_dir)) as f:
        data = json.loads(f.read())
        repository = Repository(name='default',
                                download_url=data['default']['download_url'],
                                api_data_url=data['default']['api_data_url'],
                                api_data_file=test_maps_file
                                )

    repositories.add_repository(repository)

    # clean up in case other test failed
    if os.path.exists(test_hash_file):
        os.remove(test_hash_file)
    repositories.get_repository('default').export_hash_index(filename=test_hash_file)

    assert os.path.exists(test_hash_file)

    with open(test_hash_file) as f:
        assert f.readline().strip() == 'ef00d43838430b2d1673f03bbe1440eef100ece6 dance.pk3'
        assert f.readline().strip() == '099b0cc16fe998e5e29893dbecd5673683a5b69d gasoline_02.pk3'
        assert f.readline().strip() == 'efc827b4534c3cc15a66426a4a4da3add5246e41 map-ctf-mikectf3_nex_r3_fix.pk3'
        assert f.readline().strip() == 'fd19fed91d894248016b71702039cddf0f993c59 map-ctf-moonstone_nex_r3.pk3'
        assert f.readline().strip() == '02422d9b0ec6983eb6ddd12cbb5fad5d9f3b6020 map-ctf-polo3ctf1_nex_r3_fix.pk3'
        assert f.readline().strip() == '3df0143516f72269f465070373f165c8787964d5 map-vapor_alpha_2.pk3'

    os.remove(test_hash_file)
