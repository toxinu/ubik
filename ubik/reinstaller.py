# coding: utf-8
from ubik.core import db
from ubik.core import conf

from ubik.package import Package
from ubik.downloader import get_package

from ubik.tools import cached
from ubik.tools import checkmd5
from ubik.exceptions import ReinstallerException

from ubik.logger import logger
from ubik.logger import stream_logger

class Reinstaller(object):
	def __init__(self):
		self.packages = []

	def feed(self, packages):
		if not isinstance(packages, list):
			packages = [packages]

		for package in packages:
			if not isinstance(package, Package):
				package = db.get(package)
			if package not in self.packages:
				if package.status not in ['10']:
					self.packages.append(package)
				else:
					stream_logger.info('    - %s not installed' % package.name)

	def resolv(self, package):
		self.package = package
		self.tree = [self.package]
		self.resolved = []
		self.deps_resolv(self.package, self.resolved, [])

	def deps_resolv(self, package, resolved, unresolved):
		self.unresolved = unresolved
		self.unresolved.append(package)
		for dep in db.get(package.requires):
			if dep not in self.resolved:
				if dep in self.unresolved:
					raise Exception('Circular reference detected: %s -> %s' % (package.name, dep.name))
				self.deps_resolv(dep, self.resolved, self.unresolved)
		self.resolved.append(package)
		self.unresolved.remove(package)

	def download(self):
		stream_logger.info(' :: Download')	
		for package in self.packages:
			logger.info('Download %s' % package.name)
			# Not cached
			if not cached(package):
				logger.info('%s not cached' % package.name)
				get_package(package)
				# Invalid Md5
				if not checkmd5(package):
					logger.info('%s md5 invalid' % package.name)
					stream_logger.info('   | Md5 invalid, package corrumpt')	
					ReinstallerException('Invalid Md5')
			# Cached
			else:
				logger.info('%s already in cache' % package.name)
				# Invalid Md5, redownload
				if not checkmd5(package):
					logger.info('%s cache package md5 invalid' % package.name)
					get_package(package)
					if not checkmd5(package):
						logger.info('%s md5 invalid' % package.name)
						stream_logger.info('   | Md5 invalid, package corrumpt')	
						ReinstallerException('Invalid Md5')
				else:
					stream_logger.info('    | %s already in cache' % package.name)

	def reinstall(self, ignore_errors=False):
		if not self.packages:
			raise InstallerException('Nothing to reinstall')
		stream_logger.info(' :: Reinstall')	
		for package in self.packages:
			package.install(ignore_errors)
			stream_logger.info('      | Update database')
			package.status = "0"
			package.set_raw_version(package.remote_vers)
			package.remote_vers = ''
			db.add(package)
			db.save(conf.get('paths', 'local_db'))
