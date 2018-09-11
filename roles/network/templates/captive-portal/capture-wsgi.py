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
import sqlite3
import re

# Notes on timeout strategy
# every client timestamp is recorded
# When splash page is clicked, return 204 timeout starts (may be different for different OSs
# captive portal redirect is triggered after inactivity timeout

# Create the jinja2 environment.
CAPTIVE_PORTAL_BASE = "/opt/iiab/captive-portal"
j2_env = Environment(loader=FileSystemLoader(CAPTIVE_PORTAL_BASE),trim_blocks=True)

# Define time outs
INACTIVITY_TO = 10
PORTAL_TO = 30


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

# Use a sqlite database to store per client information
user_db = os.path.join(CAPTIVE_PORTAL_BASE,"users.sqlite")
conn = sqlite3.connect(user_db)
c = conn.cursor()
c.row_factory = sqlite3.Row
c.execute( """create table IF NOT EXISTS users 
            (ip text PRIMARY KEY, mac text, 
            lasttimestamp integer, send204after integer,
            os text, os_version text,
            ymd text)""")

MAC_SUCCESS=False
ANDROID_TRIGGER=False

# what language are we speaking?
lang = os.environ['LANG'][0:2]
logging.debug('speaking: %s'%lang)

def tstamp(dtime):
    '''return a UNIX style seconds since 1970 for datetime input'''
    epoch = datetime.datetime(1970, 1, 1,tzinfo=tzutc())
    newdtime = dtime.astimezone(tzutc())
    since_epoch_delta = newdtime - epoch
    return since_epoch_delta.total_seconds()

# datab"ase operations
def update_user(ip, mac, lasttimestamp, send204after, system, system_version, ymd):
    #print("in update_user.")
    sql = "INSERT OR REPLACE INTO users (ip,mac,lasttimestamp,os,os_version,ymd) VALUES (?,?,?,?,?,?)" 
    c.execute(sql,(ip, mac,lasttimestamp,  system, system_version, ymd ))
    conn.commit()

def platform_info(ip):
    sql = "select * FROM users WHERE ip = ?"
    c.execute(sql,(ip,))
    row = c.fetchone()
    return (row['os'],row['os_version'])
        
def timeout_info(ip):
    sql = "select * FROM users WHERE ip = ?"
    c.execute(sql,(ip,))
    row = c.fetchone()
    return (row['lasttimestamp'],row['send204after'])
        
def inactive(ip):
    ts=tstamp(datetime.datetime.now(tzutc()))
    last_ts, cp_done = timeout_info(ip) 
    print("last_ts:%s current: %s"%(last_ts,ts,))
    if not last_ts:
        return True
    if ts - int(last_ts) > INACTIVITY_TO:
        print "inactive"
        return True
    else:
        print "active"
        return False

def portal_done(ip):
    ts=tstamp(datetime.datetime.now(tzutc()))
    last_ts, cp_done = timeout_info(ip) 
    print("cp_done:%s current: %s"%(cp_done,ts,))
    if not cp_done:
        return False
    if ts - int(cp_done) > 0:
        return True
    else:
        return False

def set_portal_expire(ip,value):
    ts=tstamp(datetime.datetime.now(tzutc()))
    sql = 'UPDATE users SET send204after = ?  where ip = ?'
    c.execute(sql,(ts + value,ip,))
    conn.commit()

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
    response_body = "hello"
    status = '302 Moved Temporarily'
    response_headers = [('Location','android_https')]
    start_response(status, response_headers)
    return [response_body]

