
from purplehosts.action.baseaction import BaseAction

class AddPhpFpmPool(BaseAction):
  provides = [ ]

  def __init__(self, conf_template, filename_template):
    self._conf_template = conf_template
    self._filename_template = filename_template

  def prepare(self, args):
    self._conf = self._conf_template.value(args)
    self._conf_filename = self._filename_template.value(args)
    from plumbum.cmd import cat
    from plumbum import local
    self._cat = local['cat']
    self._initscript = local['/etc/init.d/php5-fpm']
    super(AddPhpFpmPool, self).prepare(args)
    return {}

  def execute(self):
    (self._cat << self._conf > self._conf_filename)()
    self._initscript('reload')
    super(AddPhpFpmPool, self).execute()
