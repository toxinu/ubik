# coding: utf-8
import os

from ubik_toolbelt.logger import stream_logger
from ubik_toolbelt.control import Control

from ubik_toolbelt.contrib import get_user_name
from ubik_toolbelt.contrib import get_user_group
from ubik_toolbelt.contrib import user_exists
from ubik_toolbelt.contrib import group_exists

from ubik.core import conf

class Package(Control):
    def __init__(self):
        Control.__init__(self)
        self.name = 'package_12'
        self.version = '0.1'
        self.release = '0'
        self.requires = ['package_08']
        self.arch = 'i386'
        self.dist = 'debian'
        self.vers = '6'
        self.description = ''

        self.cur_dir = os.getcwd()
        self.src_dir = os.path.join(os.getcwd(), 'source')
        self.pkg_dir = os.path.join(os.getcwd(), 'build')

        #
        # You can easily add some pre_install, post_install, *_upgrade and *_remove methods
        #

    def build(self):
        stream_logger.info('Building...')

    def package(self):
        stream_logger.info('Packaging...')
        os.system('cp -p -R %s/* %s' % (self.src_dir, self.pkg_dir))
