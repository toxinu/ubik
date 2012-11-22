#!/usr/bin/env python
# coding: utf-8
import os

import env
import unittest

import ubik.core as api

from ubik.installer import Installer
from ubik.exceptions import InstallerException

"""
Package Available:
    Good System:
      - iteself in deps(failed)   -> package_06
"""

class TestPackage_06(unittest.TestCase):

    def setUp(self):
        self.db = api.db
        self.package = self.db.packages['package_06']

    def test_01_name(self):
        self.assertEqual(str(self.package.name), 'package_06')

    def test_02_requires(self):
        self.assertEqual(self.package.requires, ['package_06'])

    def test_03_arch(self):
        self.assertEqual(str(self.package.arch), 'noarch')

    def test_04_dist(self):
        self.assertEqual(str(self.package.dist), 'nodist')

    def test_05_vers(self):
        self.assertEqual(str(self.package.vers), 'novers')

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
		raise Exception('Dependences resolving must failed')
	except InstallerException:
		pass
        self.assertEqual(len(installer.packages), 0)
        self.assertTrue(self.db.get('package_06'))

	# Just package_03 installed
        self.assertEqual(self.db.count_installed(), 1)

	path = "%s/bin/package_06" % api.conf.get('settings', 'packages')
	self.assertFalse(os.path.exists(path))

if __name__ == '__main__':
    unittest.main()
