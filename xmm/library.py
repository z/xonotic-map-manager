import os
import re
import subprocess
import json
import pickle
import urllib.request

from xmm.xonotic import Server
from xmm.util import bcolors
from xmm import util


class LibraryCommand(Server):

    def __init__(self, args, conf, store, repository):
        super().__init__(args, conf)
        self.store = store
        self.repository = repository

    def install_maps(self, args):

        map_dir = self.get_map_dir(args)
        installed_packages = self.store.get_package_db(args)

        if installed_packages:
            for m in installed_packages:
                if m['pk3'] == args.pk3:
                    print(bcolors.FAIL + args.pk3 + " already exists." + bcolors.ENDC)
                    install = util.query_yes_no('continue?', 'no')
                    if not install:
                        raise SystemExit

        installed = False
        is_url = False
        if re.match('^(ht|f)tp(s)?://', args.pk3):
            url = args.pk3
            pk3 = os.path.basename(url)
            is_url = True
        else:
            pk3 = args.pk3
            url = self.conf['repo_url'] + pk3

        pk3_with_path = os.path.join(os.path.dirname(map_dir), pk3)

        maps_json = self.repository.get_repo_data()
        map_in_repo = False
        for m in maps_json:
            if m['pk3'] == pk3:
                self.store.db_add_package(m, args)
                map_in_repo = True
                break

        if map_in_repo or is_url:
            print('Installing map: ' + bcolors.BOLD + pk3 + bcolors.ENDC)
            self.add_map(pk3_with_path, url)
            installed = True

        if not map_in_repo:
            if installed:
                print(bcolors.WARNING + 'package does not exist in the repository, ' +
                                        'it won\'t be added to the local database.' + bcolors.ENDC)
            else:
                print(bcolors.FAIL + 'package does not exist in the repository. cannot install.' + bcolors.ENDC)
                raise SystemExit

    def add_map(self, pk3_with_path, url):

        if not os.path.exists(pk3_with_path):

            if self.conf['use_curl'] == 'False':
                urllib.request.urlretrieve(url, os.path.expanduser(pk3_with_path), util.reporthook)
            else:
                subprocess.call(['curl', '-o', pk3_with_path, url])

            print(bcolors.OKBLUE + 'Done.' + bcolors.ENDC)

        else:
            print(bcolors.FAIL + 'package already exists, please remove first.' + bcolors.ENDC)
            raise SystemExit

    def remove_maps(self, args):

        pk3 = args.pk3
        map_dir = os.path.expanduser(self.get_map_dir(args))

        print('Removing package: ' + bcolors.BOLD + pk3 + bcolors.ENDC)

        if os.path.exists(map_dir):
            pk3_with_path = os.path.join(os.path.dirname(map_dir), pk3)

            if os.path.exists(pk3_with_path):
                os.remove(pk3_with_path)

                repo_data = self.repository.get_repo_data()

                for m in repo_data:
                    if m['pk3'] == pk3:
                        self.store.db_remove_package(m, args)

                print(bcolors.OKBLUE + 'Done.' + bcolors.ENDC)
            else:
                print(bcolors.FAIL + 'package does not exist.' + bcolors.ENDC)
                raise SystemExit

        else:
            print(bcolors.FAIL + 'directory does not exist.' + bcolors.ENDC)
            raise SystemExit

    def discover_maps(self, args):

        map_dir = os.path.expanduser(self.get_map_dir(args))
        packages = self.store.get_package_db(args)

        for file in os.listdir(map_dir):
            if file.endswith('.pk3'):
                args.pk3 = file
                args.shasum = util.hash_file(os.path.join(map_dir, file))
                map_found = self.show_map(file, 'all', args)

                if map_found:
                    if args.add:
                        map_installed = False
                        if packages:
                            for p in packages:
                                if p['pk3'] == args.pk3:
                                    map_installed = True

                        if not map_installed:
                            self.store.db_add_package(map_found, args)

    # local data
    def list_installed(self, args):

        packages = self.store.get_package_db(args)

        total = 0
        if packages:
            for p in packages:
                self.show_map_details(p, args)
                total += 1

        print('\n' + bcolors.OKBLUE + 'Total packages found:' + bcolors.ENDC + ' ' + bcolors.BOLD + str(total) + bcolors.ENDC)

    def show_map(self, pk3, ftype, args):

        packages = self.repository.get_repo_data()

        if ftype == 'installed':
            packages = self.store.get_package_db(args)

        found_map = False
        hash_match = True

        if packages:
            for p in packages:
                if p['pk3'] == pk3:
                    shasum = util.hash_file(os.path.join(self.conf['map_dir'], pk3))
                    if p['shasum'] == shasum:
                        self.show_map_details(p, args)
                        found_map = p
                        print('')
                    else:
                        print(bcolors.BOLD + pk3 + bcolors.ENDC + bcolors.WARNING + " hash different from repositories" + bcolors.ENDC)
                        hash_match = False

        if not found_map and hash_match:
            if ftype == 'installed':
                print(bcolors.BOLD + pk3 + bcolors.ENDC + bcolors.FAIL + ' package not currently installed' + bcolors.ENDC)
            else:
                print(bcolors.BOLD + pk3 + bcolors.ENDC + bcolors.FAIL + ' package was not found in repository' + bcolors.ENDC)

        return found_map


