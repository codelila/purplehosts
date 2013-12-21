from purplehosts.action.baseaction import BaseAction

from purplehosts.tls import TLS

class CreateTLSCert(BaseAction):
  provides = [ 'tls_key_path', 'tls_crt_path' ]

  def __init__(self):
    pass

  def prepare(self, args):
    self._tls = TLS(args)
    _ret = {
      'tls_key_path': self._tls._getFilename('key'),
      'tls_crt_path': self._tls._getFilename('crt')
    }
    super(CreateTLSCert, self).prepare(args)
    return _ret

  def execute(self):
    self._tls.make()
    super(CreateTLSCert, self).execute()

