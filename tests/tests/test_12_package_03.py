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
      - nod deps(success)   -> package_03
"""

class TestPackage_03(unittest.TestCase):

    def setUp(self):
        self.db = api.db
        self.package = self.db.packages['package_03']

    def test_01_name(self):
        self.assertEqual(str(self.package.name), 'package_03')

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
        installer.resolv(self.package)
        installer.feed(installer.get_resolved())
        self.assertEqual(len(installer.packages), 1)

        installer.download()
        installer.install()
        self.assertTrue(self.db.get('package_03'))
        self.assertEqual(self.db.count_installed(), 1)

    def test_101_bin_package(self):
        p = Popen('package_03', shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        self.assertEqual(p.stdout.read(), 'Im package_03\n')

if __name__ == '__main__':
    unittest.main()