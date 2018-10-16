# -*- coding: utf8 -*-

import os
import json
from flask import Flask, request, render_template

from bp_api_course import pages_api_course

DEBUG = True
HOST = '0.0.0.0'
PORT = 50613
SECRET_KEY = 'development key for MOOCbd 618'

app = Flask(__name__)
app.config.from_object(__name__)

# Register API
app.register_blueprint(pages_api_course)

# The only page for this demo
@app.route('/')
def index():
    return render_template('index.html')


if __name__=='__main__':
    app.run(host=HOST, port=PORT)
