#! /usr/bin/env python
# Python's bundled WSGI server

from wsgiref.simple_server import make_server
import subprocess
from dateutil.tz import *
import datetime
import logging
import os
import sys

def tstamp(dtime):
    '''return a UNIX style seconds since 1970 for datetime input'''
    epoch = datetime.datetime(1970, 1, 1,tzinfo=tzutc())
    newdtime = dtime.astimezone(tzutc())
    since_epoch_delta = newdtime - epoch
    return since_epoch_delta.total_seconds()

def application (environ, start_response):
    global CATCH
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
    data.append("query: %s\n"%environ['QUERY_STRING'])
    data.append("path: %s\n"%environ['PATH_INFO'])
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
                 print line, ip
                 if ip in line:
                    found = True
                    break
        if not found:
           with open("/opt/iiab/captive-portal/users","a") as users:
               ts=tstamp(datetime.datetime.now(tzutc()))
               ymd=datetime.datetime.today().strftime("%y%m%d-%H%M")
               outstr ="%s %s %s %s\n" %  (ip, mac.strip(), ts,ymd,) 
               users.write(outstr)

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
if sys.argv[1] == '-d':
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

