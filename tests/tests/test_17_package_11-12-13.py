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
    - Dep in another arch (package_07)(fail)  -> package_11
    - Dep in another dist (package_08)(fail)  -> package_12
    - Dep in another vers (package_09)(fail)  -> package_13
"""

class TestPackage_11_12_13(unittest.TestCase):

    def setUp(self):
        self.db = api.db
        self.package_11 = self.db.packages['package_11']
        self.package_12 = self.db.packages['package_12']
        self.package_13 = self.db.packages['package_13']

    def test_01_name(self):
        self.assertEqual(str(self.package_11.name), 'package_11')
        self.assertEqual(str(self.package_12.name), 'package_12')
        self.assertEqual(str(self.package_13.name), 'package_13')

    def test_02_requires(self):
        self.assertEqual(self.package_11.requires, ['package_07'])
        self.assertEqual(self.package_12.requires, ['package_08'])
        self.assertEqual(self.package_13.requires, ['package_09'])

    def test_03_arch(self):
        self.assertEqual(str(self.package_11.arch), 'i386')
        self.assertEqual(str(self.package_12.arch), 'i386')
        self.assertEqual(str(self.package_13.arch), 'i386')

    def test_04_dist(self):
        self.assertEqual(str(self.package_11.dist), 'debian')
        self.assertEqual(str(self.package_12.dist), 'debian')
        self.assertEqual(str(self.package_13.dist), 'debian')

    def test_05_vers(self):
        self.assertEqual(str(self.package_11.vers), '6')
        self.assertEqual(str(self.package_12.vers), '6')
        self.assertEqual(str(self.package_13.vers), '6')

    def test_06_version(self):
        self.assertEqual(str(self.package_11.version), '')
        self.assertEqual(str(self.package_12.version), '')
        self.assertEqual(str(self.package_13.version), '')

    def test_07_release(self):
        self.assertEqual(str(self.package_11.release), '')
        self.assertEqual(str(self.package_12.release), '')
        self.assertEqual(str(self.package_13.release), '')

    def test_08_repo_version(self):
        self.assertEqual(str(self.package_11.repo_version), '0.1')
        self.assertEqual(str(self.package_12.repo_version), '0.1')
        self.assertEqual(str(self.package_13.repo_version), '0.1')

    def test_09_repo_release(self):
        self.assertEqual(str(self.package_11.repo_release), '0')
        self.assertEqual(str(self.package_12.repo_release), '0')
        self.assertEqual(str(self.package_13.repo_release), '0')

    def test_100_install_package_11(self):
        self.db.sync()
        installer = Installer()
	try:
		installer.resolve(self.package_11)
		raise Exception('Dependences resolving must failed')
	except DatabaseException:
		pass
        self.assertEqual(len(installer.packages), 0)
        self.assertTrue(self.db.get('package_11'))

	# Just package_03 installed
        self.assertEqual(self.db.count_installed(), 1)

	path = "%s/bin/package_11" % api.conf.get('settings', 'packages')
	self.assertFalse(os.path.exists(path))

    def test_101_install_package_12(self):
        self.db.sync()
        installer = Installer()
	try:
		installer.resolve(self.package_12)
		raise Exception('Dependences resolving must failed')
	except DatabaseException:
		pass
        self.assertEqual(len(installer.packages), 0)
        self.assertTrue(self.db.get('package_12'))

	# Just package_03 installed
        self.assertEqual(self.db.count_installed(), 1)

	path = "%s/bin/package_12" % api.conf.get('settings', 'packages')
	self.assertFalse(os.path.exists(path))

    def test_102_install_package_13(self):
        self.db.sync()
        installer = Installer()
	try:
		installer.resolve(self.package_13)
		raise Exception('Dependences resolving must failed')
	except DatabaseException:
		pass
        self.assertEqual(len(installer.packages), 0)
        self.assertTrue(self.db.get('package_13'))

	# Just package_03 installed
        self.assertEqual(self.db.count_installed(), 1)

	path = "%s/bin/package_13" % api.conf.get('settings', 'packages')
	self.assertFalse(os.path.exists(path))

if __name__ == '__main__':
    unittest.main()
