import xmm.util as util
import json
import logging.config
import os

config_file = '.xmm.ini'
logging_config_file = 'xmm.logging.ini'
config_file_with_path = os.path.expanduser(os.path.join('~', config_file))
logging_config_file_with_path = os.path.expanduser(os.path.join('~/.xmm/', logging_config_file))

util.check_if_not_create(config_file_with_path, 'config/xmm.ini')
util.check_if_not_create(logging_config_file_with_path, 'config/xmm.logging.ini')

config = util.parse_config(config_file_with_path)

conf = {
    'default': {
        'library': os.path.expanduser('~/.xmm/library.json'),
        'target_dir': os.path.expanduser(config['target_dir']),
        'download_url': os.path.expanduser(config['download_url']),
        'api_data_file': os.path.expanduser(config['api_data_file']),
        'api_data_url': os.path.expanduser(config['api_data_url']),
        'api_data_file_seed': os.path.expanduser('~/.xmm/maps.json.zip'),
        'use_curl': False,
    },
    'sources_config': os.path.expanduser(config['sources_config']),
    'servers_config': os.path.expanduser(config['servers_config']),
    'sources': {},
    'servers': {},
}

# Overcome ini pitfalls
if config['use_curl'].lower() == 'true':
    conf['default']['use_curl'] = True

util.check_if_not_create(conf['sources_config'], 'config/example.sources.json')
util.check_if_not_create(conf['servers_config'], 'config/example.servers.json')

# If maplist doesn't exist copy seed zip over
util.check_if_not_create(conf['default']['api_data_file_seed'], 'resources/data/maps.json.zip')

# Load JSON files are dicts
with open(conf['sources_config']) as f:
    data = f.read()
    sources = json.loads(data)
    conf['sources'] = sources

with open(conf['servers_config']) as f:
    data = f.read()
    servers = json.loads(data)
    conf['servers'] = servers

# Make sure needed dirs exist
for server in conf['servers']:
    os.makedirs(os.path.expanduser(conf['servers'][server]['target_dir']), exist_ok=True)

logging.config.fileConfig(logging_config_file_with_path, defaults={
    'log_filename': os.path.expanduser('~/.xmm/xmm.log')
})
