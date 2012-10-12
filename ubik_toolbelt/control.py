# coding: utf-8

from ubik_toolbelt.logger import stream_logger

class Control(object):
    def __init__(self):
        self.name = ''
        self.version = ''
        self.release = ''
        self.requires = []
        self.arch = ''
        self.dist = ''
        self.vers = ''
        self.description = ''

    def build(self):
        stream_logger.info('Building...')

    def package(self):
        stream_logger.info('Packaging...')

    def pre_install(self):
        pass

    def post_install(self):
        pass

    def pre_upgrade(self):
        pass

    def post_upgrade(self):
        pass

    def pre_remove(self):
        pass

    def post_remove(self):
        pass
