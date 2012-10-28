#!/usr/bin/env python
import os
import json 

from flask import Flask

import ubik.core as api

#######
# App #
#######
app = Flask(__name__)

app.secret_key = os.urandom(24)
app.debug = True

lock = []
sync_state = {  'success': None,
                'output': 'Never synced here',
                'last': json.load(open(api.conf.get('paths', 'infos')))['last_update']}

from ubik.web.logs import logger
from ubik.web.websocket import handle_websocket

def ubik_web(environ, start_response):  
    path = environ["PATH_INFO"]  
    if path == "/":  
        return app(environ, start_response)  
    elif path == "/websocket":  
        handle_websocket(environ["wsgi.websocket"])   
    else:  
        return app(environ, start_response)  

from ubik.web import views