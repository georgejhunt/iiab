#!/usr/bin/env python3
# read list of online portal checkers, make nginx server blocks 

outstr = ''
with open('checkurls','r') as urls:
   for line in urls:
      outstr += 'server {\n'
      outstr += '    listen 80;\n'
      outstr += '    server_name {}'.format(line)
      outstr += '    rewrite ^{} http://127.0.0.1/captive\n'.format(line.strip())
      outstr += '}\n'
print(outstr)

