# coding: utf-8
import os
import hashlib
import subprocess
import tarfile
import shutil
import bz2

from ubik.core import conf
from ubik.logger import logger
from ubik.exceptions import CmdError

import ubik.package

def cached(package):
	if not isinstance(package, ubik.package.Package):
		raise Exception('Need to be a Package object')

	if not os.path.exists('%s/%s.tar' % (conf.get('settings', 'cache'), package.name)):
		return False

	return True

def checkmd5(package):
	if not isinstance(package, ubik.package.Package):
		raise Exception('Need to be a Package object')

	package_path = '%s/%s.tar' % (conf.get('settings', 'cache'), package.name)
	
	fh = open(package_path, 'rb')
	m = hashlib.md5()
	while True:
		data = fh.read(8192)
		if not data:
			break
		m.update(data)

	if package.md5 != m.hexdigest():
		return False
	return True

def launch_cmd(cmd):
	if conf.get('packages', 'control_methods'):
		cmd = ['bash', '-c', '. %s; %s' % (conf.get('packages', 'control_methods'), cmd)]
	else:
		cmd = ['bash', '-c', cmd]
	popen = subprocess.Popen(cmd)
	popen.wait()
	if popen.returncode >= 1:
		raise CmdError('Cmd failed (%s)' % cmd)

def confirm(prompt=None, resp=False):
	if prompt is None:
		prompt = 'Confirm'

	if resp:
		prompt = '%s [%s|%s]: ' % (prompt, 'n', 'Y')
	else:
		prompt = '%s [%s|%s]: ' % (prompt, 'y', 'N')
		
	while True:
		ans = raw_input(prompt)
		if not ans:
			return resp
		if ans == 'y' or ans == 'Y':
			return True
		if ans == 'n' or ans == 'N':
			return False
		else:
			return False

def clean():
	files = os.listdir(conf.get('settings', 'cache'))
	for f in files:
		logger.debug(f)
		if not '.tar' in f and os.path.isdir(f):
			shutil.rmtree(f)

def unarchiver(package):
	src = "%s/%s.tar" % (conf.get('settings', 'cache'), package.name)
	dst = conf.get('settings', 'cache')

	# Open tarfile
	tar = tarfile.open(src)
	if tarfile.is_tarfile(src):
		tar.extractall(dst)
	else:
		raise Exception('Archive invalid (not a tarfile)')

def unpacker(package):
	archive = tarfile.open('%s/%s/files.bz2' % (conf.get('settings', 'cache'), package.name), 'r:bz2', ignore_zeros=True)
	root_content = '%s/%s/content' % (conf.get('settings', 'cache'), package.name)
	if os.path.exists(root_content):
		shutil.rmtree(root_content)
	os.makedirs(root_content)
	archive.extractall(root_content)

	for (path, dirs, files) in os.walk(root_content):
		for _dir in dirs:
			src = '%s/%s' % (path, _dir)
			dst = '%s' % src.replace(root_content, conf.get('settings', 'packages'))
			if not os.path.exists(dst):
				os.makedirs(dst)
		for _file in files:
			src = '%s/%s' % (path, _file)
			dst = '%s' % src.replace(root_content, conf.get('settings', 'packages'))
			# If safe_conf
			if conf.get('packages', 'safe_conf') == 'True':
				# Is etc
				if path.replace(root_content, '')[1:].split('/')[0] == 'etc':
					# Is file in etc
					if os.path.isfile('%s/%s' % (path, _file)):
						# If file already exist
						if os.path.exists(dst):
							logger.debug('Config file conflict: %s/%s' % (path, _file))
							dst += '.new'
			logger.debug(" :: %s - %s" % (src, dst))
			shutil.move(src, dst)

	shutil.rmtree(root_content)
	archive.close()
