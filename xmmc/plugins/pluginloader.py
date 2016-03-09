import imp
import os

plugin_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)))
main_module = '__init__'


def get_plugins():
    plugins = []
    possible_plugins = os.listdir(plugin_folder)
    for i in possible_plugins:
        location = os.path.join(plugin_folder, i)
        if not os.path.isdir(location) or not main_module + '.py' in os.listdir(location):
            continue
        info = imp.find_module(main_module, [location])
        plugins.append({'name': i, 'info': info})
    return plugins


def load_plugin(plugin):
    return imp.load_module(plugin['name'], *plugin['info'])
