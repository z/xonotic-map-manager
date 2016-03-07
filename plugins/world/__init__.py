config = {}

def register(conf):
    global config
    config = conf

def get_args():
    command='world'
    command_help={'help': 'help world'}
    args=['-b', '--bar']
    kwargs={'type': int, 'nargs': '?', 'help': 'this is a help line'}
    return command, command_help, args, kwargs

def run():
    print(config['map_dir'])
    print("World from a plugin!")
