#!/usr/bin/env python
# coding: utf-8
import os
import stat

import env
import unittest

import ubik.core as api

from ubik.installer import Installer
from ubik.reinstaller import Reinstaller
from ubik.remover import Remover

from subprocess import Popen, PIPE, STDOUT

"""
Reinstall package_05
"""

class TestPackage_05(unittest.TestCase):

    def setUp(self):
        self.db = api.db
        self.package = self.db.packages['package_05']

    def test_100_install_package(self):
        self.db.sync()
        installer = Installer()
        installer.resolve(self.package)
        installer.feed(installer.get_resolved())
        self.assertEqual(len(installer.packages), 1)

        installer.download()
        installer.install()
        self.assertTrue(self.db.get('package_05'))
        self.assertEqual(self.db.count_installed(), 5)

    def test_101_bin_package(self):
        p = Popen('package_05', shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        self.assertEqual(p.stdout.read(), 'Im package_05\n')

    def test_110_reinstall_package(self):
        self.db.sync()
        reinstaller = Reinstaller()
        reinstaller.resolve(self.package)
        reinstaller.feed(reinstaller.get_resolved())
        self.assertEqual(len(reinstaller.packages), 1)

        reinstaller.download()
        reinstaller.reinstall()
        self.assertTrue(self.db.get('package_05'))
        self.assertEqual(self.db.count_installed(), 5)

        self.package.version = '0.1'
        self.package.remote_version = ''

        self.package.release = '0'
        self.package.remote_release = ''

    def test_111_bin_package(self):
        p = Popen('package_05', shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        self.assertEqual(p.stdout.read(), 'Im package_05\n')

    def test_112_remove_bin(self):
        os.remove("%s/bin/package_05" % api.conf.get('settings', 'packages'))

    def test_113_reinstall_package(self):
        self.db.sync()
        reinstaller = Reinstaller()
        reinstaller.resolve(self.package)
        reinstaller.feed(reinstaller.get_resolved())
        self.assertEqual(len(reinstaller.packages), 1)

        reinstaller.download()
        reinstaller.reinstall()
        self.assertTrue(self.db.get('package_05'))
        self.assertEqual(self.db.count_installed(), 5)

    def test_111_bin_package(self):
        p = Popen('package_05', shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        self.assertEqual(p.stdout.read(), 'Im package_05\n')

    def test_201_remove_package_05(self):
        self.db.sync()
        remover = Remover()
        remover.feed(self.db.packages['package_05'])
        self.assertEqual(len(remover.packages), 1)
        self.assertEqual(remover.packages[0].name, 'package_05')

        remover.remove()
        self.assertEqual(self.db.count_installed(), 4)

    def test_202_remove_file_removed(self):
        path = "%s/bin/package_05" % api.conf.get('settings', 'packages')
        self.assertFalse(os.path.exists(path))

if __name__ == '__main__':
    unittest.main()
