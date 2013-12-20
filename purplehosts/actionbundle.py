from purplehosts.argdict import ArgDict

class ActionBundle:
  def __init__(self, actions):
    self._actions = actions

    self.provides = []
    for action in self._actions:
      self.provides.extend(action.provides)

  def prepare(self, args):
    substitutes = ArgDict()
    substitutes.update(args)

    # Add placeholders so that depending prepares work
    substitutes.start_testing(self.provides)

    # Testing prepares
    for action in self._actions:
      new_subs = action.prepare(substitutes)
      for k in action.provides:
        substitutes[k] = new_subs[k]

    # Running prepares
    substitutes.start_preparing()
    for action in self._actions:
      new_subs = action.prepare(substitutes)
      for k in action.provides:
        substitutes[k] = new_subs[k]

  def execute(self):
    # Start doing things
    for action in self._actions:
      action.execute()
