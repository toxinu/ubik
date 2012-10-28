#!/usr/bin/env python
import os
from flask import Flask

###########
# Modules #
###########
# from flask.ext.login import LoginManager
# from flask_debugtoolbar import DebugToolbarExtension

#######
# App #
#######
app = Flask(__name__)

app.secret_key = os.urandom(24)
app.debug = True

# toolbar = DebugToolbarExtension(app)
# login_manager = LoginManager()

from ubik.web import views