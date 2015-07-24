import unittest
from mock import patch

from purplehosts.test.plumbum_mock import commandMock

class TestAddsite(unittest.TestCase):
  @patch('purplehosts.action.createtlscert.CreateTLSCert')
  def test_run(self, CreateTLSCert):
    CreateTLSCert.return_value.provides = [ 'tls_crt_path' ]
    CreateTLSCert.return_value.prepare.return_value = {
      'tls_crt_path': 'file.crt'
    }

    from purplehosts.config import valFromDef
    import purplehosts.test.mock_config
    purplehosts.test.mock_config.setConf({
      'filename_template': ('file.$ext', 'StringTemplate'), # TLS
      'system_user_name_template': ('$host', 'StringTemplate'),
      'nginx_conf_filename_template': ('/etc/nginx/$host.conf', 'StringTemplate'),
    })
    purplehosts.test.mock_config.FileConfValue.return_value.value.return_value = "{{host}} {{fqdn}} nginx {{tls_crt_path}} {{username}}"

    import purplehosts.addsite

    from collections import namedtuple
    Args = namedtuple('Args', ['additional_args', 'domain', 'nginx'])
    purplehosts.addsite.run(Args(additional_args=[], domain='test.example.org', nginx=True))

    CreateTLSCert.assert_called_with()
    self.assertTrue(CreateTLSCert.return_value.execute.called)
    commandMock.__getitem__.assert_any_call('--system')
    commandMock.assert_any_call('test')
    commandMock.__gt__.assert_called_with('/etc/nginx/test.conf')
    commandMock.__lshift__.assert_called_with('test test.example.org nginx file.crt test')

  @patch('purplehosts.action.createtlscert.CreateTLSCert')
  def test_run_without_nginx(self, CreateTLSCert):
    CreateTLSCert.return_value.provides = [ 'tls_crt_path' ]
    CreateTLSCert.return_value.prepare.return_value = {
      'tls_crt_path': 'file.crt'
    }

    from purplehosts.config import valFromDef
    import purplehosts.test.mock_config
    purplehosts.test.mock_config.setConf({
      'filename_template': ('file.$ext', 'StringTemplate'), # TLS
      'system_user_name_template': ('$host', 'StringTemplate'),
      'nginx_conf_filename_template': ('/etc/nginx/$host.conf', 'StringTemplate'),
    })
    purplehosts.test.mock_config.FileConfValue.return_value.value.return_value = "{{host}} {{fqdn}} nginx {{tls_crt_path}} {{username}}"

    import purplehosts.addsite

    from collections import namedtuple
    Args = namedtuple('Args', ['additional_args', 'domain', 'nginx'])
    purplehosts.addsite.run(Args(additional_args=[], domain='test.example.org', nginx=False))

    commandMock.__gt__.assert_not_called()
    commandMock.__lshift__.assert_not_called()
