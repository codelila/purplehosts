import unittest
import mock

import sys
import ldap
ldap = mock.Mock(spec=ldap)
sys.modules['ldap'] = ldap

import purplehosts.ldap

class TestLdap(unittest.TestCase):
  def test_add(self):
    purplehosts.ldap.add({})
    ldap.initialize.assert_called_with('ldap://localhost:389')
