# coding: utf-8
import os

from ubik_toolbelt.logger import stream_logger
from ubik_toolbelt.control import Control

from ubik.core import conf

class Package(Control):
    def __init__(self):
        Control.__init__(self)
        self.name = 'wget'
        self.version = '1.14'
        self.release = '0'
        self.requires = []
        self.arch = ''
        self.dist = ''
        self.vers = ''
        self.description = ''

        self.cur_dir = os.getcwd()
        self.src_dir = os.path.join(os.getcwd(), 'source')
        self.pkg_dir = os.path.join(os.getcwd(), 'build')

        #
        # You can easily add some pre_install, post_install, *_upgrade and *_remove methods
        #

    def build(self):
        stream_logger.info('Building...')
        os.chdir(self.src_dir)

        os.system('wget http://ftp.gnu.org/gnu/wget/wget-%s.tar.gz' % self.version)
        os.system('tar xvf wget-%s.tar.gz' % self.version)
        os.system('rm wget-%s.tar.gz' % self.version)
        os.chdir('wget-%s' % self.version)
        os.system('./configure --prefix=%s' % conf.get('settings', 'packages'))
        os.system('make')

    def package(self):
        stream_logger.info('Packaging...')
        os.chdir(self.src_dir)
        os.chdir('wget-%s' % self.version)

        os.system('make prefix=%s install' % self.pkg_dir)
