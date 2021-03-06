import unittest
from mock import patch

from purplehosts.config import valFromDef
import purplehosts.test.mock_config

purplehosts.test.mock_config.setConf({
  'filename_template': ('/etc/ssl/$domain/$host.$ext', 'StringTemplate'),
  'openssl_pkeyopts': []
})

from purplehosts.test.plumbum_mock import commandMock
import purplehosts.tls

def retArr(arr):
  return lambda: arr.pop(0)

class TestTls(unittest.TestCase):

  def setUp(self):
    self.tls = purplehosts.tls.TLS({'fqdn': 'test.example.org', 'domain': 'example.org', 'host': 'test'})

  def test_init(self):
    commandMock.__getitem__.assert_called_with(('-p', '/etc/ssl/example.org'))

  def test_make_key_no_pkeyopts(self):
    keypath = self.tls.make_key()
    commandMock.__getitem__.assert_called_with(('genpkey', '-algorithm', 'RSA'))
    commandMock.__gt__.assert_called_with('/etc/ssl/example.org/test.key')
    self.assertEqual(keypath, '/etc/ssl/example.org/test.key')

  def test_make_key_with_pkeyopts(self):
    purplehosts.test.mock_config.setConf({
      'filename_template': ('/etc/ssl/$domain/$host.$ext', 'StringTemplate'),
      'openssl_pkeyopts': ['op:value']
    })
    reload(purplehosts.tls)
    self.setUp()

    self.tls.make_key()
    commandMock.__getitem__.assert_called_with(('-pkeyopt', 'op:value'))

  def test_make_csr(self):
    csrpath = self.tls.make_csr()
    commandMock.__getitem__.assert_called_with(('req', '-new', '-batch', '-subj', '/CN=test.example.org', '-key', '/etc/ssl/example.org/test.key'))
    commandMock.__gt__.assert_called_with('/etc/ssl/example.org/test.csr')
    self.assertEqual(csrpath, '/etc/ssl/example.org/test.csr')

  @patch('purplehosts.tls.print',create=True)
  @patch('purplehosts.tls.raw_input',create=True, side_effect=retArr(['certdata', '-----END CERTIFICATE-----']))
  def test_make_crt(self, print_mock, raw_input_mock):
    crtpath = self.tls.make_crt()
    self.assertEqual(crtpath, '/etc/ssl/example.org/test.crt')
    commandMock.__lshift__.assert_called_with('certdata\n-----END CERTIFICATE-----\n')

  @patch('purplehosts.tls.TLS.make_key', return_value='file.key')
  @patch('purplehosts.tls.TLS.make_csr', return_value='file.csr')
  @patch('purplehosts.tls.TLS.make_crt', return_value='file.crt')
  def test_make_all(self, make_key, make_csr, make_crt):
    _ret = self.tls.make()
    self.assertEqual(_ret, {
      'key': 'file.key',
      'csr': 'file.csr',
      'crt': 'file.crt'
    })
