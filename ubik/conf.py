# coding: utf-8
import os
import sys
import struct
import platform
import re
from ConfigParser import SafeConfigParser

def get_conf(conf_path):
	conf_path = conf_path
	parser = SafeConfigParser()
	parser.read(conf_path)
	parser.add_section('paths')

	# Default
	parser.set('packages', 'safe_conf', 'True')

	# Create paths
	parser.set('paths', 'local_db', '%s/packages.db' % parser.get('settings', 'var_path'))
	parser.set('paths', 'lock', '%s/db.lock' % parser.get('settings', 'var_path'))
	parser.set('paths', 'infos', '%s/infos' % parser.get('settings', 'var_path'))

	# Detect system info
	_void_ptr_size = struct.calcsize('P')
	if not parser.has_option('system', 'arch'):
		bit32 = _void_ptr_size * 8 == 32
		bit64 = _void_ptr_size * 8 == 64
		if bit32:
			parser.set('system', 'arch', 'i386')
		elif bit64:
			parser.set('system', 'arch', 'x86_64')

	if not parser.has_option('system', 'dist'):
		if 'darwin' in str(sys.platform).lower():
			dist = 'DARWIN'
			vers = platform.mac_ver()[0]
		else:
			dist = platform.dist()[0].upper()
			vers = 'n/a'
			if dist == 'DEBIAN':
				vers = platform.dist()[1].split('.')[0]
			elif dist == 'UBUNTU':
				vers = platform.dist()[1].replace('.', '')
			elif dist == 'CENTOS':
				vers = platform.dist()[1].split('.')[0]
			elif dist == 'REDHAT':
				vers = platform.dist()[1].split('.')[0]

		parser.set('system', 'dist', dist)
		parser.set('system', 'vers', vers)

	return parser
