def _fileName(fileName):
  return 'config/%s' % fileName

def _getFile(fileName):
  with open(_fileName(fileName), 'r') as content_file:
    return content_file.read()

def get(section):
  config = {}
  execfile(_fileName('%s.conf.py' % section), config)
  for key in config.keys():
    config[key] = valFromDef(config[key])
  return config

def valFromDef(definition):
  if (isinstance(definition, tuple)):
    obj = PlainConfValue(definition[0])
    for action in definition[1:]:
      obj = valFromDef.func_globals[action + 'ConfValue'](obj.value)
  else:
    obj = PlainConfValue(definition)
  return obj

class ConfValue:
  def __init__(self, upstream):
    self._upstream = upstream

class PlainConfValue(ConfValue):
  def value(self, context):
    return self._upstream

class StringTemplateConfValue(ConfValue):
  def value(self, context):
    from string import Template
    return Template(self._upstream(context)).substitute(context)

class MustacheTemplateConfValue(ConfValue):
  def value(self, context):
    from pystache import Renderer
    renderer = Renderer(missing_tags='strict')
    return renderer.render(self._upstream(context), context)

class FileConfValue(ConfValue):
  def value(self, context):
    return _getFile(self._upstream(context))
