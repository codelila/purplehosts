from __future__ import absolute_import

import ldap
import ldap.modlist

import purplehosts.config
conf = purplehosts.config.get('ldap')

def _getConnection():
  if "conn" not in _getConnection.__dict__:
    conn = _getConnection.conn = ldap.initialize(conf['server'])
    conn.simple_bind_s(conf['bind_dn'], conf['bind_pw'])
  return _getConnection.conn

def nextUid():
  return 4000

def add(args):
  if 'dn' in args:
    dn = args['dn']
    del args['dn']
  else:
    dn = "cn=%s,%s" % (args['cn'], conf['root'])

  if isinstance(args['objectClass'], basestring):
    args['objectClass'] = [ args['objectClass'] ]
  args['objectClass'].append('person')

  conn = _getConnection()
  conn.add_s(dn, ldap.modlist.addModlist(args))
