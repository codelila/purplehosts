from abc import ABCMeta, abstractmethod

class BaseAction(object):
  __metaclass__ = ABCMeta

  @abstractmethod
  def prepare(self, args):
    self.prepared = True

  @abstractmethod
  def execute(self):
    self.executed = True
