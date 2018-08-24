#! /usr/bin/env python
# -*- coding: utf-8 -*-
# using Python's bundled WSGI server

from wsgiref.simple_server import make_server
import subprocess
from subprocess import Popen, PIPE
from dateutil.tz import *
import datetime
import logging
import os
import sys
import shlex
from tempfile import mkstemp
from shutil import move
from jinja2 import Environment, FileSystemLoader

# Create the jinja2 environment.
j2_env = Environment(loader=FileSystemLoader('/opt/iiab/captive-portal'),trim_blocks=True)

EXPIRE_SECONDS = 60 * 60 * 8

# Get the IIAB variables
sys.path.append('/etc/iiab/')
from iiab_env import get_iiab_env
doc_root = get_iiab_env("WWWROOT")
iptables_trap_enabled = get_iiab_env("IPTABLES_TRAP_ENABLED")

# set up some logging
logging.basicConfig(filename='/var/log/apache2/portal.log',format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M',level=logging.DEBUG)
if len(sys.argv) > 1 and sys.argv[1] == '-d':
    CATCH = True
    LIST = False
    PORT=80
elif len(sys.argv) > 1 and sys.argv[1] == '-l':
    LIST = True
    CATCH = False
    PORT=80
else:
    CATCH = False
    LIST = False
    PORT=9090

MAC_SUCCESS=False
ANDROID_SUCCESS=True

# what language are we speaking?
lang = os.environ['LANG'][0:2]
logging.debug('speaking: %s'%lang)

def tstamp(dtime):
    '''return a UNIX style seconds since 1970 for datetime input'''
    epoch = datetime.datetime(1970, 1, 1,tzinfo=tzutc())
    newdtime = dtime.astimezone(tzutc())
    since_epoch_delta = newdtime - epoch
    return since_epoch_delta.total_seconds()

def update_user(ip, mac, ts, ymd):
    fh, target_file_path = mkstemp()
    source_file_path = "/opt/iiab/captive-portal/users"
    if os.path.isfile(source_file_path):
        with open(target_file_path, 'w') as target_file:
            with open(source_file_path, 'r') as source_file:
                for line in source_file:
                    if line == '': continue
                    if ip in line:
                        target_file.write("%s %s %8.0d %s\n" % (ip,mac,ts,ymd,))
                    else:
                        target_file.write(line)
                os.remove(source_file_path)
                move(target_file_path, source_file_path)
    else:
        with open(source_file_path, 'w') as target_file:
          target_file.write("%s %s %8.0d %s\n" % (ip,mac,ts,ymd,))
        
def microsoft(environ,start_response):
    #logging.debug("sending microsoft response")
    en_txt={ 'message':"Click on the button to go to the IIAB home page",\
            'btn1':"GO TO IIAB HOME PAGE",'doc_root':get_iiab_env("WWWROOT")}
    es_txt={ 'message':"Haga clic en el botón para ir a la página de inicio de IIAB",\
            'btn1':"IIAB",'doc_root':get_iiab_env("WWWROOT")}
    if lang == "en":
        txt = en_txt
    elif lang == "es":
        txt = es_txt
    response_body = str(j2_env.get_template("simple").render(**txt))
    status = '200 OK'
    response_headers = [('Content-type','text/html'),
            ('Content-Length',str(len(response_body)))]
    start_response(status, response_headers)
    return [response_body]

def android(environ, start_response):
    global ANDROID_SUCCESS
    if ANDROID_SUCCESS:
        response_body = "hello"
        status = '302 Moved Temporarily'
        #ANDROID_SUCCESS = False
        response_headers = [('Location','android_splash')]
        start_response(status, response_headers)
        return [response_body]

def android_splash(environ, start_response):
    en_txt={ 'message':"Click on the button to go to the IIAB home page",\
            'btn1':"GO TO IIAB HOME PAGE", 'btn2':'Go to CHROME browser',\
            'doc_root':get_iiab_env("WWWROOT") }
    es_txt={ 'message':"Haga clic en el botón para ir a la página de inicio de IIAB",\
            'btn1':"IIAB",'doc_root':get_iiab_env("WWWROOT")}
    if lang == "en":
        txt = en_txt
    elif lang == "es":
        txt = es_txt
    response_body = str(j2_env.get_template("simple").render(**txt))
    status = '200 OK'
    response_headers = [('Content-type','text/html'),
            ('Content-Length',str(len(response_body)))]
    start_response(status, response_headers)
    return [response_body]

def macintosh(environ, start_response):
    global MAC_SUCCESS
    en_txt={ 'message':"Click on the button to go to the IIAB home page",\
            'btn1':"GO TO IIAB HOME PAGE",\
            'success_token': 'SUCCESS', 'doc_root':get_iiab_env("WWWROOT")}
    es_txt={ 'message':"Haga clic en el botón para ir a la página de inicio de IIAB",\
            'btn1':"IIAB",'doc_root':get_iiab_env("WWWROOT")}
    if lang == "en":
        txt = en_txt
    elif lang == "es":
        txt = es_txt
    if MAC_SUCCESS:
        response_body = str(j2_env.get_template("simple").render(**txt))
        status = '200 OK'
        response_headers = [('Content-type','text/html'),
                ('Content-Length',str(len(response_body)))]
        status = '200 Success'
        MAC_SUCCESS = False
        start_response(status, response_headers)
        return [response_body]
    else:
        response_body = "<script>window.location.reload(true)</script>"
        status = '302 Moved Temporarily'
        MAC_SUCCESS = True
        response_headers = [('content','text/html')]
        start_response(status, response_headers)
        return [response_body]

# =============  Return html pages  ============================
def banner(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'image/png')]
    start_response(status, headers)
    image = open("%s/iiab-menu/menu-files/images/iiab_banner6.png"%doc_root, "rb").read() 
    return [image]

