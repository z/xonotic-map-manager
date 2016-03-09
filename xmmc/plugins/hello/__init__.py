from xmmc.plugins import pluginbase
from xmmc import util

bcolors = util.bcolors
config = pluginbase.get_config()


def get_args():
    command='hello'
    command_help={'help': 'hello is an example plugin'}
    args=['-f', '--foo']
    kwargs={'type': int, 'nargs': '?', 'help': 'this is a help line'}
    return command, command_help, args, kwargs


def run():
    print("Hello from a plugin!")
    print(bcolors.HEADER + "I share the xmmc util module" + bcolors.ENDC)
    print(bcolors.BOLD + "plugins can use these functions and classes" + bcolors.ENDC)
    print(bcolors.OKBLUE + "It has tools for formatting." + bcolors.ENDC)
    print(bcolors.FAIL + "oh noes! Something went wrong! (not really)" + bcolors.ENDC)
    print(bcolors.WARNING + "It's okay! Don't Cry" + bcolors.ENDC)
    print(bcolors.UNDERLINE + "Get Serious" + bcolors.ENDC)
    print(bcolors.OKGREEN + "Look, I also have access to the config: " + config['api_data'])