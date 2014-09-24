from abc import ABCMeta, abstractmethod

###
# __init__ may expect general configuration
# prepare should configure the action for the current execution
# execute runs a prepared action
###

class BaseAction(object):
  __metaclass__ = ABCMeta

  @abstractmethod
  def prepare(self, args):
    self.prepared = True

  @abstractmethod
  def execute(self):
    self.executed = True
