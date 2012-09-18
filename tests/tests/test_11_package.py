#!/usr/bin/env python
# coding: utf-8
import os

import env
import unittest

import ubik.core as api

from ubik.installer import Installer
from ubik.remover import Remover

from subprocess import Popen, PIPE, STDOUT

class TestPackage(unittest.TestCase):

	def setUp(self):
		self.db = api.db
		self.package = self.db.packages['test_deps']
		self.package = self.db.get('test_deps')[0]

	def test_01_name(self):
		self.assertEqual(str(self.package.name), 'test_deps')

	def test_02_requires(self):
		self.assertEqual(self.package.requires, ['hello_world'])

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

	def test_100_install_test_deps(self):
		# Install 'test_deps' package with it's 'hello_world' require
		self.db.sync()
		installer = Installer()
		installer.resolv(self.package)
		installer.feed(installer.resolved)
		self.assertEqual(len(installer.packages), 2)

		installer.download()
		installer.install()
		self.assertEqual(self.db.count_installed(), 2)

	def test_101_install_test_deps(self):
		# Test the hello_world which is a 'test_deps' require
		p = Popen('hello_world', shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
		self.assertEqual(p.stdout.read(), 'Hello world!\n')

	def test_200_remove_tests_deps(self):
		# Remove 'test_deps', 'hello_world' stay here
		self.db.sync()
		remover = Remover()
		remover.feed(self.package)
		self.assertEqual(len(remover.packages), 1)
		self.assertEqual(remover.packages[0].name, 'test_deps')

		remover.remove()
		self.assertEqual(self.db.count_installed(), 1)

	def test_201_remove_hello_world(self):
		# Remove 'hello_world'
		self.db.sync()
		remover = Remover()
		remover.feed(self.db.packages['hello_world'])
		self.assertEqual(len(remover.packages), 1)
		self.assertEqual(remover.packages[0].name, 'hello_world')

		remover.remove()
		self.assertEqual(self.db.count_installed(), 0)

	def test_202_remove_file_removed(self):
		# Check if 'bin/hello_world' file has been removed
		path = "%s/bin/hello_world" % api.conf.get('settings', 'packages')
		self.assertFalse(os.path.exists(path))

if __name__ == '__main__':
	unittest.main()