def android_splash(environ, start_response):
    en_txt={ 'message':"Click on the button to go to the IIAB home page",\
            'btn1':"GO TO IIAB HOME PAGE", \
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

def android_save(environ, start_response):
    status = '302 redirect'
    response_headers = [('Content-type','text/html'),('Location','http://%s'%get_iiab_env("WWWROOT"))
            ('Content-Length',str(len(response_body)))]
    start_response(status, response_headers)
    return ["hi"]

def android_https(environ, start_response):
    en_txt={ 'message':"""Please ignore the following SECURITY warning""",\
             'btn2':'Go to CHROME browser',\
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

def null(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/html')]
    start_response(status, headers)
    return [""]

def put_204(environ, start_response):
    logging.debug("in put_204")
    print("in put_204")
    '''
    # get values to update_user
    ip = environ['HTTP_X_FORWARDED_FOR'].strip()
    cmd="arp -an %s|gawk \'{print $4}\'" % ip
    mac = subprocess.check_output(cmd, shell=True)
    ts=tstamp(datetime.datetime.now(tzutc()))
    ymd=datetime.datetime.today().strftime("%y%m%d-%H%M")

    # following call removes the return_204 flag for this user
    #update_user(ip,mac.strip(),ts,ymd)
    '''
    status = '204 No Data'
    response_body = ''
    response_headers = [('Content-type','text/html'),
            ('Content-Length',str(len(response_body)))]
    start_response(status, response_headers)
    print("sending 204")
    return [response_body]

def parse_agent(agent):
    system = ''
    system_version = ''
    match = re.search(r"(Android)\s([.\d]*)",agent)
    if match:
        system = match.group(1)
        system_version = match.group(2)
    match = re.search(r"(OS X)\s([\d_]*)",agent)
    if match:
        system = match.group(1)
        system_version = match.group(2)
    match = re.search(r"(Windows NT)\s([\d.]*)",agent)
    if match:
        system = match.group(1)
        system_version = match.group(2)
    return (system, system_version)
#
# ================== Start serving the wsgi application  =================
def application (environ, start_response):
    global CATCH
    global LIST
    global INACTIVITY_TO
    global ANDROID_TRIGGER

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
        #osys = agent.split(';')[1]
        #data.append("OS: %s\n"%osys)
        data.append("AGENT: %s\n"%agent)
        logging.debug(data)
        print(data)
        found = False
        return_204_flag = "False"
        ts=tstamp(datetime.datetime.now(tzutc()))
        ymd=datetime.datetime.today().strftime("%y%m%d-%H%M")

        system, system_version = parse_agent(agent)
        
        #print("parse returned: [%s]  [%s]"%(system,system_version))

        # do more specific stuff first
        if  environ['PATH_INFO'] == "/iiab_banner6.png":
            return banner(environ, start_response) 

        if  environ['PATH_INFO'] == "/bootstrap.min.js":
            return bootstrap(environ, start_response) 

        if  environ['PATH_INFO'] == "/bootstrap.min.css":
            return bootstrap_css(environ, start_response) 

        if  environ['PATH_INFO'] == "/jquery.min.js":
            return jquery(environ, start_response) 

        if  environ['PATH_INFO'] == "/favicon.ico":
            return null(environ, start_response) 

        if  environ['PATH_INFO'] == "/home_selected":
            # the js link to home page triggers this ajax url 
            # mark the sign-in conversation completed, return 204
            #update_user(ip,mac.strip(),ts,ymd,"True")
            logging.debug("setting flag to return_204")
            set_portal_expire(ip,PORTAL_TO)
            print("setting flag to return_204")

            status = '200 OK'
            headers = [('Content-type', 'text/html')]
            start_response(status, headers)
            return [""]
        '''
        if  environ['PATH_INFO'] == "/generate_204":
           print "generate_204 detected"
           if os.path.exists("/opt/iiab/captive-portal/users"):
              with open("/opt/iiab/captive-portal/users","r") as users:
                 for line in users:
                    if line.find(ip) != -1:
                        #print line,ip
                        nibble = line.split(' ')[4]
                        if nibble.strip() == "True":
                           print "putting 204"
                           return put_204(environ,start_respone
        '''
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
        if  environ['PATH_INFO'] == "/android_https":
           return android_https(environ, start_response) 
        if environ['HTTP_HOST'] == "clients3.google.com" or\
           environ['HTTP_HOST'] == "mtalk.google.com" or\
           environ['HTTP_HOST'] == "alt7-mtalk.google.com" or\
           environ['HTTP_HOST'] == "alt6-mtalk.google.com" or\
           environ['HTTP_HOST'] == "connectivitycheck.android.com" or\
           environ['HTTP_HOST'] == "connectivitycheck.gstatic.com":
           if inactive(ip):
               ANDROID_TRIGGER = True
           else:
               #ANDROID_TRIGGER = False
               pass
           if system != "":
                update_user(ip, mac, ts, 0, system, system_version, ymd)
           if ANDROID_TRIGGER:
                return android(environ, start_response) 
           elif portal_done(ip):
                return put_204(environ,start_response)
                      

        # microsoft
        if environ['HTTP_HOST'] == "ipv6.msftncsi.com" or\
           environ['HTTP_HOST'] == "ipv6.msftncsi.com.edgesuite.net" or\
           environ['HTTP_HOST'] == "www.msftncsi.com" or\
           environ['HTTP_HOST'] == "www.msftncsi.com.edgesuite.net" or\
           environ['HTTP_HOST'] == "www.msftconnecttest.com" or\
           environ['HTTP_HOST'] == "teredo.ipv6.microsoft.com" or\
           environ['HTTP_HOST'] == "teredo.ipv6.microsoft.com.nsatc.net": 
           return microsoft(environ, start_response) 

    print("executing the defaut redirect. Agent:%s"%agent)
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

