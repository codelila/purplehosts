import os.path

from plumbum.cmd import cat, ln, nginx

from pystache import Renderer

renderer = Renderer(missing_tags='strict')

from purplehosts.action.baseaction import BaseAction

class AddNginxSite(BaseAction):
  provides = [ ]

  def __init__(self, conf_template, filename_template):
    self._conf_template = conf_template
    self._filename_template = filename_template

  def prepare(self, args):
    self._conf = renderer.render(self._conf_template, args)
    self._conf_filename = self._filename_template.substitute(args)
    super(AddNginxSite, self).prepare(args)
    return {}

  def execute(self):
    (cat << self._conf > self._conf_filename)()

    ln['-s'](os.path.relpath(self._conf_filename, '/etc/nginx/sites-enabled/'), '/etc/nginx/sites-enabled/')
    nginx('-t')

    super(AddNginxSite, self).execute()
