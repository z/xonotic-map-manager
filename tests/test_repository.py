import json
import os

from xmm.repository import Repository
from xmm.repository import Collection

root_dir = os.path.dirname(os.path.abspath(__file__))


def test_add_repository():
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

    assert len(repositories.sources) == 1
