#!/usr/bin/python3

"""
   Author: George Hunt <georgejhunt <at> gmail.com>
"""
# reminders:
# zim_name in menu-def is search item in common/assets/zim_versions_idx.json
# file_name in zim_versions_idx referenced by zim_name is href:<target url>
# To avoid collisions with rachel, or embedded '.', menu-def filename may differ
# To find search items (size, articleCount, etc) menu_item_name in menu-def
#      must match zim_versions_idx['menu_item']

import os, sys, syslog
import json
import subprocess
import shlex
from datetime import date

SCRIPT_DIR = '/opt/admin/cmdsrv/scripts'
if not SCRIPT_DIR in sys.path:
    sys.path.append(SCRIPT_DIR)
#import iiab_make_kiwix_lib as kiwix

IIAB_PATH='/etc/iiab'
if not IIAB_PATH in sys.path:
    sys.path.append(IIAB_PATH)
from iiab_env import get_iiab_env

menu_defs_path = '/library/www/html/videos/menu-defs/'
video_url = '/videos/'
source_root = '/library/www/html/info/videos'

def write_menu_def(path,filename,video_directory):
   menuDef = {}
   menu_def_lang = 'en'
   #default_logo = get_default_logo(perma_ref,menu_def_lang)
   menuDef["intended_use"] = "oer2go"
   menuDef["lang"] = menu_def_lang
   menuDef["logo_url"] = 'image-video.jpg'
   menuDef["title"] = get_file_contents(path + '/title')
   menuitem = menu_def_lang + '-' + filename 
   default_name = menuitem + '.json'
   menuDef["menu_item_name"] = menuitem
   menuDef["start_url"] = video_url + filename
   menuDef["description"] = get_file_contents(path + '/oneliner')
   menuDef["extra_description"] = ""
   menuDef["extra_html"] = ""
   menuDef["footnote"] = get_file_contents(path + '/details')

   menuDef["change_ref"] = "generated"
   menuDef['change_date'] = str(date.today())

   #if not os.path.isfile(menu_defs_path + default_name): # logic to here can still overwrite existing menu def
   if True:
       print("creating %s"%menu_defs_path + default_name)
       with open(menu_defs_path + default_name,'w') as menufile:
          menufile.write(json.dumps(menuDef,indent=2))
   return default_name[:-5]

def get_file_contents(file):
   #print('opening {}'.format(file))
   try:
      with open(file,"r") as fp:
         outstr = fp.read()
         return outstr.rstrip()
   except Exception as e:
      #print(str(e))
      return ''

video_suffixes = ('.mp4','.m4v')
for root,dirname,files in os.walk(source_root):
   for filename in files:
      dot_index = filename.rfind('.')
      if dot_index != -1 and filename[dot_index:] in video_suffixes:
         video_directory = root[len(source_root):]
         print(root + '/' + filename)
         write_menu_def(root,filename,video_directory)
      
