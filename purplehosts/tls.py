from __future__ import print_function

from plumbum.cmd import openssl, mkdir, cat, rm, echo
from plumbum import FG

from os.path import dirname
from string import Template

import purplehosts.config

conf = purplehosts.config.get('tls')

filename_template = Template(conf['filename_template'])

class TLS:

  def __init__(self, site):
    (host, _, domain) = site.partition('.')
    self.filename_template = Template(filename_template.safe_substitute({'domain': domain, 'fqdn': site, 'host': host}))
    self.site = site
    mkdir['-p', dirname(self.filename_template.template)]()

  def _getFilename(self, ext):
    return self.filename_template.substitute({'ext': ext})

  def make(self):
    self.make_key()
    self.make_csr()
    self.make_crt()

  def make_key(self):
    (reduce(lambda call, param: call['-pkeyopt', param], conf['openssl_pkeyopts'], openssl['genpkey']) > self._getFilename('key'))()

  def make_csr(self):
    (openssl['req -new -batch -subj "/CN=%s" -key %s' % (self.site, self._getFilename('key'))] > self._getFilename('csr'))()

  def make_crt(self):
    print("Paste the following CSR to CAcert:")
    cat(self._getFilename('csr')) & FG
    rm('-f %s' % self._getFilename('crt'))

    print("Enter certificate:")
    crt = ''
    line = ''

    while line != "-----END CERTIFICATE-----":
      line = raw_input()
      crt += line

    (echo << crt > self._getFilename('crt'))()
