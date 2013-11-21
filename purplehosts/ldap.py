from __future__ import absolute_import

from plumbum.cmd import ldapmodify
from plumbum import FG
from string import Template

import purplehosts.config
conf = purplehosts.config.get('ldap')

def nextUid():
  return 4000 # http://www.rexconsulting.net/ldap-protocol-uidnumber.html

userTemplate = Template(purplehosts.config.getFile('user.ldif'))

def add(args):
  args['people_root'] = conf['people_root']
  args['groups_root'] = conf['groups_root']
  (ldapmodify['-w', conf['bind_pw'], '-D', conf['bind_dn']] << userTemplate.substitute(args))()
