# coding: utf-8
import os
import requests

from requests.auth import HTTPProxyAuth

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

		auth = None
		if conf.has_option('proxy', 'http_auth') and conf.get('proxy', 'http_auth'):
			auth = conf.get('proxy', 'http_auth')

		if conf.has_option('proxy', 'https_auth') and conf.get('proxy', 'https_auth'):
			auth = conf.get('proxy', 'https_auth')

		if auth and len(auth.split(':')) == 2:
			proxies['login'] = auth.split(':')[0]
			proxies['pass']  = auth.split(':')[1]

		if conf.has_option('proxy', 'http_proxy') and conf.get('proxy', 'http_proxy'):
			proxies['http'] = 'http://%s' % (
				conf.get('proxy', 'http_proxy')
			)

		if conf.has_option('proxy', 'https_proxy') and conf.get('proxy', 'https_proxy'):
			proxies['https_proxy'] = 'http://%s' % (
				conf.get('proxy', 'https_proxy')
			)
	
	if os.environ.get('http_proxy'):
		proxies['http'] = os.environ['http_proxy']

	if os.environ.get('https_proxy'):
		proxies['https'] = os.environ['https_proxy']

	proxies['auth'] = None
	if auth:
		proxies['auth'] = HTTPProxyAuth(proxies['login'], proxies['pass'])

	return proxies

def get_timeout():
	timeout = 10
	if conf.has_option('proxy', 'timeout'):
		if conf.get('proxy', 'timeout'):
			timeout = conf.get('proxy', 'timeout')
	return float(timeout)

def get_database(file_path=None):
	url = '%s/%s/%s/Packages.json' % (
		conf.get('repo', 'url'),
		conf.get('repo', 'base'),
		conf.get('repo', 'branch'))
	proxies = get_proxies()
	timeout = get_timeout()

	r = requests.get(url, timeout=timeout, proxies=proxies, auth=proxies['auth'])
	r.raise_for_status()

	if file_path:
		if os.path.exists(file_path):
			os.remove(file_path)
		json.dump(r.json, open(file_path, 'w'))
		return r
	else:
		return r.json()

def get_package(package):
	if not isinstance(package, ubik.package.Package):
		raise Exception('Must be a Package object')

	url = '%s/%s/%s/%s/%s/%s/%s.tar' % (
		conf.get('repo', 'url'),
		conf.get('repo', 'base'),
		conf.get('repo', 'branch'),
		package.arch,
		package.dist,
		package.vers,
		package.name
		)
	proxies = get_proxies()
	timeout = get_timeout()

	r = requests.get(url, timeout=timeout, proxies=proxies, stream=False, auth=proxies['auth'])
	r.raise_for_status()

	size = int(r.headers['Content-Length'].strip())
	bytes = 0

	max_len = 25
	end_mark = '. '
	if len(package.name) > max_len:
		_diff = max_len - len(end_mark)
		package_name = package.name[_diff] + end_mark
	else:
		package_name = package.name + (max_len - len(package.name)) * ' '

	widgets = [package_name, Bar(marker="=", left="[", right=" "),
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
