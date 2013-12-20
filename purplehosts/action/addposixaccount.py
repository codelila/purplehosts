from plumbum.cmd import adduser

from purplehosts.action.baseaction import BaseAction

class AddPosixAccount(BaseAction):
  provides = [ 'username' ]

  def __init__(self, username_template):
    self._username_template = username_template
    self._adduser = adduser['--system']

  def prepare(self, args):
    self._username = self._username_template.substitute(args)
    super(AddPosixAccount, self).prepare(args)
    return { 'username': self._username }

  def execute(self):
    self._adduser(self._username)
    super(AddPosixAccount, self).execute()
