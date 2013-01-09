# coding: utf-8
import os
import sys
import platform
import re
import isit

if isit.py3:
  from configparser import SafeConfigParser
else:
  from ConfigParser import SafeConfigParser

def get_conf(conf_path):
    """
    Read the configuration file and return it
    """
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
            vers = isit.osx_version
        elif isit.linux:
            if isit.debian:
                dist = "debian"
                if isit.debian_version:
                    vers = isit.debian_version.split('.')[0]

            elif isit.ubuntu:
                dist = "ubuntu"
                if isit.ubuntu_version:
                    vers = isit.ubuntu_version

            elif isit.centos:
                dist = "centos"
                if isit.centos_version:
                    vers = isit.centos_version.split('.')[0]

            elif isit.redhat:
                dist = "redhat"
                if isit.redhat_version:
                    vers = isit.redhat_version.split('.')[0]

            elif isit.archlinux:
                dist = "archlinux"
                if isit.archlinux_version:
                    vers = isit.archlinux_version

        parser.set('system', 'dist', dist)
        parser.set('system', 'vers', vers)
    else:
        parser.set('system', 'dist', parser.get('system', 'dist').lower())

    if parser.has_option('system', 'vers'):
        parser.set('system', 'vers', parser.get('system', 'vers').lower())

    return parser
