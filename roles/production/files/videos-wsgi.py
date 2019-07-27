#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, abort
#from flask_mysqldb import MySQL
from jinja2 import Environment, FileSystemLoader
import json
import sqlite3
import sys

NEW_PATH = '/opt/iiab'
if not NEW_PATH in sys.path:
  sys.path += [NEW_PATH]
import production

# avoid ansible template language, but make clear what locates the code
VIDEOS_BASE = "/opt/iiab/producion"
TEMPLATE_DIR = VIDEOS_BASE + '/templates/'
VIDEOS_VENV = VIDEOS_BASE + "/venv"
VIDEOS_DATA_DIR = '/library/www/html/local_content'

# Create the jinja2 environment.
j2_env = Environment(loader=FileSystemLoader('/opt/iiab/production/templates'),trim_blocks=True)
#import pdb;pdb.set_trace()

# Create an interface to sqlite3 database
class Videos(object):
   def __init__(self, filename):
      self.conn = sqlite3.connect(filename)
      self.conn.row_factory = sqlite3.Row
      self.c = self.conn.cursor()

   def __del__(self):
      self.conn.commit()
      self.c.close()
      del self.conn

application = production.create_app()
"""
# Config MySQL
application.config['MYSQL_HOST'] = 'localhost'
application.config['MYSQL_USER'] = 'menus_user'
application.config['MYSQL_PASSWORD'] = 'g0adm1n'
application.config['MYSQL_DB'] = 'menus_db'
application.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(application)
"""

@application.route('/')
def one():
    rv = "hello world"
    return str(rv)


@application.route('/viewer')
def viewer():
    response_body = str(j2_env.get_template("index.html").render())
    return response_body
    
@application.route('/viewer.css')
def viewer_css():
    image = open("%s/assets/viewer.css"%VIDEOS_REPO_DIR, "rb").read() 
    return image
    
@application.route('/reader')
def reader():
   filename = request.args.get('name')   
   try:
      data = open("%s/%s"%(VIDEOS_DATA_DIR,filename),'r').read()
      return data
   except:
      return ''
   
@application.route('/writer')
def writer():
   filename = request.args.get('name')   
   try:
      data = open("%s/%s"%(VIDEOS_DATA_DIR,filename),'w').read()
      return data
   except:
      abort(404)
   
@application.route('/metadata')
def metadata():
   filename = request.args.get('name')   
   try:
      data = open("%s%s"%(VIDEOS_DATA_DIR,filename),'r').read()
      return data
   except:
      abort(404)

if __name__ == "__main__":
    application.run(host='0.0.0.0',port=9458)

#vim: tabstop=3 expandtab shiftwidth=3 softtabstop=3 background=dark
