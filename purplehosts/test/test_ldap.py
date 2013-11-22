import unittest
from mock import Mock

import purplehosts.config

purplehosts.config.get = Mock(return_value={
  'people_root': 'PEOPLE_ROOT',
  'groups_root': 'GROUPS_ROOT',
  'bind_pw': 'BIND_PW',
  'bind_dn': 'BIND_DN'
})
purplehosts.config.getFile = Mock(return_value=
  "$username"
)

from purplehosts.test.plumbum_mock import commandMock

import purplehosts.ldap

class TestLdap(unittest.TestCase):
  def test_add(self):

    purplehosts.ldap.add({
      'username': 'TEST'
    })

    commandMock.__getitem__.assert_called_with(('-w', 'BIND_PW', '-D', 'BIND_DN'))
    commandMock.__lshift__.assert_called_with('TEST')
