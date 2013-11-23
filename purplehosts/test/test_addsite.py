import unittest
from mock import patch, call

import purplehosts.test.mock_config
from purplehosts.test.plumbum_mock import commandMock

purplehosts.test.mock_config.get.return_value = {
  'filename_template': 'file.$ext', # TLS
  'system_user_name_template': '$host',
  'nginx_conf_filename_template': '/etc/nginx/$host.conf'
}

purplehosts.test.mock_config.getFile.return_value = "{{host}} {{fqdn}} nginx {{tls_paths.crt}}"

import purplehosts.addsite

class TestAddsite(unittest.TestCase):
  @patch('purplehosts.tls')
  def test_run(self, tls):
    tls.TLS.return_value.make_all.return_value = {
      'crt': 'file.crt',
      'csr': 'file.csr',
      'key': 'file.key'
    }
    from collections import namedtuple
    Args = namedtuple('Args', ['additional_args', 'domain'])
    purplehosts.addsite.run(Args(additional_args=[], domain='test.example.org'))

    tls.TLS.assert_called_with('test.example.org')
    self.assertTrue(tls.TLS.return_value.make_all.called)
    commandMock.__getitem__.assert_any_call('--system')
    commandMock.assert_any_call('test')
    commandMock.__gt__.assert_called_with('/etc/nginx/test.conf')
    commandMock.__lshift__.assert_called_with('test test.example.org nginx file.crt')
