import unittest

from purplehosts.argdict import ArgDict

class TestArgdict(unittest.TestCase):
  def test_contains(self):
    argdict = ArgDict()
    self.assertFalse(argdict.__contains__('shimmed'))
    self.assertFalse(argdict.__contains__('not-shimmed'))
    self.assertNotIn('shimmed', argdict)
    self.assertNotIn('not-shimmed', argdict)
    argdict.start_testing(['shimmed'])
    self.assertTrue(argdict.__contains__('shimmed'))
    self.assertFalse(argdict.__contains__('not-shimmed'))
    self.assertIn('shimmed', argdict)
    self.assertNotIn('not-shimmed', argdict)
    argdict.start_preparing()
    self.assertFalse(argdict.__contains__('shimmed'))
    self.assertFalse(argdict.__contains__('not-shimmed'))
    self.assertNotIn('shimmed', argdict)
    self.assertNotIn('not-shimmed', argdict)

  def test_getitem(self):
    argdict = ArgDict()
    self.assertRaises(KeyError, argdict.__getitem__, 'shimmed')
    self.assertRaises(KeyError, argdict.__getitem__, 'not-shimmed')
    argdict.start_testing(['shimmed'])
    argdict.__getitem__('shimmed')
    argdict['shimmed']
    self.assertRaises(KeyError, argdict.__getitem__, 'not-shimmed')
    argdict.start_preparing()
    self.assertRaises(KeyError, argdict.__getitem__, 'shimmed')
    self.assertRaises(KeyError, argdict.__getitem__, 'not-shimmed')
