import json
import os
import time

from xmm.util import bcolors
from xmm import util


class Server:

    def __init__(self, args, conf):
        self.conf = conf
        self.map_dir = self.get_map_dir(args)

    def get_map_dir(self, args):

        if args.T:
            target_dir = args.T
        elif args.s:
            servers_file = os.path.expanduser(self.conf['servers'])
            f = open(servers_file)
            data = f.read()
            server_data = json.loads(data)
            f.close()
            target_dir = server_data[args.s]['target_dir']
        else:
            target_dir = os.path.expanduser(self.conf['map_dir'])

        return target_dir

    def show_map_details(self, m, args):

        highlight = False
        search_string = ''

        if 'string' in args:
            search_string = args.string
        elif 'pk3' in args:
            search_string = args.pk3

        if 'highlight' in args and args.highlight:
            highlight = True

        bsps = m['bsp']
        keys = list(bsps)
        keys.sort()

        # little ugly here for a lot of pretty out
        if args.long:
            print('')
            print('         pk3: ' + bcolors.BOLD + str(m['pk3']) + bcolors.ENDC)

            for bsp in keys:
                # Handle Hightlight
                if search_string and highlight:
                    print('         bsp: ' + bcolors.OKBLUE
                                                + bsp.replace(search_string, bcolors.ENDC + bcolors.OKGREEN + search_string + bcolors.ENDC + bcolors.OKBLUE)
                                            + bcolors.ENDC)
                else:
                    print('         bsp: ' + bcolors.OKBLUE + bsp + bcolors.ENDC)

                # bsp specific
                print('       title:  ' + str(m['bsp'][bsp]['title']))
                print(' description:  ' + str(m['bsp'][bsp]['description']))
                print('      author:  ' + str(m['bsp'][bsp]['author']))

            # pk3 specific
            print('      shasum: ' + str(m['shasum']))
            print('        date: ' + time.strftime('%Y-%m-%d', time.localtime(m['date'])))
            print('        size: ' + util.convert_size(m['filesize']).strip())
            print('          dl: ' + self.conf['repo_url'] + m['pk3'])

        # Formatting
        elif args.short:
            print(str(m['pk3']))
        else:
            bsp_string = '\n' + bcolors.BOLD + str(m['pk3']) + bcolors.ENDC + ' ['
            for bsp in keys:
                if search_string and highlight:
                    bsp_string += bcolors.OKBLUE +\
                                  bsp.replace(search_string, bcolors.ENDC + bcolors.OKGREEN + search_string + bcolors.ENDC + bcolors.OKBLUE)\
                                  + bcolors.ENDC + ', '
                else:
                    bsp_string += bcolors.OKBLUE + bsp + bcolors.ENDC + ', '
            bsp_string = util.replace_last(bsp_string, ', ', '')
            bsp_string += bcolors.ENDC + ']'
            print(bsp_string)
            print(self.conf['repo_url'] + str(m['pk3']))
