import unittest
from mock import patch, call

from purplehosts.test.plumbum_mock import commandMock

class TestAddsite(unittest.TestCase):
  @patch('purplehosts.tls.TLS')
  def test_run(self, TLS):
    TLS.return_value._getFilename.return_value = 'file.crt'

    import purplehosts.test.mock_config
    purplehosts.test.mock_config.get.return_value = {
      'filename_template': 'file.$ext', # TLS
      'system_user_name_template': '$host',
      'nginx_conf_filename_template': '/etc/nginx/$host.conf',
    }
    purplehosts.test.mock_config.getFile.return_value = "{{host}} {{fqdn}} nginx {{tls_crt_path}} {{username}}"

    import purplehosts.addsite

    from collections import namedtuple
    Args = namedtuple('Args', ['additional_args', 'domain'])
    purplehosts.addsite.run(Args(additional_args=[], domain='test.example.org'))

    TLS.assert_called_with('test.example.org')
    self.assertTrue(TLS.return_value.make.called)
    commandMock.__getitem__.assert_any_call('--system')
    commandMock.assert_any_call('test')
    commandMock.__gt__.assert_called_with('/etc/nginx/test.conf')
    commandMock.__lshift__.assert_called_with('test test.example.org nginx file.crt test')
