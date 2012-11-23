#!/usr/bin/env python
# coding: utf-8
import os
import stat

import env
import unittest

import ubik.core as api

from ubik.installer import Installer
from ubik.remover import Remover

from subprocess import Popen, PIPE, STDOUT

"""
Package Available:
  Good System (i386/debian/6):
    - without dep, 777 on bin          -> package_15
"""

class TestPackage_15(unittest.TestCase):

    def setUp(self):
        self.db = api.db
        self.package = self.db.packages['package_15']

    def test_01_name(self):
        self.assertEqual(str(self.package.name), 'package_15')

    def test_02_requires(self):
        self.assertEqual(self.package.requires, [])

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
        installer.resolve(self.package)
        installer.feed(installer.get_resolved())
        self.assertEqual(len(installer.packages), 1)

        installer.download()
        installer.install()
        self.assertTrue(self.db.get('package_15'))
        self.assertEqual(self.db.count_installed(), 2)

    def test_101_bin_package(self):
        p = Popen('package_15', shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        self.assertEqual(p.stdout.read(), 'Im package_15\n')

    def test_102_check_permissions(self):
	self.assertEqual(stat.S_IMODE(os.stat('%s/bin/package_15' % api.conf.get('settings', 'packages')).st_mode), int('777', 8))

    def test_201_remove_package_15(self):
        self.db.sync()
        remover = Remover()
        remover.feed(self.db.packages['package_15'])
        self.assertEqual(len(remover.packages), 1)
        self.assertEqual(remover.packages[0].name, 'package_15')

        remover.remove()
        self.assertEqual(self.db.count_installed(), 1)

    def test_202_remove_file_removed(self):
        path = "%s/bin/package_15" % api.conf.get('settings', 'packages')
        self.assertFalse(os.path.exists(path))

if __name__ == '__main__':
    unittest.main()
