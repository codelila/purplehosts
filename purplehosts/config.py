def fileName(fileName):
  return 'config/%s' % fileName

def get(section):
  config = {}
  execfile(fileName('%s.conf.py' % section), config)
  return config
