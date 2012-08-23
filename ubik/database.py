# coding: utf-8
import os
import sys
import re
import json
import time

from ubik.logger import logger
from ubik.logger import stream_logger

from ubik.core import conf
from ubik.package import Package

from ubik.downloader import get_database
from ubik.exceptions import DatabaseError

class Database(object):
	def __init__(self, content=None):
		self.content = content
		self.file_path = None
		self.packages = self.parse()

	def sync(self):
		stream_logger.info('    | Get %s/%s/%s/Packages.list' % (
						conf.get('repo', 'url'),
						conf.get('repo', 'base'),
						conf.get('repo', 'vers')))
		db_remote = Database(get_database())

		for package in db_remote.packages.values():
			# Check installed
			if package.name not in self.packages.keys():
				package.status = "10"
				self.packages[package.name] = package
			elif self.packages[package.name].status == "10":
				package.status = "10"
			# Check version
			elif package.version > self.packages[package.name].version:
				package.status = "1"
			elif package.version < self.packages[package.name].version:
				package.status = "11"
			# Check release
			elif package.release > self.packages[package.name].release:
				package.status = "2"
			elif package.release < self.packages[package.name].release:
				package.status = "12"
			# Up-to-date
			else:
				package.status = 0
				
			if package.status in ['1','2','11','12']:
				package.remote_vers = package.raw_version
				package.raw_version = self.packages[package.name].raw_version
				package.version = self.packages[package.name].version
				package.release = self.packages[package.name].release
			elif package.status in ['10']:
				package.remote_vers = package.raw_version
				package.version = ''
				package.release = ''
				package.raw_version = ''
			else:
				package.remote_vers = ''

			self.packages[package.name] = package

		# Save databases
		self.save(conf.get('paths', 'local_db'))

		# Save informations
		if not os.path.exists(conf.get('paths', 'infos')):
			open(conf.get('paths', 'infos'), 'w').close()
		
		infos = json.dump(
			{'last_update': time.ctime()},
		open(conf.get('paths', 'infos'), 'w'))

	def get(self, packages, regexp = True):
		if not isinstance(packages, list):
			packages = [packages]

		result = []
		for package in packages:
			if regexp:
				for key,value in self.packages.items():
					if package[-1] != '*':
						pattern = re.compile(r'%s$' % package)
					else:
						logger.debug(package)
						pattern = re.compile(package)
					if re.search(pattern, key):
						result.append(value)
			else:
				try:
					result.append(self.packages[package])
				except:
					raise DatabaseError('Package %s not available' % package)

		return result
		
	def check_system(self, package):
		if package.arch != conf.get('system', 'arch'):
			if package.arch != "noarch":
				return False
		if package.dist != conf.get('system', 'dist'):
			if package.dist != "nodist":
				return False
		if package.vers != conf.get('system', 'vers'):
			if package.vers != "novers":
				return False
		return True

	def check_packages(self, p, o):
		# p is new package
		# o is old package
		if o.arch == 'noarch' and o.dist == 'nodist' and o.vers == 'novers':
			return False
		return True

	def parse(self):
		packages = {}
		for line in self.content:
			name = line.split('|')[0]
			if len(line.split('|')) == 9:
				infos = {	'raw_version': line.split('|')[1],
							'version': line.split('|')[1].split('-')[:-1],
							'release': line.split('|')[1].split('-')[-1],
							'status' : line.split('|')[2],
							'md5'	 : line.split('|')[3],
							'deps'	 : line.split('|')[4].split(),
							'arch'	 : line.split('|')[5],
							'dist'	 : line.split('|')[6],
							'vers'	 : line.split('|')[7],
							'remote_vers': line.split('|')[8].replace('\n', '')}
			else:
				infos = {	'raw_version': line.split('|')[1],
							'version': line.split('|')[1].split('-')[:-1],
							'release': line.split('|')[1].split('-')[-1],
							'status' : line.split('|')[2],
							'md5'	 : line.split('|')[3],
							'deps'	 : line.split('|')[4].split(),
							'arch'	 : line.split('|')[5],
							'dist'	 : line.split('|')[6],
							'vers'	 : line.split('|')[7].replace('\n', '')}
			p = Package(name)
			p.fill(**infos)

			if not self.check_system(p):
				continue

			if packages.get(name, False):
				if not self.check_packages(p, packages[name]):
					continue
			packages[name] = p
		return packages

	def add(self, package):
		if not isinstance(package, Package):
			raise DatabaseError('Package must be Package object')
		self.packages[package.name] = package

	def delete(self, package):
		if not isinstance(package, Package):
			package_name = package
		else:
			package_name = package.name
		try:
			del self.packages[package_name]
		except:
			pass

	def save(self, path):
		self.file_path = path
		open(path, 'w').close()
		for package in self.packages.values():
			with open(path, 'a') as f:
				f.write(package.get_raw() + '\n')

	def get_upgrades(self):
		res = []
		for package in self.packages.values():
			if package.status in ['1','2']:
				res.append(package)
		return res

	def count_upgrades(self):
		res = 0
		for package in self.packages.values():
			if package.status in ['1','2']:
				res += 1
		return res

	def get_installed(self):
		res = []
		for package in self.packages.values():
			if package.status in ['0','1','2','11','12','20','21']:
				res.append(package)
		return res

	def count_installed(self):
		res = 0
		for package in self.packages.values():
			if package.status in ['0','1','2','11','12','20','21']:
				res += 1
		return res

	def get_packages(self):
		return self.packages

	def count_packages(self):
		return len(self.packages)
