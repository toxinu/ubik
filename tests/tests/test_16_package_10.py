#!/usr/bin/env python
# coding: utf-8
import os

import env
import unittest

import ubik.core as api

from ubik.installer import Installer
from ubik.exceptions import DatabaseException

"""
Package Available:
    Good System:
      - unvailable deps (jambon)(failed)   -> package_10
"""

class TestPackage_10(unittest.TestCase):

    def setUp(self):
        self.db = api.db
        self.package = self.db.packages['package_10']

    def test_01_name(self):
        self.assertEqual(str(self.package.name), 'package_10')

    def test_02_requires(self):
        self.assertEqual(self.package.requires, ['jambon'])

    def test_03_arch(self):
        self.assertEqual(str(self.package.arch), 'i386')

    def test_04_dist(self):
        self.assertEqual(str(self.package.dist), 'debian')

    def test_05_vers(self):
        self.assertEqual(str(self.package.vers), '6')

    def test_06_version(self):
        self.assertEqual(str(self.package.version), '')

    def test_07_release(self):
        self.assertEqual(str(self.package.release), '')

    def test_08_repo_version(self):
        self.assertEqual(str(self.package.repo_version), '0.1')

    def test_09_repo_release(self):
        self.assertEqual(str(self.package.repo_release), '0')

    def test_100_install_package(self):
        self.db.sync()
        installer = Installer()
	try:
		installer.resolve(self.package)
		raise Exception('Dependence must be unvailable')
	except DatabaseException:
		pass
        self.assertEqual(len(installer.packages), 0)
        self.assertTrue(self.db.get('package_10'))

	# Just package_03 installed
        self.assertEqual(self.db.count_installed(), 1)

	path = "%s/bin/package_10" % api.conf.get('settings', 'packages')
	self.assertFalse(os.path.exists(path))

if __name__ == '__main__':
    unittest.main()
