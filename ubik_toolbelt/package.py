# coding: utf-8
# For Python < 2.6
from __future__ import with_statement

import os
import sys

from ubik_toolbelt.logger import stream_logger

def create(package_name):
	name = package_name

	control_py = """# coding: utf-8

from ubik_toolbelt.logger import stream_logger

class Control(object):
    def __init__(self):
        self.name = '%s'
        self.version = ''
        self.release = ''
        self.requires = []
        self.arch = ''
        self.dist = ''
        self.vers = ''
        self.description = ''

    def build(self):
        stream_logger.info('Building...')

    def package(self):
        stream_logger.info('Packaging...')

    def pre_install(self):
        pass

    def post_install(self):
        pass

    def pre_upgrade(self):
        pass

    def post_upgrade(self):
        pass

    def pre_remove(self):
        pass

    def post_remove(self):
        pass
""" % name

	stream_logger.info(' :: Create %s package structure' % name)
	os.makedirs(name)
	os.chdir(name)
	os.makedirs('build')
	os.makedirs('src')
	open('blacklist', 'w').close()
	with open('control.py', 'w') as control:
		control.write(control_py)
	stream_logger.info(' :: Done')

def build():
	import control
	control = control.Control()
	control.build()

def package():
	import control
	control = control.Control()
	control.package()