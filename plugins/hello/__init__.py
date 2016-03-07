config = {}


def register(conf):
    global config
    config = conf


def get_args():
    command='hello'
    command_help={'help': 'help for hello'}
    args=['-f', '--foo']
    kwargs={'type': int, 'nargs': '?', 'help': 'this is a help line'}
    return command, command_help, args, kwargs


def run():
    print("Hello from a plugin!")
    print("Look, I have access to the config: " + config['api_data'])