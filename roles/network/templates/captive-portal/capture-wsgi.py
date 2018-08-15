#! /usr/bin/env python
# Python's bundled WSGI server

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

EXPIRE_SECONDS = 60 * 60 * 8

def tstamp(dtime):
    '''return a UNIX style seconds since 1970 for datetime input'''
    epoch = datetime.datetime(1970, 1, 1,tzinfo=tzutc())
    newdtime = dtime.astimezone(tzutc())
    since_epoch_delta = newdtime - epoch
    return since_epoch_delta.total_seconds()

def update_user(ip, mac, newts,ymd):
    fh, target_file_path = mkstemp()
    source_file_path = "/opt/iiab/captive-portal/users"
    if os.path.isfile(source_file_path):
        with open(target_file_path, 'w') as target_file:
            with open(source_file_path, 'r') as source_file:
                for line in source_file:
                    if ip in line:
                        target_file.write("%s %s %8.0d %s" % (ip,mac,ts,ymd,))
                    else:
                        target_file.write(line)
                os.remove(source_file_path)
                move(target_file_path, source_file_path)
    else:
        with open(source_file_path, 'w') as target_file:
          target_file.write("%s %s %8.0d %s" % (ip,mac,ts,ymd,))
        
def microsoft(environ,start_response):
    response_body = "This worked"
    status = '302 Moved Temporarily'
    response_headers = [('Location','http://box.lan/home')]
    start_response(status, response_headers)
    return [response_body]

def android(environ, start_response):
    response_body = "This worked"
    status = '302 Moved Temporarily'
    response_headers = [('Location','http://box.lan/home')]
    start_response(status, response_headers)
    return [response_body]

def macintosh(environ, start_response):
    response_body = """
    <h1>Welcome to IIAB</h1>
    <form method="post" action="http://box.lan/home"> 
       <input type="submit" value="Go To MENU" style="padding:10px 20px;" /> 
    </form> """
    
    status = '302 Moved Temporarily'
    response_headers = [('Content','text/html')]
    start_response(status, response_headers)
    return [response_body]

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
        logging.debug("Checking for url %s"%environ['HTTP_HOST'])
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
    else:
        ip = environ['HTTP_X_FORWARDED_FOR'].strip()
        cmd="arp -an %s|gawk \'{print $4}\'" % ip
        mac = subprocess.check_output(cmd, shell=True)
        data = []
        data.append("host: %s\n"%environ['HTTP_HOST'])
        data.append("path: %s\n"%environ['PATH_INFO'])
        data.append("query: %s\n"%environ['QUERY_STRING'])
        data.append("ip: %s\n"%environ['HTTP_X_FORWARDED_FOR'])
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

        # since this user is in our list, free her from iptables trap
        cmd="sudo iptables -I internet 1 -t mangle -m mac --mac-source %s -j RETURN"%mac
        logging.debug(cmd)
        args = shlex.split(cmd)
        process = Popen(args, stderr=PIPE, stdout=PIPE)
        stdout, stderr = process.communicate()
        if len(stderr) != 0:
            logging.debug("untrap user from iptables trap returned" + stderr)

        if environ['HTTP_HOST'] == "captive.apple.com" or\
           environ['HTTP_HOST'] == "appleiphonecell.com" or\
           environ['HTTP_HOST'] == "detectportal.firefox.com" or\
           environ['HTTP_HOST'] == "*.apple.com.edgekey.net" or\
           environ['HTTP_HOST'] == "gsp1.apple.com" or\
           environ['HTTP_HOST'] == "apple.com" or\
           environ['HTTP_HOST'] == "www.apple.com": 
           return macintosh(environ, start_response) 

        if environ['HTTP_HOST'] == "clients3.google.com" or\
           environ['HTTP_HOST'] == "connectivitycheck.gstatic.com":
           return android(environ, start_response) 
           
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

# Get the IIAB variables
sys.path.append('/etc/iiab/')
from iiab_env import get_iiab_env

# set up some logging
logging.basicConfig(filename='/var/log/apache2/portal.log',format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M',level=logging.DEBUG)
if len(sys.argv) > 1 and sys.argv[1] == '-d':
    CATCH = True
    LIST = False
    PORT=80
elif len(sys.argv) > 1 and sys.argv[1] == '-l':
    LIST = True
    CATCH = False
else:
    CATCH = False
    LIST = False
    PORT=9090
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

