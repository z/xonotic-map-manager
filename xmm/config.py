import xmm.util as util
import os

config_file = '.xmm.cfg'
home = os.path.expanduser('~')
config_file_with_path = os.path.join(home, config_file)

util.check_if_not_create(config_file_with_path, 'config/xmm.cfg')

config = util.parse_config(config_file_with_path)

conf = {
    'map_dir': os.path.expanduser(config['map_dir']),
    'repo_url': os.path.expanduser(config['repo_url']),
    'api_data': os.path.expanduser(config['api_data']),
    'api_data_url': os.path.expanduser(config['api_data_url']),
    'use_curl': os.path.expanduser(config['use_curl']),
    'package_store': os.path.expanduser(config['package_store']),
    'servers': os.path.expanduser(config['servers']),
}
