from abc import ABCMeta, abstractmethod

class BaseAction(object):
  __metaclass__ = ABCMeta

  @abstractmethod
  def prepare(self):
    pass

  @abstractmethod
  def execute(self):
    pass
