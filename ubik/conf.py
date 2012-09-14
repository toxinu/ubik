# coding: utf-8
import os
import sys
import platform
import re
import isit
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
	if not parser.has_option('system', 'arch'):
		if isit.bit32:
			parser.set('system', 'arch', 'i386')
		elif isit.bit64:
			parser.set('system', 'arch', 'x86_64')

	dist = 'unknown'
	vers = 'unknown'
	if not parser.has_option('system', 'dist'):
		if isit.osx:
			dist = 'osx'
			vers = isit.osx_vers
		elif isit.linux:
			if isit.debian:
				dist = "debian"
				vers = isit.debian_vers
			elif isit.ubuntu:
				dist = "ubuntu"
				vers = isit.ubuntu_vers
			elif isit.centos:
				dist = "centos"
				vers = isit.centos_vers
			elif isit.redhat:
				dist = "redhat"
				vers = isit.redhat_vers
			elif isit.archlinux:
				dist = "archlinux"
				vers = isit.archlinux_vers

		parser.set('system', 'dist', dist)
		parser.set('system', 'vers', vers)

	return parser
