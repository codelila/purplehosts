
from purplehosts.action.baseaction import BaseAction

class AddNginxSite(BaseAction):
  provides = [ ]

  def __init__(self, conf_template, filename_template):
    self._conf_template = conf_template
    self._filename_template = filename_template

  def prepare(self, args):
    self._conf = self._conf_template.value(args)
    self._conf_filename = self._filename_template.value(args)
    super(AddNginxSite, self).prepare(args)
    return {}

  def execute(self):
    import os.path
    from plumbum.cmd import cat, ln, nginx

    (cat << self._conf > self._conf_filename)()

    ln['-s'](os.path.relpath(self._conf_filename, '/etc/nginx/sites-enabled/'), '/etc/nginx/sites-enabled/')
    nginx('-t')

    super(AddNginxSite, self).execute()
