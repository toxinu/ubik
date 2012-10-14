#!/usr/bin/env python
# coding: utf-8
import os

import env
import unittest

import ubik.core as api

from ubik.installer import Installer
from ubik.remover import Remover

from subprocess import Popen, PIPE, STDOUT

"""
Package Available:
    Good System:
      - with one dep(success)      -> package_01
      - without dep(success)       -> package_02
"""

class TestPackage_01_02(unittest.TestCase):

	def setUp(self):
		self.db = api.db
		self.package_01 = self.db.packages['package_01']
		self.package_02 = self.db.packages['package_02']

	def test_01_name_package_01(self):
		self.assertEqual(str(self.package_01.name), 'package_01')

	def test_01_name_package_02(self):
		self.assertEqual(str(self.package_02.name), 'package_02')

	def test_02_requires_package_01(self):
		self.assertEqual(self.package_01.requires, ['package_02'])

	def test_02_requires_package_02(self):
		self.assertEqual(self.package_02.requires, [])

	def test_03_arch_package_01(self):
		self.assertEqual(str(self.package_01.arch), 'i386')

	def test_03_arch_package_02(self):
		self.assertEqual(str(self.package_02.arch), 'i386')

	def test_04_dist_package_01(self):
		self.assertEqual(str(self.package_01.dist), 'debian')

	def test_04_dist_package_02(self):
		self.assertEqual(str(self.package_02.dist), 'debian')

	def test_05_vers_package_01(self):
		self.assertEqual(str(self.package_01.vers), '6')

	def test_05_vers_package_02(self):
		self.assertEqual(str(self.package_02.vers), '6')

	def test_06_version_package_01(self):
		self.assertEqual(str(self.package_01.version), '')

	def test_06_version_package_02(self):
		self.assertEqual(str(self.package_02.version), '')

	def test_07_release_package_01(self):
		self.assertEqual(str(self.package_01.release), '')

	def test_07_release_package_02(self):
		self.assertEqual(str(self.package_02.release), '')

	def test_08_repo_version_package_01(self):
		self.assertEqual(str(self.package_01.repo_version), '0.2')

	def test_08_repo_version_package_02(self):
		self.assertEqual(str(self.package_02.repo_version), '0.1')

	def test_09_repo_release_package_01(self):
		self.assertEqual(str(self.package_01.repo_release), '0')

	def test_09_repo_release_package_02(self):
		self.assertEqual(str(self.package_02.repo_release), '2')

	def test_100_install_package_01(self):
		# Install 'package_01' package with it's 'package_02' require
		self.db.sync()
		installer = Installer()
		installer.resolv(self.package_01)
		installer.feed(installer.resolved)
		self.assertEqual(len(installer.packages), 2)

		installer.download()
		installer.install()
		self.assertEqual(self.db.count_installed(), 2)

	def test_101_bin_package_01(self):
		# Test the package_01 which have 'package_02' require
		p = Popen('package_01', shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
		self.assertEqual(p.stdout.read(), 'Im package_01\n')

	def test_102_bin_package_02(self):
		# Test the package_02 which is a 'package_01' require
		p = Popen('package_02', shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
		self.assertEqual(p.stdout.read(), 'Im package_02\n')

	def test_200_remove_package_01(self):
		self.db.sync()
		remover = Remover()
		remover.feed(self.package_01)
		self.assertEqual(len(remover.packages), 1)
		self.assertEqual(remover.packages[0].name, 'package_01')

		remover.remove()
		self.assertEqual(self.db.count_installed(), 1)

	def test_201_remove_package_02(self):
		self.db.sync()
		remover = Remover()
		remover.feed(self.db.packages['package_02'])
		self.assertEqual(len(remover.packages), 1)
		self.assertEqual(remover.packages[0].name, 'package_02')

		remover.remove()
		self.assertEqual(self.db.count_installed(), 0)

	def test_202_remove_file_removed(self):
		# Check if 'bin/package_01' and 02 files has been removed
		path = "%s/bin/package_01" % api.conf.get('settings', 'packages')
		self.assertFalse(os.path.exists(path))
		path = "%s/bin/package_02" % api.conf.get('settings', 'packages')
		self.assertFalse(os.path.exists(path))

if __name__ == '__main__':
	unittest.main()
