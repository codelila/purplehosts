from mock import Mock

import purplehosts.config
purplehosts.config.get = Mock(return_value={})

def setConf(conf):
  for key in conf.keys():
    conf[key] = purplehosts.config.valFromDef(conf[key])
  purplehosts.config.get.return_value = conf

FileConfValue = purplehosts.config.FileConfValue = Mock()
