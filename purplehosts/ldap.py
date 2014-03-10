from __future__ import absolute_import

from plumbum.cmd import ldapmodify, ldapsearch

import purplehosts.config
conf = purplehosts.config.get('ldap')

def nextUid():
  return 4000 # http://www.rexconsulting.net/ldap-protocol-uidnumber.html

userTemplate = purplehosts.config.valFromDef(('user.ldif', 'File', 'StringTemplate'))

def add(args):
  args['people_root'] = conf['people_root'].value(args)
  args['groups_root'] = conf['groups_root'].value(args)
  (ldapmodify['-w', conf['bind_pw'].value(args), '-D', conf['bind_dn'].value(args)] << userTemplate.value(args))()

def getUser(cn):
  from purplehosts.ldifparser import PurpleLDIFParser

  from StringIO import StringIO

  cmdRes = (ldapsearch['-LLL', '-w', conf['bind_pw'].value(), '-D', conf['bind_dn'].value(), '-b', conf['people_root'].value(), cn])()
  ldifParser = PurpleLDIFParser(StringIO(cmdRes))
  return ldifParser.getParsed()[cn + ',' + conf['people_root'].value()]

def modify(ldif):
  (ldapmodify['-w', conf['bind_pw'].value(), '-D', conf['bind_dn'].value()] << ldif)()
