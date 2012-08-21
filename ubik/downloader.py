# coding: utf-8
import os
import requests

from progressbar import ProgressBar
from progressbar import Bar
from progressbar import FileTransferSpeed
from progressbar import Percentage

from ubik.core import conf
from ubik.core import logger

import ubik.package

def get_proxies():
	proxies = {}
	if conf.has_section('proxy'):
		if conf.has_option('proxy', 'http_proxy'):
			if conf.get('proxy', 'http_proxy'):
				if conf.has_option('proxy', 'http_auth'):
					if conf.get('proxy', 'http_auth'): 
						proxies['http_proxy'] = '%s@%s' % (
						conf.get('proxy', 'http_auth'),
						conf.get('proxy', 'http_proxy'))
				else:			
					proxies['http_proxy'] = '%s' % (
					conf.get('proxy', 'http_proxy'))
	if conf.has_option('proxy', 'https_proxy'):
		if conf.get('proxy', 'https_proxy'):
			if conf.has_option('proxy', 'https_auth'):
				if conf.get('proxy', 'https_auth'): 
					proxies['https_proxy'] = '%s@%s' % (
					conf.get('proxy', 'https_auth'),
					conf.get('proxy', 'https_proxy'))
			else:			
				proxies['https_proxy'] = '%s' % (
				conf.get('proxy', 'https_proxy'))

def get_timeout():
	timeout = 10
	if conf.has_option('proxy', 'timeout'):
		if conf.get('proxy', 'timeout'):
			timeout = conf.get('proxy', 'timeout')
	return float(timeout)

def get_database(file_path=None):
	url = '%s/%s/%s/Packages.list' % (
		conf.get('repo', 'url'),
		conf.get('repo', 'base'),
		conf.get('repo', 'vers'))
	proxies = get_proxies()
	timeout = get_timeout()

	r = requests.get(url, timeout=timeout, proxies=proxies)
	r.raise_for_status()

	if file_path:
		if os.path.exists(file_path):
			os.remove(file_path)
		f = open(file_path, 'w')		
		f.write(r.text)
		return r
	else:
		return r.text.split('\n')[:-1]

def get_package(package):
	if not isinstance(package, ubik.package.Package):
		raise Exception('Must be a Package object')

	url = '%s/%s/%s/%s/%s/%s/%s.tar' % (
		conf.get('repo', 'url'),
		conf.get('repo', 'base'),
		conf.get('repo', 'vers'),
		package.arch,
		package.dist,
		package.vers,
		package.name
		)
	proxies = get_proxies()
	timeout = get_timeout()

	r = requests.get(url, timeout=timeout, proxies=proxies, pre_fetch=False)
	r.raise_for_status()	

	size = int(r.headers['Content-Length'].strip())
	bytes = 0
	widgets = [package.name, ":", Bar(marker="|", left="[", right=" "),
		Percentage(), " ",  FileTransferSpeed(), "] ",
		"{0}MB".format(str(round(size / 1024 / 1024, 2))[:4])]
	pbar = ProgressBar(widgets=widgets, maxval=size).start()
	with open('%s/%s.tar' % (conf.get('settings', 'cache'), package.name), 'w') as f:
		for buf in r.iter_content(1024):
			if buf:
				f.write(buf)
				bytes += len(buf)
				pbar.update(bytes)
	pbar.finish()
