from plumbum.cmd import adduser

from purplehosts.action.baseaction import BaseAction

class AddPosixAccount(BaseAction):
  def __init__(self, username_template):
    self._username_template = username_template

  def prepare(self, args):
    self._username = self._username_template.substitute(args)
    args['username'] = self._username
    return args

  def execute(self):
    adduser['--system'](self._username)
    return
