
def getHost(fqdn):
  (host, _, domain) = fqdn.partition('.')
  return host

def getDomain(fqdn):
  (host, _, domain) = fqdn.partition('.')
  return domain
