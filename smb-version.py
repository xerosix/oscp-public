#!/usr/bin/python

import sys
from pprint import pprint
from impacket.smbconnection import SMBConnection

debug = False

if len(sys.argv) < 1:
   print "smb-version.py {ip:port} [optional: --debug]"
   quit()
else:
   smb = None
   [host, port] = sys.argv[1].split(":")

   if '--debug' in sys.argv:
      debug = True

   #connect to the smb service
   try:
      print "SMB Info for: ", sys.argv[1]
      smb = SMBConnection(host, host, None, port, timeout=2)
      smb.login('' , '')
   except:
      print "{Error}: Could not connect to SMB."
      print ""
      quit()
   
   if smb:
      if vars(smb).get('_SMBConnection'):
         found_os_version = False
         found_host_name = False
         found_smb_version = False

         #found smb service version
         if vars(smb._SMBConnection).get('_SMB__server_lanman'):
            print "SMB Version:", smb._SMBConnection._SMB__server_lanman
            found_smb_version = True


         #found os version
         if vars(smb._SMBConnection).get('_Session'):
            if smb._SMBConnection._Session.get('ServerOS'):
               print "OS Version (Session):", smb._SMBConnection._Session.get('ServerOS')
               found_os_version = True

         if vars(smb._SMBConnection).get('_SMB__server_os'):
            print "OS Version (SMB):", smb._SMBConnection._SMB__server_os
            found_os_version = True

         #found hostname
         if vars(smb._SMBConnection).get('_SMB__server_name'):
            print "Host (SMB):", smb._SMBConnection._SMB__server_name
            found_host_name = True

         if vars(smb._SMBConnection).get('_Session'):
            if smb._SMBConnection._Session.get('ServerDNSDomainName'):
               print "Host (Domain):", smb._SMBConnection._Session.get('ServerDNSDomainName')
               found_host_name = True

            if smb._SMBConnection._Session.get('ServerName'):
               print "Host:", smb._SMBConnection._Session.get('ServerName')
               found_host_name = True
         
         if not found_os_version or not found_host_name or not found_smb_version:
            if debug:
               print ""
               pprint(vars(smb))
               pprint(vars(smb._SMBConnection))
   print ""

