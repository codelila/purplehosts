from __future__ import absolute_import

from plumbum.cmd import ldapmodify
from plumbum import FG

import purplehosts.config
conf = purplehosts.config.get('ldap')

def nextUid():
  return 4000 # http://www.rexconsulting.net/ldap-protocol-uidnumber.html

userTemplate = purplehosts.config.valFromDef(('user.ldif', 'File', 'StringTemplate'))

def add(args):
  args['people_root'] = conf['people_root'].value(args)
  args['groups_root'] = conf['groups_root'].value(args)
  (ldapmodify['-w', conf['bind_pw'].value(args), '-D', conf['bind_dn'].value(args)] << userTemplate.value(args))()
