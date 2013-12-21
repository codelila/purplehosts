import unittest
from mock import patch

from purplehosts.test.plumbum_mock import commandMock

class TestAddsite(unittest.TestCase):
  @patch('purplehosts.tls.TLS')
  def setUp(self, TLS):
    from purplehosts.action.createtlscert import CreateTLSCert
    self._action = CreateTLSCert()

  # FIXME Every action needs that test
  def test_provides(self):
    _ret = self._action.prepare({'fqdn': 'test.example.org', 'domain': 'example.org', 'host': 'test'})
    self.assertEqual(_ret.keys().sort(), self._action.provides.sort())
