def get(section):
  config = {}
  execfile('config/%s.conf.py' % section, config)
  return config
