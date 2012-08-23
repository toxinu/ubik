# coding: utf-8

from ubik.core import db
from ubik.core import conf

from ubik.logger import logger
from ubik.logger import stream_logger

from ubik.package import Package
from ubik.exceptions import RemoverError

class Remover(object):
	def __init__(self):
		self.pkg_blacklist = conf.get('packages', 'pkg_blacklist').split()
		self.packages = []
	
	def feed(self, packages):
		if not isinstance(packages, list):
			packages = [packages]

		for package in packages:
			if not isinstance(package, Package):
				package = db.get(package)[0]
			if package not in self.packages:
				if package.status not in ['10']:
					if package.name not in self.pkg_blacklist:
						self.packages.append(package)
					else:
						stream_logger.info(' :: %s is blacklisted' % package.name)
				else:
					stream_logger.info(' :: %s not installed' % package.name)

	def remove(self, ignore_errors=False):
		if not self.packages:
			raise RemoverError('Nothing to remove')
		stream_logger.info(' :: Remove')
		for package in self.packages:
			package.remove(ignore_errors)
			stream_logger.info('     | Update database')
			package.status = "10"
			package.remote_vers = package.raw_version
			package.raw_version = ''
			package.version = ''
			package.release = ''
			db.add(package)
			db.save(conf.get('paths', 'local_db'))
