# coding: utf-8
import os
import sys
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
		self.raw_version = ''
		self.version = ''
		self.release = ''
		self.status = ''
		self.deps = []
		self.md5 = ''
		self.arch = ''
		self.dist = ''
		self.vers = ''
		self.remote_vers = ''

		self.raw_deps = self.get_raw_deps()

	def fill(self, **kwargs):
		for key in kwargs:
			if key == 'name':
				self.name = kwargs[key]
			elif key == 'raw_version':
				self.raw_version = kwargs[key]
			elif key == 'version':
				self.version = kwargs[key]
			elif key == 'release':
				self.release = kwargs[key]
			elif key == 'status':
				self.status = kwargs[key]
			elif key == 'deps':
				self.deps = kwargs[key]
			elif key == 'md5':
				self.md5 = kwargs[key]
			elif key == 'arch':
				self.arch = kwargs[key]
			elif key == 'dist':
				self.dist = kwargs[key]
			elif key == 'vers':
				self.vers = kwargs[key]
			elif key == 'remote_vers':
				self.remote_vers = kwargs[key]

		if (not self.version and not self.release) and self.raw_version:
			self.version = self.raw_version.split('-')[:-1]
			self.release = self.raw_version.split('-')[-1]
			
		elif (self.version and self.release) and not self.raw_version:
			self.raw_version = self.version + '-' + self.release

	def set_raw_version(self, version):
		self.raw_version = version
		self.version = self.raw_version.split('-')[:-1]
		self.release = self.raw_version.split('-')[-1]

	def get_raw_deps(self):
		return ' '.join(self.deps)

	def get_raw(self):
		return '%s|%s|%s|%s|%s|%s|%s|%s|%s' % (
					self.name, self.raw_version, self.status,
					self.md5, self.get_raw_deps(),
					self.arch, self.dist, self.vers,
					self.remote_vers)

	def unarchive(self):
		unarchiver(self)

	def install(self, force=False):
		stream_logger.info('    - %s' % self.name)
		stream_logger.info('      | Unarchive')
		self.unarchive()
		control = Control(self)
		stream_logger.info('      | Pre Install')
		try:
			control.pre_install()
		except CmdError as err:
			stream_logger.info('Error: %s' % err)
			sys.exit(1)
		stream_logger.info('      | Unpack')
		unpacker(self)
		stream_logger.info('      | Post Install')
		try:
			control.post_install()
		except CmdError as err:
			stream_logger.info('Error: %s' % err)
			sys.exit(1)
		stream_logger.info('      | Clean')
		shutil.rmtree('%s/%s' % (conf.get('settings', 'cache'), self.name))

	def upgrade(self):
		stream_logger = get_stream_logger()
		stream_logger.info('    - %s' % self.name)
		stream_logger.info('      | Unarchive')
		self.unarchive()
		control = Control(self)
		stream_logger.info('      | Pre Update')
		try:
			control.pre_update()
		except CmdError as err:
			stream_logger.info('Error: %s' % err)
			sys.exit(1)
		stream_logger.info('      | Unpack')
		unpacker(self)
		stream_logger.info('      | Post Update')
		try:
			control.post_update()
		except CmdError as err:
			stream_logger.info('Error: %s' % err)
			sys.exit(1)
		stream_logger.info('      | Clean')
		shutil.rmtree('%s/%s' % (conf.get('settings', 'cache'), self.name))

	def remove(self):
		stream_logger.info('   - %s' % self.name)

		# If archive not already extract
		if not os.path.exists('%s/%s' % (
					conf.get('settings', 'cache'),
					self.name)):
			self.unarchive()

		control = Control(self)

		# Pre Remove
		stream_logger.info('     | Pre Remove')
		try:
			control.pre_remove()
		except CmdError as err:
			stream_logger.info('Error: %s' % err)
			sys.exit(1)

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
		try:
			control.post_remove()
		except CmdError as err:
			stream_logger.info('Error: %s' % err)
			sys.exit(1)

		stream_logger.info('     | Clean')
		shutil.rmtree('%s/%s' % (conf.get('settings', 'cache'), self.name))
