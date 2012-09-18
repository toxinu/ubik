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
		self.assertTrue(self.db.packages.get('test_deps'))
		self.assertTrue(self.db.get('test_deps'))

if __name__ == '__main__':
	unittest.main()
