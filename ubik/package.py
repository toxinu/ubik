# coding: utf-8
import os
import shutil

from ubik.core import conf

from ubik.downloader import get_package

from ubik.logger import logger
from ubik.logger import stream_logger

from ubik.control import Control
from ubik.tools import unarchiver
from ubik.tools import unpacker

from ubik.exceptions import *

class Package(object):
	def __init__(self, name):
		self.name = name
		self.version = ''
		self.release = ''
		self.status = ''
		self.requires = []
		self.md5 = ''
		self.arch = ''
		self.dist = ''
		self.vers = ''
		self.repo_version = ''
		self.repo_release = ''

		self.raw_requires = self.get_raw_requires()

	def fill(self, **kwargs):
		for key in kwargs:
			if key == 'name':
				self.name = kwargs[key]
			elif key == 'version':
				self.version = kwargs[key]
			elif key == 'release':
				self.release = kwargs[key]
			elif key == 'status':
				self.status = kwargs[key]
			elif key == 'requires':
				self.requires = kwargs[key]
			elif key == 'md5':
				self.md5 = kwargs[key]
			elif key == 'arch':
				self.arch = kwargs[key]
			elif key == 'dist':
				self.dist = kwargs[key]
			elif key == 'vers':
				self.vers = kwargs[key]
			elif key == 'repo_version':
				self.repo_version = kwargs[key]
			elif key == 'repo_release':
				self.repo_release = kwargs[key]
		logger.debug(' SELF: %s-%s' % (self.version, self.release))

	def get_raw_requires(self):
		return ' '.join(self.requires)

	def unarchive(self):
		unarchiver(self)

	def install(self, ignore_errors=False):
		stream_logger.info('    - %s' % self.name)
		stream_logger.info('      | Unarchive')
		self.unarchive()
		control = Control(self, ignore_errors)
		stream_logger.info('      | Pre Install')
		control.pre_install()
		stream_logger.info('      | Unpack')
		unpacker(self)
		stream_logger.info('      | Post Install')
		control.post_install()
		stream_logger.info('      | Clean')
		shutil.rmtree('%s/%s' % (conf.get('settings', 'cache'), self.name))

	def upgrade(self, ignore_errors=False):
		stream_logger.info('    - %s' % self.name)
		stream_logger.info('      | Unarchive')
		self.unarchive()
		control = Control(self, ignore_errors)
		stream_logger.info('      | Pre Update')
		control.pre_update()
		stream_logger.info('      | Unpack')
		unpacker(self)
		stream_logger.info('      | Post Update')
		control.post_update()
		stream_logger.info('      | Clean')
		shutil.rmtree('%s/%s' % (conf.get('settings', 'cache'), self.name))

	def remove(self, ignore_errors=False):
		stream_logger.info('   - %s' % self.name)

		# If archive not already extract
		if not os.path.exists('%s/%s' % (
					conf.get('settings', 'cache'),
					self.name)):
			self.unarchive()

		control = Control(self, ignore_errors)

		# Pre Remove
		stream_logger.info('     | Pre Remove')
		control.pre_remove()

		# Remove
		stream_logger.info('     | Remove')
		files_list = open('%s/%s/files.lst' % (
						conf.get('settings', 'cache'),
						self.name)).readlines()
		for _file in files_list:
			try:
				os.remove('%s/%s' % (conf.get('settings', 'packages'), _file.replace('\n', '')))
			except:
				pass
		# Post Remove
		stream_logger.info('     | Post Remove')
		control.post_remove()

		stream_logger.info('     | Clean')
		shutil.rmtree('%s/%s' % (conf.get('settings', 'cache'), self.name))
