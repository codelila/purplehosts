import unittest

from surrogate import surrogate
from mock import Mock, patch

class TestLdap(unittest.TestCase):
  def test_add(self):
    from purplehosts.config import valFromDef
    import purplehosts.test.mock_config

    purplehosts.test.mock_config.setConf({
      'people_root': 'PEOPLE_ROOT',
      'groups_root': 'GROUPS_ROOT',
      'bind_pw': 'BIND_PW',
      'bind_dn': 'BIND_DN'
    })

    purplehosts.test.mock_config.FileConfValue.return_value.value.return_value = "$username"

    from purplehosts.test.plumbum_mock import commandMock

    import purplehosts.ldap

    purplehosts.ldap.add({
      'username': 'TEST'
    })

    commandMock.__getitem__.assert_called_with(('-w', 'BIND_PW', '-D', 'BIND_DN'))
    commandMock.__lshift__.assert_called_with('TEST')

  @patch('purplehosts.ldifparser.PurpleLDIFParser')
  @surrogate('ldif')
  @patch('ldif')
  def test_getUser(self, ldif, purpleLdifParser):
    from purplehosts.test.plumbum_mock import commandMock

    import purplehosts.ldap

    purplehosts.ldap.getUser('cn=test')
