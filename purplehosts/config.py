def _fileName(fileName):
  return 'config/%s' % fileName

def getFile(fileName):
  with open(_fileName(fileName), 'r') as content_file:
    return content_file.read()

def get(section):
  config = {}
  execfile(_fileName('%s.conf.py' % section), config)
  return config
