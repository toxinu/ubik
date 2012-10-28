#!/usr/bin/env python
import os
from flask import Flask

#######
# App #
#######
app = Flask(__name__)

app.secret_key = os.urandom(24)
app.debug = True

from ubik.web import views