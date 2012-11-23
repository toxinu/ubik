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
    - with a configuration file          -> package_16
    - with a configuration file          -> package_17
    - with a configuration file          -> package_18
"""

class TestPackage_16_17_18(unittest.TestCase):

    def setUp(self):
        self.db = api.db
        self.package_16 = self.db.packages['package_16']
        self.package_17 = self.db.packages['package_17']
        self.package_18 = self.db.packages['package_18']

    def test_100_install_package(self):
        self.db.sync()
        installer = Installer()
        installer.resolve(self.package_16)
        installer.feed(installer.get_resolved())
        installer.resolve(self.package_17)
        installer.feed(installer.get_resolved())
        installer.resolve(self.package_18)
        installer.feed(installer.get_resolved())
        self.assertEqual(len(installer.packages), 3)

        installer.download()
        installer.install()
        self.assertTrue(self.db.get('package_16'))
        self.assertTrue(self.db.get('package_17'))
        self.assertTrue(self.db.get('package_18'))
        self.assertEqual(self.db.count_installed(), 4)

    def test_101_bin_package(self):
        p = Popen('package_16', shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        self.assertEqual(p.stdout.read(), 'Im package_16\n')
        p = Popen('package_17', shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        self.assertEqual(p.stdout.read(), 'Im package_17\n')
        p = Popen('package_18', shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        self.assertEqual(p.stdout.read(), 'Im package_18\n')

    def test_102_conf_package(self):
        self.assertTrue(os.path.exists('%s/etc/package_16.conf' % api.conf.get('settings', 'packages')))
        self.assertTrue(os.path.exists('%s/etc/package_17.conf' % api.conf.get('settings', 'packages')))
        self.assertTrue(os.path.exists('%s/etc/package_18.conf' % api.conf.get('settings', 'packages')))

if __name__ == '__main__':
    unittest.main()
