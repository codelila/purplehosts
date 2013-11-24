from __future__ import print_function

from plumbum.cmd import openssl, mkdir, cat, rm
from plumbum import FG

from os.path import dirname
from string import Template

import purplehosts.config
from purplehosts.utils import getHost, getDomain

conf = purplehosts.config.get('tls')

filename_template = Template(conf['filename_template'])

class TLS:

  def __init__(self, site):
    host = getHost(site)
    domain = getDomain(site)
    self.filename_template = Template(filename_template.safe_substitute({'domain': domain, 'fqdn': site, 'host': host}))
    self.site = site
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
    (reduce(lambda call, param: call['-pkeyopt', param], conf['openssl_pkeyopts'], openssl['genpkey', '-algorithm', 'RSA']) > fn)()
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
      crt += line

    fn = self._getFilename('crt')
    (cat << crt > fn)()

    return fn
