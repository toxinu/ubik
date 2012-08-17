# coding: utf-8
import sys

from ubik.core import conf
from ubik.logger import logger
from ubik.tools import launch_cmd

import ubik.package

class Control(object):
	def __init__(self, package):
		if not isinstance(package, ubik.package.Package):
			raise Exception('Need a Package object')
		self.control_file = '%s/%s/control' % (
					conf.get('settings', 'cache'),
					package.name)

	def pre_install(self):
		launch_cmd('. %s; pre_install' % self.control_file)

	def post_install(self):
		launch_cmd('. %s; post_install' % self.control_file)

	def pre_remove(self):
		launch_cmd('. %s; pre_remove' % self.control_file)

	def post_remove(self):
		launch_cmd('. %s; post_remove' % self.control_file)

	def pre_update(self):
		launch_cmd('. %s; pre_update' % self.control_file)

	def post_update(self):
		launch_cmd('. %s; post_update' % self.control_file)

	def purge(self):
		launch_cmd('. %s; purge' % self.control_file)
