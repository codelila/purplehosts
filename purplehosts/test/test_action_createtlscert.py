import unittest
from mock import patch

from purplehosts.test.plumbum_mock import commandMock

class TestAddsite(unittest.TestCase):
  def setUp(self):
    from purplehosts.action.createtlscert import CreateTLSCert
    self._action = CreateTLSCert()

  # FIXME Every action needs that test
  @patch('purplehosts.tls.TLS')
  def test_provides(self, TLS):
    _ret = self._action.prepare({'fqdn': 'test.example.org', 'domain': 'example.org', 'host': 'test'})
    self.assertEqual(_ret.keys().sort(), self._action.provides.sort())
