class ArgDict(dict):
  def __init__(self):
    self._shim_args = []

  def start_testing(self, args):
    self._shim_args = args

  def start_preparing(self):
    self._shim_args = []

  def __contains__(self, k):
    return (k in self._shim_args) or super(ArgDict, self).__contains__(k)

  def __getitem__(self, k):
    if k in self._shim_args:
      return 'PLACEHOLDER'
    return super(ArgDict, self).__getitem__(k)
