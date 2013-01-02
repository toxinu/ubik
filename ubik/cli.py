# coding: utf-8
import sys
import traceback

from ubik.core import conf
from ubik.core import db

from ubik.logger import stream_logger
from ubik.logger import logger

from ubik.installer import Installer
from ubik.reinstaller import Reinstaller
from ubik.remover import Remover
from ubik.upgrader import Upgrader

from ubik.view import get_view
from ubik.view import get_conf
from ubik.view import get_stats
from ubik.view import TablePrinter

from ubik.tools import confirm
from ubik.tools import clean

from ubik.exceptions import *

class Cli(object):
    def __init__(self, *args, **kwargs):
        self.args = kwargs
        stream_logger.disabled = False

    def error_link(self, exit=True):
        stream_logger.info('!! Sorry Ubik failed. Please report this issue on my bug tracker')
        stream_logger.info('!! Before post issue, please set logging at least at level 2. Thanks!')
        stream_logger.info('Link: https://github.com/socketubs/ubik/issues?state=open')
        if exit:
           sys.exit(1)

    def start(self):
        ###################
        # conf            #
        ###################
        if self.args.get('conf', False):
            get_conf()
        ###################
        # stats           #
        ###################
        if self.args.get('stats', False):
            get_stats()
        ###################
        # list            #
        ###################
        elif self.args.get('list', False):
            get_view()
        ###################
        # update          #
        ###################
        elif self.args.get('update', False):
            stream_logger.info(' :: Update')
            try:
                db.sync()
            except Exception as err:
                if conf.get('logger','level') >= 2:
                    traceback.print_exc(file=sys.stdout)
                self.error_link()
        ###################
        # clean           #
        ###################
        elif self.args.get('clean', False):
            stream_logger.info(' :: Clean')
            clean()
        ###################
        # reinstall       #
        ###################
        elif self.args.get('reinstall', False):
            # Sync Database
            stream_logger.info(' :: Update')
            try:
                db.sync()
            except Exception as err:
                if conf.get('logger','level') >= 2:
                    traceback.print_exc(file=sys.stdout)
                self.error_link()
            # Create installer
            stream_logger.info(' :: Resolving')
            reinstaller = Reinstaller()
            if not isinstance(self.args['<package>'], list):
                packages = [self.args['<package>']]
            else:
                packages = self.args['<package>']

            try:
                if self.args.get('--with-deps', False):
                    for package in db.get(packages):
                        try:
                            reinstaller.resolv(package)
                            reinstaller.feed(reinstaller.resolved)
                        except RuntimeError as err:
                            stream_logger.info(' :: Dependencies resolv failed (%s)' % err)
                            sys.exit(1)
                else:
                    reinstaller.feed(db.get(packages))
            except DatabaseException as err:
                if conf.get('logger','level') >= 2:
                    traceback.print_exc(file=sys.stdout)
                self.error_link()

            logger.debug(reinstaller.packages)
            if not reinstaller.packages:
                stream_logger.info(' :: No package(s) to reinstall')
                sys.exit(0)
            stream_logger.info(' :: Following packages will be reinstalled:')
            for package in reinstaller.packages:
                stream_logger.info('    - %s' % package.name)
            if not self.args.get('--force-yes', False):
                if confirm():
                    reinstaller.download()
                    try:
                        reinstaller.reinstall(ignore_errors=self.args.get('--ignore-errors', False))
                    except Exception as err:
                        raise
                else:
                    stream_logger.info('Abort.')
                    sys.exit(1)
            else:
                reinstaller.download()
                try:
                    reinstaller.reinstall(ignore_errors=self.args.get('--ignore-errors', False))
                except Exception as err:
                    raise

        ###################
        # install         #
        ###################
        elif self.args.get('install', False):
            # Sync Database
            stream_logger.info(' :: Update')
            try:
                db.sync()
            except Exception as err:
                if conf.get('logger','level') >= 2:
                    traceback.print_exc(file=sys.stdout)
                self.error_link()
            # Create installer
            installer = Installer()
            # Resolv deps
            stream_logger.info(' :: Resolving dependencies')
            if not isinstance(self.args['<package>'], list):
                packages = [self.args['<package>']]
            else:
                packages = self.args['<package>']

            try:
                for package in db.get(packages):
                    try:
                        installer.resolv(package)
                        installer.feed(installer.resolved)
                    except RuntimeError as err:
                        stream_logger.info(' :: Dependencies resolv failed (%s)' % err)
                        sys.exit(1)
            except DatabaseException as err:
                if conf.get('logger','level') >= 2:
                    traceback.print_exc(file=sys.stdout)
                self.error_link()

            if not installer.packages:
                stream_logger.info('    - No package(s) found')
                sys.exit(1)
            stream_logger.info(' :: Following dependencies will be installed:')
            for dep in installer.packages:
                stream_logger.info('    - %s' % dep.name)

            if not self.args.get('--force-yes', False):
                if confirm():
                    installer.download()
                    try:
                        installer.install(ignore_errors=self.args.get('--ignore-errors', False))
                    except Exception as err:
                        raise
                else:
                    stream_logger.info('Abort.')
                    sys.exit(1)
            else:
                installer.download()
                try:
                    installer.install(ignore_errors=self.args.get('--ignore-errors', False))
                except Exception as err:
                    raise
        ###################
        # upgrade         #
        ###################
        elif self.args.get('upgrade', False):
            # Sync Database
            stream_logger.info(' :: Update')
            try:
                db.sync()
            except Exception as err:
                if conf.get('logger','level') >= 2:
                    traceback.print_exc(file=sys.stdout)
                self.error_link()

            # Create Upgrader
            upgrader = Upgrader()
            stream_logger.info(' :: Resolving')
            if not isinstance(self.args['<package>'], list):
                packages = [self.args['<package>']]
            else:
                packages = self.args['<package>']

            if not packages:
                upgrader.feed(db.get_upgrades())
            else:
                upgrader.feed(packages)

            if not upgrader.packages:
                stream_logger.info(' :: No package(s) to upgrade')
                sys.exit(0)

            stream_logger.info(' :: Following packages will be upgraded:')
            for package in upgrader.packages:
                stream_logger.info('    - %s' % package.name)

            if not self.args.get('--force-yes', False):
                if confirm():
                    upgrader.download()
                    try:
                        upgrader.upgrade(ignore_errors=self.args.get('--ignore-errors', False))
                    except Exception as err:
                        raise
                else:
                    stream_logger.info('Abort.')
                    sys.exit(1)
            else:
                upgrader.download()
                try:
                    upgrader.upgrade(ignore_errors=self.args.get('--ignore-errors', False))
                except Exception as err:
                    raise
        ###################
        # remove          #
        ###################
        elif self.args.get('remove', False):
            # Create remover
            remover = Remover()
            stream_logger.info(' :: Resolving')
            packages = db.get(self.args.get('<package>'))

            try:
                remover.feed(packages)
            except DatabaseException as err:
                if conf.get('logger','level') >= 2:
                    traceback.print_exc(file=sys.stdout)
                self.error_link()

            if not remover.packages:
                sys.exit(0)

            stream_logger.info(' :: Following packages will be removed:')
            for package in remover.packages:
                stream_logger.info('    - %s' % package.name)

            if not self.args.get('--force-yes', False):
                if confirm():
                    remover.remove(ignore_errors=self.args.get('--ignore-errors', False))
                else:
                    stream_logger.info('Abort.')
                    sys.exit(1)
            else:
                try:
                    remover.remove(ignore_errors=self.args.get('--ignore-errors', False))
                except Exception as err:
                    raise