class Store:

    def __init__(self, conf):
        self.conf = conf

    def get_package_store(self, args):
        if args.s:
            servers_file = os.path.expanduser(self.conf['servers'])
            f = open(servers_file)
            data = f.read()
            server_data = json.loads(data)
            f.close()
            if args.s in server_data:
                package_store_file = os.path.expanduser(server_data[args.s]['package_db'])
            else:
                print('server not defined in ' + self.conf['servers'])
                raise SystemExit
        else:
            package_store_file = os.path.expanduser(self.conf['package_store'])

        return package_store_file

    def get_package_db(self, args):

        package_store_file = self.get_package_store(args)

        if os.path.exists(package_store_file) and not util.file_is_empty(package_store_file):
            db = open(package_store_file, 'rb')
            package_store = pickle.load(db)
            db.close()
        else:
            print(bcolors.WARNING + 'No package database found (don\'t worry, it will be created)' + bcolors.ENDC)
            db_out = open(package_store_file, 'wb+')
            pickle.dump([], db_out)
            db_out.close()
            package_store = []

        return package_store

    def db_add_package(self, package, args):

        package_store = []
        package_store_file = self.get_package_store(args)

        if os.path.exists(package_store_file) and not util.file_is_empty(package_store_file):
            db_in = open(package_store_file, 'rb+')
            package_store = pickle.load(db_in)
            package_store.append(package)
            db_in.close()
        else:
            package_store.append(package)

        db_out = open(package_store_file, 'wb+')
        pickle.dump(package_store, db_out)
        db_out.close()

    def db_remove_package(self, package, args):

        package_store = []
        package_store_file = self.get_package_store(args)

        if not util.file_is_empty(package_store_file):
            db_in = open(package_store_file, 'rb+')
            package_store = pickle.load(db_in)
            package_store[:] = [m for m in package_store if (m.get('shasum') != package['shasum'] and m.get('pk3') != package['pk3'])]
            db_in.close()

        db_out = open(package_store_file, 'wb+')
        pickle.dump(package_store, db_out)
        db_out.close()

    def db_export_packages(self, args):

        data = self.get_package_db(args)
        package_store = json.dumps(data)

        if args.file:
            filename = args.file
        else:
            default_name = 'xmm-export.json'
            print(bcolors.WARNING + 'a name wasn\'t given. Exporting as: ' + default_name + bcolors.ENDC)
            filename = default_name

        f = open(filename, 'w')
        f.write(package_store)
        f.close()
