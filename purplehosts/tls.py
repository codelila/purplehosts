from __future__ import print_function

from plumbum.cmd import openssl, mkdir, cat, rm
from plumbum import FG

from os.path import dirname
from string import Template

import purplehosts.config

conf = purplehosts.config.get('tls')

filename_template = conf['filename_template']

class TLS:
  def __init__(self, args):
    subst_args = {}
    subst_args.update(args)
    subst_args['ext'] = '${ext}'
    self.filename_template = Template(filename_template.value(subst_args))
    self.site = args['fqdn']
    self.pkeyopts = conf['openssl_pkeyopts'].value(args)
    mkdir['-p', dirname(self.filename_template.template)]()

  def _getFilename(self, ext):
    return self.filename_template.substitute({'ext': ext})

  def make(self):
    return {
      'key': self.make_key(),
      'csr': self.make_csr(),
      'crt': self.make_crt()
    }

  def make_key(self):
    fn = self._getFilename('key')
    (reduce(lambda call, param: call['-pkeyopt', param], self.pkeyopts, openssl['genpkey', '-algorithm', 'RSA']) > fn)()
    return fn

  def make_csr(self):
    fn = self._getFilename('csr')
    (openssl['req', '-new', '-batch', '-subj', '/CN=%s' % self.site, '-key', self._getFilename('key')] > fn)()
    return fn

  def make_crt(self):
    print("Paste the following CSR to CAcert:")
    (cat < self._getFilename('csr')) & FG
    rm('-f %s' % self._getFilename('crt'))

    print("Enter certificate:")
    crt = ''
    line = ''

    while line != "-----END CERTIFICATE-----":
      line = raw_input()
      crt += line + '\n'

    fn = self._getFilename('crt')
    (cat << crt > fn)()

    return fn
