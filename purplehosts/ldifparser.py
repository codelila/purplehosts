from __future__ import absolute_import

import ldif

class PurpleLDIFParser(ldif.LDIFParser):
  def __init__(self,input):
    ldif.LDIFParser.__init__(self,input)
    self.values = {}

  def handle(self,dn,entry):
    self.values[dn] = entry

  def getParsed(self):
    self.parse()
    return self.values
