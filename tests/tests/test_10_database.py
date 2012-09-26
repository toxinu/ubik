#!/usr/bin/env python
# coding: utf-8

import env
import unittest

import ubik.core as api

class TestDatabase(unittest.TestCase):

	def setUp(self):
		self.db = api.db

	def test_01_sync(self):
		self.db.sync()

	def test_02_misc(self):
		self.assertEqual(self.db.count_installed(), 0)
		self.assertEqual(self.db.get_installed(), [])

	def test_03_find_package(self):
		pkg_a = ['package_01', 'package_02', 'package_03', 'package_04',
				'package_06', 'package_10', 'package_11', 'package_12', 'package_13']
		self.assertTrue(self.db.get(pkg_a))
		for package in pkg_a:
			self.assertTrue(self.db.packages.get(package))

		pkg_b = ['package_07', 'package_08', 'package_09']
		self.assertFalse(self.db.get(pkg_b))
		for package in pkg_b:
			self.assertFalse(self.db.packages.get(package))

		self.assertEqual(len(self.db.get('package_*')), 12)
		self.assertEqual(len(self.db.get('package_0*')), 6)
		self.assertEqual(len(self.db.get('package_0.$')), 6)
		self.assertEqual(len(self.db.get('(.*)age')), 0)
		self.assertEqual(len(self.db.get('(.*)age*')), 12)

if __name__ == '__main__':
	unittest.main()
