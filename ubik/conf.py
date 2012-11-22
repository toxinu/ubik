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
	parser.set('paths', 'web_data', '%s/ubik-web.dat' % parser.get('settings', 'var_path'))

	# Detect system info
	if not parser.has_option('system', 'arch'):
		if isit.bit32:
			parser.set('system', 'arch', 'i386')
		elif isit.bit64:
			parser.set('system', 'arch', 'x86_64')
	else:
		parser.set('system', 'arch', parser.get('system', 'arch').lower())

	if not parser.has_option('system', 'dist'):
		dist = 'unknown'
		vers = 'unknown'

		if isit.osx:
			dist = 'osx'
			vers = isit.osx_vers
		elif isit.linux:
			if isit.debian:
				dist = "debian"
				if isit.debian_vers:
					vers = isit.debian_vers.split('.')[0]

			elif isit.ubuntu:
				dist = "ubuntu"
				if isit.ubuntu_vers:
					vers = isit.ubuntu_vers

			elif isit.centos:
				dist = "centos"
				if isit.centos_vers:
					vers = isit.centos_vers.split('.')[0]

			elif isit.redhat:
				dist = "redhat"
				if isit.redhat_vers:
					vers = isit.redhat_vers.split('.')[0]

			elif isit.archlinux:
				dist = "archlinux"
				if isit.archlinux_vers:
					vers = isit.archlinux_vers

		parser.set('system', 'dist', dist)
		parser.set('system', 'vers', vers)
	else:
		parser.set('system', 'dist', parser.get('system', 'dist').lower())

	if parser.has_option('system', 'vers'):
		parser.set('system', 'vers', parser.get('system', 'vers').lower())

	return parser
