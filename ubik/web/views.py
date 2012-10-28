# coding: utf-8
import json
import platform
import ubik

import ubik.core as api

from flask import render_template
from flask import jsonify
from flask import g
from flask import redirect
from flask import abort
from flask import url_for
from flask import request

from ubik.status import status
from ubik.database import Database

from ubik.web import app
from ubik.web import lock
from ubik.web import logger

from helpers import log

@app.before_request
def before_request():
    g.api = api
    g.ubik_version = ubik.__version__
    g.system = platform.node()
    g.db = Database(json.load(open(api.conf.get('paths', 'local_db'))))

@app.route('/')
def index():
    installed = sorted(g.db.get_installed(), key=lambda k: k.name)
    _all = sorted(g.db.packages.values(), key=lambda k: k.name)
    updates = sorted(g.db.get_upgrades(), key=lambda k: k.name)
    last_update = json.load(open(api.conf.get('paths', 'infos')))['last_update']

    return render_template('index.html',
        all=_all,
        installed=installed,
        updates=updates,
        last_update=last_update,
        status=status)

@app.route('/info')
def info():
    infos = {}
    for section in api.conf.sections():
        infos[section] = {}
        for key, value in api.conf.items(section):
            infos[section][key] = value
    return render_template('info.html', infos=infos)

@app.route('/stats')
def stats():
    _stats = {  'Packages installed': g.db.count_installed(),
                'Updates available': g.db.count_upgrades(),
                'Total packages': g.db.count_packages()}
    return render_template('stats.html', stats=_stats)
