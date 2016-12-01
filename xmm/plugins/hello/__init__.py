from xmm.plugins import pluginbase
from xmm.util import zcolors
from xmm.util import cprint

config = pluginbase.get_config()


def get_args():
    command='hello'
    command_help={'help': 'hello is an example plugin'}
    args=['-f', '--foo']
    kwargs={'type': int, 'nargs': '?', 'help': 'this is a help line'}
    return command, command_help, args, kwargs


def run():
    print("Hello from a plugin!")
    cprint("I share the xmm util module", style='HEADER')
    cprint("plugins can use these functions and classes", style='BOLD')
    cprint("I share the xmm util module", style='INFO')
    cprint("oh noes! Something went wrong! (not really)", style='FAIL')
    cprint("It's okay! Don't Cry", style='WARNING')
    cprint("Get Serious", style='UNDERLINE')
    print("{}Look, I also have access to the config: {}".format(zcolors.SUCCESS, config['servers_config']))
