#! /usr/bin/env python
# Python's bundled WSGI server

from wsgiref.simple_server import make_server
import subprocess
from dateutil.tz import *
import datetime
import logging
import os
import sys
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
    with open(target_file_path, 'w') as target_file:
        with open(/opt/iiab/captive-portal/users, 'r') as source_file:
            for line in source_file:
                target_file.write(line.replace(pattern, substring))
                os.remove(source_file_path)
                move(target_file_path, source_file_path)

def replace(source_file_path, pattern, substring):
fh, target_file_path = mkstemp()
with open(target_file_path, 'w') as target_file:
            with open(source_file_path, 'r') as source_file:
                            for line in source_file:
                                                target_file.write(line.replace(pattern, substring))
                                                    remove(source_file_path)
                                                        move(target_file_path, source_file_path)
                                                                                                                                    
def application (environ, start_response):
    global CATCH
    global EXPIRE_SECONDS
    ip = environ['HTTP_X_FORWARDED_FOR'].strip()
    cmd="arp -an %s|gawk \'{print $4}\'" % ip
    mac = subprocess.check_output(cmd, shell=True)

    # Sorting and stringifying the environment key, value pairs
    '''    data = [
        '%s: %s\n' % (key, value) for key, value in sorted(environ.items())
    ]
    '''
    data = []
    data.append("host: %s\n"%environ['HTTP_HOST'])
    data.append("path: %s\n"%environ['PATH_INFO'])
    data.append("query: %s\n"%environ['QUERY_STRING'])
    data.append("ip: %s\n"%environ['HTTP_X_FORWARDED_FOR'])
    logging.debug(data)
    cmd="sudo iptables -I internet 1 -t mangle -m mac --mac-source %s -j RETURN"%mac
    print(cmd)
    if CATCH:
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
               users.write(outstr)

    else:
        found = False
        if os.path.exists("/opt/iiab/captive-portal/users"):
           with open("/opt/iiab/captive-portal/users","r") as users:
              for line in users:
                 #print line, ip
                 if ip in line:
                    session_start = int(line.explode(' ')[2])
                    ts=tstamp(datetime.datetime.now(tzutc()
                    if ts - session_start < EXPIRE_SECONDS:
                        found = True
                        break
        if not found:
           ts=tstamp(datetime.datetime.now(tzutc()
           ymd=datetime.datetime.today().strftime("%y%m%d-%H%M")
           update_user(ip,mac.strip(),ts,ymd)

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
    PORT=80
else:
    CATCH = False
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
# vim: tabstop=3 expandtab shiftwidth=3 softtabstop=3 background=light