def bootstrap(environ, start_response):
    logging.debug("in bootstrap")
    status = '200 OK'
    headers = [('Content-type', 'text/javascript')]
    start_response(status, headers)
    boot = open("%s/common/js/bootstrap.min.js"%doc_root, "rb").read() 
    return [boot]

def jquery(environ, start_response):
    logging.debug("in jquery")
    status = '200 OK'
    headers = [('Content-type', 'text/javascript')]
    start_response(status, headers)
    boot = open("%s/common/js/jquery.min.js"%doc_root, "rb").read() 
    return [boot]

def bootstrap_css(environ, start_response):
    logging.debug("in bootstrap_css")
    status = '200 OK'
    headers = [('Content-type', 'text/css')]
    start_response(status, headers)
    boot = open("%s/common/css/bootstrap.min.css"%doc_root, "rb").read() 
    return [boot]

# ================== Start serving the wsgi application  =================
def application (environ, start_response):
    global CATCH
    global LIST
    global EXPIRE_SECONDS

    # Sorting and stringifying the environment key, value pairs
    if LIST:
        data = [
        '%s: %s\n' % (key, value) for key, value in sorted(environ.items()) ]
        logging.debug(data)
    
    if CATCH:
        logging.debug("Checking for url %s. USER_AGENT:%s"%(environ['HTTP_HOST'],\
               environ['HTTP_USER_AGENT'],))
        if environ['HTTP_HOST'] == '/box.lan':
            return                            
        found = False
        if os.path.exists("/opt/iiab/captive-portal/checkurls"):
           with open("/opt/iiab/captive-portal/checkurls","r") as checkers:
              for line in checkers:
                 if environ['HTTP_HOST'] in line:
                    found = True
                    break
        if not found:
           with open("/opt/iiab/captive-portal/checkurls","a") as checkers:
               outstr ="%s\n" %  (environ['HTTP_HOST']) 
               checkers.write(outstr)
        data = [
        '%s: %s\n' % (key, value) for key, value in sorted(environ.items()) ]
        logging.debug(data)
    
    else:
        ip = environ['HTTP_X_FORWARDED_FOR'].strip()
        cmd="arp -an %s|gawk \'{print $4}\'" % ip
        mac = subprocess.check_output(cmd, shell=True)
        data = []
        data.append("host: %s\n"%environ['HTTP_HOST'])
        data.append("path: %s\n"%environ['PATH_INFO'])
        data.append("query: %s\n"%environ['QUERY_STRING'])
        data.append("ip: %s\n"%environ['HTTP_X_FORWARDED_FOR'])
        agent = environ['HTTP_USER_AGENT']
        data.append("agent: %s\n"%agent)
        logging.debug(data)
        found = False
        ts=tstamp(datetime.datetime.now(tzutc()))
        if os.path.exists("/opt/iiab/captive-portal/users"):
           with open("/opt/iiab/captive-portal/users","r") as users:
              for line in users:
                 #print line, ip
                 if ip in line:
                    session_start = int(line.split(' ')[2])
                    if ts - session_start < EXPIRE_SECONDS:
                        found = True
                        break
        if not found:
           ymd=datetime.datetime.today().strftime("%y%m%d-%H%M")
           update_user(ip,mac.strip(),ts,ymd)

        # do more specific stuff first
        if  environ['PATH_INFO'] == "/iiab_banner6.png":
            return banner(environ, start_response) 

        if  environ['PATH_INFO'] == "/bootstrap.min.js":
            return bootstrap(environ, start_response) 

        if  environ['PATH_INFO'] == "/bootstrap.min.css":
            return bootstrap_css(environ, start_response) 

        if  environ['PATH_INFO'] == "/jquery.min.js":
            return jquery(environ, start_response) 

        # mac
        if environ['HTTP_HOST'] == "captive.apple.com" or\
           environ['HTTP_HOST'] == "appleiphonecell.com" or\
           environ['HTTP_HOST'] == "detectportal.firefox.com" or\
           environ['HTTP_HOST'] == "*.apple.com.edgekey.net" or\
           environ['HTTP_HOST'] == "gsp1.apple.com" or\
           environ['HTTP_HOST'] == "apple.com" or\
           environ['HTTP_HOST'] == "www.apple.com": 
           return macintosh(environ, start_response) 

        # android
        if  environ['PATH_INFO'] == "/android_splash":
            return android_splash(environ, start_response) 
        if environ['HTTP_HOST'] == "clients3.google.com" or\
           environ['HTTP_HOST'] == "mtalk.google.com" or\
           environ['HTTP_HOST'] == "alt7-mtalk.google.com" or\
           environ['HTTP_HOST'] == "alt6-mtalk.google.com" or\
           environ['HTTP_HOST'] == "connectivitycheck.android.com" or\
           environ['HTTP_HOST'] == "connectivitycheck.gstatic.com":
           return android(environ, start_response) 

        # microsoft
        if environ['HTTP_HOST'] == "ipv6.msftncsi.com" or\
           environ['HTTP_HOST'] == "ipv6.msftncsi.com.edgesuite.net" or\
           environ['HTTP_HOST'] == "www.msftncsi.com" or\
           environ['HTTP_HOST'] == "www.msftncsi.com.edgesuite.net" or\
           environ['HTTP_HOST'] == "www.msftconnecttest.com" or\
           environ['HTTP_HOST'] == "teredo.ipv6.microsoft.com" or\
           environ['HTTP_HOST'] == "teredo.ipv6.microsoft.com.nsatc.net": 
           return microsoft(environ, start_response) 

    response_body = "This worked"
    status = '302 Moved Temporarily'
    response_headers = [('Location','http://box.lan/home')]
    start_response(status, response_headers)

    return [response_body]

# Instantiate the server
httpd = make_server (
    "", # The host name
    PORT, # A port number where to wait for the request
    application # The application object name, in this case a function
)

# Wait for a single request, serve it and quit
#httpd.handle_request()
httpd.serve_forever()
#vim: tabstop=3 expandtab shiftwidth=3 softtabstop=3 background=dark

