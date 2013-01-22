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
        self.name = 'package_02'
        self.version = '0.1'
        self.release = '2'
        self.requires = []
        self.arch = 'i386'
        self.dist = 'debian'
        self.vers = '6'
        self.description = ''

    def build(self):
        stream_logger.info('Building...')

    def package(self):
        stream_logger.info('Packaging...')
        os.system('cp -p -R %s/* %s' % (self.src_dir, self.pkg_dir))
