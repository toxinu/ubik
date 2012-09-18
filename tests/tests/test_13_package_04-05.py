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
    Any System:
      - with one dep(success)      -> package_04
      - without dep(success)       -> package_05
"""

class TestPackage_04_05(unittest.TestCase):

    def setUp(self):
        self.db = api.db
        self.package_04 = self.db.packages['package_04']
        self.package_05 = self.db.packages['package_05']

    def test_01_name_package_04(self):
        self.assertEqual(str(self.package_04.name), 'package_04')

    def test_01_name_package_05(self):
        self.assertEqual(str(self.package_05.name), 'package_05')

    def test_02_requires_package_04(self):
        self.assertEqual(self.package_04.requires, ['package_05'])

    def test_02_requires_package_05(self):
        self.assertEqual(self.package_05.requires, [])

    def test_03_arch_package_04(self):
        self.assertEqual(str(self.package_04.arch), 'noarch')

    def test_03_arch_package_05(self):
        self.assertEqual(str(self.package_05.arch), 'noarch')

    def test_04_dist_package_04(self):
        self.assertEqual(str(self.package_04.dist), 'nodist')

    def test_04_dist_package_05(self):
        self.assertEqual(str(self.package_05.dist), 'nodist')

    def test_05_vers_package_04(self):
        self.assertEqual(str(self.package_04.vers), 'novers')

    def test_05_vers_package_05(self):
        self.assertEqual(str(self.package_05.vers), 'novers')

    def test_06_version_package_04(self):
        self.assertEqual(str(self.package_04.version), '')

    def test_06_version_package_05(self):
        self.assertEqual(str(self.package_05.version), '')

    def test_07_release_package_04(self):
        self.assertEqual(str(self.package_04.release), '')

    def test_07_release_package_05(self):
        self.assertEqual(str(self.package_05.release), '')

    def test_08_repo_version_package_04(self):
        self.assertEqual(str(self.package_04.repo_version), '0.1')

    def test_08_repo_version_package_05(self):
        self.assertEqual(str(self.package_05.repo_version), '0.1')

    def test_09_repo_release_package_04(self):
        self.assertEqual(str(self.package_04.repo_release), '0')

    def test_09_repo_release_package_05(self):
        self.assertEqual(str(self.package_05.repo_release), '0')

    def test_100_install_package_04(self):
        # Install 'package_04' package with it's 'package_05' require
        self.db.sync()
        installer = Installer()
        installer.resolv(self.package_04)
        installer.feed(installer.resolved)
        self.assertEqual(len(installer.packages), 2)

        installer.download()
        installer.install()
        self.assertEqual(self.db.count_installed(), 3)

    def test_101_bin_package_04(self):
        # Test the package_04 which have 'package_05' require
        p = Popen('package_04', shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        self.assertEqual(p.stdout.read(), 'Im package_04\n')

    def test_102_bin_package_05(self):
        # Test the package_05 which is a 'package_04' require
        p = Popen('package_05', shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        self.assertEqual(p.stdout.read(), 'Im package_05\n')

    def test_200_remove_package_04(self):
        self.db.sync()
        remover = Remover()
        remover.feed(self.package_04)
        self.assertEqual(len(remover.packages), 1)
        self.assertEqual(remover.packages[0].name, 'package_04')

        remover.remove()
        self.assertEqual(self.db.count_installed(), 2)

    def test_201_remove_package_05(self):
        self.db.sync()
        remover = Remover()
        remover.feed(self.db.packages['package_05'])
        self.assertEqual(len(remover.packages), 1)
        self.assertEqual(remover.packages[0].name, 'package_05')

        remover.remove()
        self.assertEqual(self.db.count_installed(), 1)

    def test_202_remove_file_removed(self):
        # Check if 'bin/package_04' and 02 files has been removed
        path = "%s/bin/package_04" % api.conf.get('settings', 'packages')
        self.assertFalse(os.path.exists(path))
        path = "%s/bin/package_05" % api.conf.get('settings', 'packages')
        self.assertFalse(os.path.exists(path))

if __name__ == '__main__':
    unittest.main()
