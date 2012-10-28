import json
import platform
import ubik

from flask import render_template
from flask import jsonify
from flask import g
from flask import redirect
from flask import abort
from flask import url_for

from ubik.web import app
from ubik.status import status
from ubik.database import Database
from ubik.installer import Installer
from ubik.reinstaller import Reinstaller
from ubik.remover import Remover
from ubik.upgrader import Upgrader

import ubik.core as api

def install_package(package):
    g.db.sync()
    installer = Installer()
    package = g.db.get(package)[0]
    installer.resolv(package)
    installer.feed(installer.resolved)
    installer.download()
    installer.install()

def reinstall_package(package):
    g.db.sync()
    reinstaller = Reinstaller()
    package = g.db.get(package)[0]
    reinstaller.resolv(package)
    reinstaller.feed(reinstaller.resolved)
    reinstaller.download()
    reinstaller.reinstall()

def upgrade_package(package):
    g.db.sync()
    upgrader = Upgrader()
    package = g.db.get(package)[0]
    upgrader.feed(package)
    upgrader.download()
    upgrader.upgrade()

def remove_package(package):
    remover = Remover()
    remover.feed(package)
    remover.remove()

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
    #installed = g.db.get_installed()
    updates = sorted(g.db.get_upgrades(), key=lambda k: k.name)
    last_update = json.load(open(api.conf.get('paths', 'infos')))['last_update']

    return render_template('index.html',
        all=_all,
        installed=installed,
        updates=updates,
        last_update=last_update,
        status=status)

@app.route('/do/<action>/<package>')
def do(action, package):
    if action == 'install':
        install_package(package)
    elif action == 'reinstall':
        reinstall_package(package)
    elif action == 'remove':
        remove_package(package)
    elif action == 'upgrade':
        upgrade_package(package)
    else:
        return abort(404)
    return redirect(url_for('index'))

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

@app.route('/sync')
def sync():
    try:
        api.db.sync()
        last_update = json.load(open(api.conf.get('paths', 'infos')))['last_update']
        return jsonify({'success': True, 'last': last_update})
    except Exception as err:
        last_update = json.load(open(api.conf.get('paths', 'infos')))['last_update']
        return jsonify({'success': False, 'message': str(err), 'last': last_update})
