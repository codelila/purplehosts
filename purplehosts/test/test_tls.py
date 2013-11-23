import unittest
from mock import patch

import purplehosts.test.mock_config

purplehosts.test.mock_config.get.return_value = {
  'filename_template': '/etc/ssl/$domain/$host.$ext',
  'openssl_pkeyopts': []
}

from purplehosts.test.plumbum_mock import commandMock
import purplehosts.tls

class TestTls(unittest.TestCase):

  def setUp(self):
    self.tls = purplehosts.tls.TLS('test.example.org')

  def test_init(self):
    commandMock.__getitem__.assert_called_with(('-p', '/etc/ssl/example.org'))

  def test_make_key_no_pkeyopts(self):
    self.tls.make_key()
    commandMock.__getitem__.assert_called_with('genpkey')
    commandMock.__gt__.assert_called_with('/etc/ssl/example.org/test.key')

  def test_make_key_with_pkeyopts(self):
    purplehosts.test.mock_config.get.return_value = {
      'filename_template': '/etc/ssl/$domain/$host.$ext',
      'openssl_pkeyopts': ['op:value']
    }
    reload(purplehosts.tls)
    self.setUp()

    self.tls.make_key()
    commandMock.__getitem__.assert_called_with(('-pkeyopt', 'op:value'))

  def test_make_csr(self):
    self.tls.make_csr()
    commandMock.__getitem__.assert_called_with('req -new -batch -subj "/CN=test.example.org" -key /etc/ssl/example.org/test.key')
    commandMock.__gt__.assert_called_with('/etc/ssl/example.org/test.csr')

  @patch('purplehosts.tls.print',create=True)
  @patch('purplehosts.tls.raw_input',create=True, return_value='-----END CERTIFICATE-----')
  def test_make_crt(self, print_mock, raw_input_mock):
    self.tls.make_crt()
